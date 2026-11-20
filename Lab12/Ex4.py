from sodapy import Socrata
import pandas as pd

client = Socrata("data.cityofchicago.org", None)
results = client.get("rr23-ymwb", limit=500)
df = pd.DataFrame.from_records(results)
print(df.head())
print(df.columns)
print(df[['vehicle_make', 'vehicle_fuel_source']])
print(df.groupby('vehicle_fuel_source').size())