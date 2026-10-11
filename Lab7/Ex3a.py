"""Count the string elements in a tuple of word-number pairs."""

items = (("hello", 10), ("goodbye", 3), ("goodnight", 5))
string_count = 0

for pair in items:
	for element in pair:
		if isinstance(element, str):
			string_count += 1

print("There are", string_count, "strings in the tuple.")
