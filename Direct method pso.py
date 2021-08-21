import time
import pandas as pd
import numpy as np
from PSO_Algorithm import pso
from pso_data_for_test import Interpolate, I3, Ex3, Tyear, Fyear, Days

start_time = time.time()
print(I3)

swarmsize = 20
wmax = 1
wmin = 1
C1 = 1
C2 = 0.5
X = 0.9
pem = 0.05
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
lower_release = 0


def listmaker(n):
	listofzeros = [0.0] * n
	return listofzeros


Tmonth = Tyear * 12
Ovariables = 2
T_O_V = Tmonth * Ovariables
lb = np.zeros(T_O_V)  # initial lower bounds for releases all values are zero
ub = np.zeros(T_O_V)  # initial upper bounds for releases all values are zero

for i in range(0, T_O_V):
	if i < Tmonth:
		ub[i] = (S3_rated_discharge * Days[i] * 24 * 3600) / 10 ** 6
		lb[i] = lower_release
	elif i >= Tmonth:
		print(I3[i-Tmonth])
		ub[i] = I3[i-Tmonth]
		lb[i] = 0


print('lb:',lb)
print('ub:',ub)


def fitness(x):
	F = 0
	S3 = Storage3(x)[0]
	R3 = x[:Tmonth]
	O3 = x[Tmonth:]
	for i in range(Tmonth):
		z = (R3[i]-ub[i]) ** 2 + O3[i]
		if S3[i] > S3max:
			penalty1 = (S3[i] - S3max) ** 2
		else:
			penalty1 = 0
		if S3[i] < S3min:
			penalty2 = (S3min - S3[i]) ** 2
		else:
			penalty2 = 0
		F = F + z + penalty1 + penalty2
	return F


def Storage3(x):
	S3 = np.zeros(Tmonth + 1)
	O3 = np.zeros(Tmonth)  # initial overflow all values are zero
	ev3 = []
	S3[0] = S3max  # taking initial condition as minimum storage
	R3 = x[:Tmonth]
	O3 = x[Tmonth:]
	j = 0
	for i in range(Tmonth):
		Ev3 = Evaporation3(S3[i], j, i)
		ev3.append(Ev3)
		S3[i + 1] = I3[i] + S3[i] - (R3[i] + Ev3 + O3[i])
		j += 1
		if j == 12:
			j = 0
	return S3, ev3


# Height for Sunkoshi-3
def Height3(x):
	H3 = np.zeros(Tmonth)  # initial Height all values are zero
	S3 = Storage3(x)[0]
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
print("Storage:", Storage3(xopt)[0])
