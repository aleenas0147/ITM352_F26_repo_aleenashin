# Hypothesis: removing items while looping skips the next item,
# so some low scores (like 30) are never checked.
scores = [60, 45, 30, 85, 10, 90]
passing = []
for score in scores:
    if score >= 50:
        passing.append(score)
print(passing)
# Edge case tests
for test in [[], [10, 20, 30], [50, 49, 51]]:
    result = []
    for s in test:
        if s >= 50:
            result.append(s)
    print(test, "->", result)
