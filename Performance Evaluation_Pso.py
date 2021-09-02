import numpy as np
import pandas as pd

Datas = pd.read_excel(r'S3-check.xlsx', sheet_name='Outputs')
Energy = Datas["Energy_Sunkoshi_3"]
X = 100  # float(input('Please Enter Energy limit to check for:'))  # Satisfactory_Energy_limit
total = Energy.count()
count = sum(i > X for i in Energy)
print("Number of favorable occurrence", count)
print("reliability percent:", count / total * 100)
print(Energy)
P = sum(abs(Energy - X))
print("Vulnerability:", P / (total - count))
