
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

df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
df["sales"] = df["quantity"] * df["unit_price"]

pd.set_option("display.max_columns", None)

pivot = pd.pivot_table(df, values="sales", index="sales_region",
                       columns="order_type", aggfunc=np.sum, margins=True)
print(pivot)

pd.set_option("display.float_format", "${:,.2f}".format)

pivot2 = pd.pivot_table(df, values="sales",
                        index=["sales_region", "customer_state"],
                        columns="order_type",
                        aggfunc=[np.sum, np.mean], margins=True)
print(pivot2)