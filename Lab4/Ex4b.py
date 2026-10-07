email = input("Enter your email: ")

parts = email.split("@")
print("Username:", parts[0])
print("Domain:", parts[1])