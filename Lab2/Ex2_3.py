number = float(input("Enter a decimal number between 1 and 100: "))
square = number ** 2

rounded_number = round(number, 2)
rounded_square = round(square, 2)

print(f"You entered {rounded_number}. The square is {rounded_square}.")