#!c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe
############################################################################################
#File: db_layeranalysis_infoform.py
#Name: Shad Ahmed
#Date Created: 3/30/2020
#Last Modified: Ongoing 
#Usage: Internal | localhost -> to be used externally
#Overview: This file is a python script using CGI to compute a layer analysis based on files uploaded.
#		   Layer Analysis uses the DB connection to build a layer analysis and run a summation calculation. 
#		   This script adds the endpoint_appendix to reduce overhead of iteration. Runs one query and loops thru once. 
#Github/Git: sahmed85/ | *this is a private repo*
#Project: UpgradePlanTool
############################################################################################### 
import pandas as pd 
from openpyxl import load_workbook
import numpy as np
import sys
import cx_Oracle
import os.path
import pyodbc

#############################################################################################################################
# This section of the script works on building a connection to the database based on command line arguments:
# sys.argv[1] = hostname
# sys.argv[2] = port 
# sys.argv[3] = sid/db name
# sys.argv[4] = password
# sys.argv[5] = current Firmware filter
# sys.argv[6] = session id for FILE IO 
# sys.argv[7] = db type 
# The query can be seen inside the qutotations. Throws errors if fails. 
#############################################################################################################################

try:
	if sys.argv[8] == "oracle":
		try:
			dsn_tns = cx_Oracle.makedsn(sys.argv[1], sys.argv[2], service_name= sys.argv[3])
			conn = cx_Oracle.connect(user = sys.argv[4], password = sys.argv[5], dsn = dsn_tns)
			db_query = conn.cursor()
			firmware_str = sys.argv[6]
			firmware_str = "".join(firmware_str.split())
			firmware_ll = firmware_str.split(",")
			firmware_str = ""
			if len(firmware_ll) == 1:
				if firmware_ll[0] == "All":
					firmware_str = "'%.%'"
				else:
					firmware_str = "'%" + firmware_ll[0] + "%'"
			else:
				for x in range(0,len(firmware_ll)):
					if x == 0:
						firmware_str = "'%" + firmware_ll[x] + "%'"
					else:
						firmware_str = firmware_str + " OR endpoints.firmwareversion LIKE " + "'%" + firmware_ll[x] + "%'"
			try:
				db_query.execute(""" alter session set current_schema = centralservcies """)
				db_query.execute("""SELECT *****.endpointid AS "Meter" , *****.name AS "Hardware Model",*****.firmwareversion AS "Firmware Version", *****.dcwversion AS "DCW Version",*****.firmwareversion AS "Meter Firmware Version", *****.layer AS "Layer"
								FROM *****
								JOIN ***** ON *****s.endpointmodelid = *****.hwmodelid
								JOIN ***** ON*****.endpointid =*****.endpointid
								JOIN meters ON meters.meterid = *****.meterid
								WHERE e*****.firmwareversion LIKE {firmware}
								AND *****.statuscodeid in ('8','14','13','28','31','33','34','50','72')
								AND *****.endpointmodelid not in ('65560','65579','65569')""".format(firmware = firmware_str))
			except:
				db_query.execute("""SELECT *****.endpointid AS "Meter" ,*****.name AS "Hardware Model", *****.firmwareversion AS "Firmware Version",*****.dcwversion AS "DCW Version", *****.firmwareversion AS "Meter Firmware Version", *****.layer AS "Layer"
								FROM e*****
								JOIN ***** ON e*****.endpointmodelid = *****.hwmodelid
								JOIN r***** ON *****.endpointid = e*****s.endpointid
								JOIN ***** ON *****.meterid = *****.meterid
								WHERE e*****.firmwareversion LIKE {firmware}
								AND *****.statuscodeid in ('8','14','13','28','31','33','34','50','72')
								AND e*****.endpointmodelid not in ('65560','65579','65569')""".format(firmware = firmware_str))

		except Exception as error:
			print("""<h5> <span class= "glyphicon glyphicon-remove"> </span> Connection ERROR 101 </h5> """)
			print("""{error_message} """.format(error_message=error))
			exit()

		#####################################################################################################################
		# This part using the query to compute the pivot table to be return to the html page it was called for.
		#####################################################################################################################
		df_endpoints = pd.DataFrame(db_query, columns=['Endpoint ID','Hardware Model','Firmware Version','DCW Version','Meter Firmware Version','Layer'])


		layer_count = {-1:0}
		totalmeter_count = 0

		endpoint_info = {}

		for ind in df_endpoints.index:
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
				continue

		## Layer Analysis
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

		print(df_table.to_html(index=False))
		save_path = 'C:/wamp64/www/upgradeplantool/session_files/'
		file_name = os.path.join(save_path,"{session_id}_layer.txt".format(session_id = sys.argv[7]))
		file_appendix = open(file_name,'w')
		file_appendix.write(df_table.to_html(index = False))
		file_appendix.close()


		## endpoints appendix file
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


		save_path = 'C:/wamp64/www/upgradeplantool/session_files/'
		file_name = os.path.join(save_path,"{session_id}_appendix.txt".format(session_id = sys.argv[7]))
		file_appendix = open(file_name,'w')
		file_appendix.write(endpoint_table.to_html(index = False))
		file_appendix.close()

	elif sys.argv[8] == "mssql":
		try:
			server = sys.argv[1]
			database = sys.argv[3]
			username = ''
			password = ''
			cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

			firmware_str = sys.argv[6]
			firmware_str = "".join(firmware_str.split())
			firmware_ll = firmware_str.split(",")
			firmware_str = ""
			if len(firmware_ll) == 1:
				if firmware_ll[0] == "All":
					firmware_str = "'%.%'"
				else:
					firmware_str = "'%" + firmware_ll[0] + "%'"
			else:
				for x in range(0,len(firmware_ll)):
					if x == 0:
						firmware_str = "'%" + firmware_ll[x] + "%'"
					else:
						firmware_str = firmware_str + " OR endpoints.firmwareversion LIKE " + "'%" + firmware_ll[x] + "%'"

			df_endpoints = pd.read_sql_query("""SELECT *****.endpointid AS "Endpoint ID" , *****.name AS "Hardware Model", *****.firmwareversion AS "Firmware Version", *****.dcwversion AS "DCW Version", *****.firmwareversion AS "Meter Firmware Version", *****.layer AS "Layer"
								FROM *****
								JOIN ***** ON *****.endpointmodelid = *****.hwmodelid
								JOIN ***** ON *****.endpointid = *****.endpointid
								JOIN ***** ON *****.meterid = *****.meterid
								WHERE e*****.firmwareversion LIKE {firmware}
								AND *****.statuscodeid in ('8','14','13','28','31','33','34','50','72')
								AND *****.endpointmodelid not in ('65560','65579','65569')""".format(firmware = firmware_str),cnxn)

		except Exception as error:
			print("""<h5> <span class= "glyphicon glyphicon-remove"> </span> Connection ERROR 101 </h5> """)
			print("""{error_message} """.format(error_message=error))
			exit()	

		#####################################################################################################################
		# This part using the query to compute the pivot table to be return to the html page it was called for.
		#####################################################################################################################

		layer_count = {-1:0}
		totalmeter_count = 0

		endpoint_info = {}

		for ind in df_endpoints.index:
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
				continue

		## Layer Analysis
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

		print(df_table.to_html(index=False))
		save_path = 'C:/wamp64/www/upgradeplantool/session_files/'
		file_name = os.path.join(save_path,"{session_id}_layer.txt".format(session_id = sys.argv[7]))
		file_appendix = open(file_name,'w')
		file_appendix.write(df_table.to_html(index = False))
		file_appendix.close()


		## endpoints appendix file
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


		save_path = 'C:/wamp64/www/upgradeplantool/session_files/'
		file_name = os.path.join(save_path,"{session_id}_appendix.txt".format(session_id = sys.argv[7]))
		file_appendix = open(file_name,'w')
		file_appendix.write(endpoint_table.to_html(index = False))
		file_appendix.close()
		
except Exception as error:
	print("""<h5> <span class= "glyphicon glyphicon-remove"> </span> Connection ERROR 102 </h5> """)
	print("""{error_message} """.format(error_message=error))
	exit()
