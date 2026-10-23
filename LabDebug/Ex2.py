# Hypothesis: "=" replaces total_price each loop, so only the last item counts.
prices = [5.95, 3.00, 12.50]
total_price = 0
tax_rate = 1.08    # 8% tax
for price in prices:
    total_price += price * tax_rate
print(f"Total price (with tax): ${total_price:.2f}")
# Edge case tests
for test in [[], [10], [1.00, 2.00]]:
    t = 0
    for price in test:
        t += price * tax_rate
    print(test, "->", f"${t:.2f}")