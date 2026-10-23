# Hypothesis: price is a string ('$0.34'), so it can't be multiplied by a float.
# Also product.name is wrong for a dictionary - should be product["name"].
product = {"name": "small gumball", "price": 0.34}
tax_rate = 0.045
total = product["price"] + product["price"] * tax_rate
print(f"A {product['name']} costs ${total:.2f}")
# Edge case tests
for p in [0.34, 0, 10.00]:
    print(f"{p} -> {p + p * tax_rate:.2f}")