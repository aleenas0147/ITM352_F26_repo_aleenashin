from HandyMath import max, min, midpoint, squareroot, exponent

first_number = float(input("Enter the first number: "))
second_number = float(input("Enter the second number: "))

print(f"The midpoint is {HandyMath.midpoint(first_number, second_number)}.")
print(f"The square root of the square of {first_number} is {HandyMath.squareroot(first_number ** 2)}.")
print(f"{first_number} raised to the exponent {second_number} is {HandyMath.exponent(first_number, second_number)}.")
print(f"The maximum is {HandyMath.max(first_number, second_number)} and the minimum is {HandyMath.min(first_number, second_number)}.")

