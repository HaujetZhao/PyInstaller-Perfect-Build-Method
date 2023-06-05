import sys
from pathlib import Path
from pprint import pprint

BASE_DIR = Path(__file__).parent

for p in sys.path.copy():
    relative_p = Path(p).relative_to(BASE_DIR)
    new_p = BASE_DIR / 'libs' / relative_p
    sys.path.insert(0, str(new_p))
