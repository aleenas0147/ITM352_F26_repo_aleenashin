# Hypothesis: x and y don't exist outside the function (NameError),
# and multiply() never returns a value. b is also a string.
def multiply(x, y):
    result = x * y
    return result
 
a = 5
b = 6
result = multiply(a, b)
print(result)
# Edge case tests
print(multiply(0, 6))
print(multiply(-2, 3))
print(multiply(2.5, 2))
