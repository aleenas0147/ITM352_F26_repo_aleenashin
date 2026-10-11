"""Create the odd numbers from 1 through 50 in four different ways."""

# 1. Traditional for loop with range() and an if-statement
odd_numbers_if = []
for number in range(1, 51):
	if number % 2 == 1:
		odd_numbers_if.append(number)

# 2. Use the fact that each odd number is 2 * num + 1
odd_numbers_formula = []
for num in range(25):
	odd_numbers_formula.append(2 * num + 1)

# 3. Use a step of 2, with no if-statement or formula
odd_numbers_step = []
for number in range(1, 51, 2):
	odd_numbers_step.append(number)

# 4. List comprehension
odd_numbers_comprehension = [number for number in range(1, 51) if number % 2 == 1]

print("For loop with if-statement:", odd_numbers_if)
print("Using 2 * num + 1:", odd_numbers_formula)
print("For loop with step of 2:", odd_numbers_step)
print("List comprehension:", odd_numbers_comprehension)
