#!c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe
############################################################################################
#File: router_appendix.py
#Name: Shad Ahmed
#Date Created: 3//2020
#Last Modified: 04/29/2020 
#Usage: Internal | localhost -> to be used externally
#Overview: This file is a python script using CGI to compute table of router count. 
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
	############network devices
	df_networks = pd.read_excel('C:/wamp64/www/upgradeplantool/uploads/{session_id}_network.xlsx'.format(session_id = sys.argv[1]))
	df_networks = df_networks.replace(np.nan,'(blank)',regex=True)
	network_info = {}

	for ind in df_networks.index:
		hardware_model = str(df_networks["Hardware Model"][ind])
		firmware_version = str(df_networks["Firmware Version"][ind])
		dcw_version = str(df_networks["DCW Version"][ind])
		if hardware_model not in network_info:
			network_info[hardware_model] = {firmware_version:{dcw_version:1}}
		elif firmware_version not in network_info[hardware_model]:
			network_info[hardware_model][firmware_version] = {dcw_version:1}
		elif dcw_version not in network_info[hardware_model][firmware_version]:
			network_info[hardware_model][firmware_version][dcw_version] = 1
		else:
			network_info[hardware_model][firmware_version][dcw_version] += 1

	network_table = pd.DataFrame(columns=['Router Model','Firmware Version','DCW Version','Router Count'])
	total = 0
	for key in network_info:
		if len(network_table) == 0:
			model_pos = len(network_table)
		else:
			model_pos = len(network_table) 
		local_total = 0
		for key_firmware in network_info[key]:
			for key_dcw in network_info[key][key_firmware]:
				if len(network_table) == 0:
					fw_pos = len(network_table)
					total_pos = fw_pos + len(network_info[key][key_firmware])
				else:
					fw_pos = len(network_table) - (len(network_info[key][key_firmware])-1)
					total_pos = fw_pos + len(network_info[key][key_firmware])
				local_total += network_info[key][key_firmware][key_dcw] 
				network_table= network_table.append({'Router Count': int(network_info[key][key_firmware][key_dcw]),'DCW Version': key_dcw}, ignore_index=True)
			network_table.at[fw_pos,'Firmware Version'] = key_firmware
		#network_table = network_table.append({'Router Model': key + " Total:",'Router Count': local_total}, ignore_index=True)
		network_table.at[total_pos,'Router Model'] = key + " Total:"
		network_table.at[total_pos,'Router Count'] = local_total
		network_table.at[model_pos,'Router Model'] = key 


	network_table = network_table.replace(np.nan,'',regex=True)
	#print(network_table)
	print(network_table.to_html(index=False))
except Exception as error:
	print("""<h5> <span class= "glyphicon glyphicon-remove"> </span> Connection ERROR 202 </h5> """)
	print("""{error_message} """.format(error_message=error))
	exit()