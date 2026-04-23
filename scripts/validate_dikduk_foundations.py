from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation_dikduk import validate_dikduk_foundations


def main():
    errors = validate_dikduk_foundations()
    if errors:
        for message in errors:
            print(message)
        raise SystemExit(1)
    print("Dikduk foundations package is valid.")


if __name__ == "__main__":
    main()
