import pandas as pd

homes = pd.read_csv("homes_data.csv")

print(homes.shape)    # (67638, 11)
print(homes.head(10))

big = homes[homes["units"] >= 500].drop(columns=["id","easement","block","lot"])
print(big.head(10))

print(homes.dtypes)
for c in ["land_sqft","gross_sqft","sale_price"]:
    homes[c] = pd.to_numeric(homes[c], errors="coerce")
homes["borough"] = homes["borough"].astype("category")
print(homes.dtypes)
print(homes)

homes = homes.drop(columns=["easement"])   # column is empty
homes = homes.dropna().drop_duplicates()
print(homes)

homes = homes[homes["sale_price"] > 0]
print(homes)
print("Average sale price:", homes["sale_price"].mean())   # about 1,534,948