import os
import sys
from datetime import date
import csv
import shutil
import fileinput

"""
This script automates Arbin schedule file creation from a text file for 3-step policies.
author: pattia@stanford.edu 
December 4, 2017
"""

# 1. Pull from AWS

# TODO

# 2. Check for CSV with today's date in C://Policies folder
today = date.today().strftime('%Y-%m-%d')
today2 = date.today().strftime('%Y%m%d')
filename = 'C:\\Policies\\' + today + '_policies.csv'
print('Searching for ' + filename)

# If it doesn't exist, quit program
if not os.path.isfile(filename):
	print('No new policy file today')
	quit()

print('New CSV detected - create new schedule files')

# 3. Read in csv
policies = []
with open(filename) as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        policies.append(row)

num_policies = len(policies)

print(str(num_policies) + ' new policies to create')

# 4. Make new folder
foldername = 'C:\\ArbinSoftware\\MITS_PRO\\Work\\' + today + '_tests'
if not os.path.exists(foldername):
	os.makedirs(foldername)
	print('Created new directory: ' + foldername)
else:
	print('Loading files into: ' + foldername)

# 5. Copy and rename template.sdu. 
# Filename should look something like: 20170814-2C_15per_4_4C
for i in range(0,num_policies):
	schedule_file_name = today2 + '-' + policies[i][0] +'C_' \
		+ policies[i][3]+ 'per_' + policies[i][1]+ 'C' \
		+ policies[i][4]+ 'per_' + policies[i][2]+ 'C'
	schedule_file_name = schedule_file_name.replace('.','_')
	schedule_file_name = schedule_file_name + '.sdu'
	print(schedule_file_name)
	shutil.copy2('C:\\Users\\Arbin\\Documents\\GitHub\\'
		+ 'automate-Arbin-schedule-files\\template_3step.sdu', 
		foldername + '\\' + schedule_file_name)

	# 6. Change lines in text file
	# https://stackoverflow.com/questions/4719438/
	# editing-specific-line-in-text-file-in-python

	# Read in the file
	with open(foldername + '\\' + schedule_file_name, 'r') as file:
	    # read a list of lines into data
	    data = file.readlines()

	## Policies

	# CC1: Line 462
	CC1  = round(float(policies[i][0]) * 1.1 * 10000)/10000
	data[461] = 'm_szCtrlValue=' + str(CC1) + '\n'

	# Q1: Line 544
	Q1  = round(float(policies[i][3])/100 * 1.1 * 10000)/10000
	data[543] = 'Equation0_szRight=' + str(Q1) + '\n'

	# CC2: Line 557
	CC2  = round(float(policies[i][1]) * 1.1 * 10000)/10000
	data[556] = 'm_szCtrlValue=' + str(CC2) + '\n'

	# Q2: Line 626
	Q2  = round(float(policies[i][4])/100 * 1.1 * 10000)/10000
	data[625] = 'Equation0_szRight=' + str(Q2) + '\n'

	# CC3: Line 652
	CC3  = round(float(policies[i][2]) * 1.1 * 10000)/10000
	data[651] = 'm_szCtrlValue=' + str(CC3) + '\n'

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

	# and write everything back
	with open(foldername + '\\' + schedule_file_name, 'w') as file:
	    file.writelines( data )

# 7. Batch file?


