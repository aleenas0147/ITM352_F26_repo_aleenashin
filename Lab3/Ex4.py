def celsius_to_fahrenheit(celsius):
	return (celsius * 9 / 5) + 32


def fahrenheit_to_celsius(fahrenheit):
	return (fahrenheit - 32) * 5 / 9


def celsius_to_kelvin(celsius):
	return celsius + 273.15


def kelvin_to_celsius(kelvin):
	return kelvin - 273.15


def fahrenheit_to_kelvin(fahrenheit):
	return (fahrenheit - 32) * 5 / 9 + 273.15


def kelvin_to_fahrenheit(kelvin):
	return (kelvin - 273.15) * 9 / 5 + 32


def convert_temperature(temperature, conversion_function):
	return conversion_function(temperature)


temperature = float(input("Enter a temperature: "))
print(f"Celsius to Fahrenheit: {convert_temperature(temperature, celsius_to_fahrenheit)}")
print(f"Fahrenheit to Celsius: {convert_temperature(temperature, fahrenheit_to_celsius)}")
print(f"Celsius to Kelvin: {convert_temperature(temperature, celsius_to_kelvin)}")
print(f"Kelvin to Celsius: {convert_temperature(temperature, kelvin_to_celsius)}")
print(f"Fahrenheit to Kelvin: {convert_temperature(temperature, fahrenheit_to_kelvin)}")
print(f"Kelvin to Fahrenheit: {convert_temperature(temperature, kelvin_to_fahrenheit)}")
