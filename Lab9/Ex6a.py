import json

with open("quiz.json", "r") as file:
    quiz = json.load(file)

print(quiz)