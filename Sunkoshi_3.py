import time
import pandas as pd
import numpy as np

start_time = time.time()

"""
  Initialization
  ===============
   Input following commands on python console if error of these modules not present. 
     pip install numpy
     pip install pandas
     Make sure data_pso python file is in same folder as this file.
     
   Things to note.
   ===============
     Make sure data_pso python file is in same folder as this file.
     Make sure PSO_Algorithm python file is in same folder as this file.
     Make sure data_pso.xlsx file is in same folder as this file.
     Make sure Sunkoshi.xlsx file is in same folder as this file.

   Parameters
   ===============
    Following are preset initial parameters.
    They can be changed here.

    swarmsize : int
        The number of particles in the swarm (Default: 100)
    Chi(X) : constriction factor which is used to control and constrict
        velocities (Default: 1)
    omega(w) : scalar (wmax and wmin)
        Particle velocity scaling factor (Default: 1.2 to 0.1)
    phip(c1) : scalar
        Scaling factor to search away from the particle's best known position
        (Default: 0.5)
    phig(c2) : scalar
        Scaling factor to search away from the swarm's best known position
        (Default: 0.5)
    Pem(pem) : Probability of elitist mutation (Default: 0.2)
    maxiter : int
        The maximum number of iterations for the swarm to search (Default: 100)
    minstep : scalar
        The minimum stepsize of swarm's best position before the search
        terminates (Default: 1e-8)
    minfunc : scalar
        The minimum change of swarm's best objective value before the search
        terminates (Default: 1e-8)
    debug : boolean
        If True, progress statements will be displayed every iteration
        (Default: False)

"""
swarmsize = 100
wmax = 1
wmin = 0.2
C1 = 1
C2 = 0.5
X = 0.9
pem = 0.3
maxiter = 500
minstep = 1e-8
minfunc = 1e-8

from PSO_Algorithm import pso
from data_pso import Interpolate, I3, Ex3, Tyear, Fyear

""""
  Introduction
  ============
   Objective Function for Multi-reservoir release optimization using PSO algorithm

   Objective Function maximize E=∑(t=0)to(t=n)[P(R3 * H3)]

   Where,
     P = turbine efficiency * Density of water * Acceleration due to gravity
     R3 = Release from Sunkoshi-3 at time t
     H3 = Height of Sunkoshi-3 water head at time t


  Imports and Variables
  ======================

   Importing PSO algorithm from github id:https://github.com/tisimst/pyswarm
   with many changes done to the algorithm

   Also importing input variables from data_pso.py file

     I3     : Inflow at Sunkoshi-3 [Pachuwarghat(630)] + local inflow at sunkoshi 3
     Ex3    : H-V-A curve data for Sunkoshi-3
     S3max  : Maximum Sunkoshi-3 reservoir capacity in MCM
     S3min  : Minimum Sunkoshi-3 reservoir capacity in MCM     
     S3_twl : Turbine level at Sunkoshi-3
     Ev3    : Evaporation loss from Sunkoshi-3 reservoir at time t is function of surface area
     O3     : Overflow from Sunkoshi-3 reservoir at time t  
     S3a    : Surface area water in Sunkoshi-3 reservoir at time t
     H3     : Water level in Sunkoshi-3 reservoir at time t 
     e3     : Energy output by Sunkoshi-3 at time t, is in KWh
     Qme    : Energy output by Sunkoshi Marine Diversion at time t, is in KWh
     ev     : Evaporation in mm per month
"""
ita = 0.86  # Efficiency of Hydro-Electric plant
g = 9.810  # Acceleration due to gravity
power = 683  # Installed Capacity in Megawatt
seconds_per_month = 2.6298 * 10 ** 6
S3max = 1769.286774  # h = 700 m
S3min = 769.457152  # h = 660 m
S3_twl = 535
ev = (1.51, 2.34, 3.6, 5.09, 5.49, 4.97, 4.14, 4.22, 3.91, 3.41, 2.46, 1.72) * 30
"""
   Environment
  ============
   Listmaker: Is function which takes any positive integer(n) as input and returns a list 
             with n number of elements whose value are set to zero.

   Here,
        In this code Fyear to Lyear are taken as optimizing years
        So,total number of years to optimize is Tyear = Lyear - Fyear + 1 years

   Then with each year having 12 months, total number of optimizing instances: Tyear * 12 = Tmonth

   We have Ovariables = 1 Releases to optimize each month for R3 which takes total size of
   optimized values to : Tmonth * Ovariables = T_O_V

     lb  : Lower bound for pso search for all T_O_V optimization values
     ub  : upper bound for pso search for all T_O_V optimization values     
     cons: Stores constrains output used to check for feasible solution 
"""


def listmaker(n):
	listofzeros = [0.0] * n
	return listofzeros


Tmonth = Tyear * 12
Ovariables = 1
T_O_V = Tmonth * Ovariables
lb = np.zeros(T_O_V)  # initial lower bounds for releases all values are zero
ub = np.zeros(T_O_V)  # initial upper bounds for releases all values are zero

# Giving upper and lower value for pso search function,here limit on irrigation and release output can de defined.
"""
  ub-lb Section
  ==============
   Here each optimization values (i.e Releases) are given:
    lb : lower bound
    ub : upper bound

   following code facilities this process such that these bounds can be given for each releases. 
"""

for i in range(0, T_O_V):
	ub[i] = 1288  # bonds for jan in Sunkoshi-3
	lb[i] = 0  # bonds for jan in Sunkoshi-3

"""
  Objective function
  ===================

  The algorithm Swarm searches for minimum value value so objective function is multiplied by -1
  Two types of fitness function can be made with above objective function 
  i) Here value of total energy is normalized
  ii) Here the value of energy is combine total

  Only one function can be used at a time

  From T_O_V optimized values
  ---------------------------
    Values that are indexed in range [0-Tmonth] are stored in R3 

  Here the value of releases are in MCM per month.
  Fitness function gives the total amount energy potential that can be generated when input parameters and optimized released are used as operation policy.
"""


def fitness(x):
	F = 0
	H3 = Height3(x)
	R3 = (x * 10 ** 6) / seconds_per_month
	for i in range(Tmonth):
		z = 1 - (g * ita * R3[i] * 10 ** 6 * H3[i]) / (1000 * seconds_per_month * power)
		F = F + z
	return F


# objective function maximizing power production
# def Fitnessfunc(x, *args):
#    z = 0
#    z_dry = 0
#    z_wet = 0
#    R3 = (x * 10 ** 6) / seconds_per_month
#    H3 = Height3(x, *args)
#    for i in range(Tmonth):
#        if i % 12 == 0 or i % 12 == 1 or i % 12 == 2 or i % 12 == 3 or i % 12 == 4 or i % 12 == 11:
#            z_dry = (g * ita * R3[i] / 1000 * H3[i])
#        elif i % 12 == 5 or i % 12 == 6 or i % 12 == 7 or i % 12 == 8 or i % 12 == 9 or i % 12 == 10:
#            z_wet = (g * ita * R3[i] / 1000 * H3[i])
#        Total = z_dry + z_wet
#        z += Total
#    return -z
"""
  Minimum Dry Energy 
  ===================
  In this function the out put of PSO is introduced to output percentage of Dry energy for each year which is used below in mycons function to check for feasible solutions.

"""


def Dry_energy_checkA(x):  # Annual dry energy check
	z_dry = 0
	z_wet = 0
	dry_percentA = listmaker(int(Tmonth / 12))
	H3 = Height3(x)
	R3 = (x * 10 ** 6) / seconds_per_month  # Changing value of release from MCM to cms
	j = 0
	for i in range(Tmonth):
		if i % 12 == 0 or i % 12 == 1 or i % 12 == 2 or i % 12 == 3 or i % 12 == 4 or i % 12 == 11:
			z_dry += (g * ita * R3[i] * H3[i] / 1000)
			if i % 12 == 11:
				dry_percentA[j] = dry_energy(z_dry, z_wet)
				j = j + 1
				z_dry = 0
				z_wet = 0
		elif i % 12 == 5 or i % 12 == 6 or i % 12 == 7 or i % 12 == 8 or i % 12 == 9 or i % 12 == 10:
			z_wet += (g * ita * R3[i] * H3[i] / 1000)
	return dry_percentA


def Dry_energy_checkT(x):  # Total dry energy check
	z_dry = 0
	z_wet = 0
	dry_percentT = 0
	H3 = Height3(x)
	R3 = (x * 10 ** 6) / seconds_per_month  # Changing value of release from MCM to cms
	j = 0
	for i in range(Tmonth):
		if i % 12 == 0 or i % 12 == 1 or i % 12 == 2 or i % 12 == 3 or i % 12 == 4 or i % 12 == 11:
			z_dry += (g * ita * R3[i] * H3[i] / 1000)
		elif i % 12 == 5 or i % 12 == 6 or i % 12 == 7 or i % 12 == 8 or i % 12 == 9 or i % 12 == 10:
			z_wet += (g * ita * R3[i] * H3[i] / 1000)
	dry_percentT = dry_energy(z_dry, z_wet)
	return dry_percentT


def dry_energy(z_dry, z_wet):
	dry_percent_total = (z_dry / (z_dry + z_wet) * 100) if (z_dry + z_wet) != 0 else 0
	return dry_percent_total


"""                                                                                                                                                
   Mass Balance                                                                                                                               
   =============
    Here, 
     S_(t) is the storage at the beginning of time period t
      For Sunkoshi-3 dam:
      -------------------
      S3(t) = I3(inflow) + S3(t-1)-{R3(t-1)(release from sunkoshi-3)-Evaporation at time t}


      Constrains
      ----------

       When storage volume obtained is lower than minimum storage capacity{i.e. S_min > S_(t)}
       ---------------------------------------------------------------------------------------
         Then,PSO search takes the value as infeasible because it violates one of the constrains
         So new value to satisfy the constrain is searched.
         and, R_(t) <= total inflow at t (sum of inflow and overflow from dam upstream if any)  

       When storage volume obtained is greater than storage capacity{i.e. S_max < S_(t)}
       ----------------------------------------------------------------------------------
         then,S_(t) = S_max
         and,Overflow[O_(t)] = S_(t) - S_max
         Otherwise Overflow[O_(t)] = 0
         
         Constrain for maximum energy is also given.
         constrains for irrigation demand can be addressed in [ld - ub] section.

"""


# all constrains required
def mycons(x):
	# dry_percent = Dry_energy_check(x)
	cons = []
	return cons


# mass balance for sunkoshi 3
def Storage3(x):
	S3 = np.zeros(Tmonth + 1)
	O3 = np.zeros(Tmonth)  # initial overflow all values are zero
	S3[0] = S3min  # taking initial condition as minimum storage
	R3 = x
	j = 0
	for i in range(Tmonth):
		S3_temp = 0
		S3_temp2 = 0
		Ev3 = Evaporation3(S3[i], j)
		S3_temp = I3[i] + S3[i] - (R3[i] + Ev3)
		if S3_temp < S3min:
			x[i] = np.random.rand() * (I3[i] + S3[i] - Ev3 - S3min)
			S3[i + 1] = I3[i] + S3[i] - (R3[i] + Ev3)
		else:
			S3[i + 1] = I3[i] + S3[i] - (R3[i] + Ev3)
		S3_temp2 = S3[i + 1]
		if S3_temp2 > S3max:
			if x[i] < ub[i]:
				x[i] = x[i] + S3_temp2 - S3max
				if x[i] > ub[i]:
					O3[i] = x[i]-ub[i]
					x[i] = ub[i]
			else:
				O3[i] = I3[i] + S3[i] - (R3[i] + Ev3) - S3max
			S3[i + 1] = I3[i] + S3[i] - (R3[i] + Ev3 + O3[i])
		else:
			S3[i + 1] = I3[i] + S3[i] - (R3[i] + Ev3 + O3[i])
		j += 1
		if j == 12:
			j = 0
	return S3, O3


def Overflow(Si, Smax):
	if Si >= Smax:
		return Si - Smax, Smax
	else:
		return 0, Si


def Storage_check(Si, Smin):
	if Si <= Smin:
		n = Smin - Si
		return Smin, n
	if Si > Smin:
		return Si, 0


"""
  Energy
  =======
   Energy = P * release * Net head
"""


# Energy output per month for Sunkoshi 3
def E3(x):
	e3 = np.zeros(Tmonth)  # initial Energy all values are zero
	H3 = Height3(x)
	R3 = (x * 10 ** 6) / seconds_per_month
	for i in range(Tmonth):
		e3[i] = g * ita * R3[i] * H3[i] / 1000
	return e3


"""
  Height
  =======
   Height function H=f(storage)
   Obtained from H-V-A curve
"""


# Height for Sunkoshi-3
def Height3(x):
	H3 = np.zeros(Tmonth)  # initial Height all values are zero
	S3 = Storage3(x)[0]
	for i in range(Tmonth):
		H3[i] = Interpolate(Ex3, S3[i], c='Elev')
		H3[i] = H3[i] - S3_twl
	return H3


""" 
  Surface Area
  =============                         
   Surface Area function S_a = f(storage)
   Obtained from H-V-A curve

  Evaporation
  ============
   Evaporation function Ev = f(Surface Area)
   Obtained from equation    
"""


def Evaporation3(a, b):
	S3a = Interpolate(Ex3, a, c='SArea')
	Eva = (ev[b] * S3a) / 10 ** 9
	return Eva


# calling pso function in pso.py

xopt, fopt, iter_vs_swamp_vs_fitness, iter_vs_globalbest = pso(fitness, lb, ub, swarmsize=swarmsize, pem=pem, wmax=wmax, wmin=wmin, c1=C1, c2=C2, X=X, maxiter=maxiter, minstep=minstep, minfunc=minfunc, debug=False)

Day_energy_percent_for_total = Dry_energy_checkT(xopt)
Day_energy_percent_Annually = Dry_energy_checkA(xopt)

print("Dry energy Total:", Dry_energy_checkT(xopt))
print("Dry energy Annually:", Dry_energy_checkA(xopt))
"""
  Printing and Saving Outputs
  ============================

"""
print('Optimal fitness function value:')
print('    myfunc: {}'.format(fopt))

print('The optimum releases for each stations are:')

Release_Sunkoshi_3 = []
Storage_Sunkoshi_3 = []
Overflow_Sunkoshi_3 = []
Dry_energy_percent_Annually_for_S3 = []
Energy_Sunkoshi_3 = []
Fitness_value = fopt
Inputs = ['swarmsize', 'wmax', 'wmin', 'C1', 'C2', 'X', 'maxiter', 'minstep', 'minfunc', 'Fitness_value', 'Dry_energy percent Total']

# Optimized Releases
print("{:<7} {:<7} {:<25}".format('Year', 'Months', 'Release at S3'))
j = -1
month = 'error'
for i in range(Tmonth):
	if i % 12 == 0 or i == 0:
		month = "Jan"
		print('-' * 150)
		j = j + 1
	elif i % 12 == 1:
		month = "Feb"
	elif i % 12 == 2:
		month = "Mar"
	elif i % 12 == 3:
		month = "Apr"
	elif i % 12 == 4:
		month = "May"
	elif i % 12 == 5:
		month = "Jun"
	elif i % 12 == 6:
		month = "Jul"
	elif i % 12 == 7:
		month = "Aug"
	elif i % 12 == 8:
		month = "Sep"
	elif i % 12 == 9:
		month = "Oct"
	elif i % 12 == 10:
		month = "Nov"
	elif i % 12 == 11:
		month = "Dec"

	# print('Year/', 'Months /', 'Release at S3/', 'Release at S2/', 'Release at S1/', 'Release at Smd/', 'Release at Skd/')
	Release_Sunkoshi_3.append(xopt[i])
	print("{:<7} {:<7} {:<25}".format(Fyear + j, month, xopt[i]))

# Storage for optimized Releases
print("{:<10} {:<10} {:<25}".format('Year', 'Months', 'Storage at S3'))
Storage_for_S3, Overflow_for_S3 = Storage3(xopt)
j = -1
for i in range(Tmonth):
	if i % 12 == 0 or i == 0:
		month = "Jan"
		print('-' * 100)
		j = j + 1
	elif i % 12 == 1:
		month = "Feb"
	elif i % 12 == 2:
		month = "Mar"
	elif i % 12 == 3:
		month = "Apr"
	elif i % 12 == 4:
		month = "May"
	elif i % 12 == 5:
		month = "Jun"
	elif i % 12 == 6:
		month = "Jul"
	elif i % 12 == 7:
		month = "Aug"
	elif i % 12 == 8:
		month = "Sep"
	elif i % 12 == 9:
		month = "Oct"
	elif i % 12 == 10:
		month = "Nov"
	elif i % 12 == 11:
		month = "Dec"

	Storage_Sunkoshi_3.append(Storage_for_S3[i])

	print("{:<10} {:<10} {:<25}".format(Fyear + j, month, Storage_for_S3[i]))

# Overflow for Optimized Releases
print("{:<10} {:<10} {:<25}".format('Year', 'Months', 'Overflow at S3'))
j = -1
for i in range(Tmonth):
	if i % 12 == 0 or i == 0:
		month = "Jan"
		print('-' * 100)
		j = j + 1
	elif i % 12 == 1:
		month = "Feb"
	elif i % 12 == 2:
		month = "Mar"
	elif i % 12 == 3:
		month = "Apr"
	elif i % 12 == 4:
		month = "May"
	elif i % 12 == 5:
		month = "Jun"
	elif i % 12 == 6:
		month = "Jul"
	elif i % 12 == 7:
		month = "Aug"
	elif i % 12 == 8:
		month = "Sep"
	elif i % 12 == 9:
		month = "Oct"
	elif i % 12 == 10:
		month = "Nov"
	elif i % 12 == 11:
		month = "Dec"

	Overflow_Sunkoshi_3.append(Overflow_for_S3[i])
	print("{:<10} {:<10} {:<25}".format(Fyear + j, month, Overflow_for_S3[i]))

# Energy generation for Optimized Releases
print("{:<7} {:<7} {:<25}".format('Year', 'Months', 'Energy at S3'))
Energy_for_S3 = E3(xopt)
j = -1
for i in range(Tmonth):
	if i % 12 == 0 or i == 0:
		month = "Jan"
		print('-' * 150)
		j = j + 1
	elif i % 12 == 1:
		month = "Feb"
	elif i % 12 == 2:
		month = "Mar"
	elif i % 12 == 3:
		month = "Apr"
	elif i % 12 == 4:
		month = "May"
	elif i % 12 == 5:
		month = "Jun"
	elif i % 12 == 6:
		month = "Jul"
	elif i % 12 == 7:
		month = "Aug"
	elif i % 12 == 8:
		month = "Sep"
	elif i % 12 == 9:
		month = "Oct"
	elif i % 12 == 10:
		month = "Nov"
	elif i % 12 == 11:
		month = "Dec"

	Energy_Sunkoshi_3.append(Energy_for_S3[i])
	print("{:<7} {:<7} {:<25}".format(Fyear + j, month, Energy_for_S3[i]))

'''
 Writing to Excel
 =================
 Here,writing the output obtained to excel file PSO_Outputs.xlsx
'''
PSO_Outputs = pd.ExcelWriter('PSO_Outputs_Sunkoshi3(1985-2014).xlsx')

Parameters = pd.DataFrame()
Outputs = pd.DataFrame()
Storage = pd.DataFrame()
Release = pd.DataFrame()
Overflow = pd.DataFrame()
Energy = pd.DataFrame()
pso_data1 = pd.DataFrame(iter_vs_swamp_vs_fitness, columns=['Iteration', 'Swamp_Number', 'Fitness_Value'])
pso_data2 = pd.DataFrame(iter_vs_globalbest, columns=['Iteration', 'Global_best_fitness'])
Day_energy_percent_A = pd.DataFrame()

Date = pd.date_range(start='1985-1-1', end='2015-1-1', freq='M').year.tolist()
Date1 = pd.date_range(start='1985-1-1', end='2015-1-1', freq='Y').year.tolist()
Month = pd.date_range(start='1985-1-1', end='2015-1-1', freq='M').month_name().tolist()

Parameters['Parameters'] = Inputs
Parameters['Values'] = [swarmsize, wmax, wmin, C1, C2, X, maxiter, minstep, minfunc, Fitness_value, Day_energy_percent_for_total]

Outputs['Date'] = Date
Outputs['Month'] = Month
Outputs['Inflows'] = I3
Outputs['Release_Sunkoshi_3'] = Release_Sunkoshi_3
Outputs['Storage_Sunkoshi_3'] = Storage_Sunkoshi_3
Outputs['Overflow_Sunkoshi_3'] = Overflow_Sunkoshi_3
Outputs['Energy_Sunkoshi_3'] = Energy_Sunkoshi_3

Release['Date'] = Date
Release['Month'] = Month
Release['Release_Sunkoshi_3'] = Release_Sunkoshi_3

Storage['Date'] = Date
Storage['Month'] = Month
Storage['Storage_Sunkoshi_3'] = Storage_Sunkoshi_3

Overflow['Date'] = Date
Overflow['Month'] = Month
Overflow['Overflow_Sunkoshi_3'] = Overflow_Sunkoshi_3

Energy['Date'] = Date
Energy['Month'] = Month
Energy['Energy_Sunkoshi_3'] = Energy_Sunkoshi_3

Day_energy_percent_A['Date'] = Date1
Day_energy_percent_A['Dry Energy percent S3'] = Day_energy_percent_Annually

Parameters.to_excel(PSO_Outputs, sheet_name='Inputs', index=False)
Outputs.to_excel(PSO_Outputs, sheet_name='Outputs', index=False)
Release.to_excel(PSO_Outputs, sheet_name='Release', index=False)
Storage.to_excel(PSO_Outputs, sheet_name='Storage', index=False)
Overflow.to_excel(PSO_Outputs, sheet_name='Overflow', index=False)
Energy.to_excel(PSO_Outputs, sheet_name='Energy', index=False)
pso_data1.to_excel(PSO_Outputs,sheet_name='iter_vs_swamp_vs_fitness', index=False)
pso_data2.to_excel(PSO_Outputs,sheet_name='iter_vs_Global_best_fitness', index=False)
Day_energy_percent_A.to_excel(PSO_Outputs, sheet_name='Dry_Energy', index=False)

PSO_Outputs.save()

# print('    mycon : {}'.format(mycons(xopt, *args)))

print("time elapsed: {:.2f}s".format(time.time() - start_time))
