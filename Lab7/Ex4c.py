def check_budget(purchases, budget):
    results = []
    for expense in purchases:
        if expense > budget:
            results.append("This purchase is over budget!")
        else:
            results.append("This purchase is within budget")
    return results

# Test cases
assert check_budget([36.13, 183.35], 50) == [
    "This purchase is within budget",
    "This purchase is over budget!",
]
assert check_budget([50], 50) == ["This purchase is within budget"]  # equal to budget
assert check_budget([], 50) == []                                     # empty list
assert check_budget([100, 200], 50) == ["This purchase is over budget!"] * 2
print("All tests passed!")