import os
import sys
from datetime import date
import csv
import shutil
import fileinput
import numpy as np
import random
import tkinter as tk
from tkinter import filedialog


"""
This script automates Arbin schedule file creation from a text file for 4-step policies.
author: pattia@stanford.edu 
June 19, 2018
"""

today = date.today().strftime('%Y-%m-%d')
today2 = date.today().strftime('%Y%m%d')

root = tk.Tk()
root.withdraw()

filename = filedialog.askopenfilename()

# 1. Check for CSV in current folder
print('Searching for ' + filename)

# If it doesn't exist, quit program
if not os.path.isfile(filename):
	print('Cannot find policy file')
	quit()

print('Create new batch file')

# 2. Read in csv
policies = []
with open(filename) as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        policies.append(row)

num_policies = len(policies)
random.shuffle(policies)

foldername = 'C:\\ArbinSoftware\\MITS_PRO\\Work\\'
batch_file_name = foldername + today2 + '_batch.bth'

shutil.copy2('batch_template.bth', batch_file_name)

# 6. Change lines in text file
# https://stackoverflow.com/questions/4719438/
# editing-specific-line-in-text-file-in-python

# Read in the file
with open(batch_file_name, 'r') as file:
    # read a list of lines into data
    data = file.readlines()

# 4. Copy and rename batch_template.bth
for i in range(0,num_policies):
	# C rates
	C1 = float(policies[i][0])
	C2 = float(policies[i][1])
	C3 = float(policies[i][2])
	C4 = round(0.2/(1/6-(0.2/C1 + 0.2/C2 + 0.2/C3))*1000)/1000

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

	schedule_file_name = '20190124-{0}_{1}_{2}_{3}'.format(C1, C2, C3, C4)
	schedule_file_name = schedule_file_name.replace('.','pt')
	schedule_file_name = schedule_file_name + '.sdu'
	schedule_file_name = schedule_file_name.replace('pt0_','_')
	schedule_file_name = schedule_file_name.replace('pt0.','.')
	print(schedule_file_name)

	data[14+49*i] = "IvChan_"+str(i)+"_m_szScheduleName=2019-01-24_validation\\" + schedule_file_name + "\n"

# and write everything back
with open(batch_file_name, 'w') as file:
	file.writelines(data)