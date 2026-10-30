import csv

salaries = []
with open("my_custom_sheet.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        salaries.append(float(row["Annual_Salary"]))

print("Average:", sum(salaries) / len(salaries))
print("Maximum:", max(salaries))
print("Minimum:", min(salaries))