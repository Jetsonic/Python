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
    elevation and surface area.pso_data(1985-2014)
"""
Inflow = pd.read_excel(r'pso_data(1985-2014).xlsx', sheet_name='Inflow')  # here if pso_data1.xlsx(1978-1980) replaced by pso_data.xlsx the code will take input for 47 years(1968-2014)
Start = Inflow['Date'][0]
End = Inflow['Date'][Inflow.index[-1]]
Inflow['Year'] = pd.DatetimeIndex(Inflow['Date']).year
Fyear = Inflow['Year'][0]
Lyear = Inflow['Year'][Inflow.index[-1]]
Tyear = Lyear - Fyear + 1
I3 = Inflow['Pachuwarghat'] + Inflow['Local Inflow at Sunkoshi III']
I3 = I3.tolist()
l2 = Inflow['Local Inflow at Sunkoshi II'].tolist()
l1 = Inflow['Sangutar'] + Inflow['Rabuwa Bazar'] + Inflow['Local Inflow at Sunkoshi I']
l1_ = Inflow['Sangutar'] + Inflow['Local Inflow at Sunkoshi I']
l1_ = l1_.tolist()
l1 = l1.tolist()
Is1 = Inflow['Khurkot'] + Inflow['Sangutar'] + Inflow['Rabuwa Bazar'] + Inflow['Local Inflow at Sunkoshi I']
Is2 = Inflow['Khurkot']
Dk = Inflow['Rabuwa Bazar'].tolist()
Demand = pd.read_excel(r'pso_data(1985-2014).xlsx', sheet_name='Irrigation demand')
Dmd = Demand['DEMAND']
Days_in_month = pd.read_excel(r'pso_data(1985-2014).xlsx', sheet_name='Days_in_month')
Days = Days_in_month['Days']
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
