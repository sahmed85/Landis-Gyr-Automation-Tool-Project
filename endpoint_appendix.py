#!c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe
############################################################################################
#File: endpoint_appendix.py
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
	this_file = open('C:/wamp64/www/upgradeplantool/session_files/{session}_excel_appendix.txt'.format(session = sys.argv[1]))
	html_content = this_file.read()
	print(html_content)
	this_file.close()
except:
	df_endpoints = pd.read_excel('C:/wamp64/www/upgradeplantool/uploads/{session_id}_endpoints.xlsx'.format(session_id = sys.argv[1]))
	df_endpoints = df_endpoints.replace(np.nan,'(blank)',regex=True)
	endpoint_info = {}

	for ind in df_endpoints.index:
		if df_endpoints["Status Code"][ind] in ["Normal", "Discovered", "Installed"]:
			hardware_model = str(df_endpoints["Hardware Model"][ind])
			firmware_version = str(df_endpoints["Firmware Version"][ind])
			dcw_version = str(df_endpoints["DCW Version"][ind])
			meterfw_version = str(df_endpoints["Meter Firmware Version"][ind])
			if hardware_model not in endpoint_info:
				endpoint_info[hardware_model] = {firmware_version:{dcw_version:{meterfw_version:1}}}
			elif firmware_version not in endpoint_info[hardware_model]:
				endpoint_info[hardware_model][firmware_version] = {dcw_version:{meterfw_version:1}}
			elif dcw_version not in endpoint_info[hardware_model][firmware_version]:
				endpoint_info[hardware_model][firmware_version][dcw_version] = {meterfw_version:1}
			elif meterfw_version not in endpoint_info[hardware_model][firmware_version][dcw_version]:
				endpoint_info[hardware_model][firmware_version][dcw_version][meterfw_version] = 1
			else:
				endpoint_info[hardware_model][firmware_version][dcw_version][meterfw_version] += 1

	endpoint_table = pd.DataFrame(columns = ['Hardware Model','Firmware Version','DCW Version','Meter Firmware Version','Count of Meter'])
	total = 0
	for key in endpoint_info:
		if len(endpoint_info) == 0:
			model_pos = len(endpoint_table)
		else:
			model_pos = len(endpoint_table)
		local_total = 0
		for key_firmware in endpoint_info[key]:
			for key_dcw in endpoint_info[key][key_firmware]:
				if len(endpoint_table) == 0:
					fw_pos = len(endpoint_table)
				else:
					fw_pos = len(endpoint_table) - (len(endpoint_info[key][key_firmware])-1)
				total_pos = fw_pos + len(endpoint_info[key][key_firmware])
				for key_meterfw in endpoint_info[key][key_firmware][key_dcw]:
					if len(endpoint_table) == 0:
						dcw_pos = len(endpoint_table)
					else:
						dcw_pos = len(endpoint_table) - (len(endpoint_info[key][key_firmware][key_dcw])-1)
					local_total += endpoint_info[key][key_firmware][key_dcw][key_meterfw]
					endpoint_table = endpoint_table.append({'Count of Meter': int(endpoint_info[key][key_firmware][key_dcw][key_meterfw]),'Meter Firmware Version':key_meterfw},ignore_index=True)
				endpoint_table.at[dcw_pos,'DCW Version'] = key_dcw
			endpoint_table.at[fw_pos,'Firmware Version'] = key_firmware
		endpoint_table.at[total_pos,'Hardware Model'] = key + " Total:"	
		endpoint_table.at[total_pos,'Count of Meter'] = local_total
		endpoint_table.at[model_pos,'Hardware Model'] = key

	endpoint_table = endpoint_table.replace(np.nan,'',regex=True)
	#print(endpoint_table)
	print(endpoint_table.to_html(index = False))