from typing import Generator, KeysView

SERVICES_FOR_GROUP = {
    "all": "timecoin_harvester timecoin_timelord_launcher timecoin_timelord timecoin_farmer timecoin_full_node timecoin_wallet".split(),
    "node": "timecoin_full_node".split(),
    "harvester": "timecoin_harvester".split(),
    "farmer": "timecoin_harvester timecoin_farmer timecoin_full_node timecoin_wallet".split(),
    "farmer-no-wallet": "timecoin_harvester timecoin_farmer timecoin_full_node".split(),
    "farmer-only": "timecoin_farmer".split(),
    "timelord": "timecoin_timelord_launcher timecoin_timelord timecoin_full_node".split(),
    "timelord-only": "timecoin_timelord".split(),
    "timelord-launcher-only": "timecoin_timelord_launcher".split(),
    "wallet": "timecoin_wallet timecoin_full_node".split(),
    "wallet-only": "timecoin_wallet".split(),
    "introducer": "timecoin_introducer".split(),
    "simulator": "timecoin_full_node_simulator".split(),
}


def all_groups() -> KeysView[str]:
    return SERVICES_FOR_GROUP.keys()


def services_for_groups(groups) -> Generator[str, None, None]:
    for group in groups:
        for service in SERVICES_FOR_GROUP[group]:
            yield service


def validate_service(service: str) -> bool:
    return any(service in _ for _ in SERVICES_FOR_GROUP.values())
