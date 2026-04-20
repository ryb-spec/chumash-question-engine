import json
import random

# Load questions
with open("questions.json", "r", encoding="utf-8") as f:
    questions_data = json.load(f)

questions = questions_data["questions"]

# Load progress
try:
    with open("progress.json", "r", encoding="utf-8") as f:
        progress = json.load(f)
except:
    progress = {"words": {}}

# Initialize missing words
for q in questions:
    word = q["word"]
    if word not in progress["words"]:
        progress["words"][word] = 50  # start at neutral

# Pick weakest word
sorted_words = sorted(progress["words"].items(), key=lambda x: x[1])
weakest_word = sorted_words[0][0]

# Get questions for that word
filtered_questions = [q for q in questions if q["word"] == weakest_word]

question = random.choice(filtered_questions)

print(f"\n🎯 Word focus: {weakest_word} (Score: {progress['words'][weakest_word]})")
print("\nQuestion:")
print(question["question"])

for i, choice in enumerate(question["choices"], 1):
    print(f"{i}. {choice}")

user_input = input("\nEnter your answer (1-4): ")

try:
    selected = question["choices"][int(user_input) - 1]
except:
    print("Invalid input.")
    exit()

# Check answer
if selected == question["correct_answer"]:
    print("\n✅ Correct!")
    progress["words"][weakest_word] += 10
else:
    print("\n❌ Incorrect.")
    print(f"Correct answer: {question['correct_answer']}")
    progress["words"][weakest_word] -= 10

# Clamp score between 0–100
progress["words"][weakest_word] = max(0, min(100, progress["words"][weakest_word]))

print(f"\n📊 New Score for {weakest_word}: {progress['words'][weakest_word]}")
print(f"Explanation: {question['explanation']}")

# Save progress
with open("progress.json", "w", encoding="utf-8") as f:
    json.dump(progress, f, indent=2, ensure_ascii=False)    