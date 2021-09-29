import time
import pandas as pd
import numpy as np
from PSO_Algorithm import pso
from data_pso_100_2003 import Interpolate, I3, Dmd_MD, Dmd_KD, Dk, l2, l1_, Ex2, Ex3, Exd, Ex1, Ex_Ko, Tyear, Fyear, Days, l_Ko
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
wmax = 1
wmin = 0.3
C1 = 1.5
C2 = 1.5
X = 1
pem = 0.3
maxiter = 1
minstep = 1e-8
minfunc = 1e-8
""""
  Introduction
  ============
   Objective Function for Multi-reservoir release optimization using PSO algorithm

   Objective Function maximize E=∑(t=0)to(t=n)[P(R3 * H3 + Qm * Hm +  R2 * H2 + R1 * H1 + Qk * Hk )]

   Where,
     P = turbine efficiency * Density of water * Acceleration due to gravity
     R3 = Release from Sunkoshi-3 at time t
     H3 = Height of Sunkoshi-3 water head at time t
     Qm = Release from Sunkoshi marine diversion at time t
     Hm = Height of Sunkoshi marine diversion net water head at time t
     R2 = Release from Sunkoshi-2 at time t
     H2 = Height of Sunkoshi-2 water head at time t
     R1 = Release from Sunkoshi-1 at time t
     H1 = Height of Sunkoshi-1 water head at time t
     R_sk = Release Dudhkoshi for sunkoshi powerhouse
     R_dt = Release Dudhkoshi for Dam toe powerhouse
     H_sk = Height of Dudhkoshi water head for sunkoshi powerhouse
     H_dt = Height of Dudhkoshi water head for Dam toe powerhouse

  Imports and Variables
  ======================

   Importing PSO algorithm from github id:https://github.com/tisimst/pyswarm

   Also importing input variables from data_pso.py file

     I3     : Inflow at Sunkoshi-3 [Pachuwarghat(630)]
     L2     : Local inflow at Sunkoshi-2 [Khurkot(652)-Pachuwarghat(630)] # Some data's have -ve value which are taken as zero
     L2     : Local inflow at Sunkoshi-1 
     Ex1    : H-V-A curve data for Sunkoshi-1
     Ex2    : H-V-A curve data for Sunkoshi-2
     Ex3    : H-V-A curve data for Sunkoshi-3
     S3max  : Maximum Sunkoshi-3 reservoir capacity in MCM
     S2max  : Maximum Sunkoshi-2 reservoir capacity in MCM
     S1max  : Maximum Sunkoshi-1 reservoir capacity in MCM
     S3min  : Minimum Sunkoshi-3 reservoir capacity in MCM
     S2min  : Minimum Sunkoshi-2 reservoir capacity in MCM
     S1min  : Minimum Sunkoshi-1 reservoir capacity in MCM
     S1_twl : Turbine level at Sunkoshi-1
     S2_twl : Turbine level at Sunkoshi-2         
     S3_twl : Turbine level at Sunkoshi-3
     Ev3    : Evaporation loss from Sunkoshi-3 reservoir at time t is function of surface area
     Ev2    : Evaporation loss from Sunkoshi-2 reservoir at time t is function of surface area
     Ev1    : Evaporation loss from Sunkoshi-1 reservoir at time t is function of surface area
     O3     : Overflow from Sunkoshi-3 reservoir at time t  
     O2     : Overflow from Sunkoshi-2 reservoir at time t
     O1     : Overflow from Sunkoshi-1 reservoir at time t         
     S3a    : Surface area water in Sunkoshi-3 reservoir at time t
     S2a    : Surface area water in Sunkoshi-2 reservoir at time t
     S1a    : Surface area water in Sunkoshi-1 reservoir at time t
     H3     : Water level in Sunkoshi-3 reservoir at time t 
     H2     : Water level in Sunkoshi-2 reservoir at time t
     H1     : Water level in Sunkoshi-1 reservoir at time t
     Hm		: Net water head in Sunkoshi marine diversion reservoir at time t
     E3     : Energy output by Sunkoshi-3 at time t, is in KWh
     E2     : Energy output by Sunkoshi-2 at time t, is in KWh
     Em    : Energy output by Sunkoshi Marine Diversion at time t, is in KWh
     E1     : Energy output by Sunkoshi-1 at time t, is in KWh
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

#  Sunkoshi-3
ita_S3 = 0.86  # Efficiency of Hydro-Electric plant of Sunkoshi-3 (from DOED report)
power3 = 683  # Installed Capacity in Megawatt of Sunkoshi-3 (from DOED report)
S3max = 1769.286774  # h = 700  # Sunkoshi-3 maximum Storage volume in MCM at masl 700 m (from DOED report)
S3min = 769.457152  # h = 660   # Sunkoshi-3 minimum Storage volume in MCM at masl 660 m (from DOED report)
S3_effective_twl = 535  # Sunkoshi-3 turbine level in masl m (from DOED report)
S3_rated_discharge = 490  # Sunkoshi-3 total rated discharge in m3/s(from DOED report)

#  Sunkoshi-2
ita_S2 = 0.86  # Efficiency of Hydro-Electric plant of Sunkoshi-2 (from DOED report)
power2 = 978  # Installed Capacity in Megawatt of Sunkoshi-2 (from DOED report)
S2max = 1806.892334  # h = 535   # Sunkoshi-2 maximum Storage volume in MCM at masl 560 m (from DOED report)
S2min = 776.999601  # h = 505   # Sunkoshi-2 minimum Storage volume in MCM at masl 510 m (from DOED report)
S2_effective_twl = 424.6  # Sunkoshi-2 turbine level in masl m (from DOED report)
S2_rated_discharge = 1048  # Sunkoshi-2 total rated discharge in m3/s(from DOED report)

#  Sunkoshi-1
ita_S1 = 0.87  # Efficiency of Hydro-Electric plant of Sunkoshi-3 (from DOED report)
power1 = 1357  # Installed Capacity in Megawatt of Sunkoshi-1 (from jica report)
S1max = 1341.308929  # h = 424.6,Assumed as twl of Sunkoshi 2
S1min = 409.5746392  # h = 385 ,Assumed for sediment settlement
S1_twl = 304.8
S1_effective_twl = 311  # Assumed as F.S.L of saptakoshi high dam as of jica study or 334.8 as of indian study
S1_rated_discharge = 1340.4

# Sunkoshi Marine Diversion
ita_MD = 0.91  # Efficiency of Hydro-Electric plant of Marine Diversion (from DOED report)
power_MD = 28.62  # Installed Capacity in Megawatt of Sunkoshi-1 (from DOED report)
H_MD = 47.7  # Sunkoshi Marine Diversion project Net Head in m (from DOED report)
S_MD_Max_discharge = 67  # Maximum release from Marine Diversion is taken as design discharge 67 m3/s

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

#  Sapta koshi
ita_Ko = 0.87  # Efficiency of Hydro-Electric plant of Sunkoshi-2 (from DOED report)
power_Ko = 3489  # Installed Capacity in Megawatt of Sunkoshi-2 (from DOED report)
S_Ko_max = 8612.70  # h = 300   # Saptakoshi maximum Storage volume in MCM at masl  m (from DOED report)
S_Ko_min = 4192.684579  # h = 259   # Saptakoshi minimum Storage volume in MCM at masl  m (from DOED report)
Ko_twl = 129.5
Ko_headloss = 6.98
Ko_effective_twl = 136.48  # Sunkoshi-2 turbine level in masl m (from DOED report)
Ko_rated_discharge = 2500  # Sunkoshi-2 total rated discharge in m3/s(from DOED report)

# Sunkoshi Kamala Diversion
ita_KD = 0.87  # Efficiency of Hydro-Electric plant of Marine Diversion (from DOED report)
power_KD = 61  # Installed Capacity in Megawatt of Sunkoshi-1 (from DOED report)
H_KD = 99.27  # Sunkoshi Marine Diversion project Net Head in m (from DOED report)dam height 49
S_KD_Max_discharge = 72  # Maximum release from Marine Diversion is taken as design discharge 72 m3/s

"""
   Environment
  ============
   Listmaker: Is function which takes any positive integer(n) as input and returns a list 
             with n number of elements whose value are set to zero.

   Here,
        In this code Fyear to Lyear are taken as optimizing years
        So,total number of years to optimize is Tyear = Lyear - Fyear + 1 years

   Then with each year having 12 months, total number of optimizing instances: Tyear * 12 = Tmonth

   We have Ovariables = 6 Releases to optimize each month R3, R2, R1, Rm R_sk and R_dt which takes total size of
   optimized values to : Tmonth * Ovariables = T_O_V

     lb  : Lower bound for pso search for all T_O_V optimization values
     ub  : upper bound for pso search for all T_O_V optimization values     
     cons: Stores constrains output can be used to check errors 
"""


def listmaker(n):
	listofzeros = [0.0] * n
	return listofzeros


Tmonth = Tyear * 12
Ovariables = 8
T_O_V = Tmonth * Ovariables
lb = np.zeros(T_O_V)
ub = np.zeros(T_O_V)

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
		ub[i] = (S_KD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Kamala Diversion
		lb[i] = Dmd_KD[0]  # lowerbounds for Sunkoshi Kamala Diversion
		if i < (Tmonth * 7):
			ub[i] = (Ko_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Saptakoshi
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Saptakoshi
		if i < (Tmonth * 6):
			ub[i] = (S_MD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Marine Diversion
			lb[i] = Dmd_MD[0]  # lowerbounds for Sunkoshi Marine Diversion
		if i < (Tmonth * 5):
			ub[i] = (Dt_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		if i < (Tmonth * 4):
			ub[i] = (SK_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi Sunkoshi powerhouse
			lb[i] = 0  # bonds for Dudhkoshi Sunkoshi powerhouse
		if i < (Tmonth * 3):
			ub[i] = (S1_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-1
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-1
		if i < (Tmonth * 2):
			ub[i] = (S2_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
		if i < Tmonth:
			ub[i] = (S3_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
	elif i % 12 == 1:
		month = "Feb"
		ub[i] = (S_KD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Kamala Diversion
		lb[i] = Dmd_KD[1]  # lowerbounds for Sunkoshi Marine Diversion
		if i < (Tmonth * 7):
			ub[i] = (Ko_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Saptakoshi
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Saptakoshi
		if i < (Tmonth * 6):
			ub[i] = (S_MD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Marine Diversion
			lb[i] = Dmd_MD[1]  # lowerbounds for Sunkoshi Marine Diversion
		if i < (Tmonth * 5):
			ub[i] = (Dt_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		if i < (Tmonth * 4):
			ub[i] = (SK_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi Sunkoshi powerhouse
			lb[i] = 0  # bonds for Dudhkoshi Sunkoshi powerhouse
		if i < (Tmonth * 3):
			ub[i] = (S1_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-1
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-1
		if i < (Tmonth * 2):
			ub[i] = (S2_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
		if i < Tmonth:
			ub[i] = (S3_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
	elif i % 12 == 2:
		month = "Mar"
		ub[i] = (S_KD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Kamala Diversion
		lb[i] = Dmd_KD[2]  # lowerbounds for Sunkoshi Marine Diversion
		if i < (Tmonth * 7):
			ub[i] = (Ko_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Saptakoshi
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Saptakoshi
		if i < (Tmonth * 6):
			ub[i] = (S_MD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Marine Diversion
			lb[i] = Dmd_MD[2]  # lowerbounds for Sunkoshi Marine Diversion
		if i < (Tmonth * 5):
			ub[i] = (Dt_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		if i < (Tmonth * 4):
			ub[i] = (SK_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi Sunkoshi powerhouse
			lb[i] = 0  # bonds for Dudhkoshi Sunkoshi powerhouse
		if i < (Tmonth * 3):
			ub[i] = (S1_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-1
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-1
		if i < (Tmonth * 2):
			ub[i] = (S2_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
		if i < Tmonth:
			ub[i] = (S3_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
	elif i % 12 == 3:
		month = "Apr"
		ub[i] = (S_KD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Kamala Diversion
		lb[i] = Dmd_KD[3]  # lowerbounds for Sunkoshi Marine Diversion
		if i < (Tmonth * 7):
			ub[i] = (Ko_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Saptakoshi
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Saptakoshi
		if i < (Tmonth * 6):
			ub[i] = (S_MD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Marine Diversion
			lb[i] = Dmd_MD[3]  # lowerbounds for Sunkoshi Marine Diversion
		if i < (Tmonth * 5):
			ub[i] = (Dt_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		if i < (Tmonth * 4):
			ub[i] = (SK_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi Sunkoshi powerhouse
			lb[i] = 0  # bonds for Dudhkoshi Sunkoshi powerhouse
		if i < (Tmonth * 3):
			ub[i] = (S1_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-1
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-1
		if i < (Tmonth * 2):
			ub[i] = (S2_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
		if i < Tmonth:
			ub[i] = (S3_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
	elif i % 12 == 4:
		month = "May"
		ub[i] = (S_KD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Kamala Diversion
		lb[i] = Dmd_KD[4]  # lowerbounds for Sunkoshi Marine Diversion
		if i < (Tmonth * 7):
			ub[i] = (Ko_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Saptakoshi
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Saptakoshi
		if i < (Tmonth * 6):
			ub[i] = (S_MD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Marine Diversion
			lb[i] = Dmd_MD[4]  # lowerbounds for Sunkoshi Marine Diversion
		if i < (Tmonth * 5):
			ub[i] = (Dt_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		if i < (Tmonth * 4):
			ub[i] = (SK_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi Sunkoshi powerhouse
			lb[i] = 0  # bonds for Dudhkoshi Sunkoshi powerhouse
		if i < (Tmonth * 3):
			ub[i] = (S1_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-1
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-1
		if i < (Tmonth * 2):
			ub[i] = (S2_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
		if i < Tmonth:
			ub[i] = (S3_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
	elif i % 12 == 5:
		month = "Jun"
		ub[i] = (S_KD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Kamala Diversion
		lb[i] = Dmd_KD[5]  # lowerbounds for Sunkoshi Marine Diversion
		if i < (Tmonth * 7):
			ub[i] = (Ko_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Saptakoshi
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Saptakoshi
		if i < (Tmonth * 6):
			ub[i] = (S_MD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Marine Diversion
			lb[i] = Dmd_MD[5]  # lowerbounds for Sunkoshi Marine Diversion
		if i < (Tmonth * 5):
			ub[i] = (Dt_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		if i < (Tmonth * 4):
			ub[i] = (SK_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi Sunkoshi powerhouse
			lb[i] = 0  # bonds for Dudhkoshi Sunkoshi powerhouse
		if i < (Tmonth * 3):
			ub[i] = (S1_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-1
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-1
		if i < (Tmonth * 2):
			ub[i] = (S2_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
		if i < Tmonth:
			ub[i] = (S3_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
	elif i % 12 == 6:
		month = "Jul"
		ub[i] = (S_KD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Kamala Diversion
		lb[i] = Dmd_KD[6]  # lowerbounds for Sunkoshi Marine Diversion
		if i < (Tmonth * 7):
			ub[i] = (Ko_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Saptakoshi
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Saptakoshi
		if i < (Tmonth * 6):
			ub[i] = (S_MD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Marine Diversion
			lb[i] = Dmd_MD[6]  # lowerbounds for Sunkoshi Marine Diversion
		if i < (Tmonth * 5):
			ub[i] = (Dt_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		if i < (Tmonth * 4):
			ub[i] = (SK_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi Sunkoshi powerhouse
			lb[i] = 0  # bonds for Dudhkoshi Sunkoshi powerhouse
		if i < (Tmonth * 3):
			ub[i] = (S1_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-1
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-1
		if i < (Tmonth * 2):
			ub[i] = (S2_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
		if i < Tmonth:
			ub[i] = (S3_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
	elif i % 12 == 7:
		month = "Aug"
		ub[i] = (S_KD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Kamala Diversion
		lb[i] = Dmd_KD[7]  # lowerbounds for Sunkoshi Marine Diversion
		if i < (Tmonth * 7):
			ub[i] = (Ko_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Saptakoshi
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Saptakoshi
		if i < (Tmonth * 6):
			ub[i] = (S_MD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Marine Diversion
			lb[i] = Dmd_MD[7]  # lowerbounds for Sunkoshi Marine Diversion
		if i < (Tmonth * 5):
			ub[i] = (Dt_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		if i < (Tmonth * 4):
			ub[i] = (SK_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi Sunkoshi powerhouse
			lb[i] = 0  # bonds for Dudhkoshi Sunkoshi powerhouse
		if i < (Tmonth * 3):
			ub[i] = (S1_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-1
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-1
		if i < (Tmonth * 2):
			ub[i] = (S2_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
		if i < Tmonth:
			ub[i] = (S3_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
	elif i % 12 == 8:
		month = "Sep"
		ub[i] = (S_KD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Kamala Diversion
		lb[i] = Dmd_KD[8]  # lowerbounds for Sunkoshi Marine Diversion
		if i < (Tmonth * 7):
			ub[i] = (Ko_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Saptakoshi
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Saptakoshi
		if i < (Tmonth * 6):
			ub[i] = (S_MD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Marine Diversion
			lb[i] = Dmd_MD[8]  # lowerbounds for Sunkoshi Marine Diversion
		if i < (Tmonth * 5):
			ub[i] = (Dt_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		if i < (Tmonth * 4):
			ub[i] = (SK_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi Sunkoshi powerhouse
			lb[i] = 0  # bonds for Dudhkoshi Sunkoshi powerhouse
		if i < (Tmonth * 3):
			ub[i] = (S1_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-1
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-1
		if i < (Tmonth * 2):
			ub[i] = (S2_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
		if i < Tmonth:
			ub[i] = (S3_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
	elif i % 12 == 9:
		month = "Oct"
		ub[i] = (S_KD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Kamala Diversion
		lb[i] = Dmd_KD[9]  # lowerbounds for Sunkoshi Marine Diversion
		if i < (Tmonth * 7):
			ub[i] = (Ko_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Saptakoshi
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Saptakoshi
		if i < (Tmonth * 6):
			ub[i] = (S_MD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Marine Diversion
			lb[i] = Dmd_MD[9]  # lowerbounds for Sunkoshi Marine Diversion
		if i < (Tmonth * 5):
			ub[i] = (Dt_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		if i < (Tmonth * 4):
			ub[i] = (SK_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi Sunkoshi powerhouse
			lb[i] = 0  # bonds for Dudhkoshi Sunkoshi powerhouse
		if i < (Tmonth * 3):
			ub[i] = (S1_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-1
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-1
		if i < (Tmonth * 2):
			ub[i] = (S2_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
		if i < Tmonth:
			ub[i] = (S3_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
	elif i % 12 == 10:
		month = "Nov"
		ub[i] = (S_KD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Kamala Diversion
		lb[i] = Dmd_KD[10]  # lowerbounds for Sunkoshi Marine Diversion
		if i < (Tmonth * 7):
			ub[i] = (Ko_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Saptakoshi
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Saptakoshi
		if i < (Tmonth * 6):
			ub[i] = (S_MD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Marine Diversion
			lb[i] = Dmd_MD[10]  # lowerbounds for Sunkoshi Marine Diversion
		if i < (Tmonth * 5):
			ub[i] = (Dt_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		if i < (Tmonth * 4):
			ub[i] = (SK_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi Sunkoshi powerhouse
			lb[i] = 0  # bonds for Dudhkoshi Sunkoshi powerhouse
		if i < (Tmonth * 3):
			ub[i] = (S1_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-1
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-1
		if i < (Tmonth * 2):
			ub[i] = (S2_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
		if i < Tmonth:
			ub[i] = (S3_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
	elif i % 12 == 11:
		month = "Dec"
		ub[i] = (S_KD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Kamala Diversion
		lb[i] = Dmd_KD[11]  # lowerbounds for Sunkoshi Marine Diversion
		if i < (Tmonth * 7):
			ub[i] = (Ko_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Saptakoshi
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Saptakoshi
		if i < (Tmonth * 6):
			ub[i] = (S_MD_Max_discharge * Days[j] * 24 * 3600) / 10 ** 6  # upperbounds for Sunkoshi Marine Diversion
			lb[i] = Dmd_MD[11]  # lowerbounds for Sunkoshi Marine Diversion
		if i < (Tmonth * 5):
			ub[i] = (Dt_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi dam toe powerhouse
		if i < (Tmonth * 4):
			ub[i] = (SK_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Dudhkoshi Sunkoshi powerhouse
			lb[i] = 0  # bonds for Dudhkoshi Sunkoshi powerhouse
		if i < (Tmonth * 3):
			ub[i] = (S1_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-1
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-1
		if i < (Tmonth * 2):
			ub[i] = (S2_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-2
		if i < Tmonth:
			ub[i] = (S3_rated_discharge * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
			lb[i] = (MDR * Days[j] * 24 * 3600) / 10 ** 6  # bonds for Sunkoshi-3
	j = j + 1

"""
  Objective function
  ===================

  The algorithm Swarm searches for minimum value value so objective function is multiplied by -1

  From T_O_V optimized values
  ---------------------------
    Values that are indexed in range [0-Tmonth] are stored in R3 
    Values that are indexed in range [Tmonth-2*Tmonth] are stored in R2
    Values that are indexed in range [2*Tmonth-3*Tmonth] are stored in R1
    Values that are indexed in range [3*Tmonth-4*Tmonth] are stored in R_sk
    Values that are indexed in range [4*Tmonth-5*Tmonth] are stored in R_dt
    Values that are indexed in range [5*Tmonth-6*Tmonth] are stored in R_MD
    Values that are indexed in range [6*Tmonth-7*Tmonth] are stored in R_Ko
    Values that are indexed in range [7*Tmonth-8*Tmonth] are stored in R_KD

  Here the value of releases are in MCM per month.
  Fitness function gives the total amount energy potential that can be generated when input parameters and optimized released are used as operation policy.

"""


# objective function maximizing power production
def fitness(x):
	F = 0
	H3 = Height3(x)  # Calling function Height3(x) for sunkoshi 3 it returns storage water level - turbine level i.e. head for energy generation.
	H2 = Height2(x)
	H_dt = Height_dt(x)
	H_sk = Height_sk(x)
	H1 = Height1(x)
	H_Ko = Height_Ko(x)
	R3 = (x[:Tmonth] * 10 ** 6) / (Days * 24 * 3600)
	R2 = (x[Tmonth:Tmonth * 2] * 10 ** 6) / (Days * 24 * 3600)
	R1 = (x[Tmonth * 2:Tmonth * 3] * 10 ** 6) / (Days * 24 * 3600)
	R_sk = (x[Tmonth * 3:Tmonth * 4] * 10 ** 6) / (Days * 24 * 3600)
	R_dt = (x[Tmonth * 4:Tmonth * 5] * 10 ** 6) / (Days * 24 * 3600)
	R_MD = (x[Tmonth * 5:Tmonth * 6] * 10 ** 6) / (Days * 24 * 3600)
	R_Ko = (x[Tmonth * 6:Tmonth * 7] * 10 ** 6) / (Days * 24 * 3600)
	R_KD = (x[Tmonth * 7:Tmonth * 8] * 10 ** 6) / (Days * 24 * 3600)
	for i in range(Tmonth):
		z3 = (1 - (g * ita_S3 * R3[i] * H3[i]) / (1000 * power3))
		z2 = (1 - (g * ita_S2 * R2[i] * H2[i]) / (1000 * power2))
		z1 = (1 - (g * ita_S1 * R1[i] * H1[i]) / (1000 * power1))
		z4 = (1 - (g * ita_Ko * R_Ko[i] * H_Ko[i]) / (1000 * power_Ko))
		zd = (1 - (g * ita_sk * R_sk[i] * H_sk[i]) / (1000 * power_sk)) + (1 - (g * ita_dt * R_dt[i] * H_dt[i]) / (1000 * power_dt))
		zk = (1 - (g * ita_MD * R_MD[i] * H_MD) / (1000 * power_MD))
		zm = (1 - (g * ita_KD * R_KD[i] * H_KD) / (1000 * power_KD))
		F = F + z1 + z2 + z3 + zd + zm + z4 + zk
	return F / (Ovariables * Tmonth)


"""
  Minimum Dry Energy 
  ===================
  In this function the out put of PSO is introduced to output percentage of Dry energy for each year which is used below in mycons function to check for feasible solutions.

"""


def Dry_energy_checkA(x, c="v"):  # Annual dry energy check
	z_dry = 0
	z_wet = 0
	ita = 0
	H = np.zeros(Tmonth)
	R = np.zeros(Tmonth)
	H3 = Height3(x)
	H2 = Height2(x)
	H_sk = Height_sk(x)
	H_dt = Height_dt(x)
	H1 = Height1(x)
	H_Ko = Height_Ko(x)
	dry_percentA = np.zeros(int(Tmonth / 12))
	R3 = (x[:Tmonth] * 10 ** 6) / (Days * 24 * 3600)
	R2 = (x[Tmonth:Tmonth * 2] * 10 ** 6) / (Days * 24 * 3600)
	R1 = (x[Tmonth * 2:Tmonth * 3] * 10 ** 6) / (Days * 24 * 3600)
	R_sk = (x[Tmonth * 3:Tmonth * 4] * 10 ** 6) / (Days * 24 * 3600)
	R_dt = (x[Tmonth * 4:Tmonth * 5] * 10 ** 6) / (Days * 24 * 3600)
	R_MD = (x[Tmonth * 5:Tmonth * 6] * 10 ** 6) / (Days * 24 * 3600)
	R_Ko = (x[Tmonth * 6:Tmonth * 7] * 10 ** 6) / (Days * 24 * 3600)
	R_KD = (x[Tmonth * 7:Tmonth * 8] * 10 ** 6) / (Days * 24 * 3600)
	if c == 'S3':
		R = R3
		ita = ita_S3
		H = H3
	if c == 'S2':
		R = R2
		ita = ita_S2
		H = H2
	if c == 'sk':
		R = R_sk
		ita = ita_sk
		H = H_sk
	if c == 'dt':
		R = R_dt
		ita = ita_dt
		H = H_dt
	if c == 'S1':
		R = R1
		ita = ita_S1
		H = H1
	if c == 'MD':
		R = R_MD
		ita = ita_MD
		H = H + H_MD
	if c == 'Ko':
		R = R_Ko
		ita = ita_Ko
		H = H_Ko
	if c == 'KD':
		R = R_KD
		ita = ita_KD
		H = H + H_KD
	j = 0
	for i in range(Tmonth):
		if i % 12 == 0 or i % 12 == 1 or i % 12 == 2 or i % 12 == 3 or i % 12 == 4 or i % 12 == 11:
			z_dry += (g * ita * R[i] * H[i] / 1000)
			if i % 12 == 11:
				dry_percentA[j] = dry_energy(z_dry, z_wet)
				j = j + 1
				z_dry = 0
				z_wet = 0
		elif i % 12 == 5 or i % 12 == 6 or i % 12 == 7 or i % 12 == 8 or i % 12 == 9 or i % 12 == 10:
			z_wet += (g * ita * R[i] * H[i] / 1000)
	return dry_percentA


def Dry_energy_checkT(x, c="v"):  # Total dry energy check
	z_dry = 0
	z_wet = 0
	ita = 0
	H = np.zeros(Tmonth)
	R = np.zeros(Tmonth)
	H3 = Height3(x)
	H2 = Height2(x)
	H_sk = Height_sk(x)
	H_dt = Height_dt(x)
	H1 = Height1(x)
	H_Ko = Height_Ko(x)
	dry_percentA = np.zeros(int(Tmonth / 12))
	R3 = (x[:Tmonth] * 10 ** 6) / (Days * 24 * 3600)
	R2 = (x[Tmonth:Tmonth * 2] * 10 ** 6) / (Days * 24 * 3600)
	R1 = (x[Tmonth * 2:Tmonth * 3] * 10 ** 6) / (Days * 24 * 3600)
	R_sk = (x[Tmonth * 3:Tmonth * 4] * 10 ** 6) / (Days * 24 * 3600)
	R_dt = (x[Tmonth * 4:Tmonth * 5] * 10 ** 6) / (Days * 24 * 3600)
	R_MD = (x[Tmonth * 5:Tmonth * 6] * 10 ** 6) / (Days * 24 * 3600)
	R_Ko = (x[Tmonth * 6:Tmonth * 7] * 10 ** 6) / (Days * 24 * 3600)
	R_KD = (x[Tmonth * 7:Tmonth * 8] * 10 ** 6) / (Days * 24 * 3600)
	if c == 'S3':
		R = R3
		ita = ita_S3
		H = H3
	if c == 'S2':
		R = R2
		ita = ita_S2
		H = H2
	if c == 'sk':
		R = R_sk
		ita = ita_sk
		H = H_sk
	if c == 'dt':
		R = R_dt
		ita = ita_dt
		H = H_dt
	if c == 'S1':
		R = R1
		ita = ita_S1
		H = H1
	if c == 'MD':
		R = R_MD
		ita = ita_MD
		H = H + H_MD
	if c == 'Ko':
		R = R_Ko
		ita = ita_Ko
		H = H_Ko
	if c == 'KD':
		R = R_KD
		ita = ita_KD
		H = H + H_KD
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
      S3(t) = I3(inflow) + S3(t-1)-{R3(t-1)(release from sunkoshi-3)-Evaporation at time t}

      For Sunkoshi-2 dam: 
      -------------------                                                                                                                        
      S2(t) = S2(t-1) + R3(t-1) + O3(t-1) + l2(t-1) - {Qm(t-1) + R2(t-1) + Ev2(t-1)}

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


# mass balance for sunkoshi 2
def Storage2(x):
	S2 = np.zeros(Tmonth + 1)
	O2 = np.zeros(Tmonth)
	O3 = Storage3(x)[1]
	ev2 = []
	S2[0] = S2max
	R3 = x[:Tmonth]
	R2 = x[Tmonth:Tmonth * 2]
	R_MD = x[5 * Tmonth:Tmonth * 6]
	j = 0
	for i in range(Tmonth):
		Ev2 = Evaporation2(S2[i], j, i)
		ev2.append(Ev2)
		S2[i + 1] = S2[i] + R3[i] + O3[i] + l2[i] - (R2[i] + R_MD[i] + Ev2 + O2[i])
		if S2[i + 1] < S2min:
			R_MD[i] = lb[i + 5 * Tmonth]
			R2[i] = np.random.rand() * (S2[i] + R3[i] + O3[i] + l2[i] - R_MD[i] - Ev2 - S2min - O2[i])
			S2[i + 1] = S2[i] + R3[i] + O3[i] + l2[i] - (R2[i] + R_MD[i] + Ev2 + O2[i])
			if R2[i] < 0:
				R2[i] = 0
				R_MD[i] = 0.98 * (S2[i] + R3[i] + O3[i] + l2[i] - R2[i] - Ev2 - S2min - O2[i])
				S2[i + 1] = S2[i] + R3[i] + O3[i] + l2[i] - (R2[i] + R_MD[i] + Ev2 + O2[i])
		else:
			S2[i + 1] = S2[i] + R3[i] + O3[i] + l2[i] - (R2[i] + R_MD[i] + Ev2 + O2[i])
		if S2[i + 1] > S2max:
			if R2[i] < ub[i + Tmonth]:
				R2[i] = R2[i] + S2[i + 1] - S2max
				if R2[i] > ub[i + Tmonth]:
					O2[i] = R2[i] - ub[i + Tmonth]
					R2[i] = ub[i + Tmonth]
			else:
				O2[i] = S2[i] + R3[i] + O3[i] + l2[i] - (R2[i] + R_MD[i] + Ev2) - S2max
			S2[i + 1] = S2[i] + R3[i] + O3[i] + l2[i] - (R2[i] + R_MD[i] + Ev2 + O2[i])
		else:
			S2[i + 1] = S2[i] + R3[i] + O3[i] + l2[i] - (R2[i] + R_MD[i] + Ev2 + O2[i])
		j += 1
		if j == 12:
			j = 0
	return S2, O2, ev2


# mass balance for Dudhkoshi
def Storaged(x):
	Sd = np.zeros(Tmonth + 1)
	Od = np.zeros(Tmonth)  # initial overflow all values are zero
	evd = []
	Sd[0] = Sdmax
	R_sk = x[3 * Tmonth:4 * Tmonth]
	R_dt = x[4 * Tmonth:5 * Tmonth]
	j = 0
	for i in range(Tmonth):
		Evd = Evaporationd(Sd[i], j, i)
		evd.append(Evd)
		Sd[i + 1] = Dk[i] + Sd[i] - (R_dt[i] + R_sk[i] + Evd + Od[i])
		if Sd[i + 1] < Sdmin:
			R_dt[i] = lb[i + 4 * Tmonth]
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


# mass balance for sunkoshi 1
def Storage1(x):
	S1 = np.zeros(Tmonth + 1)
	O1 = np.zeros(Tmonth)  # initial overflow all values are zero
	O2 = Storage2(x)[1]
	Od = Storaged(x)[1]
	ev1 = []
	S1[0] = S1max
	R1 = x[2 * Tmonth:3 * Tmonth]
	R_dt = x[4 * Tmonth:5 * Tmonth]
	R2 = x[Tmonth:Tmonth * 2]
	j = 0
	for i in range(Tmonth):
		Ev1 = Evaporation1(S1[i], j, i)
		ev1.append(Ev1)
		S1[i + 1] = l1_[i] + S1[i] + R2[i] + O2[i] + R_dt[i] + Od[i] - (R1[i] + Ev1 + O1[i])
		if S1[i + 1] < S1min:
			R1[i] = np.random.rand() * (l1_[i] + S1[i] + R2[i] + O2[i] + R_dt[i] + Od[i] - Ev1 - O1[i] - S1min)
			S1[i + 1] = l1_[i] + S1[i] + R2[i] + O2[i] + R_dt[i] + Od[i] - (R1[i] + Ev1 + O1[i])
		else:
			S1[i + 1] = l1_[i] + S1[i] + R2[i] + O2[i] + R_dt[i] + Od[i] - (R1[i] + Ev1 + O1[i])
		if S1[i + 1] > S1max:
			if R1[i] < ub[i + 2 * Tmonth]:
				R1[i] = R1[i] + S1[i + 1] - S1max
				if R1[i] > ub[i + 2 * Tmonth]:
					O1[i] = x[i + 2 * Tmonth] - ub[i + 2 * Tmonth]
					R1[i] = ub[i + 2 * Tmonth]
			else:
				O1[i] = l1_[i] + S1[i] + R2[i] + O2[i] + R_dt[i] + Od[i] - (R1[i] + Ev1) - S1max
			S1[i + 1] = l1_[i] + S1[i] + R2[i] + O2[i] + R_dt[i] + Od[i] - (R1[i] + Ev1 + O1[i])
		else:
			S1[i + 1] = l1_[i] + S1[i] + R2[i] + O2[i] + R_dt[i] + Od[i] - (R1[i] + Ev1 + O1[i])
		j += 1
		if j == 12:
			j = 0
	return S1, O1, ev1


# mass balance for sunkoshi 2
def Storage_Ko(x):
	S_Ko = np.zeros(Tmonth + 1)
	O_Ko = np.zeros(Tmonth)
	O1 = Storage1(x)[1]
	evKo = []
	S_Ko[0] = S_Ko_max
	R1 = x[2 * Tmonth:3 * Tmonth]
	R_sk = x[Tmonth * 3:Tmonth * 4]
	R_Ko = x[Tmonth * 6:Tmonth * 7]
	R_KD = x[Tmonth * 7:Tmonth * 8]
	j = 0
	for i in range(Tmonth):
		Ev_Ko = EvaporationKo(S_Ko[i], j, i)
		evKo.append(Ev_Ko)
		S_Ko[i + 1] = S_Ko[i] + R1[i] + R_sk[i] + O1[i] + l_Ko[i] - (R_Ko[i] + R_KD[i] + Ev_Ko + O_Ko[i])
		if S_Ko[i + 1] < S_Ko_min:
			R_KD[i] = lb[i + 7 * Tmonth]
			R_Ko[i] = np.random.rand() * (S_Ko[i] + R1[i] + R_sk[i] + O1[i] + l_Ko[i] - (R_KD[i] + Ev_Ko + O_Ko[i] + S_Ko_min))
			S_Ko[i + 1] = S_Ko[i] + R1[i] + R_sk[i] + O1[i] + l_Ko[i] - (R_Ko[i] + R_KD[i] + Ev_Ko + O_Ko[i])
			if R_Ko[i] < 0:
				R_Ko[i] = 0
				R_KD[i] = 0.98 * (S_Ko[i] + R1[i] + R_sk[i] + O1[i] + l_Ko[i] - (R_Ko[i] + Ev_Ko + O_Ko[i] + S_Ko_min))
				S_Ko[i + 1] = S_Ko[i] + R1[i] + R_sk[i] + O1[i] + l_Ko[i] - (R_Ko[i] + R_KD[i] + Ev_Ko + O_Ko[i])
		else:
			S_Ko[i + 1] = S_Ko[i] + R1[i] + R_sk[i] + O1[i] + l_Ko[i] - (R_Ko[i] + R_KD[i] + Ev_Ko + O_Ko[i])
		if S_Ko[i + 1] > S_Ko_max:
			if R_Ko[i] < ub[i + 6 * Tmonth]:
				R_Ko[i] = R_Ko[i] + S_Ko[i + 1] - S_Ko_max
				if R_Ko[i] > ub[i + 6 * Tmonth]:
					O_Ko[i] = R_Ko[i] - ub[i + 6 * Tmonth]
					R_Ko[i] = ub[i + 6 * Tmonth]
			else:
				O_Ko[i] = S_Ko[i] + R1[i] + R_sk[i] + O1[i] + l_Ko[i] - (R_Ko[i] + R_KD[i] + Ev_Ko) - S_Ko_max
			S_Ko[i + 1] = S_Ko[i] + R1[i] + R_sk[i] + O1[i] + l_Ko[i] - (R_Ko[i] + R_KD[i] + Ev_Ko + O_Ko[i])
		else:
			S_Ko[i + 1] = S_Ko[i] + R1[i] + R_sk[i] + O1[i] + l_Ko[i] - (R_Ko[i] + R_KD[i] + Ev_Ko + O_Ko[i])
		j += 1
		if j == 12:
			j = 0
	return S_Ko, O_Ko, evKo


"""
  Energy
  =======
   Energy = P * release * Net head
"""


# Energy output per month for Sunkoshi 3
def E3(x):  # Calculates energy GWH for each months
	e3 = np.zeros(Tmonth)
	H3 = Height3(x)
	R3 = (x[:Tmonth] * 10 ** 6) / (Days * 24 * 3600)
	for i in range(Tmonth):
		e3[i] = g * ita_S3 * R3[i] * H3[i] / 1000
	return e3


# Energy output per month for Sunkoshi 2
def E2(x):  # Calculates energy GWH for each months
	e2 = np.zeros(Tmonth)
	H2 = Height2(x)
	R2 = (x[Tmonth:Tmonth * 2] * 10 ** 6) / (Days * 24 * 3600)
	for i in range(Tmonth):
		e2[i] = g * ita_S2 * R2[i] * H2[i] / 1000
	return e2


# Energy output per month for Sunkoshi 1
def E1(x):
	e1 = np.zeros(Tmonth)
	H1 = Height1(x)
	R1 = (x[2 * Tmonth:Tmonth * 3] * 10 ** 6) / (Days * 24 * 3600)
	for i in range(Tmonth):
		e1[i] = ((g * ita_S1 * R1[i] * H1[i] / 1000) * Days[i] * 24) / 1000
	return e1


# Energy output per month for Sunkoshi Marine Diversion
def E_MD(x):
	e_MD = np.zeros(Tmonth)
	R_MD = (x[5 * Tmonth:Tmonth * 6] * 10 ** 6) / (Days * 24 * 3600)
	for i in range(Tmonth):
		e_MD[i] = g * ita_MD * R_MD[i] * H_MD / 1000
	return e_MD


# Energy output per month for Dudhkoshi
#  Dam toe Powerhouse
def E_dt(x):
	e_dt = np.zeros(Tmonth)
	H_dt = Height_dt(x)
	R_dt = (x[4 * Tmonth:Tmonth * 5] * 10 ** 6) / (Days * 24 * 3600)
	for i in range(Tmonth):
		e_dt[i] = g * ita_dt * R_dt[i] * H_dt[i] / 1000
	return e_dt


#  Sunkoshi Powerhouse
def E_sk(x):
	e_sk = np.zeros(Tmonth)
	H_sk = Height_sk(x)
	R_sk = (x[3 * Tmonth:Tmonth * 4] * 10 ** 6) / (Days * 24 * 3600)
	for i in range(Tmonth):
		e_sk[i] = g * ita_sk * R_sk[i] * H_sk[i] / 1000
	return e_sk


# Energy output per month for Sapta koshi
def E_Ko(x):
	e_Ko = np.zeros(Tmonth)
	H_Ko = Height_Ko(x)
	R_Ko = (x[6 * Tmonth:Tmonth * 7] * 10 ** 6) / (Days * 24 * 3600)
	for i in range(Tmonth):
		e_Ko[i] = ((g * ita_Ko * R_Ko[i] * H_Ko[i] / 1000) * Days[i] * 24) / 1000
	return e_Ko


# Energy output per month for Sunkoshi Marine Diversion
def E_KD(x):
	e_KD = np.zeros(Tmonth)
	R_KD = (x[7 * Tmonth:Tmonth * 8] * 10 ** 6) / (Days * 24 * 3600)
	for i in range(Tmonth):
		e_KD[i] = g * ita_KD * R_KD[i] * H_KD / 1000
	return e_KD


"""
  Height
  =======
   Height function H=f(storage)
   Obtained from H-V-A curve
"""


# Height for Sunkoshi-3
def Height3(x):
	H3 = np.zeros(Tmonth)
	S3 = Storage3(x)[0]
	for i in range(Tmonth):
		H3[i] = Interpolate(Ex3, (S3[i] + S3[i + 1]) / 2, c='Elev')
		H3[i] = H3[i] - S3_effective_twl
	return H3


# Height for Sunkoshi-2
def Height2(x):
	H2 = np.zeros(Tmonth)
	S2 = Storage2(x)[0]
	for i in range(Tmonth):
		H2[i] = Interpolate(Ex2, (S2[i] + S2[i + 1]) / 2, c='Elev')
		H2[i] = H2[i] - S2_effective_twl
	return H2


# Height for Sunkoshi-1
def Height1(x):
	H1 = np.zeros(Tmonth)
	S1 = Storage1(x)[0]
	for i in range(Tmonth):
		H1[i] = Interpolate(Ex1, (S1[i] + S1[i + 1]) / 2, c='Elev')
		H1[i] = H1[i] - S1_effective_twl
	return H1


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


# Height for Sunkoshi-1
def Height_Ko(x):
	H_Ko = np.zeros(Tmonth)
	S_Ko = Storage_Ko(x)[0]
	for i in range(Tmonth):
		H_Ko[i] = Interpolate(Ex_Ko, (S_Ko[i] + S_Ko[i + 1]) / 2, c='Elev')
		H_Ko[i] = H_Ko[i] - Ko_effective_twl
	return H_Ko


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


def Evaporation3(a, b, d):  # Returns potential evaporation for each months its unit is MCM
	S3a = Interpolate(Ex3, a, c='SArea')
	Eva = (ev[b] * S3a) * Days[d] / 10 ** 9
	return Eva


def Evaporation2(a, b, d):  # Returns potential evaporation for each months its unit is MCM
	S2a = Interpolate(Ex2, a, c='SArea')
	Eva = (ev[b] * S2a) * Days[d] / 10 ** 9
	return Eva


def Evaporation1(a, b, d):
	S1a = Interpolate(Ex1, a, c='SArea')
	Eva = (ev[b] * S1a) * Days[d] / 10 ** 9
	return Eva


def Evaporationd(a, b, d):
	Dka = Interpolate(Exd, a, c='SArea')
	Evd = (ev[b] * Dka) * Days[d] / 10 ** 9
	return Evd


def EvaporationKo(a, b, d):
	Koa = Interpolate(Ex_Ko, a, c='SArea')
	Ev_Ko = (ev[b] * Koa) * Days[d] / 10 ** 9
	return Ev_Ko


"""                          
  Constrains
  ===========
   Since constrain for storage is addressed in storage function it is no longer need to address here.
   Here Constrain for maximum energy is checked.
   constrains for irrigation demand can be addressed in [ld - ub] section.

"""


# all constrains required
# all constrains required
def mycons(x):
	# dry_percent = Dry_energy_check(x)
	cons = []
	return cons


# calling pso function in pso.py
xopt, fopt, iter_vs_swamp_vs_fitness, iter_vs_globalbest = pso(fitness, lb, ub, f_ieqcons=mycons, swarmsize=swarmsize, wmax=wmax, wmin=wmin, c1=C1, c2=C2, X=X, maxiter=maxiter, minstep=minstep, minfunc=minfunc, debug=False)

"""
  Printing and Saving Outputs
  ============================

"""
print('Optimal fitness function value:')
print('    myfunc: {}'.format(fopt))

print('The optimum releases for each stations and other outputs can be found in excel file generated:')

Release_Sunkoshi_1 = xopt[2 * Tmonth:Tmonth * 3]
Release_Sunkoshi_2 = xopt[Tmonth:Tmonth * 2]
Release_Sunkoshi_3 = xopt[:Tmonth]
Release_Sunkoshi_MD = xopt[5 * Tmonth:Tmonth * 6]
Release_Dudhkoshi_sk = xopt[3 * Tmonth:Tmonth * 4]
Release_Dudhkoshi_dt = xopt[4 * Tmonth:Tmonth * 5]
Release_Saptakoshi = xopt[6 * Tmonth:Tmonth * 7]
Release_Sunkoshi_KD = xopt[7 * Tmonth:Tmonth * 8]

Storage_for_S3, Overflow_for_S3, Evaporation_loss_S3 = Storage3(xopt)
Storage_for_S3 = Storage_for_S3[:-1]
Storage_for_S2, Overflow_for_S2, Evaporation_loss_S2 = Storage2(xopt)
Storage_for_S2 = Storage_for_S2[:-1]
Storage_for_DK, Overflow_for_DK, Evaporation_loss_Dk = Storaged(xopt)
Storage_for_DK = Storage_for_DK[:-1]
Storage_for_S1, Overflow_for_S1, Evaporation_loss_S1 = Storage1(xopt)
Storage_for_S1 = Storage_for_S1[:-1]
Storage_for_Ko, Overflow_for_Ko, Evaporation_loss_Ko = Storage_Ko(xopt)
Storage_for_Ko = Storage_for_Ko[:-1]

Storage_Sunkoshi_1 = Storage_for_S1
Storage_Sunkoshi_2 = Storage_for_S2
Storage_Sunkoshi_3 = Storage_for_S3
Storage_Dudhkoshi = Storage_for_DK
Storage_Saptakoshi = Storage_for_Ko

Overflow_Sunkoshi_1 = Overflow_for_S1
Overflow_Sunkoshi_2 = Overflow_for_S2
Overflow_Sunkoshi_3 = Overflow_for_S3
Overflow_Dudhkoshi = Overflow_for_DK
Overflow_Saptakoshi = Overflow_for_Ko

Dry_energy_percent_for_S3_total = Dry_energy_checkT(xopt, c='S3')
Dry_energy_percent_for_S2_total = Dry_energy_checkT(xopt, c='S2')
Dry_energy_percent_for_S1_total = Dry_energy_checkT(xopt, c='S1')
Dry_energy_percent_for_sk_total = Dry_energy_checkT(xopt, c='sk')
Dry_energy_percent_for_dt_total = Dry_energy_checkT(xopt, c='dt')
Dry_energy_percent_for_MD_total = Dry_energy_checkT(xopt, c='MD')
Dry_energy_percent_for_Ko_total = Dry_energy_checkT(xopt, c='Ko')
Dry_energy_percent_for_KD_total = Dry_energy_checkT(xopt, c='KD')

Dry_energy_percent_for_S3_Annually = Dry_energy_checkA(xopt, c='S3')
Dry_energy_percent_for_S2_Annually = Dry_energy_checkA(xopt, c='S2')
Dry_energy_percent_for_S1_Annually = Dry_energy_checkA(xopt, c='S1')
Dry_energy_percent_for_sk_Annually = Dry_energy_checkA(xopt, c='sk')
Dry_energy_percent_for_dt_Annually = Dry_energy_checkA(xopt, c='dt')
Dry_energy_percent_for_MD_Annually = Dry_energy_checkA(xopt, c='MD')
Dry_energy_percent_for_Ko_Annually = Dry_energy_checkA(xopt, c='Ko')
Dry_energy_percent_for_KD_Annually = Dry_energy_checkA(xopt, c='KD')

Energy_Sunkoshi_3 = E3(xopt)
Energy_Sunkoshi_2 = E2(xopt)
Energy_Sunkoshi_1 = E1(xopt)
Energy_Dudhkoshi_sk = E_sk(xopt)
Energy_Dudhkoshi_dt = E_dt(xopt)
Energy_Sunkoshi_MD = E_MD(xopt)
Energy_Saptakoshi = E_Ko(xopt)
Energy_Sunkoshi_KD = E_KD(xopt)

Fitness_value = fopt

Inputs = ['swarmsize', 'wmax', 'wmin', 'C1', 'C2', 'X', 'maxiter', 'minstep', 'minfunc', 'Fitness_value', 'Dry_energy percent Total for S3', 'Dry_energy percent Total for S2', 'Dry_energy percent Total for S1', 'Dry_energy percent Total for SK PH', 'Dry_energy percent Total for DT PH', 'Dry_energy percent Total for MD', 'Dry_energy percent Total for Ko', 'Dry_energy percent Total for KD']

'''
 Writing to Excel
 =================
 Here,writing the output obtained to excel file PSO_Outputs.xlsx
'''
PSO_Outputs = pd.ExcelWriter('All_2021-08-21.xlsx')

Parameters = pd.DataFrame()
Outputs = pd.DataFrame()
Storage = pd.DataFrame()
Release = pd.DataFrame()
Overflow = pd.DataFrame()
Energy = pd.DataFrame()
pso_data1 = pd.DataFrame(iter_vs_swamp_vs_fitness, columns=['Iteration', 'Swamp_Number', 'Fitness_Value'])
pso_data2 = pd.DataFrame(iter_vs_globalbest, columns=['Iteration', 'Global_best_fitness'])
Day_energy_percent_A = pd.DataFrame()
a = pd.to_datetime(Fyear, format='%Y')
c = Fyear + 1
b = pd.to_datetime(c, format='%Y')

Date = pd.date_range(start=a, end=b, freq='M').year.tolist()
Date1 = pd.date_range(start=a, end=b, freq='Y').year.tolist()
Month = pd.date_range(start=a, end=b, freq='M').month_name().tolist()

Parameters['Parameters'] = Inputs
Parameters['Values'] = [swarmsize, wmax, wmin, C1, C2, X, maxiter, minstep, minfunc, Fitness_value, Dry_energy_percent_for_S3_total, Dry_energy_percent_for_S2_total, Dry_energy_percent_for_S1_total, Dry_energy_percent_for_sk_total, Dry_energy_percent_for_dt_total, Dry_energy_percent_for_MD_total, Dry_energy_percent_for_Ko_total, Dry_energy_percent_for_KD_total]

Outputs['Date'] = Date
Outputs['Month'] = Month

Outputs['Inflows_for_S3'] = I3
Outputs['Release_Sunkoshi_3'] = Release_Sunkoshi_3
Outputs['Storage_Sunkoshi_3'] = Storage_Sunkoshi_3
Outputs['Overflow_Sunkoshi_3'] = Overflow_Sunkoshi_3
Outputs['Energy_Sunkoshi_3'] = Energy_Sunkoshi_3
Outputs["Evaporation_loss_S3"] = Evaporation_loss_S3

Outputs['Inflows_for_S2'] = l2
Outputs['Release_Sunkoshi_2'] = Release_Sunkoshi_2
Outputs['Storage_Sunkoshi_2'] = Storage_Sunkoshi_2
Outputs['Overflow_Sunkoshi_2'] = Overflow_Sunkoshi_2
Outputs['Energy_Sunkoshi_2'] = Energy_Sunkoshi_2
Outputs["Evaporation_loss_S2"] = Evaporation_loss_S2

Outputs['Inflows_for_Dk'] = Dk
Outputs['Release_Dudhkoshi_sk'] = Release_Dudhkoshi_sk
Outputs['Release_Dudhkoshi_dt'] = Release_Dudhkoshi_dt
Outputs['Storage_Dudhkoshi'] = Storage_Dudhkoshi
Outputs['Overflow_Dudhkoshi'] = Overflow_Dudhkoshi
Outputs['Energy_Dudhkoshi_sk'] = Energy_Dudhkoshi_sk
Outputs['Energy_Dudhkoshi_dt'] = Energy_Dudhkoshi_dt
Outputs["Evaporation_loss_DK"] = Evaporation_loss_Dk

Outputs['Inflows_for_S1'] = l1_
Outputs['Release_Sunkoshi_1'] = Release_Sunkoshi_1
Outputs['Storage_Sunkoshi_1'] = Storage_Sunkoshi_1
Outputs['Overflow_Sunkoshi_1'] = Overflow_Sunkoshi_1
Outputs['Energy_Sunkoshi_1'] = Energy_Sunkoshi_1
Outputs["Evaporation_loss_S1"] = Evaporation_loss_S1

Outputs['Inflows_for_Ko'] = l_Ko
Outputs['Release_Saptakoshi'] = Release_Saptakoshi
Outputs['Storage_Saptakoshi'] = Storage_Saptakoshi
Outputs['Overflow_Saptakoshi'] = Overflow_Saptakoshi
Outputs['Energy_Saptakoshi'] = Energy_Saptakoshi
Outputs["Evaporation_loss_Saptakoshi"] = Evaporation_loss_Ko

Outputs['Release_Sunkoshi_MD'] = Release_Sunkoshi_MD
Outputs['Energy_Sunkoshi_MD'] = Energy_Sunkoshi_MD

Outputs['Release_Sunkoshi_KD'] = Release_Sunkoshi_KD
Outputs['Energy_Sunkoshi_KD'] = Energy_Sunkoshi_KD

Release['Date'] = Date
Release['Month'] = Month
Release['Release_Sunkoshi_3'] = Release_Sunkoshi_3
Release['Release_Sunkoshi_2'] = Release_Sunkoshi_2
Release['Release_Sunkoshi_MD'] = Release_Sunkoshi_MD
Release['Release_Dudhkoshi_sk'] = Release_Dudhkoshi_sk
Release['Release_Dudhkoshi_dt'] = Release_Dudhkoshi_dt
Release['Release_Sunkoshi_1'] = Release_Sunkoshi_1
Release['Release_Saptakoshi'] = Release_Saptakoshi

Storage['Date'] = Date
Storage['Month'] = Month
Storage['Storage_Sunkoshi_3'] = Storage_Sunkoshi_3
Storage['Storage_Sunkoshi_2'] = Storage_Sunkoshi_2
Storage['Storage_Dudhkoshi'] = Storage_Dudhkoshi
Storage['Storage_Sunkoshi_1'] = Storage_Sunkoshi_1
Storage['Storage_Saptakoshi'] = Storage_Saptakoshi

Overflow['Date'] = Date
Overflow['Month'] = Month
Overflow['Storage_Sunkoshi_3'] = Overflow_Sunkoshi_3
Overflow['Storage_Sunkoshi_2'] = Overflow_Sunkoshi_2
Overflow['Overflow_Dudhkoshi'] = Overflow_Dudhkoshi
Overflow['Storage_Sunkoshi_1'] = Overflow_Sunkoshi_1
Overflow['Overflow_Saptakoshi'] = Overflow_Saptakoshi

Energy['Date'] = Date
Energy['Month'] = Month
Energy['Energy_Sunkoshi_3'] = Energy_Sunkoshi_3
Energy['Energy_Sunkoshi_2'] = Energy_Sunkoshi_2
Energy['Energy_Dudhkoshi_sk'] = Energy_Dudhkoshi_sk
Energy['Energy_Dudhkoshi_dt'] = Energy_Dudhkoshi_dt
Energy['Energy_Sunkoshi_1'] = Energy_Sunkoshi_1
Energy['Energy_Sunkoshi_MD'] = Energy_Sunkoshi_MD
Energy['Energy_Saptakoshi'] = Energy_Saptakoshi

Day_energy_percent_A['Date'] = Date1
Day_energy_percent_A['Dry Energy percent S3'] = Dry_energy_percent_for_S3_Annually
Day_energy_percent_A['Dry Energy percent S2'] = Dry_energy_percent_for_S2_Annually
Day_energy_percent_A['Dry Energy percent sk'] = Dry_energy_percent_for_sk_Annually
Day_energy_percent_A['Dry Energy percent dt'] = Dry_energy_percent_for_dt_Annually
Day_energy_percent_A['Dry Energy percent S1'] = Dry_energy_percent_for_S1_Annually
Day_energy_percent_A['Dry Energy percent MD'] = Dry_energy_percent_for_MD_Annually
Day_energy_percent_A['Dry Energy percent Ko'] = Dry_energy_percent_for_Ko_Annually
Day_energy_percent_A['Dry Energy percent KD'] = Dry_energy_percent_for_KD_Annually

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
