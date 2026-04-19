from __future__ import annotations

import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


from question_validation_audit import write_question_validation_audit


def main() -> None:
    write_question_validation_audit()


if __name__ == "__main__":
    main()
