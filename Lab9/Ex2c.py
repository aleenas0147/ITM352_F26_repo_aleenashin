import os

filename = "my_custom_sheet.csv"
if os.path.exists(filename) and os.access(filename, os.R_OK):
    print("Size:", os.path.getsize(filename), "bytes")
    with open(filename, "r") as file:
        print(file.read())
else:
    print("File missing or not readable")