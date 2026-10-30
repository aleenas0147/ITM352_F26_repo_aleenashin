salaries = []
with open("my_custom_sheet.csv", "r") as file:
    file.readline()  # skip header
    for line in file:
        parts = line.strip().split(",")
        salaries.append(float(parts[2]))

print("Average:", sum(salaries) / len(salaries))
print("Maximum:", max(salaries))
print("Minimum:", min(salaries))