"""Create a list of even numbers from 1 through 50 using a while loop."""

even_numbers = []
number = 1

while number <= 50:
	if number % 2 == 0:
		even_numbers.append(number)
	number += 1

print(even_numbers)
