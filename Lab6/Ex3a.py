age = 70
weekday = "Tuesday"
matinee = True

prices = [14]                       # normal price
if age >= 65:
    prices.append(8)
if weekday == "Tuesday":
    prices.append(10)
if matinee:
    prices.append(5 if age >= 65 else 8)

price = min(prices)

print("Age:", age, "| Weekday:", weekday, "| Matinee:", matinee)
print("Price: $", price)   # $5