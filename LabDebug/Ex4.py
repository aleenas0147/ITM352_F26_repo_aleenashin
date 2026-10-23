# Hypothesis: index 5 doesn't exist in a 5-item list (valid: 0 to 4),
# so Python raises an IndexError.
def get_element(my_list, index):
    if index < 0 or index >= len(my_list):
        return "Index out of range"
    return my_list[index]
 
my_list = [1, 2, 3, 4, 5]
print(get_element(my_list, 2))
print(get_element(my_list, 5))
# Edge case tests
print(get_element(my_list, 0))
print(get_element(my_list, 4))
print(get_element(my_list, -1))
print(get_element([], 0))
