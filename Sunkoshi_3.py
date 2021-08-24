import time

import pandas as pd
import numpy as np

from PSO_Algorithm import pso
from data_pso import Interpolate, I3, Ex3, Tyear, Fyear, Days

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
swarmsize = 20
wmax = 1
wmin = 0.2
C1 = 1.7
C2 = 1.7
X = 0.9
pem = 0.3
maxiter = 1
minstep = 1e-8
minfunc = 1e-8
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
lower_release = 67
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
	if i % 12 == 0 or i == 0:
		month = "Jan"
		ub[i] = (S3_rated_discharge * Days[i] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
		lb[i] = (lower_release * Days[i] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
	elif i % 12 == 1:
		month = "Feb"
		ub[i] = (S3_rated_discharge * Days[i] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
		lb[i] = (lower_release * Days[i] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
	elif i % 12 == 2:
		month = "Mar"
		ub[i] = (S3_rated_discharge * Days[i] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
		lb[i] = (lower_release * Days[i] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
	elif i % 12 == 3:
		month = "Apr"
		ub[i] = (S3_rated_discharge * Days[i] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
		lb[i] = (lower_release * Days[i] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
	elif i % 12 == 4:
		month = "May"
		ub[i] = (S3_rated_discharge * Days[i] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
		lb[i] = (lower_release * Days[i] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
	elif i % 12 == 5:
		month = "Jun"
		ub[i] = (S3_rated_discharge * Days[i] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
		lb[i] = (lower_release * Days[i] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
	elif i % 12 == 6:
		month = "Jul"
		ub[i] = (S3_rated_discharge * Days[i] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
		lb[i] = (lower_release * Days[i] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
	elif i % 12 == 7:
		month = "Aug"
		ub[i] = (S3_rated_discharge * Days[i] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
		lb[i] = (lower_release * Days[i] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
	elif i % 12 == 8:
		month = "Sep"
		ub[i] = (S3_rated_discharge * Days[i] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
		lb[i] = (lower_release * Days[i] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
	elif i % 12 == 9:
		month = "Oct"
		ub[i] = (S3_rated_discharge * Days[i] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
		lb[i] = (lower_release * Days[i] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
	elif i % 12 == 10:
		month = "Nov"
		ub[i] = (S3_rated_discharge * Days[i] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
		lb[i] = (lower_release * Days[i] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
	elif i % 12 == 11:
		month = "Dec"
		ub[i] = (S3_rated_discharge * Days[i] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
		lb[i] = (lower_release * Days[i] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3

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
	R3 = (x * 10 ** 6) / (Days * 24 * 3600)
	for i in range(Tmonth):
		z = 1 - (g * ita_S3 * R3[i] * H3[i]) / (1000 * power3)
		F = F + z
	return F


# def fitness(x):
#    z = 0
#    z_dry = 0
#    z_wet = 0
#    H3 = Height3(x)
#    R3 = (x * 10 ** 6) / (Days * 24 * 3600)
#    for i in range(Tmonth):
#        if i % 12 == 0 or i % 12 == 1 or i % 12 == 2 or i % 12 == 3 or i % 12 == 4 or i % 12 == 11:
#            z_dry = 1-(g * ita_S3 * R3[i] * H3[i] / 1000) / power3
#        elif i % 12 == 5 or i % 12 == 6 or i % 12 == 7 or i % 12 == 8 or i % 12 == 9 or i % 12 == 10:
#            z_wet = 1-(g * ita_S3 * R3[i] * H3[i] / 1000) / power3
#        Total = 100 * z_dry - z_wet
#        z = z + Total
#    return z


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
	R3 = (x * 10 ** 6) / (Days * 24 * 3600)  # Changing value of release from MCM to cms
	j = 0
	for i in range(Tmonth):
		if i % 12 == 0 or i % 12 == 1 or i % 12 == 2 or i % 12 == 3 or i % 12 == 4 or i % 12 == 11:
			z_dry += ((g * ita_S3 * R3[i] * H3[i] / 1000) * Days[i] * 24) / 1000
			if i % 12 == 11:
				dry_percentA[j] = dry_energy(z_dry, z_wet)
				j = j + 1
				z_dry = 0
				z_wet = 0
		elif i % 12 == 5 or i % 12 == 6 or i % 12 == 7 or i % 12 == 8 or i % 12 == 9 or i % 12 == 10:
			z_wet += ((g * ita_S3 * R3[i] * H3[i] / 1000) * Days[i] * 24) / 1000
	return dry_percentA


def Dry_energy_checkT(x):  # Total dry energy check
	z_dry = 0
	z_wet = 0
	dry_percentT = 0
	H3 = Height3(x)
	R3 = (x * 10 ** 6) / (Days * 24 * 3600)  # Changing value of release from MCM to cms
	j = 0
	for i in range(Tmonth):
		if i % 12 == 0 or i % 12 == 1 or i % 12 == 2 or i % 12 == 3 or i % 12 == 4 or i % 12 == 11:
			z_dry += ((g * ita_S3 * R3[i] * H3[i] / 1000) * Days[i] * 24) / 1000
		elif i % 12 == 5 or i % 12 == 6 or i % 12 == 7 or i % 12 == 8 or i % 12 == 9 or i % 12 == 10:
			z_wet += ((g * ita_S3 * R3[i] * H3[i] / 1000) * Days[i] * 24) / 1000
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
def Storage3(x):  # Function containing mass balance equation and correction for illegal storage, this function changes values sent by pso to make it feasible
	S3 = np.zeros(Tmonth + 1)  # Returns the storage values and over flow values for all months
	O3 = np.zeros(Tmonth)  # initial overflow all values are zero
	ev3 = []
	S3[0] = S3max
	R3 = x
	j = 0
	for i in range(Tmonth):
		Ev3 = Evaporation3(S3[i], j, i)
		ev3.append(Ev3)
		S3[i + 1] = I3[i] + S3[i] - (R3[i] + Ev3 + O3[i])
		if S3[i + 1] < S3min:
			R3[i] = np.random.rand() * (I3[i] + S3[i] - Ev3 - S3min - O3[i])
			S3[i + 1] = I3[i] + S3[i] - (R3[i] + Ev3 + O3[i])
		else:
			S3[i + 1] = I3[i] + S3[i] - (R3[i] + Ev3 + O3[i])
		if S3[i + 1] > S3max:
			if R3[i] < ub[i]:
				R3[i] = R3[i] + S3[i + 1] - S3max
				if R3[i] > ub[i]:
					O3[i] = R3[i] - ub[i]
					R3[i] = ub[i]
			else:
				O3[i] = S3[i + 1] - S3max
			S3[i + 1] = I3[i] + S3[i] - (R3[i] + Ev3 + O3[i])
		j += 1
		if j == 12:
			j = 0
	return S3, O3, ev3


"""
  Energy
  =======
   Energy = P * release * Net head
"""


# Energy output per month for Sunkoshi 3
def E3(x):
	e3 = np.zeros(Tmonth)  # initial Energy all values are zero
	H3 = Height3(x)
	R3 = (x * 10 ** 6) / (Days * 24 * 3600)
	for i in range(Tmonth):
		e3[i] = ((g * ita_S3 * R3[i] * H3[i] / 1000) * Days[i] * 24) / 1000
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
		H3[i] = Interpolate(Ex3, (S3[i] + S3[i + 1]) / 2, c='Elev')
		H3[i] = H3[i] - S3_effective_twl
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


def Evaporation3(a, b, d):
	S3a = Interpolate(Ex3, a, c='SArea')
	Eva = (ev[b] * S3a) * Days[d] / 10 ** 9
	return Eva


# calling pso function in pso.py

xopt, fopt, iter_vs_swamp_vs_fitness, iter_vs_globalbest = pso(fitness, lb, ub, swarmsize=swarmsize, pem=pem, wmax=wmax, wmin=wmin, c1=C1, c2=C2, X=X, maxiter=maxiter, minstep=minstep, minfunc=minfunc, debug=False)

"""
  Printing and Saving Outputs
  ============================

"""
print('Optimal fitness function value:')
print('    myfunc: {}'.format(fopt))

print('The Output of the optimization can be found in same folder as this file in Excel-file named "S3-check.xlsx":')

Release_Sunkoshi_3 = xopt
Storage_for_S3, Overflow_for_S3, Evaporation_loss_S3 = Storage3(xopt)
Storage_for_S3 = Storage_for_S3[:-1]

Storage_Sunkoshi_3 = Storage_for_S3
Overflow_Sunkoshi_3 = Overflow_for_S3

Day_energy_percent_for_total = Dry_energy_checkT(xopt)
Day_energy_percent_Annually = Dry_energy_checkA(xopt)

Energy_Sunkoshi_3 = E3(xopt)

Fitness_value = fopt

Inputs = ['swarmsize', 'wmax', 'wmin', 'C1', 'C2', 'X', 'maxiter', 'minstep', 'minfunc', 'Fitness_value', 'Dry_energy percent Total']

'''
 Writing to Excel
 =================
 Here,writing the output obtained to excel file PSO_Outputs.xlsx
'''
PSO_Outputs = pd.ExcelWriter('S3-check.xlsx')

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
Outputs["Evaporation_loss_S3"] = Evaporation_loss_S3

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
pso_data1.to_excel(PSO_Outputs, sheet_name='iter_vs_swamp_vs_fitness', index=False)
pso_data2.to_excel(PSO_Outputs, sheet_name='iter_vs_Global_best_fitness', index=False)
Day_energy_percent_A.to_excel(PSO_Outputs, sheet_name='Dry_Energy', index=False)

Time = pd.DataFrame()
Time['Time'] = [(time.time() - start_time)]
Time.to_excel(PSO_Outputs, sheet_name='Elapsed Time', index=False)

PSO_Outputs.save()

# print('    mycon : {}'.format(mycons(xopt, *args)))

print("time elapsed: {:.2f}s".format(time.time() - start_time))
