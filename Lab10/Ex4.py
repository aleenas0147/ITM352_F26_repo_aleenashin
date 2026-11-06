import pandas as pd

taxi = pd.read_json("Taxi_Trips.json")
print(taxi.describe(include="all"))
print("Median fare:", taxi["fare"].median())   # 6.65