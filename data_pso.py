import pandas as pd
import numpy as np
import bisect

"""
  Initialization
  ===============
   Input following commands on python console
     pip install pandas
     pip install numpy
     pip install bisect

  Import data's
  ===============  
    Required data's like time series inflow and H-A-V curve data's are imported.

  Interpolation
  ===============  
    H-A-V data's are is interpolated for known storage volume to return corresponding
    elevation and surface area.
"""
df = pd.read_excel(r'pso_data1.xlsx')
Start = df['Date'][0]
End = df['Date'][df.index[-1]]
df['Year'] = pd.DatetimeIndex(df['Date']).year
Fyear = df['Year'][0]
Lyear = df['Year'][df.index[-1]]
Tyear = Lyear - Fyear + 1
I3 = df['Pachuwarghat'] + df['Local Inflow at Sunkoshi III']
I3 = I3.tolist()
l2 = df['Local Inflow at Sunkoshi II'].tolist()
l1 = df['Sangutar'] + df['Rabuwa Bazar'] + df['Local Inflow at Sunkoshi I']
l1_ = df['Sangutar'] + df['Local Inflow at Sunkoshi I']
l1 = l1.tolist()
Is1 = df['Khurkot'] + df['Sangutar'] + df['Rabuwa Bazar'] + df['Local Inflow at Sunkoshi I']
Is2 = df['Khurkot']
Dk = df['Rabuwa Bazar'].tolist()
Ex1 = pd.read_excel(r'Sunkoshi.xlsx', sheet_name='SUNKOSHI1')
Ex2 = pd.read_excel(r'Sunkoshi.xlsx', sheet_name='SUNKOSHI2')
Ex3 = pd.read_excel(r'Sunkoshi.xlsx', sheet_name='SUNKOSHI3')
Exd = pd.read_excel(r'Sunkoshi.xlsx', sheet_name='Dudhkoshi1')


def get_interval(d, a):
	v = d.Vol
	i = bisect.bisect_right(v, a)
	return d[i - 1:i + 1]


def Interpolate(s, a, c='v'):
	f = get_interval(s, a)
	f = f.reset_index(drop=True)
	if c == 'Elev':
		m = np.interp(a, f.Vol, f.Elev)
		return m
	elif c == 'SArea':
		n = np.interp(a, f.Vol, f.SArea)
		return n
