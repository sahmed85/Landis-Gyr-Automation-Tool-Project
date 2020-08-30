#!c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe
############################################################################################
#File: appendix.py
#Name: Shad Ahmed
#Date Created: 3/5/2020
#Last Modified: Ongoing 
#Usage: Internal | localhost -> to be used externally
#Overview: This file is a python script using CGI to compute a current device counts based on files uploaded.
#		   Current device count uses the Endpoint, Network and Collectos Extract to build a summation of all 
#		   endpoint types. 
#Github/Git: sahmed85/ | *this is a private repo*
#Project: UpgradePlanTool
############################################################################################### 

import pandas as pd 
from openpyxl import load_workbook
import numpy as np 

#################collector devices
df_collectors = pd.read_excel('test_collectors.xlsx')
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
		device_pos = len(collector_table) + 1

	collector_table["Device Name"] = collector_info[key].keys()
	collector_table["Count of Device Sub Type"] = collector_info[key].values()
	collector_table.at[device_pos,"Device Sub Type"] = key
	collector_table.at[len(collector_table)+1,"Device Sub Type"] = key + " Total:"
	collector_table.at[len(collector_table),"Count of Device Sub Type"] = len(collector_info[key].values())

collector_table = collector_table.replace(np.nan,'',regex=True)
collector_table
#print(collector_table)
print(collector_table.to_html(index=False))
############network devices
df_networks = pd.read_excel('test_network.xlsx')
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
#######endpoints
df_endpoints = pd.read_excel('test_endpoints.xlsx')
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
