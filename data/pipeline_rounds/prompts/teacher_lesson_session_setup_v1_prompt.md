# Teacher Lesson / Session Setup V1 Prompt

You are working in the chumash-question-engine repo.

TASK TITLE:
Teacher Lesson / Session Setup V1.

PURPOSE:
Create a lightweight teacher-facing way to label or select today's lesson/session before practice begins, so classroom pilots can connect local Runtime Learning Intelligence exposure summaries to a clear instructional context.

CURRENT PRODUCT CONTEXT:
Runtime Learning Intelligence V1 is implemented, smoke-tested, fallback-confirmed, and safe enough to keep enabled for continued pilot use. The Runtime Exposure Center shows local attempt-history exposure, repeated targets, repeated pasuk/skill combinations, and fallback/scope-small status.

GOAL:
Let the teacher define local session metadata such as lesson label, optional mode focus, optional class period label, and optional teacher notes without adding auth, database, PII, new content, scoring changes, or runtime scope expansion.

HARD BOUNDARIES:
Do NOT:
- add authentication
- add a database
- add student PII
- create new questions or content
- change scoring/mastery
- widen active runtime scope
- activate any new Perek
- promote reviewed-bank/runtime content
- change source truth
- expose raw logs
- change Runtime Learning Intelligence weighting
- change question-selection behavior except for existing safe filters/config if explicitly approved in the task

ALLOWED:
- Add a local teacher-facing session setup control in the existing Streamlit sidebar or teacher monitor area.
- Store session metadata in Streamlit session state and/or a safe local metadata artifact if appropriate.
- Integrate session metadata with the Runtime Exposure Center display.
- Add docs, validator, and tests.
- Keep all runtime/reviewed-bank/student-facing safety gates closed.

REQUIRED WORK PRODUCTS:
1. A short implementation report in `data/pipeline_rounds/`.
2. A machine-readable JSON contract in `data/pipeline_rounds/`.
3. A lightweight UI/session-state implementation.
4. Runtime docs update.
5. Concise README/index updates.
6. One fail-closed validator.
7. One focused test file.

VALIDATION:
Run the new validator/test, Runtime Learning Intelligence validators/tests, curriculum validators, targeted runtime/UI tests, and full pytest.

FINAL SAFETY CONFIRMATION:
Report whether runtime scope changed, scoring/mastery changed, question selection changed, auth/database/PII was added, raw logs were exposed, or student-facing content was created.
