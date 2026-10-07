def celsius_to_fahrenheit(celsius):
    assert celsius >= -273.15, "Temperature is below absolute zero"
    return celsius * 9 / 5 + 32

print(celsius_to_fahrenheit(100))     # 212.0
print(celsius_to_fahrenheit(-300))    # AssertionError: Temperature is below absolute zero