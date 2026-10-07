test_cases = [
    [],                                  # fewer than 5
    [1, 2, 3, 4],                        # fewer than 5 (upper edge)
    [1, 2, 3, 4, 5],                     # 5 (lower edge)
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],     # 10 (upper edge)
    list(range(11)),                     # more than 10 (lower edge)
    list(range(20)),                     # more than 10
]

for case in test_cases:
    n = len(case)
    if n < 5:
        print(n, "-> Fewer than 5 elements")
    elif n <= 10:
        print(n, "-> Between 5 and 10 elements")
    else:
        print(n, "-> More than 10 elements")