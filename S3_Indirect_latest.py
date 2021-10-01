import random
import time
import pandas as pd
import numpy as np
from PSO_Algorithm import pso
from data_pso import Interpolate, I3, Ex3, Tyear, Fyear, Days

start_time = time.time()

swarmsize = 100
wmax = 1
wmin = 1
C1 = 1
C2 = 0.5
X = 0.9
pem = 0.3
maxiter = 100
minstep = 1e-8
minfunc = 1e-8

#  All Input Constant Data's
g = 9.810  # Acceleration due to gravity
ev = (1.51, 2.34, 3.6, 5.09, 5.49, 4.97, 4.14, 4.22, 3.91, 3.41, 2.46, 1.72)  # mean daily evapo-transpiration index of koshi basin

#  Sunkoshi-3
ita_S3 = 0.86  # Efficiency of Hydro-Electric plant of Sunkoshi-3 (from DOED report)
power3 = 683  # Installed Capacity in Megawatt of Sunkoshi-3 (from DOED report)
S3max = 1769.286774  # h = 700  # Sunkoshi-3 maximum Storage volume in MCM at masl 695 m (from DOED report)
S3min = 769.457152  # h = 660   # Sunkoshi-3 minimum Storage volume in MCM at masl 660 m (from DOED report)
S3_effective_twl = 535  # Sunkoshi-3 turbine level in masl m (from DOED report)
S3_rated_discharge = 490  # Sunkoshi-3 total rated discharge in m3/s(from DOED report)
R3max = S3_rated_discharge


def listmaker(n):
	listofzeros = [0.0] * n
	return listofzeros


Tmonth = Tyear * 12
Ovariables = 1
T_O_V = Tmonth * Ovariables
lb = np.zeros(T_O_V + 1)  # initial lower bounds for releases all values are zero
ub = np.zeros(T_O_V + 1)  # initial upper bounds for releases all values are zero

for i in range(0, Tmonth + 1):
	ub[i] = S3max
	lb[i] = S3min


def fitness(x):
	F = 0
	H3 = Height3(x)
	Q3 = Storage3(x)[2]
	for i in range(Tmonth):
		z_dry = 0
		z_wet = 0
		if i % 12 == 0 or i % 12 == 1 or i % 12 == 2 or i % 12 == 3 or i % 12 == 4 or i % 12 == 11:
			z_dry = 1 - (g * ita_S3 * Q3[i] * H3[i] / 1000) / power3
		elif i % 12 == 5 or i % 12 == 6 or i % 12 == 7 or i % 12 == 8 or i % 12 == 9 or i % 12 == 10:
			z_wet = 1 - (g * ita_S3 * Q3[i] * H3[i] / 1000) / power3
		Total = z_dry + z_wet
		F = F + Total
	return F


def Dry_energy_checkA(x):  # Annual dry energy check
	z_dry = 0
	z_wet = 0
	dry_percentA = listmaker(int(Tmonth / 12))
	E3 = x  # Changing value of Energy
	j = 0
	for i in range(Tmonth):
		if i % 12 == 0 or i % 12 == 1 or i % 12 == 2 or i % 12 == 3 or i % 12 == 4 or i % 12 == 11:
			z_dry += E3[i]
			if i % 12 == 11:
				dry_percentA[j] = dry_energy(z_dry, z_wet)
				j = j + 1
				z_dry = 0
				z_wet = 0
		elif i % 12 == 5 or i % 12 == 6 or i % 12 == 7 or i % 12 == 8 or i % 12 == 9 or i % 12 == 10:
			z_wet += E3[i]
	return dry_percentA


def Dry_energy_checkT(x):  # Total dry energy check
	z_dry = 0
	z_wet = 0
	dry_percentT = 0
	E3 = x  # Changing value of energy GWH
	j = 0
	for i in range(Tmonth):
		if i % 12 == 0 or i % 12 == 1 or i % 12 == 2 or i % 12 == 3 or i % 12 == 4 or i % 12 == 11:
			z_dry += E3[i]
		elif i % 12 == 5 or i % 12 == 6 or i % 12 == 7 or i % 12 == 8 or i % 12 == 9 or i % 12 == 10:
			z_wet += E3[i]
	dry_percentT = dry_energy(z_dry, z_wet)
	return dry_percentT


def dry_energy(z_dry, z_wet):
	dry_percent_total = (z_dry / (z_dry + z_wet) * 100) if (z_dry + z_wet) != 0 else 0
	return dry_percent_total


def Storage3(x):
	R3 = np.zeros(Tmonth)
	ev3 = []
	S3 = x
	j = 0
	for i in range(Tmonth):
		Ev3 = Evaporation3(S3[i], j, i)
		ev3.append(Ev3)
		R3[i] = S3[i] - S3[i + 1] + I3[i] - Ev3
		#while R3[i] < 0:
		#	S3[i+1] = random.uniform(S3min, S3max)
		#	R3[i] = S3[i] - S3[i + 1] + I3[i] - Ev3
		j += 1
		if j == 12:
			j = 0
	e3, Q3, Sp3, p = E3(R3, x)
	return R3, e3, Q3, Sp3, p, ev3


def E3(R, x):
	e3 = np.zeros(Tmonth)  # initial Energy all values are zero
	p3 = np.zeros(Tmonth)
	H3 = Height3(x)
	R3 = (R * 10 ** 6) / (Days * 24 * 3600)
	Q3 = np.zeros(Tmonth)
	Sp3 = np.zeros(Tmonth)
	for i in range(Tmonth):
		p3[i] = g * ita_S3 * R3[i] * H3[i] / 1000 if (g * ita_S3 * R3[i] * H3[i] / 1000) <= power3 else power3
		e3[i] = (p3[i] * Days[i] * 24) / 1000
		Q3[i] = (p3[i] / (g * ita_S3 * H3[i]) * 1000)
		Sp3[i] = ((R3[i] - Q3[i]) * Days[i] * 24 * 3600) / 10 ** 6 if Q3[i] <= R3[i] else 0
	return e3, Q3, Sp3, p3


# Height for Sunkoshi-3
def Height3(x):
	H3 = np.zeros(Tmonth)  # initial Height all values are zero
	S3 = x
	for i in range(Tmonth):
		H3[i] = Interpolate(Ex3, (S3[i] + S3[i + 1]) / 2, c='Elev')
		H3[i] = H3[i] - S3_effective_twl
	return H3


def Evaporation3(a, b, d):
	S3a = Interpolate(Ex3, a, c='SArea')
	Eva = (ev[b] * S3a) * Days[d] / 10 ** 9
	return Eva


def cons(x):
	con = []
	R3 = Storage3(x)[0]
	for i in range(Tmonth):
		con.append(R3[i])
	return con


xopt, fopt, iter_vs_swamp_vs_fitness, iter_vs_globalbest = pso(fitness, lb, ub, f_ieqcons=cons, swarmsize=swarmsize, pem=pem, wmax=wmax, wmin=wmin, c1=C1, c2=C2, X=X, maxiter=maxiter, minstep=minstep, minfunc=minfunc, debug=False)

"""
  Printing and Saving Outputs
  ============================

"""
print('Optimal fitness function value:')
print('    myfunc: {}'.format(fopt))

print('The Output of the optimization can be found in same folder as this file in Excel-file named "S3-check.xlsx":')

Storage_Sunkoshi_3 = xopt
Release_Sunkoshi_3, Energy_Sunkoshi_3, Discharge_for_Sunkoshi_3, Spill_for_Sunkoshi_3, Power_for_Sunkoshi_3, Evaporation_loss_S3 = Storage3(xopt)
Storage_for_S3 = Storage_Sunkoshi_3[:-1]
Elevation_for_Sunkoshi_3 = Height3(xopt) + S3_effective_twl
Storage_Sunkoshi_3 = Storage_for_S3

Day_energy_percent_for_total = Dry_energy_checkT(Energy_Sunkoshi_3)
Day_energy_percent_Annually = Dry_energy_checkA(Energy_Sunkoshi_3)

Fitness_value = fopt

Inputs = ['swarmsize', 'wmax', 'wmin', 'C1', 'C2', 'X', 'maxiter', 'minstep', 'minfunc', 'Fitness_value', 'Dry_energy percent Total']

'''
 Writing to Excel
 =================
 Here,writing the output obtained to excel file PSO_Outputs.xlsx
'''
PSO_Outputs = pd.ExcelWriter('S3_indirect.xlsx')

Parameters = pd.DataFrame()
Outputs = pd.DataFrame()
Storage = pd.DataFrame()
Release = pd.DataFrame()
Energy = pd.DataFrame()
pso_data1 = pd.DataFrame(iter_vs_swamp_vs_fitness, columns=['Iteration', 'Swamp_Number', 'Fitness_Value'])
pso_data2 = pd.DataFrame(iter_vs_globalbest, columns=['Iteration', 'Global_best_fitness'])
Day_energy_percent_A = pd.DataFrame()

y = pd.to_datetime(Fyear, format='%Y')
c = Tyear + Fyear
m = pd.to_datetime(c, format='%Y')

Date = pd.date_range(start=y, end=m, freq='M').year.tolist()
Date1 = pd.date_range(start=y, end=m, freq='Y').year.tolist()
Month = pd.date_range(start=y, end=m, freq='M').month_name().tolist()

Parameters['Parameters'] = Inputs
Parameters['Values'] = [swarmsize, wmax, wmin, C1, C2, X, maxiter, minstep, minfunc, Fitness_value, Day_energy_percent_for_total]

Outputs['Date'] = Date
Outputs['Month'] = Month
Outputs['Inflows'] = I3
Outputs['Outflow_Sunkoshi_3'] = Release_Sunkoshi_3
Outputs['Storage_Sunkoshi_3'] = Storage_Sunkoshi_3
Outputs['Discharge_for_Sunkoshi_3'] = Discharge_for_Sunkoshi_3
Outputs['Spill_for_Sunkoshi_3'] = Spill_for_Sunkoshi_3
Outputs['Power_for_Sunkoshi_3'] = Power_for_Sunkoshi_3
Outputs['Elevation_Sunkoshi_3'] = Elevation_for_Sunkoshi_3
Outputs['Energy_Sunkoshi_3'] = Energy_Sunkoshi_3
Outputs["Evaporation_loss_S3"] = Evaporation_loss_S3

Release['Date'] = Date
Release['Month'] = Month
Release['Release_Sunkoshi_3'] = Release_Sunkoshi_3

Storage['Date'] = Date
Storage['Month'] = Month
Storage['Storage_Sunkoshi_3'] = Storage_Sunkoshi_3

Energy['Date'] = Date
Energy['Month'] = Month
Energy['Energy_Sunkoshi_3'] = Energy_Sunkoshi_3

Day_energy_percent_A['Date'] = Date1
Day_energy_percent_A['Dry Energy percent S3'] = Day_energy_percent_Annually

Parameters.to_excel(PSO_Outputs, sheet_name='Inputs', index=False)
Outputs.to_excel(PSO_Outputs, sheet_name='Outputs', index=False)
Release.to_excel(PSO_Outputs, sheet_name='Release', index=False)
Storage.to_excel(PSO_Outputs, sheet_name='Storage', index=False)
Energy.to_excel(PSO_Outputs, sheet_name='Energy', index=False)
pso_data1.to_excel(PSO_Outputs, sheet_name='iter_vs_swamp_vs_fitness', index=False)
pso_data2.to_excel(PSO_Outputs, sheet_name='iter_vs_Global_best_fitness', index=False)
Day_energy_percent_A.to_excel(PSO_Outputs, sheet_name='Dry_Energy', index=False)

Time = pd.DataFrame()
Time['Time'] = [(time.time() - start_time)]
Time.to_excel(PSO_Outputs, sheet_name='Elapsed Time', index=False)

PSO_Outputs.save()

# print('    mycon : {}'.format(mycons(xopt, *args)))

print("time elapsed: {:.2f}s".format(time.time() - start_time))
