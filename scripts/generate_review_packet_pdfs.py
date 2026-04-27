from __future__ import annotations

import argparse
import html
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "data" / "curriculum_extraction" / "reports"

DEFAULT_PACKET_SPECS = (
    (
        "Batch 002 Trusted Source Extraction Accuracy Review Packet",
        REPORTS_DIR / "batch_002_trusted_source_extraction_accuracy_review_packet_print.md",
        REPORTS_DIR / "batch_002_trusted_source_extraction_accuracy_review_packet_print.pdf",
    ),
    (
        "Batch 003 Trusted Source Extraction Accuracy Review Packet",
        REPORTS_DIR / "batch_003_trusted_source_extraction_accuracy_review_packet_print.md",
        REPORTS_DIR / "batch_003_trusted_source_extraction_accuracy_review_packet_print.pdf",
    ),
)

DEFAULT_COMBINED_PDF = REPORTS_DIR / "batch_002_003_trusted_source_extraction_accuracy_review_packets_combined.pdf"

GENERATED_REVIEW_NOTE = (
    "Review purpose: Yossi extraction-accuracy confirmation only. "
    "This does not approve runtime use, question generation, reviewed-bank promotion, or student-facing release."
)


def repo_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def find_chrome() -> Path | None:
    candidates = [
        os.environ.get("CHROME_PATH"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    ]
    for candidate in candidates:
        if not candidate:
            continue
        path = Path(candidate)
        if path.exists():
            return path
    for executable in ("chrome", "google-chrome", "chromium", "msedge"):
        found = shutil.which(executable)
        if found:
            return Path(found)
    return None


def inline_markdown(value: str) -> str:
    escaped = html.escape(value)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


def split_table_row(line: str) -> list[str]:
    stripped = line.strip().strip("|")
    return [cell.strip() for cell in stripped.split("|")]


def is_table_separator(line: str) -> bool:
    return bool(re.fullmatch(r"\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*", line))


def render_table(lines: list[str]) -> str:
    headers = split_table_row(lines[0])
    body_lines = lines[2:] if len(lines) > 1 and is_table_separator(lines[1]) else lines[1:]
    rendered = ["<table>", "<thead><tr>"]
    for header in headers:
        rendered.append(f"<th>{inline_markdown(header)}</th>")
    rendered.append("</tr></thead>")
    rendered.append("<tbody>")
    for line in body_lines:
        cells = split_table_row(line)
        rendered.append("<tr>")
        for index in range(len(headers)):
            cell = cells[index] if index < len(cells) else ""
            rendered.append(f'<td dir="auto">{inline_markdown(cell)}</td>')
        rendered.append("</tr>")
    rendered.append("</tbody></table>")
    return "\n".join(rendered)


def markdown_to_body(markdown_text: str) -> str:
    lines = markdown_text.splitlines()
    output: list[str] = []
    list_stack: list[str] = []
    index = 0

    def close_lists() -> None:
        while list_stack:
            output.append(f"</{list_stack.pop()}>")

    while index < len(lines):
        raw_line = lines[index]
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped:
            close_lists()
            index += 1
            continue

        if stripped.startswith("<div") and "page-break-after" in stripped:
            close_lists()
            output.append('<div class="page-break"></div>')
            index += 1
            continue

        if stripped.startswith("|") and index + 1 < len(lines) and is_table_separator(lines[index + 1]):
            close_lists()
            table_lines = [stripped]
            index += 1
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append(lines[index].strip())
                index += 1
            output.append(render_table(table_lines))
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            close_lists()
            level = len(heading.group(1))
            output.append(f"<h{level}>{inline_markdown(heading.group(2))}</h{level}>")
            index += 1
            continue

        numbered = re.match(r"^\d+\.\s+(.+)$", stripped)
        if numbered:
            if not list_stack or list_stack[-1] != "ol":
                close_lists()
                output.append("<ol>")
                list_stack.append("ol")
            output.append(f"<li>{inline_markdown(numbered.group(1))}</li>")
            index += 1
            continue

        bullet = re.match(r"^-\s+(.+)$", stripped)
        if bullet:
            if not list_stack or list_stack[-1] != "ul":
                close_lists()
                output.append("<ul>")
                list_stack.append("ul")
            item = bullet.group(1)
            if item.startswith("[ ] "):
                label = item[4:]
                output.append(f'<li class="checkbox"><span class="box"></span>{inline_markdown(label)}</li>')
            else:
                output.append(f"<li>{inline_markdown(item)}</li>")
            index += 1
            continue

        close_lists()
        output.append(f'<p dir="auto">{inline_markdown(stripped)}</p>')
        index += 1

    close_lists()
    return "\n".join(output)


def render_html_document(title: str, markdown_text: str) -> str:
    body = markdown_to_body(markdown_text)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
{print_styles()}
</head>
<body>
<section class="generated-note">
  <strong>{html.escape(GENERATED_REVIEW_NOTE)}</strong>
</section>
{body}
</body>
</html>
"""


def print_styles() -> str:
    return """<style>
@page { size: Letter landscape; margin: 0.48in; }
* { box-sizing: border-box; }
body {
  color: #182431;
  font-family: Arial, "Noto Sans Hebrew", "Times New Roman", sans-serif;
  font-size: 11.8px;
  line-height: 1.38;
  margin: 0;
}
h1 {
  color: #102a43;
  font-size: 25px;
  margin: 0 0 12px;
  border-bottom: 3px solid #102a43;
  padding-bottom: 8px;
}
h2 {
  color: #17324d;
  font-size: 18px;
  margin: 20px 0 8px;
  break-after: avoid;
}
h3 {
  color: #243b53;
  font-size: 15px;
  margin: 16px 0 8px;
  padding: 7px 9px;
  background: #f0f4f8;
  border-left: 5px solid #486581;
  break-after: avoid;
}
p { margin: 6px 0; unicode-bidi: plaintext; }
ul, ol { margin: 6px 0 10px 22px; padding: 0; }
li { margin: 3px 0; }
code {
  background: #f3f4f6;
  border: 1px solid #d9e2ec;
  border-radius: 4px;
  font-family: Consolas, "Courier New", monospace;
  padding: 1px 4px;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin: 8px 0 12px;
  table-layout: fixed;
  break-inside: avoid;
  page-break-inside: avoid;
}
th, td {
  border: 1px solid #9fb3c8;
  padding: 6px 7px;
  vertical-align: top;
  overflow-wrap: anywhere;
  unicode-bidi: plaintext;
}
th {
  background: #d9eaf7;
  color: #102a43;
  font-weight: bold;
}
tr:nth-child(even) td { background: #fbfdff; }
.checkbox {
  list-style: none;
  margin-left: -16px;
}
.box {
  display: inline-block;
  width: 13px;
  height: 13px;
  border: 1.6px solid #111827;
  margin-right: 7px;
  vertical-align: -2px;
}
.generated-note {
  border: 2px solid #17324d;
  border-radius: 10px;
  background: #f8fbfd;
  padding: 10px 12px;
  margin: 0 0 14px;
  color: #102a43;
}
.page-break { break-after: page; page-break-after: always; height: 0; }
section.packet-divider {
  break-before: page;
  page-break-before: always;
  min-height: 7in;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}
section.packet-divider h1 {
  border-bottom: none;
  font-size: 30px;
}
@media print {
  h1, h2, h3, table { break-inside: avoid; }
}
</style>"""


def render_combined_html(packet_docs: list[tuple[str, str]]) -> str:
    sections: list[str] = []
    for index, (title, markdown_text) in enumerate(packet_docs):
        if index:
            sections.append(
                f'<section class="packet-divider"><h1>{html.escape(title)}</h1>'
                '<p>Continuation of combined Yossi extraction-accuracy review packet.</p></section>'
            )
        sections.append('<section class="generated-note"><strong>' + html.escape(GENERATED_REVIEW_NOTE) + "</strong></section>")
        sections.append(markdown_to_body(markdown_text))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Batch 002 and 003 Trusted Source Review Packets</title>
{print_styles()}
</head>
<body>
{''.join(sections)}
</body>
</html>
"""


def print_html_to_pdf(chrome_path: Path, html_text: str, pdf_path: Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="review-packet-pdf-") as tmpdir:
        tmp_path = Path(tmpdir)
        html_path = tmp_path / "packet.html"
        user_data_dir = tmp_path / "chrome-profile"
        user_data_dir.mkdir()
        html_path.write_text(html_text, encoding="utf-8")
        command = [
            str(chrome_path),
            "--headless",
            "--disable-gpu",
            "--no-first-run",
            "--no-default-browser-check",
            f"--user-data-dir={user_data_dir}",
            f"--print-to-pdf={pdf_path}",
            "--print-to-pdf-no-header",
            html_path.as_uri(),
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode not in (0, None):
            raise RuntimeError(
                f"Chrome PDF generation failed for {repo_relative(pdf_path)} with exit code {result.returncode}: "
                f"{result.stderr.strip() or result.stdout.strip()}"
            )
    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        raise RuntimeError(f"PDF was not created or is empty: {repo_relative(pdf_path)}")


def generate_default_pdfs() -> list[Path]:
    chrome_path = find_chrome()
    if chrome_path is None:
        raise RuntimeError(
            "No PDF backend found. Install Chrome/Edge, pandoc, wkhtmltopdf, or a Python PDF backend before running this script."
        )

    generated: list[Path] = []
    packet_docs: list[tuple[str, str]] = []
    for title, markdown_path, pdf_path in DEFAULT_PACKET_SPECS:
        if not markdown_path.exists():
            raise FileNotFoundError(f"source Markdown packet missing: {repo_relative(markdown_path)}")
        markdown_text = markdown_path.read_text(encoding="utf-8")
        packet_docs.append((title, markdown_text))
        print_html_to_pdf(chrome_path, render_html_document(title, markdown_text), pdf_path)
        generated.append(pdf_path)

    combined_html = render_combined_html(packet_docs)
    print_html_to_pdf(chrome_path, combined_html, DEFAULT_COMBINED_PDF)
    generated.append(DEFAULT_COMBINED_PDF)
    return generated


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate print-ready PDFs from trusted-source review packet Markdown.")
    parser.add_argument("--default-batches", action="store_true", help="Generate Batch 002, Batch 003, and combined PDFs.")
    args = parser.parse_args()

    if not args.default_batches:
        parser.error("Only --default-batches is currently supported.")

    generated = generate_default_pdfs()
    for path in generated:
        print(f"created {repo_relative(path)} ({path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
