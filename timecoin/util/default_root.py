import os
from pathlib import Path

DEFAULT_ROOT_PATH = Path(os.path.expanduser(os.getenv("TIMECOIN_ROOT", "~/.timecoin/mainnet"))).resolve()

DEFAULT_KEYS_ROOT_PATH = Path(os.path.expanduser(os.getenv("TIMECOIN_KEYS_ROOT", "~/.timecoin_keys"))).resolve()
