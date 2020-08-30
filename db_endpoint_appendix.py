#!c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe
############################################################################################
#File: db_endpoint_appendix.py
#Name: Shad Ahmed
#Date Created: 3/5/2020
#Last Modified: Ongoing 
#Usage: Internal | localhost -> to be used externally
#Overview: This file is a python script using CGI to compute table of collector count. 
# 		   Layer Analysis uses the DB connection to build a layer analysis and run a summation calculation.
#Github/Git: sahmed85/ | *this is a private repo*
#Project: UpgradePlanTool
############################################################################################### 

import pandas as pd 
from openpyxl import load_workbook
import numpy as np 
import cx_Oracle
import sys
import pyodbc
import traceback

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
			layer_file = open('C:/wamp64/www/upgradeplantool/session_files/{session}_appendix.txt'.format(session = sys.argv[7]))
			html_content = layer_file.read()
			print(html_content)
			layer_file.close()
		except:
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
					db_query.execute("""SELECT ***** AS "Meter" ,***** AS "Hardware Model", ***** AS "Firmware Version", rfendpointproperties.dcwversion AS "DCW Version", meters.firmwareversion AS "Meter Firmware Version", rfendpointproperties.layer AS "Layer"
										FROM *****
										JOIN *****ON ***** = *****
										JOIN ***** ON***** = *****
										JOIN ***** ON***** = e*****
										WHERE ***** LIKE {firmware}
										AND ***** in ('8','14','13','28','31','33','34','50','72')
										AND ***** not in ('65560','65579','65569')""".format(firmware = firmware_str))
				except:
					db_query.execute("""SELECT ***** AS "Meter" , ***** AS "Hardware Model", ***** AS "Firmware Version", rfendpointproperties.dcwversion AS "DCW Version", meters.firmwareversion AS "Meter Firmware Version", rfendpointproperties.layer AS "Layer"
										FROM *****
										JOIN ***** ON *****.endpointmodelid = *****.hwmodelid
										JOIN ***** ON *****.endpointid = *****.endpointid
										JOIN ***** ON *****.meterid = *****.meterid
										WHERE *****.firmwareversion LIKE {firmware}
										AND *****.statuscodeid in ('8','14','13','28','31','33','34','50','72')
										AND *****s.endpointmodelid not in ('65560','65579','65569')""".format(firmware = firmware_str))

			except Exception as error:
				print("""<h5> <span class= "glyphicon glyphicon-remove"> </span> Connection ERROR 101 </h5> """)
				print("""{error_message} """.format(error_message=error))
				exit()

			#####################################################################################################################
			# This part using the query to compute the pivot table to be return to the html page it was called for.
			#####################################################################################################################

			df_endpoints = pd.DataFrame(db_query, columns=['Endpoint ID','Hardware Model','Firmware Version','DCW Version','Meter Firmware Version','Layer'])
			df_endpoints = df_endpoints.replace(np.nan,'(blank)',regex=True)
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

	elif sys.argv[8] == "mssql":
		try:
			layer_file = open('C:/wamp64/www/upgradeplantool/session_files/{session}_appendix.txt'.format(session = sys.argv[7]))
			html_content = layer_file.read()
			print(html_content)
			layer_file.close()
		except:
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

				df_endpoints = pd.read_sql_query("""SELECT endpoints.endpointid AS "Meter" , endpointModels.name AS "Hardware Model", endpoints.firmwareversion AS "Firmware Version", rfendpointproperties.dcwversion AS "DCW Version", meters.firmwareversion AS "Meter Firmware Version", rfendpointproperties.layer AS "Layer"
										FROM endpoints
										JOIN endpointModels ON endpointmodels.endpointmodelid = endpoints.hwmodelid
										JOIN rfendpointproperties ON rfendpointproperties.endpointid = endpoints.endpointid
										JOIN meters ON meters.meterid = endpoints.meterid
										WHERE endpoints.firmwareversion LIKE {firmware}
										AND endpoints.statuscodeid in ('8','14','13','28','31','33','34','50','72')
										AND endpointModels.endpointmodelid not in ('65560','65579','65569')""".format(firmware = firmware_str), cnxn)
			except Exception as error:
				print("""<h5> <span class= "glyphicon glyphicon-remove"> </span> Connection ERROR 101 </h5> """)
				print("""{error_message} """.format(error_message=error))
				exit()
			#####################################################################################################################
			# This part using the query to compute the pivot table to be return to the html page it was called for.
			#####################################################################################################################
			df_endpoints = df_endpoints.replace(np.nan,'(blank)',regex=True)
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
			
except Exception as error:
	print("""<h5> <span class= "glyphicon glyphicon-remove"> </span> Connection ERROR 102 </h5> """)
	traceback.print_exc()
	print("""{error_message} """.format(error_message=error))
	exit()



