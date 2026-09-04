# Basic calculator program

while True:
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        continue

    print("Choose an operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")

    choice = input("Enter your choice (1/2/3/4): ")

    if choice == '1':
        result = num1 + num2
        operation = 'Addition'
    elif choice == '2':
        result = num1 - num2
        operation = 'Subtraction'
    elif choice == '3':
        result = num1 * num2
        operation = 'Multiplication'
    elif choice == '4':
        if num2 == 0:
            print("Error: Cannot divide by zero.")
            continue
        result = num1 / num2
        operation = 'Division'
    else:
        print("Invalid operation selected.")
        continue

    print(f"{operation} result: {result}")

    again = input("Would you like to perform another calculation? (y/n): ").lower()
    if again != 'y':
        break
