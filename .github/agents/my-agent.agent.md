# adaptive_engine.py

class AdaptiveEngine:
    def __init__(self, min_difficulty=1, max_difficulty=5):
        self.min_difficulty = min_difficulty
        self.max_difficulty = max_difficulty

        self.current_difficulty = 1
        self.correct_streak = 0
        self.wrong_streak = 0

    def update(self, is_correct):
        if is_correct:
            self.correct_streak += 1
            self.wrong_streak = 0
        else:
            self.wrong_streak += 1
            self.correct_streak = 0

        difficulty_change = 0

        # Increase difficulty
        if self.correct_streak >= 3:
            if self.current_difficulty < self.max_difficulty:
                self.current_difficulty += 1
                difficulty_change = +1
            self.correct_streak = 0  # reset after level up

        # Decrease difficulty
        elif self.wrong_streak >= 2:
            if self.current_difficulty > self.min_difficulty:
                self.current_difficulty -= 1
                difficulty_change = -1
            self.wrong_streak = 0  # reset after drop

        return {
            "difficulty": self.current_difficulty,
            "difficulty_change": difficulty_change,
            "repeat": not is_correct
        }
