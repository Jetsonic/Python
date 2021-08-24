# SUNKOSHI-3
"""
  Printing and Saving Outputs
  ============================

"""
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
Storage_for_S3, Overflow_for_S3, Evaporation_loss_S3 = Storage3(xopt)
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
Day_energy_percent_for_total = Dry_energy_checkT(xopt)
Day_energy_percent_Annually = Dry_energy_checkA(xopt)
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
        Dry_energy_percent_Annually_for_S3.append(Day_energy_percent_Annually[j])
    Energy_Sunkoshi_3.append(Energy_for_S3[i])
    print("{:<7} {:<7} {:<25}".format(Fyear + j, month, Energy_for_S3[i]))

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

Date = pd.date_range(start='2004-1-1', end='2015-1-1', freq='M').year.tolist()
Date1 = pd.date_range(start='2004-1-1', end='2015-1-1', freq='Y').year.tolist()
Month = pd.date_range(start='2004-1-1', end='2015-1-1', freq='M').month_name().tolist()

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
"""
# SUNKOSHI-2

"""
  Printing and Saving Outputs
  ============================

"""
"""
print('Optimal fitness function value:')
print('    myfunc: {}'.format(fopt))

print('The optimum releases for each stations are:')

Release_Sunkoshi_2 = []
Storage_Sunkoshi_2 = []
Overflow_Sunkoshi_2 = []
Dry_energy_percent_Annually_for_S2 = []
Energy_Sunkoshi_2 = []
Fitness_value = fopt
Inputs = ['swarmsize', 'wmax', 'wmin', 'C1', 'C2', 'X', 'maxiter', 'minstep', 'minfunc', 'Fitness_value','Dry_energy percent Total for S2']

# Optimized Releases
print("{:<7} {:<7} {:<25}".format('Year', 'Months', 'Release at S2'))
j = -1
month = "error"
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

    # print('Year/', 'Months /', 'Release at S2/', 'Release at S2/', 'Release at S1/', 'Release at Smd/', 'Release at Skd/')
    Release_Sunkoshi_2.append(xopt[i])
    print("{:<7} {:<7} {:<25}".format(Fyear + j, month, xopt[i + 0]))

# Storage for optimized Releases
print("{:<10} {:<10} {:<25}".format('Year', 'Months', 'Storage at S2'))
Storage_for_S2, Overflow_for_S2 = Storage2(xopt)
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

    Storage_Sunkoshi_2.append(Storage_for_S2[i])

    print("{:<10} {:<10} {:<25}".format(Fyear + j, month, Storage_for_S2[i]))

# Overflow for Optimized Releases
print("{:<10} {:<10} {:<25}".format('Year', 'Months', 'Overflow at S2'))
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

    Overflow_Sunkoshi_2.append(Overflow_for_S2[i])
    print("{:<10} {:<10} {:<25}".format(Fyear + j, month, Overflow_for_S2[i]))

# Energy generation for Optimized Releases
print("{:<7} {:<7} {:<25}".format('Year', 'Months', 'Energy at S2'))
Day_energy_percent_for_S2_total = Dry_energy_checkT(xopt)
Day_energy_percent_for_S2_Annually = Dry_energy_checkA(xopt)
Energy_for_S2 = E2(xopt)
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
        Dry_energy_percent_Annually_for_S2.append(Day_energy_percent_for_S2_Annually[j])

    Energy_Sunkoshi_2.append(Energy_for_S2[i])
    print("{:<7} {:<7} {:<25}".format(Fyear + j, month, Energy_for_S2[i]))

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
Outputs['Inflows_for_S2'] = Is2
Outputs['Release_Sunkoshi_2'] = Release_Sunkoshi_2
Outputs['Storage_Sunkoshi_2'] = Storage_Sunkoshi_2
Outputs['Overflow_Sunkoshi_2'] = Overflow_Sunkoshi_2
Outputs['Energy_Sunkoshi_2'] = Energy_Sunkoshi_2

Release['Date'] = Date
Release['Month'] = Month
Release['Release_Sunkoshi_2'] = Release_Sunkoshi_2

Storage['Date'] = Date
Storage['Month'] = Month
Storage['Storage_Sunkoshi_2'] = Storage_Sunkoshi_2

Overflow['Date'] = Date
Overflow['Month'] = Month
Overflow['Storage_Sunkoshi_2'] = Overflow_Sunkoshi_2

Energy['Date'] = Date
Energy['Month'] = Month
Energy['Energy_Sunkoshi_2'] = Energy_Sunkoshi_2

Day_energy_percent_A['Date'] = Date1
Day_energy_percent_A['Dry Energy percent S2'] = Day_energy_percent_for_S2_Annually


Parameters.to_excel(PSO_Outputs, sheet_name='Parameters', index=False)
Outputs.to_excel(PSO_Outputs, sheet_name='Outputs', index=False)
Release.to_excel(PSO_Outputs, sheet_name='Release', index=False)
Storage.to_excel(PSO_Outputs, sheet_name='Storage', index=False)
Overflow.to_excel(PSO_Outputs, sheet_name='Overflow', index=False)
Energy.to_excel(PSO_Outputs, sheet_name='Energy', index=False)
pso_data1.to_excel(PSO_Outputs,sheet_name='iter_vs_swamp_vs_fitness', index=False)
pso_data2.to_excel(PSO_Outputs,sheet_name='iter_vs_Global_best_fitness', index=False)
Day_energy_percent_A.to_excel(PSO_Outputs, sheet_name='Dry_Energy', index=False)

Time = pd.DataFrame()
Time['Time'] = [(time.time() - start_time)]
Time.to_excel(PSO_Outputs, sheet_name='Elapsed Time', index=False)

PSO_Outputs.save()
"""
# SUNKOSHI-1

"""
  Printing and Saving Outputs
  ============================

"""
"""
print('Optimal fitness function value:')
print('    myfunc: {}'.format(fopt))

print('The optimum releases for each stations are:')

Release_Sunkoshi_1 = []
Storage_Sunkoshi_1 = []
Overflow_Sunkoshi_1 = []
Dry_energy_percent_Annually_for_S1 = []
Energy_Sunkoshi_1 = []
Fitness_value = fopt
Inputs = ['swarmsize', 'wmax', 'wmin', 'C1', 'C2', 'X', 'maxiter', 'minstep', 'minfunc', 'Fitness_value','Dry_energy percent Total for S1']

# Optimized Releases
print("{:<7} {:<7} {:<25}".format('Year', 'Months', 'Release at S1'))
j = -1
month = "error"
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
	Release_Sunkoshi_1.append(xopt[i + 0])
	print("{:<7} {:<7} {:<25}".format(Fyear + j, month, xopt[i + 0]))

# Storage for optimized Releases
print("{:<10} {:<10} {:<25}".format('Year', 'Months', 'Storage at S1'))
Storage_for_S1, Overflow_for_S1 = Storage1(xopt)
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

	Storage_Sunkoshi_1.append(Storage_for_S1[i])

	print("{:<10} {:<10} {:<25}".format(Fyear + j, month, Storage_for_S1[i]))

# Overflow for Optimized Releases
print("{:<10} {:<10} {:<25}".format('Year', 'Months', 'Overflow at S1'))
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

	Overflow_Sunkoshi_1.append(Overflow_for_S1[i])
	print("{:<10} {:<10} {:<25}".format(Fyear + j, month, Overflow_for_S1[i]))

# Energy generation for Optimized Releases
print("{:<7} {:<7} {:<25}".format('Year', 'Months', 'Energy at S1'))
Day_energy_percent_for_S1_total = Dry_energy_checkT(xopt)
Day_energy_percent_for_S1_Annually = Dry_energy_checkA(xopt)
Energy_for_S1 = E1(xopt)
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
		Dry_energy_percent_Annually_for_S1.append(Day_energy_percent_for_S1_Annually[j])

	Energy_Sunkoshi_1.append(Energy_for_S1[i])
	print("{:<7} {:<7} {:<25}".format(Fyear + j, month, Energy_for_S1[i]))

'''
 Writing to Excel
 =================
 Here,writing the output obtained to excel file PSO_Outputs.xlsx
'''
PSO_Outputs = pd.ExcelWriter('PSO_Outputs_Sunkoshi1_Only.xlsx')

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
Parameters['Values'] = [swarmsize, wmax, wmin, C1, C2, X, maxiter, minstep, minfunc, Fitness_value, Day_energy_percent_for_S1_total]

Outputs['Date'] = Date
Outputs['Month'] = Month
Outputs['Inflows_for_S1'] = Is1
Outputs['Release_Sunkoshi_1'] = Release_Sunkoshi_1
Outputs['Storage_Sunkoshi_1'] = Storage_Sunkoshi_1
Outputs['Overflow_Sunkoshi_1'] = Overflow_Sunkoshi_1
Outputs['Energy_Sunkoshi_1'] = Energy_Sunkoshi_1

Release['Date'] = Date
Release['Month'] = Month
Release['Release_Sunkoshi_1'] = Release_Sunkoshi_1

Storage['Date'] = Date
Storage['Month'] = Month
Storage['Storage_Sunkoshi_1'] = Storage_Sunkoshi_1

Overflow['Date'] = Date
Overflow['Month'] = Month
Overflow['Storage_Sunkoshi_1'] = Overflow_Sunkoshi_1

Energy['Date'] = Date
Energy['Month'] = Month
Energy['Energy_Sunkoshi_1'] = Energy_Sunkoshi_1

Day_energy_percent_A['Date'] = Date1
Day_energy_percent_A['Dry Energy percent S1'] = Day_energy_percent_for_S1_Annually


Parameters.to_excel(PSO_Outputs, sheet_name='Parameters', index=False)
Outputs.to_excel(PSO_Outputs, sheet_name='Outputs', index=False)
Release.to_excel(PSO_Outputs, sheet_name='Release', index=False)
Storage.to_excel(PSO_Outputs, sheet_name='Storage', index=False)
Overflow.to_excel(PSO_Outputs, sheet_name='Overflow', index=False)
Energy.to_excel(PSO_Outputs, sheet_name='Energy', index=False)
pso_data1.to_excel(PSO_Outputs,sheet_name='iter_vs_swamp_vs_fitness', index=False)
pso_data2.to_excel(PSO_Outputs,sheet_name='iter_vs_Global_best_fitness', index=False)
Day_energy_percent_A.to_excel(PSO_Outputs, sheet_name='Dry_Energy', index=False)

Time = pd.DataFrame()
Time['Time'] = [(time.time() - start_time)]
Time.to_excel(PSO_Outputs, sheet_name='Elapsed Time', index=False)


PSO_Outputs.save()
"""
# DUDHKOSHI

"""
  Printing and Saving Outputs
  ============================

"""
"""
print('Optimal fitness function value:')
print('    myfunc: {}'.format(fopt))

print('The optimum releases for each stations are:')

Release_Dudhkoshi_sk = []
Release_Dudhkoshi_dt = []
Storage_Dudhkoshi = []
Overflow_Dudhkoshi = []
Dry_energy_percent_Annually_for_sk = []
Dry_energy_percent_Annually_for_dt = []
Energy_Dudhkoshi_sk = []
Energy_Dudhkoshi_dt = []
Fitness_value = fopt
Inputs = ['swarmsize', 'wmax', 'wmin', 'C1', 'C2', 'X', 'maxiter', 'minstep', 'minfunc', 'fitness', 'Dry_energy percent Total for SK PH', 'Dry_energy percent Total for DT PH']

# Optimized Releases
print("{:<7} {:<7} {:<25} {:<25}".format('Year', 'Months', 'Release at DK_sk', 'Release at DK_dt'))
j = -1
month = "error"
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
	Release_Dudhkoshi_sk.append(xopt[i])
	Release_Dudhkoshi_dt.append(xopt[i + Tmonth])
	print("{:<7} {:<7} {:<25}".format(Fyear + j, month, xopt[i + 0], xopt[Tmonth + i]))

# Storage for optimized Releases
print("{:<10} {:<10} {:<25}".format('Year', 'Months', 'Storage at Dk'))
Storage_for_DK, Overflow_for_DK = Storaged(xopt)
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

	Storage_Dudhkoshi.append(Storage_for_DK[i])
	print("{:<10} {:<10} {:<25}".format(Fyear + j, month, Storage_for_DK[i]))

# Overflow for Optimized Releases
print("{:<10} {:<10} {:<25}".format('Year', 'Months', 'Overflow at Dk'))
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

	Overflow_Dudhkoshi.append(Overflow_for_DK[i])
	print("{:<10} {:<10} {:<25}".format(Fyear + j, month, Overflow_for_DK[i]))

# Energy generation for Optimized Releases
print("{:<7} {:<7} {:<25} {:<25}".format('Year', 'Months', 'Energy at Sk PH', 'Energy at DT PH'))
Day_energy_percent_for_sk_total = Dry_energy_checkT(xopt, c='sk')
Day_energy_percent_for_dt_total = Dry_energy_checkT(xopt, c='dt')
Day_energy_percent_for_sk_Annually = Dry_energy_checkA(xopt, c='sk')
Day_energy_percent_for_dt_Annually = Dry_energy_checkA(xopt, c='dt')
Energy_for_sk = E_sk(xopt)
Energy_for_dt = E_dt(xopt)
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

	Energy_Dudhkoshi_sk.append(Energy_for_sk[i])
	Energy_Dudhkoshi_dt.append(Energy_for_dt[i])
	print("{:<7} {:<7} {:<25}".format(Fyear + j, month, Energy_for_sk[i], Energy_for_dt[i]))

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
"""
# SUNKOSHI 3+2 only

"""
  Printing and Saving Outputs
  ============================

"""
"""
print('Optimal fitness function value:')
print('    myfunc: {}'.format(fopt))

print('The optimum releases for each stations are:')

Release_Sunkoshi_2 = []
Release_Sunkoshi_3 = []
Storage_Sunkoshi_2 = []
Storage_Sunkoshi_3 = []
Overflow_Sunkoshi_2 = []
Overflow_Sunkoshi_3 = []
Dry_energy_percent_Annually_for_S3 = []
Dry_energy_percent_Annually_for_S2 = []
Energy_Sunkoshi_2 = []
Energy_Sunkoshi_3 = []
Fitness_value = fopt
Inputs = ['swarmsize', 'wmax', 'wmin', 'C1', 'C2', 'X', 'maxiter', 'minstep', 'minfunc', 'Fitness_value', 'Dry_energy percent Total for S3', 'Dry_energy percent Total for S2']

# Optimized Releases
print("{:<7} {:<7} {:<25} {:<25}".format('Year', 'Months', 'Release at S3', 'Release at S2'))
j = -1
month = "error"
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
	Release_Sunkoshi_2.append(xopt[i + Tmonth])
	Release_Sunkoshi_3.append(xopt[i])
	print("{:<7} {:<7} {:<25} {:<25}".format(Fyear + j, month, xopt[i], xopt[i + Tmonth]))

# Storage for optimized Releases
print("{:<10} {:<10} {:<25} {:<25}".format('Year', 'Months', 'Storage at S3', 'Storage at S2'))
Storage_for_S2, Overflow_for_S2 = Storage2(xopt)
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

	Storage_Sunkoshi_2.append(Storage_for_S2[i])
	Storage_Sunkoshi_3.append(Storage_for_S3[i])

	print("{:<10} {:<10} {:<25} {:<25}".format(Fyear + j, month, Storage_for_S3[i], Storage_for_S2[i]))

# Overflow for Optimized Releases
print("{:<10} {:<10} {:<25} {:<25}".format('Year', 'Months', 'Overflow at S3', 'Overflow at S2'))
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

	Overflow_Sunkoshi_2.append(Overflow_for_S2[i])
	Overflow_Sunkoshi_3.append(Overflow_for_S3[i])
	print("{:<10} {:<10} {:<25} {:<25}".format(Fyear + j, month, Overflow_for_S3[i], Overflow_for_S2[i]))

# Energy generation for Optimized Releases
print("{:<7} {:<7} {:<25} {:<25}".format('Year', 'Months', 'Energy at S3', 'Energy at S2'))
Day_energy_percent_for_S3_total = Dry_energy_checkT(xopt, c='S3')
Day_energy_percent_for_S2_total = Dry_energy_checkT(xopt, c='S2')
Day_energy_percent_for_S3_Annually = Dry_energy_checkA(xopt, c='S3')
Day_energy_percent_for_S2_Annually = Dry_energy_checkA(xopt, c='S2')
Energy_for_S3 = E3(xopt)
Energy_for_S2 = E2(xopt)
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
		Dry_energy_percent_Annually_for_S3.append(Day_energy_percent_for_S3_Annually[j])
		Dry_energy_percent_Annually_for_S2.append(Day_energy_percent_for_S2_Annually[j])

	Energy_Sunkoshi_2.append(Energy_for_S2[i])
	Energy_Sunkoshi_3.append(Energy_for_S3[i])
	print("{:<7} {:<7} {:<25} {:<25}".format(Fyear + j, month, Energy_for_S3[i], Energy_for_S2[i]))

'''
 Writing to Excel
 =================
 Here,writing the output obtained to excel file PSO_Outputs.xlsx
'''
PSO_Outputs = pd.ExcelWriter('S3+2_2021-8-15.xlsx')

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
Parameters['Values'] = [swarmsize, wmax, wmin, C1, C2, X, maxiter, minstep, minfunc, Fitness_value, Day_energy_percent_for_S3_total, Day_energy_percent_for_S2_total]

Outputs['Date'] = Date
Outputs['Month'] = Month
Outputs['Inflows_for_S3'] = I3
Outputs['Release_Sunkoshi_3'] = Release_Sunkoshi_3
Outputs['Storage_Sunkoshi_3'] = Storage_Sunkoshi_3
Outputs['Overflow_Sunkoshi_3'] = Overflow_Sunkoshi_3
Outputs['Energy_Sunkoshi_3'] = Energy_Sunkoshi_3
Outputs['Inflows_for_S2'] = l2
Outputs['Release_Sunkoshi_2'] = Release_Sunkoshi_2
Outputs['Storage_Sunkoshi_2'] = Storage_Sunkoshi_2
Outputs['Overflow_Sunkoshi_2'] = Overflow_Sunkoshi_2
Outputs['Energy_Sunkoshi_2'] = Energy_Sunkoshi_2

Release['Date'] = Date
Release['Month'] = Month
Release['Release_Sunkoshi_2'] = Release_Sunkoshi_2
Release['Release_Sunkoshi_3'] = Release_Sunkoshi_3

Storage['Date'] = Date
Storage['Month'] = Month
Storage['Storage_Sunkoshi_2'] = Storage_Sunkoshi_2
Storage['Storage_Sunkoshi_3'] = Storage_Sunkoshi_3

Overflow['Date'] = Date
Overflow['Month'] = Month
Overflow['Overflow_Sunkoshi_2'] = Overflow_Sunkoshi_2
Overflow['Overflow_Sunkoshi_3'] = Overflow_Sunkoshi_3

Energy['Date'] = Date
Energy['Month'] = Month
Energy['Energy_Sunkoshi_2'] = Energy_Sunkoshi_2
Energy['Energy_Sunkoshi_3'] = Energy_Sunkoshi_3

Day_energy_percent_A['Date'] = Date1
Day_energy_percent_A['Dry Energy percent S3'] = Day_energy_percent_for_S3_Annually
Day_energy_percent_A['Dry Energy percent S2'] = Day_energy_percent_for_S2_Annually

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
"""
# SUNKOSHI 3+2+MD

"""
  Printing and Saving Outputs
  ============================

"""
"""
print('Optimal fitness function value:')
print('    myfunc: {}'.format(fopt))

print('The optimum releases for each stations are:')

Release_Sunkoshi_2 = []
Release_Sunkoshi_3 = []
Release_Sunkoshi_MD = []
Storage_Sunkoshi_2 = []
Storage_Sunkoshi_3 = []
Overflow_Sunkoshi_2 = []
Overflow_Sunkoshi_3 = []
Dry_energy_percent_Annually_for_S3 = []
Dry_energy_percent_Annually_for_S2 = []
Dry_energy_percent_Annually_for_MD = []
Energy_Sunkoshi_2 = []
Energy_Sunkoshi_3 = []
Energy_Sunkoshi_MD = []
Fitness_value = fopt
Inputs = ['swarmsize', 'wmax', 'wmin', 'C1', 'C2', 'X', 'maxiter', 'minstep', 'minfunc', 'Fitness_value', 'Dry_energy percent Total for S3', 'Dry_energy percent Total for S2', 'Dry_energy percent Total for MD']

# Optimized Releases
print("{:<7} {:<7} {:<25} {:<25} {:<25}".format('Year', 'Months', 'Release at S3', 'Release at S2', 'Release at Smd'))
j = -1
month = "error"
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
	Release_Sunkoshi_2.append(xopt[i + Tmonth])
	Release_Sunkoshi_3.append(xopt[i + 0])
	Release_Sunkoshi_MD.append(xopt[2 * Tmonth + i])
	print("{:<7} {:<7} {:<25} {:<25} {:<25}".format(Fyear + j, month, xopt[i], xopt[i + Tmonth], xopt[i + 2 * Tmonth]))

# Storage for optimized Releases
print("{:<10} {:<10} {:<25} {:<25}".format('Year', 'Months', 'Storage at S3', 'Storage at S2'))
Storage_for_S3, Overflow_for_S3 = Storage3(xopt)
Storage_for_S2, Overflow_for_S2 = Storage2(xopt)
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

	Storage_Sunkoshi_2.append(Storage_for_S2[i])
	Storage_Sunkoshi_3.append(Storage_for_S3[i])

	print("{:<10} {:<10} {:<25} {:<25}".format(Fyear + j, month, Storage_for_S3[i], Storage_for_S2[i]))

# Overflow for Optimized Releases
print("{:<10} {:<10} {:<25} {:<25}".format('Year', 'Months', 'Overflow at S3', 'Overflow at S2'))
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

	Overflow_Sunkoshi_2.append(Overflow_for_S2[i])
	Overflow_Sunkoshi_3.append(Overflow_for_S3[i])
	print("{:<10} {:<10} {:<25} {:<25}".format(Fyear + j, month, Overflow_for_S3[i], Overflow_for_S2[i]))

# Energy generation for Optimized Releases
print("{:<7} {:<7} {:<25} {:<25} {:<25}".format('Year', 'Months', 'Energy at S3', 'Energy at S2', 'Energy at Smd'))
Day_energy_percent_for_S3_total = Dry_energy_checkT(xopt, c='S3')
Day_energy_percent_for_S2_total = Dry_energy_checkT(xopt, c='S2')
Day_energy_percent_for_MD_total = Dry_energy_checkT(xopt, c='MD')
Day_energy_percent_for_S3_Annually = Dry_energy_checkA(xopt, c='S3')
Day_energy_percent_for_S2_Annually = Dry_energy_checkA(xopt, c='S2')
Day_energy_percent_for_MD_Annually = Dry_energy_checkA(xopt, c='MD')
Energy_for_S3 = E3(xopt)
Energy_for_S2 = E2(xopt)
Energy_for_MD = Em(xopt)
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
		Dry_energy_percent_Annually_for_S3.append(Day_energy_percent_for_S3_Annually[j])
		Dry_energy_percent_Annually_for_S2.append(Day_energy_percent_for_S2_Annually[j])
		Dry_energy_percent_Annually_for_MD.append(Day_energy_percent_for_MD_Annually[j])

	Energy_Sunkoshi_2.append(Energy_for_S2[i])
	Energy_Sunkoshi_3.append(Energy_for_S3[i])
	Energy_Sunkoshi_MD.append(Energy_for_MD[i])
	print("{:<7} {:<7} {:<25} {:<25} {:<25}".format(Fyear + j, month, Energy_for_S3[i], Energy_for_S2[i], Energy_for_MD[i]))

'''
 Writing to Excel
 =================
 Here,writing the output obtained to excel file PSO_Outputs.xlsx
'''
PSO_Outputs = pd.ExcelWriter('PSO_output_Sunkoshi_3+2+MD.xlsx')

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
Parameters['Values'] = [swarmsize, wmax, wmin, C1, C2, X, maxiter, minstep, minfunc, Fitness_value, Day_energy_percent_for_S3_total, Day_energy_percent_for_S2_total, Day_energy_percent_for_MD_total]

Outputs['Date'] = Date
Outputs['Month'] = Month
Outputs['Inflows_for_S3'] = I3
Outputs['Release_Sunkoshi_3'] = Release_Sunkoshi_3
Outputs['Storage_Sunkoshi_3'] = Storage_Sunkoshi_3
Outputs['Overflow_Sunkoshi_3'] = Overflow_Sunkoshi_3
Outputs['Energy_Sunkoshi_3'] = Energy_Sunkoshi_3
Outputs['Inflows_for_S2'] = l2
Outputs['Release_Sunkoshi_2'] = Release_Sunkoshi_2
Outputs['Storage_Sunkoshi_2'] = Storage_Sunkoshi_2
Outputs['Overflow_Sunkoshi_2'] = Overflow_Sunkoshi_2
Outputs['Energy_Sunkoshi_2'] = Energy_Sunkoshi_2
Outputs['Release_Sunkoshi_MD'] = Release_Sunkoshi_MD
Outputs['Energy_Sunkoshi_MD'] = Energy_Sunkoshi_MD

Release['Date'] = Date
Release['Month'] = Month
Release['Release_Sunkoshi_2'] = Release_Sunkoshi_2
Release['Release_Sunkoshi_3'] = Release_Sunkoshi_3
Release['Release_Sunkoshi_MD'] = Release_Sunkoshi_MD

Storage['Date'] = Date
Storage['Month'] = Month
Storage['Storage_Sunkoshi_2'] = Storage_Sunkoshi_2
Storage['Storage_Sunkoshi_3'] = Storage_Sunkoshi_3

Overflow['Date'] = Date
Overflow['Month'] = Month
Overflow['Overflow_Sunkoshi_2'] = Overflow_Sunkoshi_2
Overflow['Overflow_Sunkoshi_3'] = Overflow_Sunkoshi_3

Energy['Date'] = Date
Energy['Month'] = Month
Energy['Energy_Sunkoshi_2'] = Energy_Sunkoshi_2
Energy['Energy_Sunkoshi_3'] = Energy_Sunkoshi_3
Energy['Energy_Sunkoshi_MD'] = Energy_Sunkoshi_MD

Day_energy_percent_A['Date'] = Date1
Day_energy_percent_A['Dry Energy percent S3'] = Day_energy_percent_for_S3_Annually
Day_energy_percent_A['Dry Energy percent S2'] = Day_energy_percent_for_S2_Annually
Day_energy_percent_A['Dry Energy percent MD'] = Day_energy_percent_for_MD_Annually

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
"""
# SUNKOSHI 1+2+3+MD + DUDHKOSHI

"""
  Printing and Saving Outputs
  ============================

"""
"""
print('Optimal fitness function value:')
print('    myfunc: {}'.format(fopt))

print('The optimum releases for each stations are:')

Release_Sunkoshi_1 = []
Release_Sunkoshi_2 = []
Release_Sunkoshi_3 = []
Release_Sunkoshi_MD = []
Release_Dudhkoshi_sk = []
Release_Dudhkoshi_dt = []

Storage_Sunkoshi_1 = []
Storage_Sunkoshi_2 = []
Storage_Sunkoshi_3 = []
Storage_Dudhkoshi = []

Overflow_Sunkoshi_1 = []
Overflow_Sunkoshi_2 = []
Overflow_Sunkoshi_3 = []
Overflow_Dudhkoshi = []

Dry_energy_percent_for_S3_Annually = []
Dry_energy_percent_for_S2_Annually = []
Dry_energy_percent_for_S1_Annually = []
Dry_energy_percent_for_MD_Annually = []
Dry_energy_percent_for_sk_Annually = []
Dry_energy_percent_for_dt_Annually = []

Energy_Sunkoshi_1 = []
Energy_Sunkoshi_2 = []
Energy_Sunkoshi_3 = []
Energy_Sunkoshi_MD = []
Energy_Dudhkoshi_sk = []
Energy_Dudhkoshi_dt = []

Fitness_value = fopt

Inputs = ['swarmsize', 'wmax', 'wmin', 'C1', 'C2', 'X', 'maxiter', 'minstep', 'minfunc', 'Fitness_value', 'Dry_energy percent Total for S3', 'Dry_energy percent Total for S2', 'Dry_energy percent Total for S1', 'Dry_energy percent Total for SK PH', 'Dry_energy percent Total for DT PH', 'Dry_energy percent Total for MD']

# Optimized Releases
print("{:<7} {:<7} {:<25} {:<25} {:<25} {:<25} {:<25} {:<25}".format('Year', 'Months', 'Release at S3', 'Release at S2', 'Release at S1', 'Release at DK-sk', 'Release at DK-dt', 'Release at Smd'))
j = -1
month = "error"
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
    Release_Sunkoshi_3.append(xopt[i + 0])
    Release_Sunkoshi_2.append(xopt[i + Tmonth])
    Release_Sunkoshi_1.append(xopt[i + 2 * Tmonth])
    Release_Dudhkoshi_sk.append(xopt[i + 3 * Tmonth])
    Release_Dudhkoshi_dt.append(xopt[i + 4 * Tmonth])
    Release_Sunkoshi_MD.append(xopt[i + 5 * Tmonth])

    print("{:<7} {:<7} {:<25} {:<25} {:<25} {:<25} {:<25} {:<25}".format(Fyear + j, month, xopt[i + 0], xopt[i + Tmonth], xopt[i + Tmonth * 2], xopt[i + Tmonth * 3], xopt[i + Tmonth * 4], xopt[i + Tmonth * 5]))

# Storage for optimized Releases
print("{:<10} {:<10} {:<25} {:<25} {:<25} {:<25}".format('Year', 'Months', 'Storage at S3', 'Storage at S2', 'Storage at S1', 'Storage at DK'))
Storage_for_S3, Overflow_for_S3, Evaporation_loss_S3 = Storage3(xopt)
Storage_for_S2, Overflow_for_S2, Evaporation_loss_S2 = Storage2(xopt)
Storage_for_DK, Overflow_for_DK, Evaporation_loss_Dk = Storaged(xopt)
Storage_for_S1, Overflow_for_S1, Evaporation_loss_S1 = Storage1(xopt)
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
    Storage_Sunkoshi_2.append(Storage_for_S2[i])
    Storage_Dudhkoshi.append(Storage_for_DK[i])
    Storage_Sunkoshi_1.append(Storage_for_S1[i])

    print("{:<10} {:<10} {:<25} {:<25} {:<25} {:<25}".format(Fyear + j, month, Storage_for_S3[i], Storage_for_S2[i], Storage_for_S1[i], Storage_for_DK[i]))

# Overflow for Optimized Releases
print("{:<10} {:<10} {:<25} {:<25} {:<25} {:<25}".format('Year', 'Months', 'Overflow at S3', 'Overflow at S2', 'Overflow at S1', 'Overflow at Dk'))
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
    Overflow_Sunkoshi_2.append(Overflow_for_S2[i])
    Overflow_Dudhkoshi.append(Overflow_for_DK[i])
    Overflow_Sunkoshi_1.append(Overflow_for_S1[i])
    print("{:<10} {:<10} {:<25} {:<25} {:<25} {:<25}".format(Fyear + j, month, Overflow_for_S3[i], Overflow_for_S2[i], Overflow_for_S1[i], Overflow_for_DK[i]))

# Energy generation for Optimized Releases
print("{:<7} {:<7} {:<25} {:<25} {:<25} {:<25} {:<25}".format('Year', 'Months', 'Energy at S3', 'Energy at S2', 'Energy at S1', 'Energy at Smd', 'Energy at Skd'))

Day_energy_percent_for_S3_total = Dry_energy_checkT(xopt, c='S3')
Day_energy_percent_for_S2_total = Dry_energy_checkT(xopt, c='S2')
Day_energy_percent_for_S1_total = Dry_energy_checkT(xopt, c='S1')
Day_energy_percent_for_sk_total = Dry_energy_checkT(xopt, c='sk')
Day_energy_percent_for_dt_total = Dry_energy_checkT(xopt, c='dt')
Day_energy_percent_for_MD_total = Dry_energy_checkT(xopt, c='MD')

Day_energy_percent_for_S3_Annually = Dry_energy_checkA(xopt, c='S3')
Day_energy_percent_for_S2_Annually = Dry_energy_checkA(xopt, c='S2')
Day_energy_percent_for_S1_Annually = Dry_energy_checkA(xopt, c='S1')
Day_energy_percent_for_sk_Annually = Dry_energy_checkA(xopt, c='sk')
Day_energy_percent_for_dt_Annually = Dry_energy_checkA(xopt, c='dt')
Day_energy_percent_for_MD_Annually = Dry_energy_checkA(xopt, c='MD')

Energy_for_S3 = E3(xopt)
Energy_for_S2 = E2(xopt)
Energy_for_S1 = E1(xopt)
Energy_for_sk = E_sk(xopt)
Energy_for_dt = E_dt(xopt)
Energy_for_MD = Em(xopt)

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
        Dry_energy_percent_for_S3_Annually.append(Day_energy_percent_for_S3_Annually[j])
        Dry_energy_percent_for_S2_Annually.append(Day_energy_percent_for_S2_Annually[j])
        Dry_energy_percent_for_S1_Annually.append(Day_energy_percent_for_S1_Annually[j])
        Dry_energy_percent_for_sk_Annually.append(Day_energy_percent_for_sk_Annually[j])
        Dry_energy_percent_for_dt_Annually.append(Day_energy_percent_for_dt_Annually[j])
        Dry_energy_percent_for_MD_Annually.append(Day_energy_percent_for_MD_Annually[j])

    Energy_Sunkoshi_3.append(Energy_for_S3[i])
    Energy_Sunkoshi_2.append(Energy_for_S2[i])
    Energy_Sunkoshi_1.append(Energy_for_S1[i])
    Energy_Dudhkoshi_sk.append(Energy_for_sk[i])
    Energy_Dudhkoshi_dt.append(Energy_for_dt[i])
    Energy_Sunkoshi_MD.append(Energy_for_MD[i])
    print("{:<7} {:<7} {:<25} {:<25} {:<25} {:<25} {:<25} {:<25}".format(Fyear + j, month, Energy_for_S3[i], Energy_for_S2[i], Energy_for_S1[i], Energy_for_sk[i], Energy_for_dt[i], Energy_for_MD[i]))

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

Date = pd.date_range(start='1985-1-1', end='2015-1-1', freq='M').year.tolist()
Date1 = pd.date_range(start='1985-1-1', end='2015-1-1', freq='Y').year.tolist()
Month = pd.date_range(start='1985-1-1', end='2015-1-1', freq='M').month_name().tolist()

Parameters['Parameters'] = Inputs
Parameters['Values'] = [swarmsize, wmax, wmin, C1, C2, X, maxiter, minstep, minfunc, Fitness_value, Day_energy_percent_for_S3_total, Day_energy_percent_for_S2_total, Day_energy_percent_for_S1_total, Day_energy_percent_for_sk_total, Day_energy_percent_for_dt_total, Day_energy_percent_for_MD_total]

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

Outputs['Release_Sunkoshi_MD'] = Release_Sunkoshi_MD
Outputs['Energy_Sunkoshi_MD'] = Energy_Sunkoshi_MD

Release['Date'] = Date
Release['Month'] = Month
Release['Release_Sunkoshi_3'] = Release_Sunkoshi_3
Release['Release_Sunkoshi_2'] = Release_Sunkoshi_2
Release['Release_Sunkoshi_MD'] = Release_Sunkoshi_MD
Release['Release_Dudhkoshi_sk'] = Release_Dudhkoshi_sk
Release['Release_Dudhkoshi_dt'] = Release_Dudhkoshi_dt
Release['Release_Sunkoshi_1'] = Release_Sunkoshi_1

Storage['Date'] = Date
Storage['Month'] = Month
Storage['Storage_Sunkoshi_3'] = Storage_Sunkoshi_3
Storage['Storage_Sunkoshi_2'] = Storage_Sunkoshi_2
Storage['Storage_Dudhkoshi'] = Storage_Dudhkoshi
Storage['Storage_Sunkoshi_1'] = Storage_Sunkoshi_1

Overflow['Date'] = Date
Overflow['Month'] = Month
Overflow['Storage_Sunkoshi_3'] = Overflow_Sunkoshi_3
Overflow['Storage_Sunkoshi_2'] = Overflow_Sunkoshi_2
Overflow['Overflow_Dudhkoshi'] = Overflow_Dudhkoshi
Overflow['Storage_Sunkoshi_1'] = Overflow_Sunkoshi_1

Energy['Date'] = Date
Energy['Month'] = Month
Energy['Energy_Sunkoshi_3'] = Energy_Sunkoshi_3
Energy['Energy_Sunkoshi_2'] = Energy_Sunkoshi_2
Energy['Energy_Dudhkoshi_sk'] = Energy_Dudhkoshi_sk
Energy['Energy_Dudhkoshi_dt'] = Energy_Dudhkoshi_dt
Energy['Energy_Sunkoshi_1'] = Energy_Sunkoshi_1
Energy['Energy_Sunkoshi_MD'] = Energy_Sunkoshi_MD

Day_energy_percent_A['Date'] = Date1
Day_energy_percent_A['Dry Energy percent S3'] = Day_energy_percent_for_S3_Annually
Day_energy_percent_A['Dry Energy percent S2'] = Day_energy_percent_for_S2_Annually
Day_energy_percent_A['Dry Energy percent sk'] = Day_energy_percent_for_sk_Annually
Day_energy_percent_A['Dry Energy percent dt'] = Day_energy_percent_for_dt_Annually
Day_energy_percent_A['Dry Energy percent S1'] = Day_energy_percent_for_S1_Annually
Day_energy_percent_A['Dry Energy percent MD'] = Day_energy_percent_for_MD_Annually

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
"""
