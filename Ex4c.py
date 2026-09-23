email = input("Enter your email: ")

at = email.index("@")
print("Username:", email[:at])
print("Domain:", email[at + 1:])