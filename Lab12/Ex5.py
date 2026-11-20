import requests
import pandas as pd

url = "https://data.cityofchicago.org/resource/97wa-y6ff.json?$select=driver_type,count(license)&$group=driver_type"
records = requests.get(url).json()
print(records)
df = pd.DataFrame(records)
df.columns = ['driver_type', 'count']
df = df.set_index('driver_type')
print(df)