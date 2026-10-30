import csv

total = 0
count = 0
max_miles = 0

with open("taxi_1000.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        fare = float(row["Fare"])
        miles = float(row["Trip Miles"])
        if fare > 10:
            total += fare
            count += 1
            if miles > max_miles:
                max_miles = miles

print("Total fares:", total)
print("Average fare:", total / count)
print("Max trip miles:", max_miles)