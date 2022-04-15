#!/usr/bin/env python3

import asyncio
import cProfile
import logging
import os
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, List

import aiosqlite
import click
import zstd

from chia.cmds.init_funcs import chia_init
from chia.consensus.default_constants import DEFAULT_CONSTANTS
from chia.full_node.full_node import FullNode
from chia.protocols import full_node_protocol
from chia.server.outbound_message import Message, NodeType
from chia.types.full_block import FullBlock
from chia.util.config import load_config
from tests.block_tools import make_unfinished_block
from tools.test_constants import test_constants as TEST_CONSTANTS


class ExitOnError(logging.Handler):
    def __init__(self):
        super().__init__()
        self.exit_with_failure = False

    def emit(self, record):
        if record.levelno != logging.ERROR:
            return
        self.exit_with_failure = True


@contextmanager
def enable_profiler(profile: bool, counter: int) -> Iterator[None]:
    if not profile:
        yield
        return

    with cProfile.Profile() as pr:
        receive_start_time = time.monotonic()
        yield

    if time.monotonic() - receive_start_time > 5:
        pr.create_stats()
        pr.dump_stats(f"slow-batch-{counter:05d}.profile")


class FakeServer:
    async def send_to_all(self, messages: List[Message], node_type: NodeType):
        pass


async def run_sync_test(
    file: Path, db_version, profile: bool, single_thread: bool, test_constants: bool, keep_up: bool
) -> None:

    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)
    handler = logging.FileHandler("test-full-sync.log")
    handler.setFormatter(
        logging.Formatter(
            "%(levelname)-8s %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
    )
    logger.addHandler(handler)
    check_log = ExitOnError()
    logger.addHandler(check_log)

    with tempfile.TemporaryDirectory() as root_dir:

        root_path = Path(root_dir)
        chia_init(root_path, should_check_keys=False, v1_db=(db_version == 1))
        config = load_config(root_path, "config.yaml")

        if test_constants:
            constants = TEST_CONSTANTS
        else:
            overrides = config["network_overrides"]["constants"][config["selected_network"]]
            constants = DEFAULT_CONSTANTS.replace_str_to_bytes(**overrides)
        if single_thread:
            config["full_node"]["single_threaded"] = True
        config["full_node"]["db_sync"] = "off"
        full_node = FullNode(
            config["full_node"],
            root_path=root_path,
            consensus_constants=constants,
        )

        try:
            await full_node._start()
            full_node.set_server(FakeServer())  # type: ignore[arg-type]

            print()
            counter = 0
            height = 0
            async with aiosqlite.connect(file) as in_db:
                await in_db.execute("pragma query_only")
                rows = await in_db.execute(
                    "SELECT header_hash, height, block FROM full_blocks WHERE in_main_chain=1 ORDER BY height"
                )

                block_batch = []

                start_time = time.monotonic()
                async for r in rows:
                    with enable_profiler(profile, counter):
                        block = FullBlock.from_bytes(zstd.decompress(r[2]))
                        block_batch.append(block)

                        if len(block_batch) < 32:
                            continue

                        if keep_up:
                            for b in block_batch:
                                await full_node.respond_unfinished_block(
                                    full_node_protocol.RespondUnfinishedBlock(make_unfinished_block(b, constants)), None
                                )
                                await full_node.respond_block(full_node_protocol.RespondBlock(b))
                        else:
                            success, advanced_peak, fork_height, coin_changes = await full_node.receive_block_batch(
                                block_batch, None, None  # type: ignore[arg-type]
                            )
                            end_height = block_batch[-1].height
                            full_node.blockchain.clean_block_record(end_height - full_node.constants.BLOCKS_CACHE_SIZE)

                            assert success
                            assert advanced_peak

                    counter += len(block_batch)
                    height += len(block_batch)
                    if keep_up:
                        print(
                            f"\rheight {height} {(time.monotonic() - start_time)/len(block_batch):0.2f} s/blocks   ",
                            end="",
                        )
                        start_time = time.monotonic()
                    else:
                        print(f"\rheight {height} {counter/(time.monotonic() - start_time):0.2f} blocks/s   ", end="")
                    block_batch = []
                    if check_log.exit_with_failure:
                        raise RuntimeError("error printed to log. exiting")

                    if counter >= 100000:
                        start_time = time.monotonic()
                        counter = 0
                        print()
        finally:
            print("closing full node")
            full_node._close()
            await full_node._await_closed()


@click.group()
def main() -> None:
    pass


@main.command("run", short_help="run simulated full sync from an existing blockchain db")
@click.argument("file", type=click.Path(), required=True)
@click.option("--db-version", type=int, required=False, default=2, help="the DB version to use in simulated node")
@click.option("--profile", is_flag=True, required=False, default=False, help="dump CPU profiles for slow batches")
@click.option(
    "--test-constants",
    is_flag=True,
    required=False,
    default=False,
    help="expect the blockchain database to be blocks using the test constants",
)
@click.option(
    "--single-thread",
    is_flag=True,
    required=False,
    default=False,
    help="run node in a single process, to include validation in profiles",
)
@click.option(
    "--keep-up",
    is_flag=True,
    required=False,
    default=False,
    help="pass blocks to the full node as if we're staying synced, rather than syncing",
)
def run(file: Path, db_version: int, profile: bool, single_thread: bool, test_constants: bool, keep_up: bool) -> None:
    """
    The FILE parameter should point to an existing blockchain database file (in v2 format)
    """
    print(f"PID: {os.getpid()}")
    asyncio.run(run_sync_test(Path(file), db_version, profile, single_thread, test_constants, keep_up))


@main.command("analyze", short_help="generate call stacks for all profiles dumped to current directory")
def analyze() -> None:
    from glob import glob
    from shlex import quote
    from subprocess import check_call

    for input_file in glob("slow-batch-*.profile"):
        output = input_file.replace(".profile", ".png")
        print(f"{input_file}")
        check_call(f"gprof2dot -f pstats {quote(input_file)} | dot -T png >{quote(output)}", shell=True)


main.add_command(run)
main.add_command(analyze)

if __name__ == "__main__":
    # pylint: disable = no-value-for-parameter
    main()
