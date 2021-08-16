import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

l = "PSO_Outputs_Sunkoshi2_Only-1.xlsx"
df = pd.read_excel(l, sheet_name='Energy',usecols='Data')
print(df)
exceedance = []
it = 5
while it < 100:
    s=np.percentile(df.Data, 100 - it)
    exceedance.append([it , s])
    it = it + 5


print(exceedance)
df["Exceedance"] = exceedance
# df.to_excel("check.xlsx", index=False)
