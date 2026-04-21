from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from runtime.pilot_logging import (
    PILOT_EVENT_LOG_ENV_VAR,
    build_isolated_pilot_log_path,
    ensure_pilot_log_file,
    write_pilot_review_export,
)

DEFAULT_EXPORT_DIR = BASE_DIR / "data" / "pilot" / "exports"


def build_export_path(log_path: Path) -> Path:
    return DEFAULT_EXPORT_DIR / f"{log_path.stem}_review.json"


def prepare_run(label: str) -> None:
    log_path = ensure_pilot_log_file(build_isolated_pilot_log_path(label))
    export_path = build_export_path(log_path)
    payload = {
        "isolated_log_path": str(log_path),
        "suggested_export_path": str(export_path),
        "powershell_env_command": f"$env:{PILOT_EVENT_LOG_ENV_VAR} = '{log_path}'",
        "streamlit_command": "python -m streamlit run streamlit_app.py",
        "export_command": (
            f"python scripts/pilot_isolated_run.py export --input \"{log_path}\" "
            f"--output \"{export_path}\""
        ),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def export_run(input_path: Path, output_path: Path, max_sessions: int) -> None:
    written_path = write_pilot_review_export(
        output_path,
        max_sessions=max_sessions,
        path=input_path,
    )
    print(json.dumps({"input_log_path": str(input_path), "export_path": str(written_path)}, ensure_ascii=False, indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare or export an isolated Chumash pilot run.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare_parser = subparsers.add_parser("prepare", help="Create a fresh isolated pilot log path.")
    prepare_parser.add_argument("--label", default="", help="Optional short label for the isolated run file.")

    export_parser = subparsers.add_parser("export", help="Write a pilot review export from one input log.")
    export_parser.add_argument("--input", required=True, type=Path, help="Input pilot event log path.")
    export_parser.add_argument("--output", required=True, type=Path, help="Output JSON export path.")
    export_parser.add_argument("--max-sessions", type=int, default=20, help="Number of recent sessions to include.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command == "prepare":
        prepare_run(args.label)
        return
    export_run(args.input, args.output, args.max_sessions)


if __name__ == "__main__":
    main()
