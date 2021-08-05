import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import Testing

start_time = time.time()

"""
  Initialization
  ===============
   Input following commands on python console
     pip install pyswarm
     pip install numpy
     Make sure data_pso python file is in same folder as this file.

   Parameters
   ===============
    Following are preset initial parameters.
    They can be changed here.
'''
     swarmsize = 100  : It defines the size of swarm taken for pso search
     omega = 0.5    : Particle velocity scaling factor
     phip = 0.5     : Scaling factor to search away from the particle's best known position
     phig = 0.5     : Scaling factor to search away from the swarm's best known position
     maxiter = 100    : It limits the search to stated iteration
     minstep = 1e-2 : Its a limit to search such that change in optimized value is equal or less then search is stopped
     minfunc = 1e-2 : Its a limit to search such that change in optimization function value is equal or less then search is stopped

"""
swarmsize = 2000
wmax = 1
wmin = 1
C1 = 1
C2 = 0.5
X = 0.9
maxiter = 500
minstep = 1e-20
minfunc = 1e-20

from Testing import pso
#from pyswarm import pso
from data_pso import Interpolate, I3, l1, l2, Ex1, Ex2, Ex3, Tyear, Fyear

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
     Qk = Release from Sunkoshi Kamala diversion at time t
     Hk = Height of Sunkoshi Kamala diversion water head at time t

"""

"""
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
     e3     : Energy output by Sunkoshi-3 at time t, is in KWh
     e2     : Energy output by Sunkoshi-2 at time t, is in KWh
     e1     : Energy output by Sunkoshi-1 at time t, is in KWh
     Qme    : Energy output by Sunkoshi Marine Diversion at time t, is in KWh
     Qke    : Energy output by Sunkoshi Kamala Diversion at time t, is in KWh
     ev     : Evaporation in mm per month
"""

p = 9810
f = 0.9  # Turbine efficiency
S3max = 1769.286774  # h = 700
S3min = 769.457152  # h = 660
S3_twl = 535
dt = 30 * 24 * 60 * 60  # numbers of hours per month
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

   We have Ovariables = 5 Releases to optimize each month R3, R2, R1, Qm and Qk which takes total size of
   optimized values to : Tmonth * Ovariables = T_O_V

     lb  : Lower bound for pso search for all T_O_V optimization values
     ub  : upper bound for pso search for all T_O_V optimization values     
     cons: Stores constrains output can be used to check errors 
"""


def listmaker(n):
    listofzeros = [0] * n
    return listofzeros


Tmonth = Tyear * 12
Ovariables = 1
T_O_V = Tmonth * Ovariables
S3 = listmaker(Tmonth + 1)
S3[0] = S3min  # taking initial condition as minimun storage
# Ev3 = listmaker(492)
# Ev2 = listmaker(492)
# Ev1 = listmaker(492)
O3 = listmaker(Tmonth)
H3 = listmaker(Tmonth)
e3 = listmaker(Tmonth)
lb = listmaker(T_O_V)
ub = listmaker(T_O_V)
cons = listmaker(0)
z_each_year = []
# Giving upper and lower value for pso search function,here limit on irrigation and release output can de defined.
"""
  ub-lb Section
  ==============
   Here each optimization values (i.e Releases) are given:
    lb : lower bound
    ub : upper bound

   following code facilities this process such that these bounds can be given for each releases for each month. 
"""

for i in range(0, T_O_V):
    ub[i] = 1288  # bonds for jan in Sunkoshi-3
    lb[i] = 0  # bonds for jan in Sunkoshi-3

"""
  Objective function
  ===================

  The algorithm Swarm searches for minimum value value so objective function is multiplied by -1

  From T_O_V optimized values
  ---------------------------
    Values that are indexed in range [0-Tmonth] are stored in R3 
    Values that are indexed in range [Tmonth-2*Tmonth] are stored in R2
    Values that are indexed in range [2*Tmonth-3*Tmonth] are stored in R1
    Values that are indexed in range [3*Tmonth-4*Tmonth] are stored in Qm
    Values that are indexed in range [4*Tmonth-5*Tmonth] are stored in Qk

  Here the value of releases are in MCM per month.
  Fitness function gives the total amount energy potential that can be generated when input parameters and optimized released are used as operation policy.

"""
ita = 0.86  # Efficiency of Hydro-Electric plant
g = 9.810  # Acceleration due to gravity
PF_dry = 0.5  # Plant Factor
power = 683  # Installed Capacity
seconds_per_month = 2.6298 * 10 ** 6


def Fitnessfunc(x, *args):
    z = 0
    z_dry = 0
    z_wet = 0
    R3 = (x * 10 ** 6) / seconds_per_month
    H3 = Height3(x, *args)
    for i in range(Tmonth):
        if i % 12 == 0 or i % 12 == 1 or i % 12 == 2 or i % 12 == 3 or i % 12 == 4 or i % 12 == 11:
            z_dry = (1 - (g * ita * R3[i] / 1000 * H3[i]) / power)
        elif i % 12 == 5 or i % 12 == 6 or i % 12 == 7 or i % 12 == 8 or i % 12 == 9 or i % 12 == 10:
            z_wet = (1 - (g * ita * R3[i] / 1000 * H3[i]) / power)
        Total = z_dry + z_wet
        z += Total
    return z


# objective function maximizing power production
#def Fitnessfunc(x, *args):
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


def Dry_energy_check(x):
    count1 = 0
    count2 = 0
    z_dry = 0
    z_wet = 0
    dry_percent_total = 0
    z_dry_total = 0
    z_wet_total = 0
    R3 = (x * 10 ** 6) / seconds_per_month
    H3 = Height3(x, *args)
    for i in range(Tmonth):
        if i % 12 == 0 or i % 12 == 1 or i % 12 == 2 or i % 12 == 3 or i % 12 == 4 or i % 12 == 11:
            z_dry += (g * ita * R3[i] / 1000 * H3[i])
            if i % 12 == 11:
                count1 += dry_energy_less_than_35(z_dry, z_wet)
                count2 += dry_energy_more_than_50(z_dry, z_wet)
                z_dry_total += z_dry
                z_wet_total += z_wet
                z_dry = 0
                z_wet = 0
        elif i % 12 == 5 or i % 12 == 6 or i % 12 == 7 or i % 12 == 8 or i % 12 == 9 or i % 12 == 10:
            z_wet += (g * ita * R3[i] / 1000 * H3[i])
    dry_percent_total = dry_energy(z_dry_total, z_wet_total)
    return count1, count2, dry_percent_total


def dry_energy(z_dry_total, z_wet_total):
    dry_percent_total = (z_dry_total / (z_dry_total + z_wet_total) * 100)
    return dry_percent_total


def dry_energy_less_than_35(z_dry, z_wet):
    if (z_dry / (z_dry + z_wet) * 100) < 30:
        return 1
    else:
        return 0


def dry_energy_more_than_50(z_dry, z_wet):
    if (z_dry / (z_dry + z_wet) * 100) > 50:
        return 1
    else:
        return 0


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
def Storage3(x, *args):
    R3 = x
    j = 0
    # p, H3, Hm, H2, H1, Hk, I3, It, Id = args
    for i in range(Tmonth):
        Ev3 = Evaporation3(S3[i], j)
        S3[i + 1] = I3[i] + S3[i] - (R3[i] - Ev3)
        n = S3[i+1]
        if n < S3min:
            m = S3min - n
            R3[i] = R3[i]-m
            S3[i+1] = S3min
        if S3max > S3[i + 1] > S3min:
            O3[i] = 0
        elif S3[i + 1] > S3max:
            O3[i] = S3[i + 1] - S3max
            S3[i + 1] = S3max
        j += 1
        if j == 12:
            j = 0
    return S3



"""
  Energy
  =======
   Energy = P * release * Net head
"""


# Energy output per month for Sunkoshi 3
def E3(x, *args):
    R3 = (x * 10 ** 6) / seconds_per_month
    H3 = Height3(x, *args)
    # p, H3, Hm, H2, H1, Hk, I3, It, Id = args
    for i in range(Tmonth):
        e3[i] = g * ita * R3[i] / 1000 * H3[i]
    return e3


"""
  Height
  =======
   Height function H=f(storage)
   Obtained from H-V-A curve
"""


# Height for Sunkoshi-3
def Height3(x, *args):
    S3 = Storage3(x, *args)
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


"""                          
  Constrains
  ===========
   Since constrain for storage is addressed in storage function it is no longer need to address here.
   Here Constrain for maximum energy is checked.
   constrains for irrigation demand can be addressed in [ld - ub] section.

"""


# all constrains required
def mycons(x, *args):
    e3 = E3(x, *args)  # Energy Constrains
    cons = []
    for i in range(Tmonth):
        a = [683 - e3[i]]
        cons.extend(a)
    return cons


args = (p, H3, I3)

# calling pso function in pso.py

xopt, fopt = pso(Fitnessfunc, lb, ub, args=args, f_ieqcons=mycons, swarmsize=swarmsize, wmax=wmax, wmin=wmin, c1=C1, c2=C2, X=X, maxiter=maxiter, minstep=minstep, minfunc=minfunc, debug=False)

a, b, c = Dry_energy_check(xopt)
print("Number of years with dry energy less than 35% of total energy:", a)
print("Number of years with dry energy more than 50% of total energy:", b)
print("Total Percent of dry energy:", c)
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
Energy_Sunkoshi_3 = []
Fitness_value = fopt
Parameters = ['swarmsize', 'wmax', 'wmin', 'C1', 'C2', 'X', 'maxiter', 'minstep', 'minfunc', 'Fitness_value']

# Optimized Releases
print("{:<7} {:<7} {:<25}".format('Year', 'Months', 'Release at S3'))
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

    # print('Year/', 'Months /', 'Release at S3/', 'Release at S2/', 'Release at S1/', 'Release at Smd/', 'Release at Skd/')
    Release_Sunkoshi_3.append(xopt[i])
    print("{:<7} {:<7} {:<25}".format(Fyear + j, month, xopt[i]))

# Storage for optimized Releases
print("{:<10} {:<10} {:<25}".format('Year', 'Months', 'Storage at S3'))
S3 = Storage3(xopt, *args)
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

    Storage_Sunkoshi_3.append(S3[i])

    print("{:<10} {:<10} {:<25}".format(Fyear + j, month, S3[i]))

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

    Overflow_Sunkoshi_3.append(O3[i])
    print("{:<10} {:<10} {:<25}".format(Fyear + j, month, O3[i]))

# Energy generation for Optimized Releases
print("{:<7} {:<7} {:<25}".format('Year', 'Months', 'Energy at S3'))
e3 = E3(xopt, *args)
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

    Energy_Sunkoshi_3.append(e3[i])
    print("{:<7} {:<7} {:<25}".format(Fyear + j, month, e3[i]))

'''
 Writing to Excel
 =================
 Here,writing the output obtained to excel file PSO_Outputs.xlsx
'''
PSO_Outputs = pd.ExcelWriter('PSO_Outputs_Sunkoshi31_Only.xlsx')

Inputs = pd.DataFrame()
Storage = pd.DataFrame()
Release = pd.DataFrame()
Overflow = pd.DataFrame()
Energy = pd.DataFrame()

Date = pd.date_range(start='1968-1-1', end='2015-1-1', freq='M').date.tolist()
Month = pd.date_range(start='1968-1-1', end='2015-1-1', freq='M').month_name().tolist()

Inputs['Parameters'] = Parameters
Inputs['Values'] = [swarmsize, wmax, wmin, C1, C2, X, maxiter, minstep, minfunc, Fitness_value]

Release['Date'] = Date
Release['Month'] = Month
Release['Release_Sunkoshi_3'] = Release_Sunkoshi_3

Storage['Date'] = Date
Storage['Month'] = Month
Storage['Storage_Sunkoshi_3'] = Storage_Sunkoshi_3

Overflow['Date'] = Date
Overflow['Month'] = Month
Overflow['Storage_Sunkoshi_3'] = Overflow_Sunkoshi_3

Energy['Date'] = Date
Energy['Month'] = Month
Energy['Energy_Sunkoshi_3'] = Energy_Sunkoshi_3

Inputs.to_excel(PSO_Outputs, sheet_name='Inputs', index=False)
Release.to_excel(PSO_Outputs, sheet_name='Release', index=False)
Storage.to_excel(PSO_Outputs, sheet_name='Storage', index=False)
Overflow.to_excel(PSO_Outputs, sheet_name='Overflow', index=False)
Energy.to_excel(PSO_Outputs, sheet_name='Energy', index=False)

PSO_Outputs.save()

# print('    mycon : {}'.format(mycons(xopt, *args)))

print("time elapsed: {:.2f}s".format(time.time() - start_time))
