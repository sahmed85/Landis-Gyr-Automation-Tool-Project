#!c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe
############################################################################################
#File: target_info.py
#Name: Shad Ahmed
#Date Created: 3/11/2020
#Last Modified: 04/29/2020 
#Usage: Internal | localhost -> to be used externally
#Overview: This is python file to add to infoform.php to add allow user to fill target fw/dcw info for the specific meter. 
#Github/Git: sahmed85/ | *this is a private repo*
#Project: UpgradePlanTool
############################################################################################### 

import pandas as pd 
from openpyxl import load_workbook
import numpy as np
import sys
import os.path

try:
	###############################################################################################################################
	# This reads in the excel file and computes a pivot table to be returned to the appropiate html. Throws an error if failed to 
	# read the file.
	###############################################################################################################################
	df_endpoints = pd.read_excel('C:/wamp64/www/upgradeplantool/uploads/{session_id}_endpoints.xlsx'.format(session_id = sys.argv[1]))
	df_endpoints = df_endpoints.replace(np.nan,'(blank)', regex = True)
	##Target Info
	endpoint_names = []

	##Device Count 
	endpoint_info = {}

	##Layer Analysis
	layer_count = {-1:0}
	totalmeter_count = 0

	##Endpoint Appendix
	endpoint_appendix = {}

	##Loop thru excel rows 
	for ind in df_endpoints.index:
		if df_endpoints["Status Code"][ind] in ["Normal","Discovered","Installed"]:
			##Target Info
			hardware_model = str(df_endpoints["Hardware Model"][ind])
			if hardware_model not in endpoint_names and hardware_model != "Inventory Device":
				endpoint_names.append(hardware_model)
			##Device Count
			metertype = str(df_endpoints["Hardware Model"][ind])
			if metertype not in endpoint_info.keys():
				endpoint_info[metertype] = 1
			else:
				endpoint_info[metertype] += 1
			##Layer Analysis
			try:
				layernum = int(df_endpoints["Layer"][ind])
				if layernum not in layer_count.keys():
					layer_count[layernum] = 1
					totalmeter_count += 1
				else:
					layer_count[layernum] += 1
					totalmeter_count += 1
			except:
				layer_count[-1] += 1
				totalmeter_count += 1
			##Endpoint Appendix
			hardware_model = str(df_endpoints["Hardware Model"][ind])
			firmware_version = str(df_endpoints["Firmware Version"][ind])
			dcw_version = str(df_endpoints["DCW Version"][ind])
			meterfw_version = str(df_endpoints["Meter Firmware Version"][ind])
			if hardware_model not in endpoint_appendix:
				endpoint_appendix[hardware_model] = {firmware_version:{dcw_version:{meterfw_version:1}}}
			elif firmware_version not in endpoint_appendix[hardware_model]:
				endpoint_appendix[hardware_model][firmware_version] = {dcw_version:{meterfw_version:1}}
			elif dcw_version not in endpoint_appendix[hardware_model][firmware_version]:
				endpoint_appendix[hardware_model][firmware_version][dcw_version] = {meterfw_version:1}
			elif meterfw_version not in endpoint_appendix[hardware_model][firmware_version][dcw_version]:
				endpoint_appendix[hardware_model][firmware_version][dcw_version][meterfw_version] = 1
			else:
				endpoint_appendix[hardware_model][firmware_version][dcw_version][meterfw_version] += 1

	##############################################################################################################################
	# Use FILE IO to use the hardware model to create the html form to be used in the infoform.php
	##############################################################################################################################			
	fo = open("C:/wamp64/www/upgradeplantool/session_files/{session_id}_target_model.txt".format(session_id = sys.argv[1]), "w") ########## UPDATE HERE WITH SESSION ID ##########

	html_table = """
					<table broder="1" class="dataframe">
						<thead>
							<tr style = "text-align: center;">
								<th> Meter </th>
								<th> Firmware Version </th>
								<th> DCW Version </th>
								<th> DCW Filename </th>
								<th> Metrology </th>
								<th> Zigbee </th>
							</tr>
						</thead>
						<tbody> 
	"""

	for hardware_model in endpoint_names:
		html_table = html_table + """ <tr>
											<td> {hardwaremodel} </td>
											
											<td> 
												<input type = "text" class = "form-control" name = "fw_version[]" id= "fw_version" placeholder="13.54">
											</td>

											<td> 
												<input type = "text" class = "form-control" name = "dcw_version[]" id= "dcw_version" placeholder="240D.13.53.0014">
											</td>

											<td>
												<input type = "text" class = "form-control" name = "dcw_filename[]" id= "dcw_filename" placeholder="FAXG.13.53.hex">
											</td>

											<td>
												<input type = "text" class = "form-control" name = "metrology[]" id= "metrology" placeholder="5.70">
											</td>
											
											<td>
												<input type = "text" class = "form-control" name = "zigbee[]" id= "zigbee" placeholder="2.04.15">
											</td>

										</tr>
									""".format(hardwaremodel=hardware_model)
		if hardware_model == endpoint_names[len(endpoint_names)-1]:
			fo.write(hardware_model)
		else:
			fo.write(hardware_model + "\n")

	html_table = html_table + """ </tbody> </table> """
	fo.close()

	print(html_table)

	save_path = 'C:/wamp64/www/upgradeplantool/session_files/'

	###############################################################################################################################
	# This reads in the excel file and computes a pivot table to be returned to the appropiate html. Throws an error if failed to 
	# read the file.
	###############################################################################################################################
	##Device Count
	df_endpointsTable = pd.DataFrame(columns= ['Meter Type','Count of Meter'])
	df_endpointsTable["Meter Type"] = endpoint_info.keys()
	df_endpointsTable["Count of Meter"] = endpoint_info.values()

	file_name = os.path.join(save_path,"{session_id}_excel_count.txt".format(session_id = sys.argv[1]))
	this_file = open(file_name,'w')
	this_file.write(df_endpointsTable.to_html(index=False))
	this_file.close()

	##Layer Analysis
	culmutive_count = {}
	layer_percent = {}

	for key in layer_count:
		if key == 1:
			culmutive_count[key] = layer_count[key]
		elif key == -1:
			culmutive_count[key] = culmutive_count[prev_key] + layer_count[key]
		else:
			culmutive_count[key] = culmutive_count[prev_key] + layer_count[key]

		layer_percent[key] = round((culmutive_count[key]/totalmeter_count)*100,2)
		prev_key = key

	df_table = pd.DataFrame(columns = ['Layer','Meter Count','Culmutive Meter Count','Layer Percent %'])
	df_table["Layer"] = layer_count.keys()
	df_table["Layer"].iloc[-1] = ""
	df_table["Meter Count"] = layer_count.values()
	df_table["Culmutive Meter Count"] = culmutive_count.values()
	df_table["Layer Percent %"] = layer_percent.values()
	df_table = df_table.append({'Layer': 'Grand Total', 'Meter Count': totalmeter_count,'Culmutive Meter Count': totalmeter_count, 'Layer Percent %': ""}, ignore_index = True)

	file_name = os.path.join(save_path,"{session_id}_excel_layer.txt".format(session_id = sys.argv[1]))
	this_file = open(file_name,'w')
	this_file.write(df_table.to_html(index=False))
	this_file.close()

	###############################################################################################################################
	# This reads in the excel file and computes a pivot table to be returned to the appropiate html. Throws an error if failed to 
	# read the file.
	###############################################################################################################################
	##Endpoint Appendix
	endpoint_table = pd.DataFrame(columns = ['Hardware Model','Firmware Version','DCW Version','Meter Firmware Version','Count of Meter'])
	total = 0
	for key in endpoint_appendix:
		if len(endpoint_appendix) == 0:
			model_pos = len(endpoint_table)
		else:
			model_pos = len(endpoint_table)
		local_total = 0
		for key_firmware in endpoint_appendix[key]:
			for key_dcw in endpoint_appendix[key][key_firmware]:
				if len(endpoint_table) == 0:
					fw_pos = len(endpoint_table)
				else:
					fw_pos = len(endpoint_table) - (len(endpoint_appendix[key][key_firmware])-1)
				total_pos = fw_pos + len(endpoint_appendix[key][key_firmware])
				for key_meterfw in endpoint_appendix[key][key_firmware][key_dcw]:
					if len(endpoint_table) == 0:
						dcw_pos = len(endpoint_table)
					else:
						dcw_pos = len(endpoint_table) - (len(endpoint_appendix[key][key_firmware][key_dcw])-1)
					local_total += endpoint_appendix[key][key_firmware][key_dcw][key_meterfw]
					endpoint_table = endpoint_table.append({'Count of Meter': int(endpoint_appendix[key][key_firmware][key_dcw][key_meterfw]),'Meter Firmware Version':key_meterfw},ignore_index=True)
				endpoint_table.at[dcw_pos,'DCW Version'] = key_dcw
			endpoint_table.at[fw_pos,'Firmware Version'] = key_firmware
		endpoint_table.at[total_pos,'Hardware Model'] = key + " Total:"	
		endpoint_table.at[total_pos,'Count of Meter'] = local_total
		endpoint_table.at[model_pos,'Hardware Model'] = key

	endpoint_table = endpoint_table.replace(np.nan,'',regex=True)
	file_name = os.path.join(save_path,"{session_id}_excel_appendix.txt".format(session_id = sys.argv[1]))
	this_file = open(file_name,'w')
	this_file.write(endpoint_table.to_html(index=False))
	this_file.close()
	
except Exception as error:
	print("""<h5> <span class= "glyphicon glyphicon-remove"> </span> Connection ERROR 202 </h5> """)
	print("""{error_message} """.format(error_message=error))
	exit()


