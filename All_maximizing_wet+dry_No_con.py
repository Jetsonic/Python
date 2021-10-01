import time
import random
import pandas as pd
import numpy as np
from PSO_Algorithm import pso
from data_pso import Interpolate, I3, Dmd_MD, Dmd_KD, Dk, l2, l1_, Ex2, Ex3, Exd, Ex1, Ex_Ko, Tyear, Fyear, Days, l_Ko, MDR

PSO_Outputs = pd.ExcelWriter('All_2021-10-2_wd_nc.xlsx')

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
swarmsize = 50
wmax = 1
wmin = 0.3
C1 = 1
C2 = 0.5
X = 0.9
pem = 0.3
maxiter = 50
minstep = 1e-20
minfunc = 1e-20
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
Ovariables = 5
T_O_V = Tmonth * Ovariables + Ovariables
lb = np.zeros(Tmonth + 1)
ub = np.zeros(Tmonth + 1)

# Giving upper and lower value for pso search function,here limit on irrigation and release output can de defined.
"""
  ub-lb Section
  ==============
   Here each optimization values (i.e Releases) are given:
    lb : lower bound
    ub : upper bound

   following code facilities this process such that these bounds can be given for each releases for each month. 
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


Setup = pd.DataFrame()
verbose = ["Maximizing dry+wet energy for all stations with no constrains"]
Setup['Setup'] = verbose
Setup.to_excel(PSO_Outputs, sheet_name='Setup', index=False)
Parameters = pd.DataFrame()
Inputs = ['swarmsize', 'wmax', 'wmin', 'C1', 'C2', 'X', 'maxiter', 'minstep', 'minfunc', 'Fitness_value_S3', 'Fitness_value_S2', 'Fitness_value_S1', 'Fitness_value_Dk', 'Fitness_value_Ko', 'Dry_energy percent Total for S3', 'Dry_energy percent Total for S2', 'Dry_energy percent Total for S1', 'Dry_energy percent Total for SK PH', 'Dry_energy percent Total for DT PH', 'Dry_energy percent Total for MD', 'Dry_energy percent Total for Ko', 'Dry_energy percent Total for KD']
Parameters['Parameters'] = Inputs

Day_energy_percent_A = pd.DataFrame()
y = pd.to_datetime(Fyear, format='%Y')
c = Tyear + Fyear
m = pd.to_datetime(c, format='%Y')
Date = pd.date_range(start=y, end=m, freq='M').year.tolist()
Date1 = pd.date_range(start=y, end=m, freq='Y').year.tolist()
Month = pd.date_range(start=y, end=m, freq='M').month_name().tolist()
Day_energy_percent_A['Date'] = Date1

for St in range(0, Ovariables):
	if St == 0:
		for i in range(0, Tmonth + 1):
			ub[i] = S3max
			lb[i] = S3min


		def fitness_S3(x):
			F = 0
			Q3 = Storage3(x)[2]
			H3 = Height3(x)
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


		def Storage3(x):
			R3 = np.zeros(Tmonth)
			ev3 = []
			S3 = x
			j = 0
			for i in range(Tmonth):
				Ev3 = Evaporation3(S3[i], j, i)
				ev3.append(Ev3)
				R3[i] = S3[i] - S3[i + 1] + I3[i] - Ev3
				while R3[i] < 0:
					S3[i + 1] = random.uniform(S3min, S3max)
					R3[i] = S3[i] - S3[i + 1] + I3[i] - Ev3
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


		xopt_S3, fopt_S3, iter_vs_swamp_vs_fitness_S3, iter_vs_globalbest_S3 = pso(fitness_S3, lb, ub, swarmsize=swarmsize, pem=pem, wmax=wmax, wmin=wmin, c1=C1, c2=C2, X=X, maxiter=maxiter, minstep=minstep, minfunc=minfunc, debug=False)

		print('Optimal fitness function value:')
		print('    myfunc: {}'.format(fopt_S3))

		Fitness_value_S3 = fopt_S3

		Outputs_S3 = pd.DataFrame()

		pso_data1_S3 = pd.DataFrame(iter_vs_swamp_vs_fitness_S3, columns=['Iteration', 'Swamp_Number', 'Fitness_Value'])
		pso_data2_S3 = pd.DataFrame(iter_vs_globalbest_S3, columns=['Iteration', 'Global_best_fitness'])

		Storage_Sunkoshi_3 = xopt_S3
		Storage_S3 = Storage_Sunkoshi_3[:-1]
		Outflow_Sunkoshi_3, Energy_Sunkoshi_3, Discharge_Sunkoshi_3, Spill_Sunkoshi_3, Power_Sunkoshi_3, Evaporation_loss_S3 = Storage3(xopt_S3)
		Elevation_Sunkoshi_3 = Height3(xopt_S3) + S3_effective_twl

		Dry_energy_percent_for_S3_total = Dry_energy_checkT(Energy_Sunkoshi_3)
		Dry_energy_percent_for_S3_Annually = Dry_energy_checkA(Energy_Sunkoshi_3)

		Outputs_S3['Date'] = Date
		Outputs_S3['Month'] = Month
		Outputs_S3['Inflows_for_S3'] = I3
		Outputs_S3['Outflow_Sunkoshi_3'] = Outflow_Sunkoshi_3
		Outputs_S3["Evaporation_loss_S3"] = Evaporation_loss_S3
		Outputs_S3['Storage_Sunkoshi_3'] = Storage_S3
		Outputs_S3['Elevation_Sunkoshi_3'] = Elevation_Sunkoshi_3
		Outputs_S3['Spill_for_Sunkoshi_3'] = Spill_Sunkoshi_3
		Outputs_S3['Discharge_for_Sunkoshi_3'] = Discharge_Sunkoshi_3
		Outputs_S3['Power_for_Sunkoshi_3'] = Power_Sunkoshi_3
		Outputs_S3['Energy_Sunkoshi_3'] = Energy_Sunkoshi_3
		Day_energy_percent_A['Dry Energy percent S3'] = Dry_energy_percent_for_S3_Annually

		Outputs_S3.to_excel(PSO_Outputs, sheet_name='Outputs_S3', index=False)
		pso_data1_S3.to_excel(PSO_Outputs, sheet_name='iter_vs_swamp_vs_fitness_S3', index=False)
		pso_data2_S3.to_excel(PSO_Outputs, sheet_name='iter_vs_Global_best_fitness_S3', index=False)

	if St == 1:
		for i in range(0, Tmonth + 1):
			ub[i] = S2max
			lb[i] = S2min


		def fitness_S2(x):
			F = 0
			Q2 = Storage2(x)[3]
			Q_MD = Storage2(x)[4]
			H2 = Height2(x)
			for i in range(Tmonth):
				z_dry = 0
				z_wet = 0
				p = (g * ita_S2 * Q2[i] * H2[i]) / 1000
				if i % 12 == 0 or i % 12 == 1 or i % 12 == 2 or i % 12 == 3 or i % 12 == 4 or i % 12 == 11:
					p_dry = p
					p_MD_dry = (g * ita_MD * Q_MD[i] * H_MD) / 1000
					z_dry = (1 - (p_dry / power2)) + (1 - (p_MD_dry / power_MD))
				elif i % 12 == 5 or i % 12 == 6 or i % 12 == 7 or i % 12 == 8 or i % 12 == 9 or i % 12 == 10:
					p_wet = p
					p_MD_wet = (g * ita_MD * Q_MD[i] * H_MD) / 1000
					z_wet = (1 - (p_wet / power2)) + (1 - (p_MD_wet / power_MD))
				Total = z_dry + z_wet
				F = F + Total
			return F


		def Storage2(x):
			R2 = np.zeros(Tmonth)
			R_MD = np.zeros(Tmonth)
			ev2 = []
			S2 = x
			j = 0
			for i in range(Tmonth):
				Ev2 = Evaporation2(S2[i], j, i)
				ev2.append(Ev2)
				R2[i] = S2[i] - S2[i + 1] + Outflow_Sunkoshi_3[i] + l2[i] - Ev2
				while R2[i] < 0:
					S2[i + 1] = random.uniform(S2min, S2max)
					R2[i] = R2[i] = S2[i] - S2[i + 1] + Outflow_Sunkoshi_3[i] + l2[i] - Ev2
				if R2[i] > MDR[i]:
					if R2[i] - MDR[i] > Dmd_MD[j]:
						R_MD[i] = Dmd_MD[j]
					else:
						R_MD[i] = R2[i] - MDR[i]
				j += 1
				if j == 12:
					j = 0
			e2, e_MD, Q2, Q_MD, Sp2, p2, p_MD = E2(R2, R_MD, x)
			return R2, e2, e_MD, Q2, Q_MD, Sp2, p2, p_MD, ev2


		def E2(R, R_MD, x):
			e2 = np.zeros(Tmonth)  # initial Energy all values are zero
			e_MD = np.zeros(Tmonth)
			p2 = np.zeros(Tmonth)
			p_MD = np.zeros(Tmonth)
			H2 = Height2(x)
			R2 = (R * 10 ** 6) / (Days * 24 * 3600)
			Q_MD = (R_MD * 10 ** 6) / (Days * 24 * 3600)
			Q2 = np.zeros(Tmonth)
			Sp2 = np.zeros(Tmonth)
			for i in range(Tmonth):
				p2[i] = g * ita_S2 * (R2[i] - Q_MD[i]) * H2[i] / 1000 if (g * ita_S2 * (R2[i] - Q_MD[i]) * H2[i] / 1000) <= power2 else power2
				e2[i] = (p2[i] * Days[i] * 24) / 1000
				Q2[i] = (p2[i] / (g * ita_S2 * H2[i]) * 1000)
				p_MD[i] = (g * ita_MD * Q_MD[i] * H_MD) / 1000
				e_MD[i] = (p_MD[i] * Days[i] * 24) / 1000
				Sp2[i] = ((R2[i] - Q_MD[i] - Q2[i]) * Days[i] * 24 * 3600) / 10 ** 6 if Q2[i] < (R2[i] - Q_MD[i]) else 0
			return e2, e_MD, Q2, Q_MD, Sp2, p2, p_MD


		# Height for Sunkoshi-2
		def Height2(x):
			H2 = np.zeros(Tmonth)
			S2 = x
			for i in range(Tmonth):
				H2[i] = Interpolate(Ex2, (S2[i] + S2[i + 1]) / 2, c='Elev')
				H2[i] = H2[i] - S2_effective_twl
			return H2


		def Evaporation2(a, b, d):
			S2a = Interpolate(Ex2, a, c='SArea')
			Eva = (ev[b] * S2a) * Days[d] / 10 ** 9
			return Eva


		def cons(x):
			con = []
			R2 = Storage2(x)[0]
			for i in range(Tmonth):
				con.append(R2[i])
			return con


		xopt_S2, fopt_S2, iter_vs_swamp_vs_fitness_S2, iter_vs_globalbest_S2 = pso(fitness_S2, lb, ub, swarmsize=swarmsize, pem=pem, wmax=wmax, wmin=wmin, c1=C1, c2=C2, X=X, maxiter=maxiter, minstep=minstep, minfunc=minfunc, debug=False)

		print('Optimal fitness function value:')
		print('    myfunc: {}'.format(fopt_S2))

		Fitness_value_S2 = fopt_S2

		Outputs_S2 = pd.DataFrame()
		pso_data1_S2 = pd.DataFrame(iter_vs_swamp_vs_fitness_S2, columns=['Iteration', 'Swamp_Number', 'Fitness_Value'])
		pso_data2_S2 = pd.DataFrame(iter_vs_globalbest_S2, columns=['Iteration', 'Global_best_fitness'])

		Storage_Sunkoshi_2 = xopt_S2
		Storage_S2 = Storage_Sunkoshi_2[:-1]
		Outflow_Sunkoshi_2, Energy_Sunkoshi_2, Energy_MD, Discharge_Sunkoshi_2, Discharge_MD, Spill_Sunkoshi_2, Power_Sunkoshi_2, Power_MD, Evaporation_loss_S2 = Storage2(xopt_S2)
		Elevation_Sunkoshi_2 = Height2(xopt_S2) + S2_effective_twl

		Dry_energy_percent_for_S2_total = Dry_energy_checkT(Energy_Sunkoshi_2)
		Dry_energy_percent_for_MD_total = Dry_energy_checkT(Energy_MD)
		Dry_energy_percent_for_S2_Annually = Dry_energy_checkA(Energy_Sunkoshi_2)
		Dry_energy_percent_for_MD_Annually = Dry_energy_checkA(Energy_MD)

		Outputs_S2['Date'] = Date
		Outputs_S2['Month'] = Month
		Outputs_S2['Inflows_for_S2'] = l2 + Outflow_Sunkoshi_3
		Outputs_S2['Outflow_Sunkoshi_2'] = Outflow_Sunkoshi_2
		Outputs_S2["Evaporation_loss_S2"] = Evaporation_loss_S2
		Outputs_S2['Storage_Sunkoshi_2'] = Storage_S2
		Outputs_S2['Elevation_Sunkoshi_2'] = Elevation_Sunkoshi_2
		Outputs_S2['Spill_for_Sunkoshi_2'] = Spill_Sunkoshi_2
		Outputs_S2['Discharge_for_Sunkoshi_2'] = Discharge_Sunkoshi_2
		Outputs_S2['Power_for_Sunkoshi_2'] = Power_Sunkoshi_2
		Outputs_S2['Energy_Sunkoshi_2'] = Energy_Sunkoshi_2
		Outputs_S2['Discharge_for_Sunkoshi_MD'] = Discharge_MD
		Outputs_S2['Power_for_Sunkoshi_MD'] = Power_MD
		Outputs_S2['Energy_Sunkoshi_MD'] = Energy_MD
		Day_energy_percent_A['Dry Energy percent S2'] = Dry_energy_percent_for_S2_Annually
		Day_energy_percent_A['Dry Energy percent MD'] = Dry_energy_percent_for_MD_Annually


		Outputs_S2.to_excel(PSO_Outputs, sheet_name='Outputs_S2', index=False)
		pso_data1_S2.to_excel(PSO_Outputs, sheet_name='iter_vs_swamp_vs_fitness_S2', index=False)
		pso_data2_S2.to_excel(PSO_Outputs, sheet_name='iter_vs_Global_best_fitness_S2', index=False)

	if St == 2:
		for i in range(0, Tmonth + 1):
			ub[i] = S1max
			lb[i] = S1min


		def fitness_Dk(x):
			F = 0
			Q_sk = Storaged(x)[4]
			Q_dt = Storaged(x)[3]
			H_dt = Height_dt(x)
			H_sk = Height_sk(x)
			for i in range(Tmonth):
				z_dry = 0
				z_wet = 0
				p_dt = (g * ita_dt * Q_dt[i] * H_dt[i]) / 1000
				p_sk = (g * ita_sk * Q_sk[i] * H_sk[i]) / 1000
				if i % 12 == 0 or i % 12 == 1 or i % 12 == 2 or i % 12 == 3 or i % 12 == 4 or i % 12 == 11:
					p_dt_dry = p_dt
					p_sk_dry = p_sk
					z_dry = (1 - (p_dt_dry / power_dt)) + (1 - (p_sk_dry / power_sk))
				elif i % 12 == 5 or i % 12 == 6 or i % 12 == 7 or i % 12 == 8 or i % 12 == 9 or i % 12 == 10:
					p_dt_wet = p_dt
					p_sk_wet = p_sk
					z_wet = (1 - (p_dt_wet / power_dt)) + (1 - (p_sk_wet / power_sk))
				Total = z_dry + z_wet
				F = F + Total
			return F


		def Storaged(x):
			Rd = np.zeros(Tmonth)
			R_dt = np.zeros(Tmonth)  # initial overflow all values are zero
			R_sk = np.zeros(Tmonth)
			evd = []
			Sd = x
			j = 0
			for i in range(Tmonth):
				Evd = Evaporationd(Sd[i], j, i)
				evd.append(Evd)
				Rd[i] = Sd[i] - Sd[i + 1] + Dk[i] - Evd
				while Rd[i] < 0:
					Sd[i + 1] = random.uniform(Sdmin, Sdmax)
					Rd[i] = Sd[i] - Sd[i + 1] + Dk[i] - Evd
				if Rd[i] > MDR[i]:
					R_sk[i] = Rd[i] - MDR[i]
					R_dt[i] = MDR[i]
				else:
					R_dt[i] = Rd[i]
					R_sk[i] = 0
				j += 1
				if j == 12:
					j = 0
			e_dt, e_sk, Q_dt, Q_sk, Sp_D, p_dt, p_sk = E_D(R_dt, R_sk, x)
			R_dt = Q_dt * (Days * 24 * 3600) / (10 ** 6)
			R_sk = Q_sk * (Days * 24 * 3600) / (10 ** 6)
			return Rd, e_dt, e_sk, Q_dt, Q_sk, Sp_D, p_dt, p_sk, evd, R_dt, R_sk


		def E_D(R_dt, R_sk, x):
			e_dt = np.zeros(Tmonth)
			e_sk = np.zeros(Tmonth)
			p_dt = np.zeros(Tmonth)
			p_sk = np.zeros(Tmonth)
			H_dt = Height_dt(x)
			H_sk = Height_sk(x)
			Q_dt_temp = (R_dt * 10 ** 6) / (Days * 24 * 3600)
			Q_sk_temp = (R_sk * 10 ** 6) / (Days * 24 * 3600)
			Q_dt = np.zeros(Tmonth)
			Q_sk = np.zeros(Tmonth)
			Sp_D = np.zeros(Tmonth)
			for i in range(Tmonth):
				p_sk[i] = g * ita_sk * Q_sk_temp[i] * H_sk[i] / 1000 if (g * ita_sk * Q_sk_temp[i] * H_sk[i] / 1000) <= power_sk else power_sk
				Q_sk[i] = (p_sk[i] / (g * ita_sk * H_sk[i]) * 1000)
				if Q_sk_temp[i] > Q_sk[i]:
					Q_dt_temp[i] = Q_dt_temp[i] + (Q_sk_temp[i] - Q_sk[i])
				e_sk[i] = (p_sk[i] * Days[i] * 24) / 1000
				p_dt[i] = (g * ita_dt * Q_dt_temp[i] * H_dt[i]) / 1000 if ((g * ita_dt * Q_dt_temp[i] * H_dt[i]) / 1000) <= power_dt else power_dt
				Q_dt[i] = (p_dt[i] / (g * ita_dt * H_dt[i]) * 1000)
				e_dt[i] = (p_dt[i] * Days[i] * 24) / 1000
				Sp_D[i] = ((Q_dt_temp[i] - Q_dt[i]) * Days[i] * 24 * 3600) / 10 ** 6 if Q_dt[i] <= Q_dt_temp[i] else 0
			return e_dt, e_sk, Q_dt, Q_sk, Sp_D, p_dt, p_sk


		#  Dam toe Powerhouse
		def Height_dt(x):
			H_dt = np.zeros(Tmonth)
			Sd = x
			for i in range(Tmonth):
				H_dt[i] = Interpolate(Exd, (Sd[i] + Sd[i + 1]) / 2, c='Elev')
				H_dt[i] = H_dt[i] - Dt_effective_twl
			return H_dt


		#  Sunkoshi Powerhouse
		def Height_sk(x):
			H_sk = np.zeros(Tmonth)
			Sd = x
			for i in range(Tmonth):
				H_sk[i] = Interpolate(Exd, (Sd[i] + Sd[i + 1]) / 2, c='Elev')
				H_sk[i] = H_sk[i] - SK_effective_twl
			return H_sk


		def Evaporationd(a, b, d):
			Dka = Interpolate(Exd, a, c='SArea')
			Evd = (ev[b] * Dka) * Days[d] / 10 ** 9
			return Evd


		def cons(x):
			con = []
			Rd = Storaged(x)[0]
			for i in range(Tmonth):
				con.append(Rd[i])
			return con


		xopt_Dk, fopt_Dk, iter_vs_swamp_vs_fitness_Dk, iter_vs_globalbest_Dk = pso(fitness_Dk, lb, ub, swarmsize=swarmsize, pem=pem, wmax=wmax, wmin=wmin, c1=C1, c2=C2, X=X, maxiter=maxiter, minstep=minstep, minfunc=minfunc, debug=False)

		print('Optimal fitness function value:')
		print('    myfunc: {}'.format(fopt_Dk))

		Fitness_value_Dk = fopt_Dk

		Outputs_Dk = pd.DataFrame()
		pso_data1_Dk = pd.DataFrame(iter_vs_swamp_vs_fitness_Dk, columns=['Iteration', 'Swamp_Number', 'Fitness_Value'])
		pso_data2_Dk = pd.DataFrame(iter_vs_globalbest_Dk, columns=['Iteration', 'Global_best_fitness'])

		Storage_Dudhkoshi_Dk = xopt_Dk
		Storage_Dk = Storage_Dudhkoshi_Dk[:-1]
		Outflow_Dudhkoshi, Energy_Dudhkoshi_dt, Energy_Dudhkoshi_sk, Discharge_Dudhkoshi_dt, Discharge_Dudhkoshi_sk, Spill_Dudhkoshi, Power_Dudhkoshi_dt, Power_Dudhkoshi_sk, Evaporation_loss_Dudhkoshi, MCM_R_dt, MCM_R_sk = Storaged(xopt_Dk)
		Elevation_DudhKoshi = Height_sk(xopt_Dk) + SK_effective_twl

		Dry_energy_percent_for_sk_total = Dry_energy_checkT(Energy_Dudhkoshi_sk)
		Dry_energy_percent_for_dt_total = Dry_energy_checkT(Energy_Dudhkoshi_dt)
		Dry_energy_percent_for_sk_Annually = Dry_energy_checkA(Energy_Dudhkoshi_sk)
		Dry_energy_percent_for_dt_Annually = Dry_energy_checkA(Energy_Dudhkoshi_dt)

		Outputs_Dk['Date'] = Date
		Outputs_Dk['Month'] = Month
		Outputs_Dk['Inflows_for_S2'] = Dk
		Outputs_Dk['Outflow_Dudhkoshi'] = Outflow_Dudhkoshi
		Outputs_Dk["Evaporation_loss_Dudhkoshi"] = Evaporation_loss_Dudhkoshi
		Outputs_Dk['Storage_Dudhkoshi'] = Storage_Dk
		Outputs_Dk['Elevation_Dudhkoshi'] = Elevation_DudhKoshi
		Outputs_Dk['Spill_for_Dudhkoshi'] = Spill_Dudhkoshi
		Outputs_Dk['Discharge_for_Dudhkoshi_dt'] = Discharge_Dudhkoshi_dt
		Outputs_Dk['Discharge_for_Dudhkoshi_sk'] = Discharge_Dudhkoshi_sk
		Outputs_Dk['Power_for_Dudhkoshi_dt'] = Power_Dudhkoshi_dt
		Outputs_Dk['Power_for_Dudhkoshi_sk'] = Power_Dudhkoshi_sk
		Outputs_Dk['Energy_Dudhkoshi_dt'] = Energy_Dudhkoshi_dt
		Outputs_Dk['Energy_Dudhkoshi_sk'] = Energy_Dudhkoshi_sk

		Day_energy_percent_A['Dry Energy percent sk'] = Dry_energy_percent_for_sk_Annually
		Day_energy_percent_A['Dry Energy percent dt'] = Dry_energy_percent_for_dt_Annually

		Outputs_Dk.to_excel(PSO_Outputs, sheet_name='Outputs_Dk', index=False)
		pso_data1_Dk.to_excel(PSO_Outputs, sheet_name='iter_vs_swamp_vs_fitness_Dk', index=False)
		pso_data2_Dk.to_excel(PSO_Outputs, sheet_name='iter_vs_Global_best_fitness_Dk', index=False)

	if St == 3:
		for i in range(0, Tmonth + 1):
			ub[i] = Sdmax
			lb[i] = Sdmin


		def fitness_S1(x):
			F = 0
			Q1 = Storage1(x)[2]
			H1 = Height1(x)
			for i in range(Tmonth):
				z_dry = 0
				z_wet = 0
				p1 = (g * ita_S1 * Q1[i] * H1[i]) / 1000
				if i % 12 == 0 or i % 12 == 1 or i % 12 == 2 or i % 12 == 3 or i % 12 == 4 or i % 12 == 11:
					p1_dry = p1
					z_dry = (1 - (p1_dry / power1))
				elif i % 12 == 5 or i % 12 == 6 or i % 12 == 7 or i % 12 == 8 or i % 12 == 9 or i % 12 == 10:
					p1_wet = p1
					z_wet = (1 - (p1_wet / power1))
				Total = z_dry + z_wet
				F = F + Total
			return F


		def Storage1(x):
			R1 = np.zeros(Tmonth)
			ev1 = []
			S1 = x
			j = 0
			for i in range(Tmonth):
				Ev1 = Evaporation1(S1[i], j, i)
				ev1.append(Ev1)
				R1[i] = S1[i] - S1[i + 1] + Outflow_Sunkoshi_2[i] + Spill_Dudhkoshi[i] + MCM_R_dt[i] + l1_[i] - Ev1
				while R1[i] < 0:
					S1[i + 1] = random.uniform(S1min, S1max)
					R1[i] = S1[i] - S1[i + 1] + Outflow_Sunkoshi_2[i] + Spill_Dudhkoshi[i] + MCM_R_dt[i] + l1_[i] - Ev1
				j += 1
				if j == 12:
					j = 0
			e1, Q1, Sp1, p1 = E1(R1, x)
			return R1, e1, Q1, Sp1, p1, ev1


		def E1(R, x):
			e1 = np.zeros(Tmonth)  # initial Energy all values are zero
			p1 = np.zeros(Tmonth)
			H1 = Height1(x)
			R1 = (R * 10 ** 6) / (Days * 24 * 3600)
			Q1 = np.zeros(Tmonth)
			Sp1 = np.zeros(Tmonth)
			for i in range(Tmonth):
				p1[i] = g * ita_S1 * R1[i] * H1[i] / 1000 if (g * ita_S1 * R1[i] * H1[i] / 1000) <= power1 else power1
				e1[i] = (p1[i] * Days[i] * 24) / 1000
				Q1[i] = (p1[i] / (g * ita_S1 * H1[i]) * 1000)
				Sp1[i] = ((R1[i] - Q1[i]) * Days[i] * 24 * 3600) / 10 ** 6 if Q1[i] <= R1[i] else 0
			return e1, Q1, Sp1, p1


		def Height1(x):
			H1 = np.zeros(Tmonth)
			S1 = x
			for i in range(Tmonth):
				H1[i] = Interpolate(Ex1, (S1[i] + S1[i + 1]) / 2, c='Elev')
				H1[i] = H1[i] - S1_effective_twl
			return H1


		def Evaporation1(a, b, d):
			S1a = Interpolate(Ex1, a, c='SArea')
			Eva = (ev[b] * S1a) * Days[d] / 10 ** 9
			return Eva


		def cons(x):
			con = []
			R1 = Storage1(x)[0]
			for i in range(Tmonth):
				con.append(R1[i])
			return con


		xopt_S1, fopt_S1, iter_vs_swamp_vs_fitness_S1, iter_vs_globalbest_S1 = pso(fitness_S1, lb, ub, swarmsize=swarmsize, pem=pem, wmax=wmax, wmin=wmin, c1=C1, c2=C2, X=X, maxiter=maxiter, minstep=minstep, minfunc=minfunc, debug=False)

		print('Optimal fitness function value:')
		print('    myfunc: {}'.format(fopt_S1))

		Fitness_value_S1 = fopt_S1

		Outputs_S1 = pd.DataFrame()
		pso_data1_S1 = pd.DataFrame(iter_vs_swamp_vs_fitness_S1, columns=['Iteration', 'Swamp_Number', 'Fitness_Value'])
		pso_data2_S1 = pd.DataFrame(iter_vs_globalbest_S1, columns=['Iteration', 'Global_best_fitness'])

		Storage_Sunkoshi_1 = xopt_S1
		Storage_S1 = Storage_Sunkoshi_1[:-1]
		Outflow_Sunkoshi_1, Energy_Sunkoshi_1, Discharge_Sunkoshi_1, Spill_Sunkoshi_1, Power_Sunkoshi_1, Evaporation_loss_S1 = Storage1(xopt_S1)
		Elevation_Sunkoshi_1 = Height1(xopt_S1) + S1_effective_twl

		Dry_energy_percent_for_S1_total = Dry_energy_checkT(Energy_Sunkoshi_1)
		Dry_energy_percent_for_S1_Annually = Dry_energy_checkA(Energy_Sunkoshi_1)

		Outputs_S1['Date'] = Date
		Outputs_S1['Month'] = Month
		Outputs_S1['Inflows_for_S1'] = l1_ + Spill_Dudhkoshi + Outflow_Sunkoshi_2 + MCM_R_dt
		Outputs_S1['Outflow_Sunkoshi_1'] = Outflow_Sunkoshi_1
		Outputs_S1["Evaporation_loss_S1"] = Evaporation_loss_S1
		Outputs_S1['Storage_Sunkoshi_1'] = Storage_S1
		Outputs_S1['Elevation_Sunkoshi_1'] = Elevation_Sunkoshi_1
		Outputs_S1['Spill_Sunkoshi_1'] = Spill_Sunkoshi_1
		Outputs_S1['Discharge_for_Sunkoshi_1'] = Discharge_Sunkoshi_1
		Outputs_S1['Power_for_Sunkoshi_1'] = Power_Sunkoshi_1
		Outputs_S1['Energy_Sunkoshi_1'] = Energy_Sunkoshi_1
		Day_energy_percent_A['Dry Energy percent S1'] = Dry_energy_percent_for_S1_Annually

		Outputs_S1.to_excel(PSO_Outputs, sheet_name='Outputs_S1', index=False)
		pso_data1_S1.to_excel(PSO_Outputs, sheet_name='iter_vs_swamp_vs_fitness_S1', index=False)
		pso_data2_S1.to_excel(PSO_Outputs, sheet_name='iter_vs_Global_best_fitness_S1', index=False)

	if St == 4:
		for i in range(0, Tmonth + 1):
			ub[i] = S_Ko_max
			lb[i] = S_Ko_min


		def fitness_Ko(x):
			F = 0
			Q_Ko = Storage_Ko(x)[3]
			Q_KD = Storage_Ko(x)[4]
			H_Ko = Height_Ko(x)
			for i in range(Tmonth):
				z_dry = 0
				z_wet = 0
				p_Ko = (g * ita_Ko * Q_Ko[i] * H_Ko[i]) / 1000
				p_KD = (g * ita_KD * Q_KD[i] * H_KD) / 1000
				if i % 12 == 0 or i % 12 == 1 or i % 12 == 2 or i % 12 == 3 or i % 12 == 4 or i % 12 == 11:
					p_Ko_dry = p_Ko
					p_KD_dry = p_KD
					z_dry = (1 - (p_Ko_dry / power_Ko)) + (1 - (p_KD_dry / power_KD))
				elif i % 12 == 5 or i % 12 == 6 or i % 12 == 7 or i % 12 == 8 or i % 12 == 9 or i % 12 == 10:
					p_Ko_wet = p_Ko
					p_KD_wet = p_KD
					z_wet = (1 - (p_Ko_wet / power_Ko)) + (1 - (p_KD_wet / power_KD))
				Total = z_dry + z_wet
				F = F + Total
			return F


		def Storage_Ko(x):
			R_Ko = np.zeros(Tmonth)
			R_KD = np.zeros(Tmonth)
			evKo = []
			S_Ko = x
			j = 0
			for i in range(Tmonth):
				Ev_Ko = EvaporationKo(S_Ko[i], j, i)
				evKo.append(Ev_Ko)
				R_Ko[i] = S_Ko[i] - S_Ko[i + 1] + l_Ko[i] + Outflow_Sunkoshi_1[i] + MCM_R_sk[i] - Ev_Ko
				while R_Ko[i] < 0:
					S_Ko[i + 1] = random.uniform(S_Ko_min, S_Ko_max)
					R_Ko[i] = S_Ko[i] - S_Ko[i + 1] + l_Ko[i] + Outflow_Sunkoshi_1[i] + MCM_R_sk[i] - Ev_Ko
				if R_Ko[i] > MDR[i]:
					if (R_Ko[i] - MDR[i]) > Dmd_KD[j]:
						R_KD[i] = Dmd_MD[j]
					else:
						R_KD[i] = R_Ko[i] - MDR[i]
				j += 1
				if j == 12:
					j = 0
			e_Ko, e_KD, Q_Ko, Q_KD, Sp_Ko, p_Ko, p_KD = E_Ko(R_Ko, R_KD, x)
			return R_Ko, e_Ko, e_KD, Q_Ko, Q_KD, Sp_Ko, p_Ko, p_KD, evKo


		def E_Ko(R, R_KD, x):
			e_Ko = np.zeros(Tmonth)  # initial Energy all values are zero
			e_KD = np.zeros(Tmonth)
			p_Ko = np.zeros(Tmonth)
			p_KD = np.zeros(Tmonth)
			H_Ko = Height_Ko(x)
			R_Ko = (R * 10 ** 6) / (Days * 24 * 3600)
			Q_KD = (R_KD * 10 ** 6) / (Days * 24 * 3600)
			Q_Ko = np.zeros(Tmonth)
			Sp_Ko = np.zeros(Tmonth)
			for i in range(Tmonth):
				p_Ko[i] = g * ita_Ko * (R_Ko[i] - Q_KD[i]) * H_Ko[i] / 1000 if (g * ita_Ko * (R_Ko[i] - Q_KD[i]) * H_Ko[i] / 1000) <= power_Ko else power_Ko
				e_Ko[i] = (p_Ko[i] * Days[i] * 24) / 1000
				Q_Ko[i] = (p_Ko[i] / (g * ita_Ko * H_Ko[i]) * 1000)
				p_KD[i] = (g * ita_KD * Q_KD[i] * H_KD) / 1000
				e_KD[i] = (p_KD[i] * Days[i] * 24) / 1000
				Sp_Ko[i] = ((R_Ko[i] - Q_KD[i] - Q_Ko[i]) * Days[i] * 24 * 3600) / 10 ** 6 if Q_Ko[i] < (R_Ko[i] - Q_KD[i]) else 0
			return e_Ko, e_KD, Q_Ko, Q_KD, Sp_Ko, p_Ko, p_KD


		def Height_Ko(x):
			H_Ko = np.zeros(Tmonth)
			S_Ko = x
			for i in range(Tmonth):
				H_Ko[i] = Interpolate(Ex_Ko, (S_Ko[i] + S_Ko[i + 1]) / 2, c='Elev')
				H_Ko[i] = H_Ko[i] - Ko_effective_twl
			return H_Ko


		def EvaporationKo(a, b, d):
			Koa = Interpolate(Ex_Ko, a, c='SArea')
			Ev_Ko = (ev[b] * Koa) * Days[d] / 10 ** 9
			return Ev_Ko


		def cons(x):
			con = []
			R_Ko = Storage_Ko(x)[0]
			for i in range(Tmonth):
				con.append(R_Ko[i])
			return con


		xopt_Ko, fopt_Ko, iter_vs_swamp_vs_fitness_Ko, iter_vs_globalbest_Ko = pso(fitness_Ko, lb, ub, swarmsize=swarmsize, pem=pem, wmax=wmax, wmin=wmin, c1=C1, c2=C2, X=X, maxiter=maxiter, minstep=minstep, minfunc=minfunc, debug=False)

		print('Optimal fitness function value:')
		print('    myfunc: {}'.format(fopt_Ko))

		Fitness_value_Ko = fopt_Ko

		Outputs_Ko = pd.DataFrame()
		pso_data1_Ko = pd.DataFrame(iter_vs_swamp_vs_fitness_Ko, columns=['Iteration', 'Swamp_Number', 'Fitness_Value'])
		pso_data2_Ko = pd.DataFrame(iter_vs_globalbest_Ko, columns=['Iteration', 'Global_best_fitness'])

		Storage_Saptakoshi_Ko = xopt_Ko
		Storage_SKo = Storage_Saptakoshi_Ko[:-1]
		Outflow_SaptaKoshi, Energy_SaptaKoshi, Energy_KD, Discharge_SaptaKoshi, Discharge_KD, Spill_SaptaKoshi, Power_SaptaKoshi, Power_KD, Evaporation_loss_SaptaKoshi = Storage_Ko(xopt_Ko)
		Elevation_SaptaKoshi = Height_Ko(xopt_Ko) + Ko_effective_twl

		Dry_energy_percent_for_Ko_total = Dry_energy_checkT(Energy_SaptaKoshi)
		Dry_energy_percent_for_KD_total = Dry_energy_checkT(Energy_KD)
		Dry_energy_percent_for_Ko_Annually = Dry_energy_checkA(Energy_SaptaKoshi)
		Dry_energy_percent_for_KD_Annually = Dry_energy_checkA(Energy_KD)

		Outputs_Ko['Date'] = Date
		Outputs_Ko['Month'] = Month
		Outputs_Ko['Inflows_for_Ko'] = l_Ko + Outflow_Sunkoshi_1 + MCM_R_sk
		Outputs_Ko['Outflow_Saptakoshi'] = Outflow_SaptaKoshi
		Outputs_Ko["Evaporation_loss_Saptakoshi"] = Evaporation_loss_SaptaKoshi
		Outputs_Ko['Storage_Saptakoshi'] = Storage_SKo
		Outputs_Ko['Elevation_Saptakoshi'] = Elevation_SaptaKoshi
		Outputs_Ko['Spill_for_Saptakoshi'] = Spill_SaptaKoshi
		Outputs_Ko['Discharge_for_Saptakoshi'] = Discharge_SaptaKoshi
		Outputs_Ko['Power_for_Saptakoshi'] = Power_SaptaKoshi
		Outputs_Ko['Energy_Saptakoshi'] = Energy_SaptaKoshi
		Outputs_Ko['Discharge_for_Sunkoshi_KD'] = Discharge_KD
		Outputs_Ko['Power_for_Sunkoshi_KD'] = Power_KD
		Outputs_Ko['Energy_Sunkoshi_KD'] = Energy_KD

		Day_energy_percent_A['Dry Energy percent Ko'] = Dry_energy_percent_for_Ko_Annually
		Day_energy_percent_A['Dry Energy percent KD'] = Dry_energy_percent_for_KD_Annually

		Outputs_Ko.to_excel(PSO_Outputs, sheet_name='Outputs_Ko', index=False)
		pso_data1_Ko.to_excel(PSO_Outputs, sheet_name='iter_vs_swamp_vs_fitness_Ko', index=False)
		pso_data2_Ko.to_excel(PSO_Outputs, sheet_name='iter_vs_Global_best_fitness_Ko', index=False)

Parameters['Values'] = [swarmsize, wmax, wmin, C1, C2, X, maxiter, minstep, minfunc, Fitness_value_S3, Fitness_value_S2, Fitness_value_S1, Fitness_value_Dk, Fitness_value_Ko, Dry_energy_percent_for_S3_total, Dry_energy_percent_for_S2_total, Dry_energy_percent_for_S1_total, Dry_energy_percent_for_sk_total, Dry_energy_percent_for_dt_total, Dry_energy_percent_for_MD_total, Dry_energy_percent_for_Ko_total, Dry_energy_percent_for_KD_total]
Parameters.to_excel(PSO_Outputs, sheet_name='Parameters', index=False)
Day_energy_percent_A.to_excel(PSO_Outputs, sheet_name='Dry_Energy', index=False)

Time = pd.DataFrame()
Time['Time'] = [(time.time() - start_time)]
Time.to_excel(PSO_Outputs, sheet_name='Elapsed Time', index=False)

PSO_Outputs.save()

# print('    mycon : {}'.format(mycons(xopt, *args)))

print("time elapsed: {:.2f}s".format(time.time() - start_time))
