import pandas as pd, ssl
ssl._create_default_https_context = ssl._create_unverified_context

url = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202603"
tables = pd.read_html(url)
df = tables[0]
print(df.columns)
for index, row in df.iterrows():
    print(row['Date'], row['1 Mo'])