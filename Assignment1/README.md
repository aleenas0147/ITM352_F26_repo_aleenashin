# Hawaii Trivia Quiz

Run with `python quiz.py`. Files: `quiz.py`, `questions.txt`, `scores.txt` (created automatically).

My two additional requirements: (1) write score history to a file, and (3) allow different numbers of answer options per question (4, 5, or 6 in my questions).

## Data Structure Justification
Questions are stored in `questions.txt`, one per line: `question|correct answer|wrong 1|wrong 2|...`. When loaded, each question becomes a dictionary (`{"text": ..., "options": [...]}`) and all questions go in a list.
- **Human readable / easy to edit:** one line per question means anyone can add or delete a question in a text editor without touching the code. Swapping topics only means changing `QUESTION_FILE`.
- **Easy to read in:** a single `split("|")` turns a line into its parts, so loading needs very little code.
- **Flexible:** because options are a list, a question can have any number of options, which meets requirement 3. The correct answer is always listed first in the file, so I don't need to store a letter. This avoids mistakes when someone edits the file, and the program shuffles the options so the answer position is random.
- A dictionary with named keys (`"text"`, `"options"`) is clearer than using index numbers.

## Function Design
`ask_question(question)` is the main custom function. It shuffles the options, builds the valid letters from the number of options, prints the question, validates the input, and returns `True`/`False`. It solves the problem of handling one whole question, even though questions have different numbers of options. Because it returns a boolean, `main()` only has to count the score. Other functions (`load_questions`, `save_score`, `show_history`) each do one job so the code is easy to read and test.

## Control Flow
Input is checked with a `while` loop that repeats while the answer is not exactly one valid letter (`len(answer) != 1 or answer not in valid`). The length check matters because an empty string counts as "in" any string in Python. The loop re-prompts and lists the valid letters, so the program cannot crash or move on with a bad answer. I used a loop (not a one-time `if`) because the user may make several mistakes in a row. The valid letters come from the number of options, so the same check works for 4, 5 or 6 options. `.strip().lower()` accepts "B " or "b".

## Use of AI
I used an AI assistant (Claude) as a helper on this project, mainly for generating a first draft of the code structure and the README. I decided on the quiz concept and the two additional requirements (score history file and a varying number of answer options), and I reviewed, tested, and edited the AI’s suggestions before submitting. The AI also helped me check my work against the assignment requirements and the scorecard.