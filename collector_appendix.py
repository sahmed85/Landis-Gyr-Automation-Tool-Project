#!c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe
############################################################################################
#File: collector_appendix.py
#Name: Shad Ahmed
#Date Created: 3/5/2020
#Last Modified: 04/29/2020  
#Usage: Internal | localhost -> to be used externally
#Overview: This file is a python script using CGI to compute table of collector count. 
#Github/Git: sahmed85/ | *this is a private repo*
#Project: UpgradePlanTool
############################################################################################### 

import pandas as pd 
from openpyxl import load_workbook
import numpy as np 
import sys

try: 
	###############################################################################################################################
	# This reads in the excel file and computes a pivot table to be returned to the appropiate html. Throws an error if failed to 
	# read the file.
	###############################################################################################################################
	#################collector devices
	df_collectors = pd.read_excel('C:/wamp64/www/upgradeplantool/uploads/{session_id}_collectors.xlsx'.format(session_id = sys.argv[1]))
	df_collectors = df_collectors.replace(np.nan,'(blank)',regex=True)
	collector_info = {}

	for ind in df_collectors.index:
		devicetype = str(df_collectors["Device Sub Type"][ind])
		devicename = str(df_collectors["Device Name"][ind])
		if devicetype not in collector_info.keys():
			collector_info[devicetype]= {devicename:1}
		else:
			if devicename in collector_info[devicetype].keys():
				collector_info[devicetype][devicename] += 1
			else:
				collector_info[devicetype].update({devicename:1})

	collector_table = pd.DataFrame(columns=['Device Sub Type', 'Device Name', 'Count of Device Sub Type'])

	temp_namelist = []
	temp_countlist = []

	for key in collector_info:
		if len(collector_table) == 0:
			device_pos = len(collector_table)
		else:
			device_pos = len(collector_table) 
		for device_key in collector_info[key]:
			collector_table = collector_table.append({'Count of Device Sub Type': collector_info[key][device_key], 'Device Name': device_key}, ignore_index = True)
		collector_table.at[len(collector_table)+1,'Device Sub Type'] = key + " Total:"
		collector_table.at[len(collector_table), 'Count of Device Sub Type'] = len(collector_info[key].values())
		collector_table.at[device_pos, 'Device Sub Type'] = key 

	collector_table = collector_table.replace(np.nan,'',regex=True)
	collector_table
	#print(collector_table)
	print(collector_table.to_html(index=False))

except Exception as error:
	print("""<h5> <span class= "glyphicon glyphicon-remove"> </span> Connection ERROR 202 </h5> """)
	print("""{error_message} """.format(error_message=error))
	exit()
