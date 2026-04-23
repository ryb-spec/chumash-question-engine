from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from runtime.pilot_logging import (
    PILOT_EVENT_LOG_ENV_VAR,
    build_pilot_review_export,
    build_isolated_pilot_log_path,
    ensure_pilot_log_file,
    write_pilot_review_export,
)

DEFAULT_EXPORT_DIR = BASE_DIR / "data" / "pilot" / "exports"


def build_export_path(log_path: Path) -> Path:
    return DEFAULT_EXPORT_DIR / f"{log_path.stem}_review.json"


def resolve_export_path(input_path: Path, output_path: Path | None = None) -> Path:
    return output_path or build_export_path(input_path)


def prepare_run(label: str) -> None:
    log_path = ensure_pilot_log_file(build_isolated_pilot_log_path(label))
    export_path = build_export_path(log_path)
    payload = {
        "isolated_log_path": str(log_path),
        "suggested_export_path": str(export_path),
        "fresh_run_only_expected": True,
        "powershell_env_command": f"$env:{PILOT_EVENT_LOG_ENV_VAR} = '{log_path}'",
        "streamlit_command": "python -m streamlit run streamlit_app.py",
        "export_command": (
            f"python scripts/pilot_isolated_run.py export --input \"{log_path}\" "
            f"--output \"{export_path}\""
        ),
        "review_command": (
            f"python scripts/pilot_isolated_run.py review --input \"{log_path}\" "
            f"--output \"{export_path}\""
        ),
        "next_steps": [
            f"$env:{PILOT_EVENT_LOG_ENV_VAR} = '{log_path}'",
            "python -m streamlit run streamlit_app.py",
            f"python scripts/pilot_isolated_run.py review --input \"{log_path}\" --output \"{export_path}\"",
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def export_run(
    input_path: Path,
    output_path: Path | None,
    max_sessions: int,
    *,
    session_start_since: str | None = None,
    session_start_until: str | None = None,
    scope_id: str | None = None,
    trusted_active_scope_only: bool = False,
    latest_session_only: bool = False,
) -> None:
    resolved_output_path = resolve_export_path(input_path, output_path)
    written_path = write_pilot_review_export(
        resolved_output_path,
        max_sessions=max_sessions,
        path=input_path,
        session_start_since=session_start_since,
        session_start_until=session_start_until,
        scope_id=scope_id,
        trusted_active_scope_only=trusted_active_scope_only,
        latest_session_only=latest_session_only,
    )
    print(
        json.dumps(
            {
                "input_log_path": str(input_path),
                "export_path": str(written_path),
                "filters": {
                    "session_start_since_utc": session_start_since,
                    "session_start_until_utc": session_start_until,
                    "scope_id": scope_id,
                    "trusted_active_scope_only": trusted_active_scope_only,
                    "latest_session_only": latest_session_only,
                },
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def review_run(
    input_path: Path,
    output_path: Path | None,
    max_sessions: int,
    *,
    session_start_since: str | None = None,
    session_start_until: str | None = None,
    scope_id: str | None = None,
    trusted_active_scope_only: bool = False,
    latest_session_only: bool = False,
) -> None:
    resolved_output_path = resolve_export_path(input_path, output_path)
    export = build_pilot_review_export(
        max_sessions=max_sessions,
        path=input_path,
        session_start_since=session_start_since,
        session_start_until=session_start_until,
        scope_id=scope_id,
        trusted_active_scope_only=trusted_active_scope_only,
        latest_session_only=latest_session_only,
    )
    resolved_output_path.parent.mkdir(parents=True, exist_ok=True)
    resolved_output_path.write_text(
        json.dumps(export, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "input_log_path": str(input_path),
                "export_path": str(resolved_output_path),
                "filters": {
                    "session_start_since_utc": session_start_since,
                    "session_start_until_utc": session_start_until,
                    "scope_id": scope_id,
                    "trusted_active_scope_only": trusted_active_scope_only,
                    "latest_session_only": latest_session_only,
                },
                "release_review_summary": export.get("release_review_summary"),
                "review_window": export.get("review_window"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare or export an isolated Chumash pilot run.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare_parser = subparsers.add_parser("prepare", help="Create a fresh isolated pilot log path.")
    prepare_parser.add_argument("--label", default="", help="Optional short label for the isolated run file.")

    export_parser = subparsers.add_parser("export", help="Write a pilot review export from one input log.")
    export_parser.add_argument("--input", required=True, type=Path, help="Input pilot event log path.")
    export_parser.add_argument("--output", type=Path, help="Output JSON export path.")
    export_parser.add_argument("--max-sessions", type=int, default=20, help="Number of recent sessions to include.")
    export_parser.add_argument(
        "--session-start-since",
        default=None,
        help="Optional inclusive ISO timestamp; include only sessions that started at or after this time.",
    )
    export_parser.add_argument(
        "--session-start-until",
        default=None,
        help="Optional inclusive ISO timestamp; include only sessions that started at or before this time.",
    )
    export_parser.add_argument(
        "--scope-id",
        default=None,
        help="Optional scope_id filter for the export.",
    )
    export_parser.add_argument(
        "--trusted-active-scope-only",
        action="store_true",
        help="Include only trusted active-scope sessions in the export.",
    )
    export_parser.add_argument(
        "--latest-session-only",
        action="store_true",
        help="Include only the latest included session window after other filters are applied.",
    )

    review_parser = subparsers.add_parser(
        "review",
        help="Write a pilot review export and print the compact release-decision summary.",
    )
    review_parser.add_argument("--input", required=True, type=Path, help="Input pilot event log path.")
    review_parser.add_argument("--output", type=Path, help="Output JSON export path.")
    review_parser.add_argument("--max-sessions", type=int, default=20, help="Number of recent sessions to include.")
    review_parser.add_argument(
        "--session-start-since",
        default=None,
        help="Optional inclusive ISO timestamp; include only sessions that started at or after this time.",
    )
    review_parser.add_argument(
        "--session-start-until",
        default=None,
        help="Optional inclusive ISO timestamp; include only sessions that started at or before this time.",
    )
    review_parser.add_argument(
        "--scope-id",
        default=None,
        help="Optional scope_id filter for the export.",
    )
    review_parser.add_argument(
        "--trusted-active-scope-only",
        action="store_true",
        help="Include only trusted active-scope sessions in the export.",
    )
    review_parser.add_argument(
        "--latest-session-only",
        action="store_true",
        help="Include only the latest included session window after other filters are applied.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command == "prepare":
        prepare_run(args.label)
        return
    if args.command == "review":
        review_run(
            args.input,
            args.output,
            args.max_sessions,
            session_start_since=args.session_start_since,
            session_start_until=args.session_start_until,
            scope_id=args.scope_id,
            trusted_active_scope_only=bool(args.trusted_active_scope_only),
            latest_session_only=bool(getattr(args, "latest_session_only", False)),
        )
        return
    export_run(
        args.input,
        args.output,
        args.max_sessions,
        session_start_since=args.session_start_since,
        session_start_until=args.session_start_until,
        scope_id=args.scope_id,
        trusted_active_scope_only=bool(args.trusted_active_scope_only),
        latest_session_only=bool(getattr(args, "latest_session_only", False)),
    )


if __name__ == "__main__":
    main()
