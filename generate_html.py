import json
import html as h

with open('questions.json', encoding='utf-8') as f:
    data = json.load(f)

questions = data['questions']

rows = []
for i, q in enumerate(questions, 1):
    choices_html = ''.join(
        f'<li class="correct">{h.escape(c)}</li>' if c == q['correct_answer']
        else f'<li>{h.escape(c)}</li>'
        for c in q['choices']
    )
    rows.append(f'''
    <tr>
      <td>{i}</td>
      <td class="hebrew">{h.escape(q.get("word",""))}</td>
      <td>{h.escape(q.get("skill",""))}</td>
      <td dir="auto">{h.escape(q["question"])}</td>
      <td><ol>{choices_html}</ol></td>
      <td class="correct-cell">{h.escape(q["correct_answer"])}</td>
      <td>{h.escape(q.get("explanation",""))}</td>
      <td>{q.get("difficulty","")}</td>
      <td>{h.escape(q.get("standard",""))}</td>
      <td>{h.escape(q.get("micro_standard",""))}</td>
    </tr>''')

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chumash Question Bank</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 20px; background: #f9f9f9; color: #222; }}
    h1 {{ text-align: center; color: #2c3e50; }}
    .subtitle {{ text-align: center; color: #666; margin-bottom: 20px; }}
    table {{ border-collapse: collapse; width: 100%; background: #fff; box-shadow: 0 1px 4px rgba(0,0,0,.1); }}
    th {{ background: #2c3e50; color: #fff; padding: 10px 8px; text-align: left; position: sticky; top: 0; }}
    td {{ padding: 8px; border-bottom: 1px solid #e0e0e0; vertical-align: top; }}
    tr:nth-child(even) {{ background: #f4f6f8; }}
    tr:hover {{ background: #eaf1fb; }}
    .hebrew {{ font-size: 1.3em; direction: rtl; unicode-bidi: isolate; font-weight: bold; }}
    td[dir="auto"], li, .correct-cell {{ unicode-bidi: plaintext; }}
    ol {{ margin: 0; padding-left: 18px; }}
    li.correct {{ color: #27ae60; font-weight: bold; }}
    .correct-cell {{ color: #27ae60; font-weight: bold; }}
    input#search {{ display: block; margin: 0 auto 16px; padding: 8px 14px; width: 340px; border: 1px solid #ccc; border-radius: 20px; font-size: 1em; }}
  </style>
</head>
<body>
  <h1>&#x1F4DA; Chumash Question Bank</h1>
  <p class="subtitle">{len(questions)} questions &nbsp;&bull;&nbsp; Standards: WM &amp; CF</p>
  <input id="search" type="text" placeholder="Search questions, words, skills..." oninput="filterTable(this.value)">
  <table id="qtable">
    <thead>
      <tr>
        <th>#</th>
        <th>Word</th>
        <th>Skill</th>
        <th>Question</th>
        <th>Choices</th>
        <th>Answer</th>
        <th>Explanation</th>
        <th>Difficulty</th>
        <th>Standard</th>
        <th>Micro</th>
      </tr>
    </thead>
    <tbody>
{''.join(rows)}
    </tbody>
  </table>
  <script>
    function filterTable(val) {{
      const lower = val.toLowerCase();
      document.querySelectorAll('#qtable tbody tr').forEach(row => {{
        row.style.display = row.textContent.toLowerCase().includes(lower) ? '' : 'none';
      }});
    }}
  </script>
</body>
</html>"""

with open('questions.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f'Generated questions.html with {len(questions)} questions.')
