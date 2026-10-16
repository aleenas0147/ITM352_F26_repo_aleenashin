# Hawaii Trivia Quiz
# - Questions are loaded from a text file (easy to add/remove/swap topics).
# - Questions can have a different number of answer options (4, 5, 6...).
# - Every score is saved to a history file.
 
import random
from pathlib import Path
 
BASE_DIR = Path(__file__).resolve().parent
QUESTION_FILE = BASE_DIR / "questions.txt"   # change this to use a different topic
SCORE_FILE = BASE_DIR / "scores.txt"         # history of scores is appended here
LETTERS = "abcdefgh"              # letters used to label the options
 
 
def load_questions(filename):
    """Read questions from a file and return a list of dictionaries.
 
    Each line looks like:  question|correct answer|wrong 1|wrong 2|...
    The correct answer is always listed first in the file; the program
    shuffles the options later so the answer position is random.
    """
    questions = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line == "":              # skip blank lines
                continue
            parts = line.split("|")
            questions.append({"text": parts[0], "options": parts[1:]})
    return questions
 
 
def ask_question(question):
    """Ask one question, keep asking until the answer is valid,
    then tell the user if they were right. Returns True or False."""
    options = question["options"][:]    # copy so the original is not changed
    correct_text = options[0]           # correct answer is first in the file
    random.shuffle(options)
 
    # Only letters that match the number of options are valid
    valid = LETTERS[:len(options)]
 
    print("\n" + question["text"])
    for i in range(len(options)):
        print("  " + valid[i] + ") " + options[i])
 
    # Validation loop: repeat until the user types exactly one valid letter
    answer = input("Your answer (" + valid[0] + "-" + valid[-1] + "): ").strip().lower()
    while len(answer) != 1 or answer not in valid:
        print("Invalid choice. Please enter one of: " + ", ".join(valid))
        answer = input("Your answer (" + valid[0] + "-" + valid[-1] + "): ").strip().lower()
 
    chosen_text = options[valid.index(answer)]
    if chosen_text == correct_text:
        print("Correct!")
        return True
    print("Wrong. The correct answer was: " + correct_text)
    return False
 
 
def save_score(name, score, total):
    """Add this player's score to the end of the history file."""
    with open(SCORE_FILE, "a", encoding="utf-8") as file:
        file.write(name + "," + str(score) + "," + str(total) + "\n")
 
 
def show_history():
    """Print every score saved in the history file."""
    print("\n--- Score History ---")
    if not SCORE_FILE.exists():
        print("No scores saved yet.")
        return
    with open(SCORE_FILE, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(",")
            print(parts[0] + ": " + parts[1] + "/" + parts[2])
 
 
def main():
    questions = load_questions(QUESTION_FILE)
    name = input("Enter your name: ").strip()
    play_again = "y"
 
    while play_again == "y":
        random.shuffle(questions)       # new question order each round
        score = 0
        for question in questions:
            if ask_question(question):
                score += 1
            print("Score so far: " + str(score))
 
        print("\nFinal score: " + str(score) + "/" + str(len(questions)))
        save_score(name, score, len(questions))
        show_history()
 
        play_again = input("\nPlay again? (y/n): ").strip().lower()
 
    print("Thanks for playing!")
 
 
main()