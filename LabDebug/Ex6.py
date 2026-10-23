# Hypothesis: range(10) is 0-9, not 1-10. Also, the continue runs for
# every number except 5, so the "if x == 8" check is never reached.
for x in range(1, 11):
    if x == 8:
        print("done!")
        break
    if x == 5:
        continue
    print(x)
