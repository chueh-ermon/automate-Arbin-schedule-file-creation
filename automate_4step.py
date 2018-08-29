import os
import sys
from datetime import date
import csv
import shutil
import fileinput
import numpy as np

"""
This script automates Arbin schedule file creation from a text file for 4-step policies.
author: pattia@stanford.edu 
August 28, 2018
"""

today = date.today().strftime('%Y-%m-%d')
today2 = date.today().strftime('%Y%m%d')
filename = 'policies_all.csv'

# 1. Check for CSV in current folder 'policies.csv'
print('Searching for ' + filename)

# If it doesn't exist, quit program
if not os.path.isfile(filename):
	print('Cannot find policy file')
	quit()

print('Create new schedule files')

# 2. Read in csv
policies = []
with open(filename) as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        policies.append(row)

num_policies = len(policies)

print(str(num_policies) + ' new policies to create')

# 3. Make new folder
# foldername = 'C:\\ArbinSoftware\\MITS_PRO\\Work\\' + today + '_tests'
foldername = 'C:\\ArbinSoftware\\MITS_PRO\\Work\\OED'
if not os.path.exists(foldername):
	os.makedirs(foldername)
	print('Created new directory: ' + foldername)
else:
	print('Loading files into: ' + foldername)

# 4. Copy and rename template_4step.sdu. 
# Filename should look something like: 20180619-5pt2_5pt6_3_4pt8
for i in range(0,num_policies):
	# C rates
	C1 = float(policies[i][0])
	C2 = float(policies[i][1])
	C3 = float(policies[i][2])
	C4 = float(policies[i][3])

	# Currents
	CC1 = round(C1 * 1.1 * 10000)/10000
	CC2 = round(C2 * 1.1 * 10000)/10000
	CC3 = round(C3 * 1.1 * 10000)/10000
	CC4 = round(C4 * 1.1 * 10000)/10000

	"""
	print(policies[i][:])
	print('  ', C1, C2, C3, C4)
	print('  ', CC1, CC2, CC3, CC4)
	"""

	schedule_file_name = today2 + '-{0}_{1}_{2}_{3}'.format(C1, C2, C3, C4)
	schedule_file_name = schedule_file_name.replace('.','pt')
	schedule_file_name = schedule_file_name + '.sdu'
	schedule_file_name = schedule_file_name.replace('pt0_','_')
	schedule_file_name = schedule_file_name.replace('pt0.','.')
	print(schedule_file_name)
	shutil.copy2('template_4step.sdu', foldername + '\\' + schedule_file_name)

	# 6. Change lines in text file
	# https://stackoverflow.com/questions/4719438/
	# editing-specific-line-in-text-file-in-python

	# Read in the file
	with open(foldername + '\\' + schedule_file_name, 'r') as file:
	    # read a list of lines into data
	    data = file.readlines()

	## Policy-specific currents
	# CC1: Line 237
	data[236] = 'm_szCtrlValue=' + str(CC1) + '\n'
	# CC2: Line 322
	data[321] = 'm_szCtrlValue=' + str(CC2) + '\n'
	# CC3: Line 407
	data[406] = 'm_szCtrlValue=' + str(CC3) + '\n'
	# CC4: Line 492
	data[491] = 'm_szCtrlValue=' + str(CC4) + '\n'

	"""
	For now, we are keeping all current ranges as Range1
	## Current ranges

	# CC1 current range: Line 460
	if float(policies[i][0])*1.1 > 6:
		data[459] = 'm_szCurrentRange=Range1\n'
	else:
		data[459] = 'm_szCurrentRange=Range2\n'

	# CC2 current range: Line 555
	if float(policies[i][1])*1.1 > 6:
		data[554] = 'm_szCurrentRange=Range1\n'
	else:
		data[554] = 'm_szCurrentRange=Range2\n'

	# CC3 current range: Line 650
	if float(policies[i][2])*1.1 > 6:
		data[649] = 'm_szCurrentRange=Range1\n'
	else:
		data[649] = 'm_szCurrentRange=Range2\n'
	"""

	# and write everything back
	with open(foldername + '\\' + schedule_file_name, 'w') as file:
	    file.writelines( data )