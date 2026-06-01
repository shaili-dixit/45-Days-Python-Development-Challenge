"""
Hangman Game with Word Categories, ASCII Art and Session Score Tracking
Full Hangman with categories, progressive ASCII art, wins/losses tracked to file.
"""

import random
import os
import json

SCORE_FILE = "hangman_scores.json"
MAX_WRONG = 6

HANGMAN_STAGES = [
    # 0 wrong
    """
   +---+
   |   |
       |
       |
       |
       |
=========
""",
    # 1 wrong
    """
   +---+
   |   |
   O   |
       |
       |
       |
=========
""",
    # 2 wrong
    """
   +---+
   |   |
   O   |
   |   |
       |
       |
=========
""",
    # 3 wrong
    """
   +---+
   |   |
   O   |
  /|   |
       |
       |
=========
""",
    # 4 wrong
    """
   +---+
   |   |
   O   |
  /|\\  |
       |
       |
=========
""",
    # 5 wrong
    """
   +---+
   |   |
   O   |
  /|\\  |
  /    |
       |
=========
""",
    # 6 wrong (dead)
    """
   +---+
   |   |
   O   |
  /|\\  |
  / \\  |
       |
=========
""",
]

WORD_CATEGORIES = {
    "Animals": [
        "elephant", "rhinoceros", "chimpanzee", "alligator", "flamingo",
        "kangaroo", "porcupine", "chameleon", "platypus", "armadillo",
    ],
    "Countries": [
        "afghanistan", "bangladesh", "cambodia", "djibouti", "ethiopia",
        "guatemala", "honduras", "indonesia", "jamaica", "kazakhstan",
    ],
    "Programming": [
        "recursion", "inheritance", "polymorphism", "encapsulation", "abstraction",
        "dictionary", "generator", "decorator", "comprehension", "middleware",
    ],
    "Science": [
        "photosynthesis", "mitochondria", "hypothesis", "chromosome", "electromagnetic",
        "thermonuclear", "biodiversity", "gravitational", "thermodynamics", "neuroscience",
    ],
    "Movies": [
        "inception", "interstellar", "gladiator", "braveheart", "shawshank",
        "casablanca", "terminator", "ghostbusters", "avengers", "jurassic",
    ],
}


def load_scores():
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE) as f:
                return json.load(f)
        except:
            pass
    return {"wins": 0, "losses": 0, "streak": 0, "best_streak": 0, "words_guessed": []}


def save_scores(scores):
    with open(SCORE_FILE, 'w') as f:
        json.dump(scores, f, indent=2)


def pick_word(category=None):
    if category and category in WORD_CATEGORIES:
        word = random.choice(WORD_CATEGORIES[category])
    else:
        category = random.choice(list(WORD_CATEGORIES.keys()))
        word = random.choice(WORD_CATEGORIES[category])
    return word, category


def display_word(word, guessed):
    return ' '.join(c.upper() if c in guessed else '_' for c in word)


def display_state(word, guessed, wrong_letters, stage_idx):
    print(HANGMAN_STAGES[stage_idx])
    print(f"  Word: {display_word(word, guessed)}")
    print(f"  Wrong letters ({len(wrong_letters)}/{MAX_WRONG}): {' '.join(sorted(wrong_letters)).upper() or 'None'}")
    remaining = MAX_WRONG - len(wrong_letters)
    print(f"  Lives remaining: {'❤ ' * remaining}{'🖤 ' * (MAX_WRONG - remaining)}")
    all_guessed = set('abcdefghijklmnopqrstuvwxyz') - guessed - set(wrong_letters)
    print(f"  Available: {' '.join(sorted(all_guessed)).upper()}")
    print()


def play_round(category=None):
    word, cat = pick_word(category)
    guessed = set()
    wrong = set()
    hint_used = False

    print(f"\n  Category: 🏷  {cat}")
    print(f"  Word length: {len(word)} letters\n")

    while True:
        stage = len(wrong)
        display_state(word, guessed, wrong, stage)

        # Win check
        if all(c in guessed for c in word):
            print(f"  🎉 YOU WIN! The word was: {word.upper()}")
            print(HANGMAN_STAGES[0])  # Happy man
            return True, word, hint_used

        # Lose check
        if len(wrong) >= MAX_WRONG:
            print(f"  💀 GAME OVER! The word was: {word.upper()}")
            return False, word, hint_used

        prompt = input("  Guess a letter (or 'hint' / 'word' to guess whole): ").strip().lower()

        if prompt == 'hint':
            if hint_used:
                print("  ✗ Hint already used!")
                continue
            # Reveal one unguessed letter
            remaining = [c for c in word if c not in guessed]
            if remaining:
                reveal = random.choice(remaining)
                guessed.add(reveal)
                hint_used = True
                print(f"  💡 Hint: The letter '{reveal.upper()}' is in the word!")
            continue

        if prompt == 'word':
            attempt = input("  Guess the full word: ").strip().lower()
            if attempt == word:
                print(f"  🎉 CORRECT! The word was: {word.upper()}")
                return True, word, hint_used
            else:
                wrong.add('*')  # Penalty for wrong full-word guess
                print(f"  ✗ Wrong! You lose a life.")
                if len(wrong) >= MAX_WRONG:
                    print(f"  💀 GAME OVER! The word was: {word.upper()}")
                    return False, word, hint_used
            continue

        if len(prompt) != 1 or not prompt.isalpha():
            print("  ✗ Please enter a single letter.")
            continue

        if prompt in guessed or prompt in wrong:
            print(f"  ✗ You already guessed '{prompt.upper()}'.")
            continue

        if prompt in word:
            guessed.add(prompt)
            count = word.count(prompt)
            print(f"  ✓ Yes! '{prompt.upper()}' appears {count} time(s).")
        else:
            wrong.add(prompt)
            print(f"  ✗ Nope! '{prompt.upper()}' is not in the word.")


def print_scoreboard(scores):
    total = scores['wins'] + scores['losses']
    win_rate = scores['wins'] / total * 100 if total > 0 else 0
    print(f"\n  {'═'*40}")
    print(f"  📊 HANGMAN SCOREBOARD")
    print(f"  {'─'*40}")
    print(f"  Wins         : {scores['wins']}")
    print(f"  Losses       : {scores['losses']}")
    print(f"  Win Rate     : {win_rate:.1f}%")
    print(f"  Streak       : {scores['streak']}")
    print(f"  Best Streak  : {scores['best_streak']}")
    words = scores.get('words_guessed', [])
    if words:
        print(f"  Words Guessed: {', '.join(words[-5:])}")
    print(f"  {'═'*40}\n")


def main():
    print("╔══════════════════════════════════════════╗")
    print("║   Hangman Game v1.0                     ║")
    print("╚══════════════════════════════════════════╝")

    scores = load_scores()

    while True:
        print("\n  [1] Play (Random Category)")
        for i, cat in enumerate(WORD_CATEGORIES.keys(), 2):
            print(f"  [{i}] Play ({cat})")
        n = len(WORD_CATEGORIES) + 2
        print(f"  [{n}] Scoreboard")
        print(f"  [{n+1}] Quit")

        choice = input("  Choice: ").strip()

        if choice == str(n + 1):
            break
        elif choice == str(n):
            print_scoreboard(scores)
            continue

        cats = list(WORD_CATEGORIES.keys())
        selected_cat = None
        if choice == '1':
            selected_cat = None
        else:
            try:
                idx = int(choice) - 2
                if 0 <= idx < len(cats):
                    selected_cat = cats[idx]
            except ValueError:
                pass

        won, word, hint = play_round(selected_cat)
        penalty = " (hint used)" if hint else ""
        if won:
            scores['wins'] += 1
            scores['streak'] += 1
            scores['best_streak'] = max(scores['best_streak'], scores['streak'])
            scores['words_guessed'].append(word)
            print(f"  +1 Win{penalty}! Streak: {scores['streak']} 🔥")
        else:
            scores['losses'] += 1
            scores['streak'] = 0
            print(f"  +1 Loss. Streak reset.")

        save_scores(scores)
        print_scoreboard(scores)

        cont = input("  Play again? (y/n): ").strip().lower()
        if cont != 'y':
            break

    print("\n  Thanks for playing Hangman!")
    if os.path.exists(SCORE_FILE):
        os.remove(SCORE_FILE)


if __name__ == "__main__":
    main()
