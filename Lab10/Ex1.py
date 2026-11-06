import numpy as np
import pandas as pd

pct = [10,20,30,40,50,60,70,80,90]
inc = [14629,25600,37002,50000,63179,79542,100162,130000,184292]
data_list = list(zip(pct, inc))
print(data_list)
arr = np.array(data_list)
print("Shape:", arr.shape)    # (9, 2)
print("Elements:", arr.size)  # 18
print("Percentile  Income")
for p, i in arr:
    print(f"{p:>10}  {i:>7}")