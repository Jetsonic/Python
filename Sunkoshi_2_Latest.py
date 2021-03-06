import time
import pandas as pd
import numpy as np

from PSO_Algorithm import pso
from data_pso import Interpolate, Is2, Ex2, Tyear, Fyear, Days, Dmd_MD, l2

start_time = time.time()

"""
  Initialization
  ===============
   Input following commands on python console if error of these modules not present.
     pip install pyswarm
     pip install numpy
     Make sure data_pso python file is in same folder as this file.

   Things to note.
   ===============
     Make sure data_pso python file is in same folder as this file.
     Make sure PSO_Algorithm python file is in same folder as this file.
     Make sure data_pso.xlsx file is in same folder as this file.
     Make sure Sunkoshi.xlsx file is in same folder as this file

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
wmax = 1
wmin = 1
C1 = 1
C2 = 0.8
X = 0.9
pem = 0.3
maxiter = 1
minstep = 1e-8
minfunc = 1e-8

""""
  Introduction
  ============
   Objective Function for Multi-reservoir release optimization using PSO algorithm

   Objective Function maximize E=???(t=0)to(t=n)[P(R2 * H3 + Qm * Hm +  R2 * H2 + R1 * H1 + Qk * Hk )]

   Where,
     P = turbine efficiency * Density of water * Acceleration due to gravity
     R2 = Release from Sunkoshi-2 at time t
     H2 = Height of Sunkoshi-2 water head at time t

  Imports and Variables
  ======================

   Importing PSO algorithm from github id:https://github.com/tisimst/pyswarm

   Also importing input variables from data_pso.py file

     I2     : Inflow at Sunkoshi 2 [Khurkot(652)]
     Ex2    : H-V-A curve data for Sunkoshi-2
     S2max  : Maximum Sunkoshi-2 reservoir capacity in MCM
     S2min  : Minimum Sunkoshi-2 reservoir capacity in MCM
     S2_twl : Turbine level at Sunkoshi-2         
     Ev2    : Evaporation loss from Sunkoshi-2 reservoir at time t is function of surface area
     O2     : Overflow from Sunkoshi-2 reservoir at time t
     H2     : Water level in Sunkoshi-2 reservoir at time t
     e2     : Energy output by Sunkoshi-2 at time t, is in KWh
     ev     : Evaporation in mm per month
"""
#  All Input Constant Data's
g = 9.810  # Acceleration due to gravity
ev = (1.51, 2.34, 3.6, 5.09, 5.49, 4.97, 4.14, 4.22, 3.91, 3.41, 2.46, 1.72)  # mean daily evapo-transpiration index of koshi basin
MDR = 10

#  Sunkoshi-2
ita_S2 = 0.86  # Efficiency of Hydro-Electric plant of Sunkoshi-2 (from DOED report)
power2 = 1978  # Installed Capacity in Megawatt of Sunkoshi-2 (from DOED report)
S2max = 1806.892334  # h = 535   # Sunkoshi-2 maximum Storage volume in MCM at masl 560 m (from DOED report)
S2min = 776.999601  # h = 505   # Sunkoshi-2 minimum Storage volume in MCM at masl 510 m (from DOED report)
S2_effective_twl = 424.6  # Sunkoshi-2 turbine level in masl m (from DOED report)
S2_rated_discharge = 1048  # Sunkoshi-2 total rated discharge in m3/s(from DOED report)
S2_upper_limit_Release = (S2max - S2min) + max(l2)  # Fixing upper-limit such that it is sum of live-storage and maximum Inflow ever
lower_release = 67

# Sunkoshi Marine Diversion
ita_MD = 0.91  # Efficiency of Hydro-Electric plant of Marine Diversion (from DOED report)
power_MD = 28.62  # Installed Capacity in Megawatt of Sunkoshi-1 (from DOED report)
H_MD = 47.7  # Sunkoshi Marine Diversion project Net Head in m (from DOED report)
S_MD_Max_discharge = 67  # Maximum release from Marine Diversion is taken as design discharge 67 m3/s

"""
   Environment
  ============
   Listmaker: Is function which takes any positive integer(n) as input and returns a list 
             with n number of elements whose value are set to zero.

   Here,
        In this code Fyear to Lyear are taken as optimizing years
        So,total number of years to optimize is Tyear = Lyear - Fyear + 1 years

   Then with each year having 12 months, total number of optimizing instances: Tyear * 12 = Tmonth

   We have Ovariables = 2 Releases to optimize each month R2 and R2
   Qm, Release from Marine Diversion is taken as constant 67 m3/s which when converted to MCM for a month equals to 67*seconds_per_month = 176 MCM
   optimized values to : Tmonth * Ovariables = T_O_V
     lb  : Lower bound for pso search for all T_O_V optimization values
     ub  : upper bound for pso search for all T_O_V optimization values
     ub_S2  : for Sunkoshi-2 is taken as rated total turbine discharge 1048 m3/s when converted to MCM for a month equals to 67*seconds_per_month = 2756 MCM 
     lb_S2  : for Sunkoshi-2 is taken as 0

"""


def listmaker(n):
	listofzeros = [0.0] * n
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
		ub[i] = (S_MD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Marine Diversion
		lb[i] = Dmd_MD[0]  # lowerbounds for Sunkoshi Marine Diversion
		if i < Tmonth:
			ub[i] = S2_upper_limit_Release  # bonds for Sunkoshi-2
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
	elif i % 12 == 1:
		month = "Feb"
		ub[i] = (S_MD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Marine Diversion
		lb[i] = Dmd_MD[1]  # lowerbounds for Sunkoshi Marine Diversion
		if i < Tmonth:
			ub[i] = S2_upper_limit_Release  # bonds for Sunkoshi-2
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
	elif i % 12 == 2:
		month = "Mar"
		ub[i] = (S_MD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Marine Diversion
		lb[i] = Dmd_MD[2]  # lowerbounds for Sunkoshi Marine Diversion
		if i < Tmonth:
			ub[i] = S2_upper_limit_Release  # bonds for Sunkoshi-2
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
	elif i % 12 == 3:
		month = "Apr"
		ub[i] = (S_MD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Marine Diversion
		lb[i] = Dmd_MD[3]  # lowerbounds for Sunkoshi Marine Diversion
		if i < Tmonth:
			ub[i] = S2_upper_limit_Release  # bonds for Sunkoshi-2
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
	elif i % 12 == 4:
		month = "May"
		ub[i] = (S_MD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Marine Diversion
		lb[i] = Dmd_MD[4]  # lowerbounds for Sunkoshi Marine Diversion
		if i < Tmonth:
			ub[i] = S2_upper_limit_Release  # bonds for Sunkoshi-2
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
	elif i % 12 == 5:
		month = "Jun"
		ub[i] = (S_MD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Marine Diversion
		lb[i] = Dmd_MD[5]  # lowerbounds for Sunkoshi Marine Diversion
		if i < Tmonth:
			ub[i] = S2_upper_limit_Release  # bonds for Sunkoshi-2
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
	elif i % 12 == 6:
		month = "Jul"
		ub[i] = (S_MD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Marine Diversion
		lb[i] = Dmd_MD[6]  # lowerbounds for Sunkoshi Marine Diversion
		if i < Tmonth:
			ub[i] = S2_upper_limit_Release  # bonds for Sunkoshi-2
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
	elif i % 12 == 7:
		month = "Aug"
		ub[i] = (S_MD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Marine Diversion
		lb[i] = Dmd_MD[7]  # lowerbounds for Sunkoshi Marine Diversion
		if i < Tmonth:
			ub[i] = S2_upper_limit_Release  # bonds for Sunkoshi-2
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
	elif i % 12 == 8:
		month = "Sep"
		ub[i] = (S_MD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Marine Diversion
		lb[i] = Dmd_MD[8]  # lowerbounds for Sunkoshi Marine Diversion
		if i < Tmonth:
			ub[i] = S2_upper_limit_Release  # bonds for Sunkoshi-2
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
	elif i % 12 == 9:
		month = "Oct"
		ub[i] = (S_MD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Marine Diversion
		lb[i] = Dmd_MD[9]  # lowerbounds for Sunkoshi Marine Diversion
		if i < Tmonth:
			ub[i] = S2_upper_limit_Release  # bonds for Sunkoshi-2
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
	elif i % 12 == 10:
		month = "Nov"
		ub[i] = (S_MD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Marine Diversion
		lb[i] = Dmd_MD[10]  # lowerbounds for Sunkoshi Marine Diversion
		if i < Tmonth:
			ub[i] = S2_upper_limit_Release  # bonds for Sunkoshi-2
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
	elif i % 12 == 11:
		month = "Dec"
		ub[i] = (S_MD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Marine Diversion
		lb[i] = Dmd_MD[11]  # lowerbounds for Sunkoshi Marine Diversion
		if i < Tmonth:
			ub[i] = S2_upper_limit_Release  # bonds for Sunkoshi-2
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
	j = j + 1
"""
  Objective function
  ===================
 The algorithm Swarm searches for minimum value value.
  Two types of fitness function can be made with above objective function 
  i) Here value of total energy is normalized
  ii) Here the value of energy is combine total

  From T_O_V optimized values
  ---------------------------
    Values that are indexed in range [0-Tmonth] are stored in R2 

  Here the value of releases are in MCM per month.
  Fitness function gives the total amount energy potential that can be generated when input parameters and optimized released are used as operation policy.

"""


# objective function maximizing power production
def fitness(x):
	F = 0
	z_dry = 0
	z_wet = 0
	H2 = Height2(x)
	R2 = ((x[:Tmonth]) * 10 ** 6) / (Days * 24 * 3600)
	Q_MD = (x[Tmonth:2 * Tmonth] * 10 ** 6) / (Days * 24 * 3600)
	for i in range(Tmonth):
		if i % 12 == 0 or i % 12 == 1 or i % 12 == 2 or i % 12 == 3 or i % 12 == 4 or i % 12 == 11:
			p_dry = (g * ita_S2 * (R2[i]-Q_MD[i]) * H2[i]) / 1000 if (g * ita_S2 * (R2[i]-Q_MD[i]) * H2[i]) / 1000 <= power2 else power2
			p_MD_dry = (g * ita_MD * Q_MD[i] * H_MD) / 1000
			z_dry = 1 - (p_dry / power2) + 1 - (p_MD_dry / power_MD)
		elif i % 12 == 5 or i % 12 == 6 or i % 12 == 7 or i % 12 == 8 or i % 12 == 9 or i % 12 == 10:
			p_wet = (g * ita_S2 * (R2[i]-Q_MD[i]) * H2[i]) / 1000 if (g * ita_S2 * (R2[i]-Q_MD[i]) * H2[i]) / 1000 <= power2 else power2
			p_MD_wet = (g * ita_MD * Q_MD[i] * H_MD) / 1000
			z_wet = 1 - (p_wet / power2) + 1 - (p_MD_wet / power_MD)
		Total = (z_dry - z_wet) / 2
		z_dry = 0
		z_wet = 0
		F = F + Total
	return F / Tmonth


# def fitness(x):
#	z = 0
#	z_dry = 0
#	z_wet = 0
#	H2 = Height2(x)
#	R2 = (x * 10 ** 6) / (Days * 24 * 3600)
#	for i in range(Tmonth):
#		if i % 12 == 0 or i % 12 == 1 or i % 12 == 2 or i % 12 == 3 or i % 12 == 4 or i % 12 == 11:
#			z_dry = 1 - (g * ita_S2 * R2[i] * H2[i]) / (1000 * power2)
#		elif i % 12 == 5 or i % 12 == 6 or i % 12 == 7 or i % 12 == 8 or i % 12 == 9 or i % 12 == 10:
#			z_wet = 1 - (g * ita_S2 * R2[i] * H2[i]) / (1000 * power2)
#		Total = 100 * z_dry - z_wet
#		z = z + Total
#	return z

"""                                                                                                                                                
   Mass Balance                                                                                                                               
   =============
    Here, 
     S_(t) is the storage at the beginning of time period t
      For Sunkoshi-3 dam:
      -------------------
      S2(t) = I3(inflow) + S2(t-1)-{R2(t-1)(release from sunkoshi-3)-Evaporation at time t}

      For Sunkoshi-2 dam: 
      -------------------                                                                                                                        
      S2(t) = S2(t-1) + R2(t-1) + O3(t-1) + l2(t-1) - {Qm(t-1) + R2(t-1) + Ev2(t-1)}

      For Sunkoshi-1 dam:
      -------------------
      S1(t) = S1(t-1) + R2(t-1) + l1(t-1) + O2(t-1) - {R1(t-1) + Ev1(t-1)} 

      Constrains
      ----------

       When storage volume obtained is lower than minimum storage capacity{i.e. S_min > S_(t)}
       ---------------------------------------------------------------------------------------
         then,S_(t) = S_min
         and, R_(t) <= total inflow at t (sum of inflow and overflow from dam upstream is any)  

       When storage volume obtained is greater than storage capacity{i.e. S_max < S_(t)}
       ----------------------------------------------------------------------------------
         then,S_(t) = S_max
         and,Overflow[O_(t)] = S_(t) - S_max

 """
"""
  Minimum Dry Energy 
  ===================
  In this function the out put of PSO is introduced to output percentage of Dry energy for each year which is used below in mycons function to check for feasible solutions.

"""


def Dry_energy_checkA(x):  # Annual dry energy check
	z_dry = 0
	z_wet = 0
	dry_percentA = listmaker(int(Tmonth / 12))
	E = x  # Changing value of release from MCM to cms
	j = 0
	for i in range(Tmonth):
		if i % 12 == 0 or i % 12 == 1 or i % 12 == 2 or i % 12 == 3 or i % 12 == 4 or i % 12 == 11:
			z_dry += E[i]
			if i % 12 == 11:
				dry_percentA[j] = dry_energy(z_dry, z_wet)
				j = j + 1
				z_dry = 0
				z_wet = 0
		elif i % 12 == 5 or i % 12 == 6 or i % 12 == 7 or i % 12 == 8 or i % 12 == 9 or i % 12 == 10:
			z_wet += E[i]
	return dry_percentA


def Dry_energy_checkT(x):  # Total dry energy check
	z_dry = 0
	z_wet = 0
	dry_percentT = 0
	E = x  # Changing value of release from MCM to cms
	j = 0
	for i in range(Tmonth):
		if i % 12 == 0 or i % 12 == 1 or i % 12 == 2 or i % 12 == 3 or i % 12 == 4 or i % 12 == 11:
			z_dry += E[i]
		elif i % 12 == 5 or i % 12 == 6 or i % 12 == 7 or i % 12 == 8 or i % 12 == 9 or i % 12 == 10:
			z_wet += E[i]
	dry_percentT = dry_energy(z_dry, z_wet)
	return dry_percentT


def dry_energy(z_dry, z_wet):
	dry_percent_total = (z_dry / (z_dry + z_wet) * 100) if (z_dry + z_wet) != 0 else 0
	return dry_percent_total


# all constrains required
def mycons(x):
	cons = []
	return cons


# mass balance for sunkoshi 2
def Storage2(x):
	S2 = np.zeros(Tmonth + 1)
	S2[0] = S2max
	ev2 = []
	R2 = x[:Tmonth]
	R_MD = x[Tmonth:2 * Tmonth]
	j = 0
	for i in range(Tmonth):
		Ev2 = Evaporation2(S2[i], j, i)
		ev2.append(Ev2)
		S2[i + 1] = l2[i] + Is2[i] + S2[i] - (R2[i] + Ev2)
		if S2[i + 1] < S2min:
			R2[i] = lb[i] + np.random.rand() * (S2[i] + Is2[i] + l2[i] - Ev2 - S2min - lb[i])
			if (R2[i] - R_MD[i]) < lb[i]:
				R_MD[i] = lb[i + Tmonth]
				if (R2[i] - R_MD[i]) < lb[i]:
					R_MD[i] = R2[i] - lb[i]
					if R_MD[i] < 0:
						R_MD[i] = 0
			S2[i + 1] = S2[i] + Is2[i] + l2[i] - (R2[i] + Ev2)
		else:
			S2[i + 1] = S2[i] + Is2[i] + l2[i] - (R2[i] + Ev2)
		if S2[i + 1] > S2max:
			R2[i] = R2[i] + S2[i + 1] - S2max
			S2[i + 1] = S2[i] + Is2[i] + l2[i] - (R2[i] + Ev2)
		else:
			S2[i + 1] = S2[i] + Is2[i] + l2[i] - (R2[i] + Ev2)
		j += 1
		if j == 12:
			j = 0
	return S2, ev2


"""
  Energy
  =======
   Energy = P * release * Net head
"""


# Energy output per month for Sunkoshi 2
def E2(x):
	e2 = np.zeros(Tmonth)  # initial Energy all values are zero
	e_MD = np.zeros(Tmonth)
	p2 = np.zeros(Tmonth)
	p_MD = np.zeros(Tmonth)
	H2 = Height2(x)
	R2 = (x[:Tmonth] * 10 ** 6) / (Days * 24 * 3600)
	Q_MD = (x[Tmonth:2 * Tmonth] * 10 ** 6) / (Days * 24 * 3600)
	Q2 = np.zeros(Tmonth)
	Sp2 = np.zeros(Tmonth)
	for i in range(Tmonth):
		p2[i] = g * ita_S2 * (R2[i] - Q_MD[i]) * H2[i] / 1000 if (g * ita_S2 * (R2[i] - Q_MD[i]) * H2[i] / 1000) <= power2 else power2
		e2[i] = (p2[i] * Days[i] * 24) / 1000
		Q2[i] = (p2[i] / (g * ita_S2 * H2[i]) * 1000)
		p_MD[i] = (g * ita_MD * Q_MD[i] * H_MD) / 1000
		e_MD[i] = (p_MD[i] * Days[i] * 24) / 1000
		Sp2[i] = ((R2[i] - Q_MD[i] - Q2[i]) * Days[i] * 24 * 3600) / 10 ** 6 if Q2[i] < (R2[i] - Q_MD) else 0
	return p2, p_MD, e2, e_MD, Q2, Q_MD, Sp2


"""
  Height
  =======
   Height function H=f(storage)
   Obtained from H-V-A curve
"""


# Height for Sunkoshi-2
def Height2(x):
	H2 = np.zeros(Tmonth)
	S2 = Storage2(x)[0]
	for i in range(Tmonth):
		H2[i] = Interpolate(Ex2, (S2[i] + S2[i + 1]) / 2, c='Elev')
		H2[i] = H2[i] - S2_effective_twl
	return H2


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


def Evaporation2(a, b, d):
	S2a = Interpolate(Ex2, a, c='SArea')
	Eva = (ev[b] * S2a) * Days[d] / 10 ** 9
	return Eva


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

Release_Sunkoshi_2 = xopt[:Tmonth]
Storage_for_S2, Evaporation_loss_S2 = Storage2(xopt)
Storage_for_S2 = Storage_for_S2[:-1]
Elevation_for_Sunkoshi_2 = Height2(xopt) + S2_effective_twl
Storage_Sunkoshi_2 = Storage_for_S2

Power_Sunkoshi_2, Power_MD, Energy_Sunkoshi_2, Energy_MD, Discharge_Sunkoshi_2, Discharge_MD, Spill_for_Sunkoshi_2 = E2(xopt)

Day_energy_percent_for_S2_total = Dry_energy_checkT(Energy_Sunkoshi_2)
Dry_energy_percent_Annually_for_S2 = Dry_energy_checkA(Energy_Sunkoshi_2)

Fitness_value = fopt

Inputs = ['swarmsize', 'wmax', 'wmin', 'C1', 'C2', 'X', 'maxiter', 'minstep', 'minfunc', 'Fitness_value', 'Dry_energy percent Total for S2']

'''
 Writing to Excel
 =================
 Here,writing the output obtained to excel file PSO_Outputs.xlsx
'''
PSO_Outputs = pd.ExcelWriter('PSO_Outputs_Sunkoshi2_Only.xlsx')

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
Parameters['Values'] = [swarmsize, wmax, wmin, C1, C2, X, maxiter, minstep, minfunc, Fitness_value, Day_energy_percent_for_S2_total]

Outputs['Date'] = Date
Outputs['Month'] = Month
Outputs['Inflows_for_S2'] = l2
Outputs['Outflow_Sunkoshi_2'] = Release_Sunkoshi_2
Outputs['Storage_Sunkoshi_2'] = Storage_Sunkoshi_2
Outputs['Elevation_Sunkoshi_2'] = Elevation_for_Sunkoshi_2
Outputs["Evaporation_loss_S2"] = Evaporation_loss_S2

Outputs['Discharge_for_Sunkoshi_2'] = Discharge_Sunkoshi_2
Outputs['Power_for_Sunkoshi_2'] = Power_Sunkoshi_2
Outputs['Energy_Sunkoshi_2'] = Energy_Sunkoshi_2

Outputs['Discharge_MD'] = Discharge_MD

Outputs['Spill_Sunkoshi_2'] = Spill_for_Sunkoshi_2

Outputs["Evaporation_loss_S2"] = Evaporation_loss_S2

Release['Date'] = Date
Release['Month'] = Month
Release['Release_Sunkoshi_2'] = Release_Sunkoshi_2

Storage['Date'] = Date
Storage['Month'] = Month
Storage['Storage_Sunkoshi_2'] = Storage_Sunkoshi_2

Energy['Date'] = Date
Energy['Month'] = Month
Energy['Energy_Sunkoshi_2'] = Energy_Sunkoshi_2

Day_energy_percent_A['Date'] = Date1
Day_energy_percent_A['Dry Energy percent S2'] = Dry_energy_percent_Annually_for_S2

Parameters.to_excel(PSO_Outputs, sheet_name='Parameters', index=False)
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
