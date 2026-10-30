first = input("First name: ")
middle = input("Middle initial: ")
last = input("Last name: ")

# 2. + operator
full = first + " " + middle + " " + last
print(full)

# 3. f-string
full = f"{first} {middle} {last}"
print(full)

# 4. % operator
full = "%s %s %s" % (first, middle, last)
print(full)

# 5. format()
full = "{} {} {}".format(first, middle, last)
print(full)

# 6. join()
full = " ".join([first, middle, last])
print(full)

# 7. format() with an unpacked list
names = [first, middle, last]
full = "{} {} {}".format(*names)
print(full)