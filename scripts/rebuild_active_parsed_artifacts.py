from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from torah_parser.export_bank import rebuild_active_parsed_pesukim_artifact


def main():
    artifact = rebuild_active_parsed_pesukim_artifact()
    summary = {
        "corpus_id": artifact.get("metadata", {}).get("corpus_id"),
        "status": artifact.get("metadata", {}).get("status"),
        "pesukim_count": artifact.get("metadata", {}).get("pesukim_count"),
        "range": artifact.get("metadata", {}).get("range"),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
