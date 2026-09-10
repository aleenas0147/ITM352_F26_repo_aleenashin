def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * (5 / 9)

temperature_fahrenheit = float(input("Enter a temperature in Fahrenheit: "))
temperature_celsius = fahrenheit_to_celsius(temperature_fahrenheit)

print(f"You entered {temperature_fahrenheit}°F, which is equivalent to {temperature_celsius}°C.")