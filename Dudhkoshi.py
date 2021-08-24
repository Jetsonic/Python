import time
import pandas as pd
import numpy as np
from PSO_Algorithm import pso
from data_pso import Interpolate, Dk, Exd, Tyear, Fyear, Days

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
swarmsize = 8
wmax = 0.5
wmin = 0.1
C1 = 1
C2 = 0.5
X = 0.9
pem = 0.3
maxiter = 1
minstep = 1e-8
minfunc = 1e-8
""""
  Introduction
  ============
   Objective Function for Multi-reservoir release optimization using PSO algorithm

   Objective Function maximize E=∑(t=0)to(t=n)[P(Rd * Hd)]

   Where,
     ita = turbine efficiency
     g = Acceleration due to gravity
     Rd = Release from Dudhkoshi at time t
     Hd = Height of Dudhkoshi water head at time t

"""

"""
  Imports and Variables
  ======================

   Importing PSO algorithm from github id:https://github.com/tisimst/pyswarm

   Also importing input variables from data_pso.py file
     Dk     : Inflow at Dudhkoshi [Rabuwa bazar]
     Exd    : H-V-A curve data for Dudhkoshi
     Sdmax  : Maximum Dudhkoshi reservoir capacity in MCM 
     Sdmin  : Minimum Dudhkoshi reservoir capacity in MCM
     Sd_twl : Turbine level at Dudhkoshi   
     Evd    : Evaporation loss from Dudhkoshi reservoir at time t is function of surface area    
     Od     : Overflow from Dudhkoshi reservoir at time t        
     Sda    : Surface area water in Dudhkoshi reservoir at time t
     Hd     : Water level in Dudhkoshi reservoir at time t
     ed     : Energy output by Dudhkoshi at time t, is in KWh
     ev     : Evaporation in mm per month
"""
#  All Input Constant Data's
g = 9.810  # Acceleration due to gravity
ev = (1.51, 2.34, 3.6, 5.09, 5.49, 4.97, 4.14, 4.22, 3.91, 3.41, 2.46, 1.72)  # mean daily evapo-transpiration index of koshi basin

# Dudhkoshi
Sdmax = 1503.37  # h = 636
Sdmin = 238.9  # h = 530
MDR = 10  # Minimum environment release

# Sunkoshi-Powerhouse
ita_sk = 0.934  # Efficiency of Hydro-Electric plant at sunkoshi
power_sk = 600  # Installed Capacity in Megawatt for sunkoshi power house
SK_effective_twl = 366.4  # Max head minus rated head of turbine
SK_rated_discharge = 242.8  # Dudhkoshi total rated discharge for sunkoshi powerhouse in m3/s(from DOED report)

#  Dam Toe-Powerhouse
ita_dt = 0.918  # Efficiency of Hydro-Electric plant at dam toe
power_dt = 35  # Installed Capacity in Megawatt for Dam toe power house
Dt_effective_twl = 451  # Max head minus rated head of turbine
Dt_rated_discharge = 21  # Dudhkoshi total rated discharge for Dam toe powerhouse in m3/s(from DOED report)

"""
  Environment
  ============
   Listmaker: Is function which takes any positive integer(n) as input and returns a list 
             with n number of elements whose value are set to zero.

   Here,
        In this code Fyear to Lyear are taken as optimizing years
        So,total number of years to optimize is Tyear = Lyear - Fyear + 1 years

   Then with each year having 12 months, total number of optimizing instances: Tyear * 12 = Tmonth

   We have Ovariables = 1 Releases to optimize each month Rd which takes total size of
   optimized values to : Tmonth * Ovariables = T_O_V

     lb  : Lower bound for pso search for all T_O_V optimization values
     ub  : upper bound for pso search for all T_O_V optimization values     
     cons: Stores constrains output can be used to check errors 

"""


def listmaker(n):
	listofzeros = [0] * n
	return listofzeros


Tmonth = Tyear * 12
Ovariables = 2
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

   following code facilities this process such that these bounds can be given for each releases for each month. 
"""

j = 0
for i in range(0, T_O_V):
	if j >= Tmonth:
		j = 0
	if i % 12 == 0 or i == 0:
		month = "Jan"
		ub[i] = (Dt_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		if i / 12 < (Tmonth / 12):
			ub[i] = (SK_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi Sunkoshi powerhouse
			lb[i] = 0  # bonds for Dudhkoshi Sunkoshi powerhouse
	elif i % 12 == 1:
		month = "Feb"
		ub[i] = (Dt_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		if i / 12 < (Tmonth / 12):
			ub[i] = (SK_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi Sunkoshi powerhouse
			lb[i] = 0  # bonds for Dudhkoshi Sunkoshi powerhouse
	elif i % 12 == 2:
		month = "Mar"
		ub[i] = (Dt_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		if i / 12 < (Tmonth / 12):
			ub[i] = (SK_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi Sunkoshi powerhouse
			lb[i] = 0  # bonds for Dudhkoshi Sunkoshi powerhouse
	elif i % 12 == 3:
		month = "Apr"
		ub[i] = (Dt_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		if i / 12 < (Tmonth / 12):
			ub[i] = (SK_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi Sunkoshi powerhouse
			lb[i] = 0  # bonds for Dudhkoshi Sunkoshi powerhouse
	elif i % 12 == 4:
		month = "May"
		ub[i] = (Dt_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		if i / 12 < (Tmonth / 12):
			ub[i] = (SK_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi Sunkoshi powerhouse
			lb[i] = 0  # bonds for Dudhkoshi Sunkoshi powerhouse
	elif i % 12 == 5:
		month = "Jun"
		ub[i] = (Dt_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		if i / 12 < (Tmonth / 12):
			ub[i] = (SK_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi Sunkoshi powerhouse
			lb[i] = 0  # bonds for Dudhkoshi Sunkoshi powerhouse
	elif i % 12 == 6:
		month = "Jul"
		ub[i] = (Dt_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		if i / 12 < (Tmonth / 12):
			ub[i] = (SK_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi Sunkoshi powerhouse
			lb[i] = 0  # bonds for Dudhkoshi Sunkoshi powerhouse
	elif i % 12 == 7:
		month = "Aug"
		ub[i] = (Dt_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		if i / 12 < (Tmonth / 12):
			ub[i] = (SK_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi Sunkoshi powerhouse
			lb[i] = 0  # bonds for Dudhkoshi Sunkoshi powerhouse
	elif i % 12 == 8:
		month = "Sep"
		ub[i] = (Dt_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		if i / 12 < (Tmonth / 12):
			ub[i] = (SK_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi Sunkoshi powerhouse
			lb[i] = 0  # bonds for Dudhkoshi Sunkoshi powerhouse
	elif i % 12 == 9:
		month = "Oct"
		ub[i] = (Dt_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		if i / 12 < (Tmonth / 12):
			ub[i] = (SK_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi Sunkoshi powerhouse
			lb[i] = 0  # bonds for Dudhkoshi Sunkoshi powerhouse
	elif i % 12 == 10:
		month = "Nov"
		ub[i] = (Dt_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		if i / 12 < (Tmonth / 12):
			ub[i] = (SK_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi Sunkoshi powerhouse
			lb[i] = 0  # bonds for Dudhkoshi Sunkoshi powerhouse
	elif i % 12 == 11:
		month = "Dec"
		ub[i] = (Dt_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		if i / 12 < (Tmonth / 12):
			ub[i] = (SK_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi Sunkoshi powerhouse
			lb[i] = 0  # bonds for Dudhkoshi Sunkoshi powerhouse

"""
Objective function
  ===================

  The algorithm Swarm searches for minimum value value so objective function is multiplied by -1
  Two types of fitness function can be made with above objective function 
  i) Here value of total energy is normalized
  ii) Here the value of energy is combine total


  From T_O_V optimized values
  ---------------------------
    Values that are indexed in range [0-Tmonth] are stored in Rsk sunkoshi powerhouse release
	Values that are indexed in range [Tmonth-2*Tmonth] are stored in Rdt dam toe powerhouse release
	
  Here the value of releases are in MCM per month.
  Fitness function gives the total amount energy potential that can be generated when input parameters and optimized released are used as operation policy.
"""


# objective function maximizing power production
def fitness(x):
	z = 0
	z_dry = 0
	z_wet = 0
	H_sk = Height_sk(x)
	H_dt = Height_dt(x)
	R_sk = (x[:Tmonth] * 10 ** 6) / (Days * 24 * 3600)  # changing the value of MCM to m3/s  for release of Sunkoshi 3
	R_dt = (x[Tmonth:Tmonth * 2] * 10 ** 6) / (Days * 24 * 3600)  # Similar to above for release of Sunkoshi 2
	for i in range(Tmonth):
		if i % 12 == 0 or i % 12 == 1 or i % 12 == 2 or i % 12 == 3 or i % 12 == 4 or i % 12 == 11:
			z_dry = 1 - (g * ita_sk * R_sk[i] * H_sk[i]) / (1000 * power_sk) + 1 - (g * ita_dt * R_dt[i] * H_dt[i]) / (1000 * power_dt)
		elif i % 12 == 5 or i % 12 == 6 or i % 12 == 7 or i % 12 == 8 or i % 12 == 9 or i % 12 == 10:
			z_wet = 1 - (g * ita_sk * R_sk[i] * H_sk[i]) / (1000 * power_sk) + 1 - (g * ita_dt * R_dt[i] * H_dt[i]) / (1000 * power_dt)
		Total = 100 * z_dry - z_wet
		z = z + Total
	return z


"""
  Minimum Dry Energy 
  ===================
  In this function the out put of PSO is introduced to output percentage of Dry energy for each year which is used below in mycons function to check for feasible solutions.

"""


def Dry_energy_checkA(x, c='v'):  # Annual dry energy check
	z_dry = 0
	z_wet = 0
	ita = 0
	H = np.zeros(Tmonth)
	R = np.zeros(Tmonth)
	H_sk = Height_sk(x)
	H_dt = Height_dt(x)
	dry_percentA = np.zeros(int(Tmonth / 12))  # defining a 1D array of zeros with size total no of years
	R_sk = (x[:Tmonth] * 10 ** 6) / (Days * 24 * 3600)
	R_dt = (x[Tmonth:Tmonth * 2] * 10 ** 6) / (Days * 24 * 3600)
	if c == 'sk':
		R = R_sk
		ita = ita_sk
		H = H_sk
	if c == 'dt':
		R = R_dt
		ita = ita_dt
		H = H_dt
	u = 0
	for i in range(Tmonth):
		if i % 12 == 0 or i % 12 == 1 or i % 12 == 2 or i % 12 == 3 or i % 12 == 4 or i % 12 == 11:
			z_dry += (g * ita * R[i] * H[i]) / 1000
			if i % 12 == 11:
				dry_percentA[u] = dry_energy(z_dry, z_wet)
				u = u + 1
				z_dry = 0
				z_wet = 0
		elif i % 12 == 5 or i % 12 == 6 or i % 12 == 7 or i % 12 == 8 or i % 12 == 9 or i % 12 == 10:
			z_wet += (g * ita * R[i] * H[i]) / 1000
	return dry_percentA


def Dry_energy_checkT(x, c='v'):  # Total dry energy check
	z_dry = 0
	z_wet = 0
	ita = 0
	H = np.zeros(Tmonth)
	R = np.zeros(Tmonth)
	H_sk = Height_sk(x)
	H_dt = Height_dt(x)
	R_sk = (x[:Tmonth] * 10 ** 6) / (Days * 24 * 3600)
	R_dt = (x[Tmonth:Tmonth * 2] * 10 ** 6) / (Days * 24 * 3600)
	if c == 'sk':
		R = R_sk
		ita = ita_sk
		H = H_sk
	if c == 'dt':
		R = R_dt
		ita = ita_dt
		H = H_dt
	for i in range(Tmonth):
		if i % 12 == 0 or i % 12 == 1 or i % 12 == 2 or i % 12 == 3 or i % 12 == 4 or i % 12 == 11:
			z_dry += (g * ita * R[i] * H[i] / 1000)
		elif i % 12 == 5 or i % 12 == 6 or i % 12 == 7 or i % 12 == 8 or i % 12 == 9 or i % 12 == 10:
			z_wet += (g * ita * R[i] * H[i] / 1000)
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
      Sd(t) = Dk(inflow) + Sd(t-1)-{Rd(t-1)(release from Dudhkoshi)-Evaporation at time t}


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


# mass balance for Dudhkoshi
def Storaged(x):
	Sd = np.zeros(Tmonth + 1)
	Od = np.zeros(Tmonth)  # initial overflow all values are zero
	evd = []
	Sd[0] = Sdmax
	R_sk = x[:Tmonth]
	R_dt = x[Tmonth:]
	j = 0
	for i in range(Tmonth):
		Evd = Evaporationd(Sd[i], j, i)
		evd.append(Evd)
		Sd[i + 1] = Dk[i] + Sd[i] - (R_dt[i] + R_sk[i] + Evd + Od[i])
		if Sd[i + 1] < Sdmin:
			R_dt[i] = lb[i+Tmonth]
			R_sk[i] = np.random.rand() * (Dk[i] + Sd[i] - Evd - R_dt[i] - Sdmin - Od[i])
			Sd[i + 1] = Dk[i] + Sd[i] - (R_dt[i] + R_sk[i] + Evd + Od[i])
			if R_sk[i] < 0:
				R_sk[i] = 0
				R_dt[i] = 0.98 * (Dk[i] + Sd[i] - Evd - R_sk[i] - Sdmin - Od[i])
				Sd[i + 1] = Dk[i] + Sd[i] - (R_dt[i] + R_sk[i] + Evd + Od[i])
		else:
			Sd[i + 1] = Dk[i] + Sd[i] - (R_sk[i] + R_dt[i] + Evd + Od[i])
		if Sd[i + 1] > Sdmax:
			Od[i] = Dk[i] + Sd[i] - (R_sk[i] + R_dt[i] + Evd) - Sdmax
			Sd[i + 1] = Dk[i] + Sd[i] - (R_sk[i] + R_dt[i] + Evd + Od[i])
		else:
			Sd[i + 1] = Dk[i] + Sd[i] - (R_sk[i] + R_dt[i] + Evd + Od[i])
		j += 1
		if j == 12:
			j = 0
	return Sd, Od, evd


"""
  Energy
  =======
   Energy = P * release * Net head
"""


# Energy output per month for Dudhkoshi
def E_dt(x):
	e_dt = np.zeros(Tmonth)
	H_dt = Height_dt(x)
	R_dt = (x[Tmonth:Tmonth * 2] * 10 ** 6) / (Days * 24 * 3600)
	for i in range(Tmonth):
		e_dt[i] = g * ita_dt * R_dt[i] * H_dt[i] / 1000
	return e_dt


def E_sk(x):
	e_sk = np.zeros(Tmonth)
	H_sk = Height_sk(x)
	R_sk = (x[:Tmonth] * 10 ** 6) / (Days * 24 * 3600)
	for i in range(Tmonth):
		e_sk[i] = g * ita_sk * R_sk[i] * H_sk[i] / 1000
	return e_sk


"""
  Height
  =======
   Height function H=f(storage)
   Obtained from H-V-A curve
"""


# Height for Dudhkoshi
#  Dam toe Powerhouse
def Height_dt(x):
	H_dt = np.zeros(Tmonth)
	Sd = Storaged(x)[0]
	for i in range(Tmonth):
		H_dt[i] = Interpolate(Exd, (Sd[i] + Sd[i + 1]) / 2, c='Elev')
		H_dt[i] = H_dt[i] - Dt_effective_twl
	return H_dt


#  Sunkoshi Powerhouse
def Height_sk(x):
	H_sk = np.zeros(Tmonth)
	Sd = Storaged(x)[0]
	for i in range(Tmonth):
		H_sk[i] = Interpolate(Exd, (Sd[i] + Sd[i + 1]) / 2, c='Elev')
		H_sk[i] = H_sk[i] - SK_effective_twl
	return H_sk


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


def Evaporationd(a, b, d):
	Dka = Interpolate(Exd, a, c='SArea')
	Evd = (ev[b] * Dka) * Days[d] / 10 ** 9
	return Evd


# def Evaporation(x,*args):

"""                          
  Constrains
  ===========
   Since constrain for storage is addressed in storage function it is no longer need to address here.
   Here Constrain for maximum energy is checked.
   constrains for irrigation demand can be addressed in [ld - ub] section.

"""

# calling pso function in pso.py
xopt, fopt, iter_vs_swamp_vs_fitness, iter_vs_globalbest = pso(fitness, lb, ub, f_ieqcons=mycons, swarmsize=swarmsize, wmax=wmax, wmin=wmin, c1=C1, c2=C2, X=X, maxiter=maxiter, minstep=minstep, minfunc=minfunc, debug=False)

"""
  Printing and Saving Outputs
  ============================

"""
print('Optimal fitness function value:')
print('    myfunc: {}'.format(fopt))

print('The optimum releases for each stations are:')

Release_Dudhkoshi_sk = xopt[:Tmonth]
Release_Dudhkoshi_dt = xopt[Tmonth:Tmonth * 2]

Storage_for_DK, Overflow_for_DK,Evaporation_loss_DK = Storaged(xopt)
Storage_for_DK = Storage_for_DK[:-1]
Storage_Dudhkoshi = Storage_for_DK
Overflow_Dudhkoshi = Overflow_for_DK

Day_energy_percent_for_sk_total = Dry_energy_checkT(xopt, c='sk')
Day_energy_percent_for_dt_total = Dry_energy_checkT(xopt, c='dt')
Day_energy_percent_for_sk_Annually = Dry_energy_checkA(xopt, c='sk')
Day_energy_percent_for_dt_Annually = Dry_energy_checkA(xopt, c='dt')

Energy_Dudhkoshi_sk = E_sk(xopt)
Energy_Dudhkoshi_dt = E_dt(xopt)

Fitness_value = fopt
Inputs = ['swarmsize', 'wmax', 'wmin', 'C1', 'C2', 'X', 'maxiter', 'minstep', 'minfunc', 'fitness', 'Dry_energy percent Total for SK PH', 'Dry_energy percent Total for DT PH']
'''
 Writing to Excel
 =================
 Here,writing the output obtained to excel file PSO_Outputs.xlsx
'''
PSO_Outputs = pd.ExcelWriter('PSO_Outputs_with_Only_dk.xlsx')

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
Parameters['Values'] = [swarmsize, wmax, wmin, C1, C2, X, maxiter, minstep, minfunc, Fitness_value, Day_energy_percent_for_sk_total, Day_energy_percent_for_dt_total]

Outputs['Date'] = Date
Outputs['Month'] = Month
Outputs['Inflows_for_Dk'] = Dk
Outputs['Release_Dudhkoshi_sk'] = Release_Dudhkoshi_sk
Outputs['Release_Dudhkoshi_dt'] = Release_Dudhkoshi_dt
Outputs['Storage_Dudhkoshi'] = Storage_Dudhkoshi
Outputs['Overflow_Dudhkoshi'] = Overflow_Dudhkoshi
Outputs['Energy_Dudhkoshi_sk'] = Energy_Dudhkoshi_sk
Outputs['Energy_Dudhkoshi_dt'] = Energy_Dudhkoshi_dt
Outputs["Evaporation_loss_S3"] = Evaporation_loss_DK

Release['Date'] = Date
Release['Month'] = Month
Release['Release_Dudhkoshi_sk'] = Release_Dudhkoshi_sk
Release['Release_Dudhkoshi_dt'] = Release_Dudhkoshi_dt

Storage['Date'] = Date
Storage['Month'] = Month
Storage['Storage_Dudhkoshi'] = Storage_Dudhkoshi

Overflow['Date'] = Date
Overflow['Month'] = Month
Overflow['Overflow_Dudhkoshi'] = Overflow_Dudhkoshi

Energy['Date'] = Date
Energy['Month'] = Month
Energy['Energy_Dudhkoshi_sk'] = Energy_Dudhkoshi_sk
Energy['Energy_Dudhkoshi_dt'] = Energy_Dudhkoshi_dt

Day_energy_percent_A['Date'] = Date1
Day_energy_percent_A['Dry Energy percent sk'] = Day_energy_percent_for_sk_Annually
Day_energy_percent_A['Dry Energy percent dt'] = Day_energy_percent_for_dt_Annually

Parameters.to_excel(PSO_Outputs, sheet_name='Inputs', index=False)
Outputs.to_excel(PSO_Outputs, sheet_name='Outputs', index=False)
Release.to_excel(PSO_Outputs, sheet_name='Release', index=False)
Storage.to_excel(PSO_Outputs, sheet_name='Storage', index=False)
Overflow.to_excel(PSO_Outputs, sheet_name='Overflow', index=False)
Energy.to_excel(PSO_Outputs, sheet_name='Energy', index=False)
Day_energy_percent_A.to_excel(PSO_Outputs, sheet_name='Dry_Energy', index=False)
pso_data1.to_excel(PSO_Outputs, sheet_name='iter_vs_swamp_vs_fitness', index=False)
pso_data2.to_excel(PSO_Outputs, sheet_name='iter_vs_Global_best_fitness', index=False)

Time = pd.DataFrame()
Time['Time'] = [(time.time() - start_time)]
Time.to_excel(PSO_Outputs, sheet_name='Elapsed Time', index=False)

PSO_Outputs.save()

print("time elapsed: {:.2f}s".format(time.time() - start_time))
