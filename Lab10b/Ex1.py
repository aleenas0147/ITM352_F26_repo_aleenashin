import pandas as pd, numpy as np

URL = "https://drive.google.com/uc?id=1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K"

try:
    df = pd.read_csv(URL, dtype_backend="pyarrow", on_bad_lines="skip")
except Exception as e:
    print("Load failed:", e)
    df = pd.read_csv("sales_data.csv", dtype_backend="pyarrow", on_bad_lines="skip")  # local fallback

print(df.head())
print(df.dtypes)

df["order_date"] = pd.to_datetime(df["order_date"], dayfirst=True,
                                  format="mixed", errors="coerce")
print(df["order_date"].head())  