import time
import pandas as pd
import numpy as np
from PSO_Algorithm import pso
from pso_data_for_test import Interpolate, I3, Ex3, Tyear, Fyear, Days

start_time = time.time()

swarmsize = 20
wmax = 1
wmin = 1
C1 = 1.7
C2 = 1.7
X = 0.9
pem = 0.3
maxiter = 50
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
	z = 0
	z_dry = 0
	z_wet = 0
	H3 = Height3(x)
	R3 = (Storage3(x)[0] * 10 ** 6) / (Days * 24 * 3600)
	for i in range(Tmonth):
		if i % 12 == 0 or i % 12 == 1 or i % 12 == 2 or i % 12 == 3 or i % 12 == 4 or i % 12 == 11:
			z_dry = 1 - (g * ita_S3 * R3[i] * H3[i] / 1000) / power3
		elif i % 12 == 5 or i % 12 == 6 or i % 12 == 7 or i % 12 == 8 or i % 12 == 9 or i % 12 == 10:
			z_wet = 1 - (g * ita_S3 * R3[i] * H3[i] / 1000) / power3
		Total = z_dry + z_wet
		z = z + Total
	return z/Tmonth


def Storage3(x):
	R3 = np.zeros(Tmonth)
	O3 = np.zeros(Tmonth)  # initial overflow all values are zero
	ev3 = []
	S3 = x
	j = 0
	for i in range(Tmonth):
		Ev3 = Evaporation3(S3[i], j, i)
		ev3.append(Ev3)
		R3[i] = S3[i] - S3[i + 1] + I3[i] - Ev3
		if R3[i] < ((R3max * Days[i] * 24 * 3600)/10**6):
			R3[i] = R3[i]
			O3[i] = 0
		else:
			O3[i] = R3[i] - ((R3max * Days[i] * 24 * 3600)/10**6)
			R3[i] = ((R3max * Days[i] * 24 * 3600)/10**6)
		j += 1
		if j == 12:
			j = 0
	return R3, O3, ev3


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


xopt, fopt, iter_vs_swamp_vs_fitness, iter_vs_globalbest = pso(fitness, lb, ub, swarmsize=swarmsize, pem=pem, wmax=wmax, wmin=wmin, c1=C1, c2=C2, X=X, maxiter=maxiter, minstep=minstep, minfunc=minfunc, debug=False)

print('Optimal fitness function value:')
print('    myfunc: {}'.format(fopt))
print(xopt)
print("Release:",Storage3(xopt)[0])