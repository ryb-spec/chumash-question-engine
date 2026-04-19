# Quiz Acceptance Checklist

Use this as a quick manual pass after quiz UI, generator, or runtime-flow changes.

## 1. First-Screen Experience

- The question appears quickly after the page loads.
- No large guidance panels sit above the active task.
- The first visible flow is: question -> answers -> submit.
- No duplicate explanatory blocks appear before the question.
- On a smaller laptop screen, the first answer choice is visible early without wasted space.

## 2. Answer / Feedback Experience

- Feedback is compact and easy to scan.
- The visible feedback shows only the essentials:
  - correctness
  - student answer
  - correct answer
  - short clue
  - short explanation
- Generic progression narration does not appear in the main feedback block.
- Extra explanation or reteach detail stays collapsed.
- The next action is visually obvious.

## 3. Transition Experience

- Continue / Retry / Next clears stale banners and stale captions.
- The next question feels fresh, not recycled.
- After an error, the same question does not repeat unless clearly intentional.
- No visible state leftovers carry over from the previous question.

## 4. Question Quality Spot-Checks

- Prefix questions are unambiguous.
- Distractors are not also plausibly correct.
- Whole-pasuk quoting is only used when actually needed.
- Morphology prompts do not bluff on stacked or ambiguous forms.

## 5. Quick Test Commands

```powershell
python -m pytest
python -m pytest tests/test_streamlit_quiz_experience.py -q
python -m pytest tests/test_streamlit_feedback_flow.py -q
python -m pytest tests/test_prefix_question_generation.py tests/test_suffix_question_generation.py -q
```
