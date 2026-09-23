first_name = input("Enter your first name: ")
middle_initial = input("Enter your middle initial: ")
last_name = input("Enter your last name: ")

full_name = first_name + " " + middle_initial + " " + last_name
print(full_name)

# + operator
full = first_name + " " + middle_initial + " " + last_name
print(full)

# f-string
full = f"{first_name} {middle_initial} {last_name}"
print(full)

# % operator
full = "%s %s %s" % (first_name, middle_initial, last_name)
print(full)

# format()
full = "{} {} {}".format(first_name, middle_initial, last_name)
print(full)

# join()
full = " ".join([first_name, middle_initial, last_name])
print(full)

# format() with an unpacked list
parts = [first_name, middle_initial, last_name]
full = "{} {} {}".format(*parts)
print(full)