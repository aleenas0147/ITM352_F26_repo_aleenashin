# List of individuals' ages
import pandas as pd


ages = [25, 30, 22, 35, 28, 40, 50, 18, 60, 45]


#Lists of individuals' names and genders
names = ["Joe", "Jaden", "Max", "Sidney", "Evgeni", "Taylor", "Pia", "Luis", "Blanca", "Cyndi"]
gender = ["M", "M", "M", "F", "M", "F", "F", "M", "F", "F"]

#Create the lists
ages = [25, 30, 22, 35, 28, 40, 50, 18, 60, 45]
names = ["Joe","Jaden","Max","Sidney","Evgeni","Taylor","Pia","Luis","Blanca","Cyndi"]
gender = ["M","M","M","F","M","F","F","M","F","F"]

#Use zip() to make (age, gender) tuples
pairs = list(zip(ages, gender))
print(pairs)

#Convert to a DataFrame and describe it
df = pd.DataFrame(pairs, index=names, columns=["Age","Gender"])
print(df)
print(df.describe())