def isLeapYear(year):
    if year % 400 == 0:
        return "Leap year"
    if year % 100 == 0:
        return "Not a leap year"
    if year % 4 == 0:
        return "Leap year"
    return "Not a leap year"

print(isLeapYear(2024))   # Leap year
print(isLeapYear(2023))   # Not a leap year
print(isLeapYear(1900))   # Not a leap year