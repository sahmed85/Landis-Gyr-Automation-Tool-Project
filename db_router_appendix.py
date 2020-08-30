#!c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe
############################################################################################
#File: db_router_appendix.py
#Name: Shad Ahmed
#Date Created: 3/25/2020
#Last Modified: Ongoing 
#Usage: Internal | localhost -> to be used externally
#Overview: This file is a python script using CGI to compute table of router count using a db connection. 
#Github/Git: sahmed85/ | *this is a private repo*
#Project: UpgradePlanTool
############################################################################################### 

import pandas as pd 
from openpyxl import load_workbook
import numpy as np 
import sys
import cx_Oracle
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
	if sys.argv[7] == "oracle":
		try:
			dsn_tns = cx_Oracle.makedsn(sys.argv[1], sys.argv[2], service_name= sys.argv[3])
			conn = cx_Oracle.connect(user = sys.argv[4], password = sys.argv[5], dsn = dsn_tns)
			db_query = conn.cursor()
			try:
				db_query.execute(""" alter session set current_schema = centralservcies """)	
				db_query.execute("""		SELECT*****s.name AS "Hardware Model", *****s.firmwareversion AS "Firmware Version", *****es.dcwversion AS "DCW Version"
										FROM *****
										JOIN ***** ON endpointmodels.endpointmodelid = endpoints.hwmodelid
										JOIN ***** ON rfendpointproperties.endpointid = endpoints.endpointid
										WHERE e*****.endpointmodelfamilyid in ('65550','65558')
										AND *****.statuscodeid in ('8','14','13','28','31','33','34','50','72')""")
			except:
				db_query.execute("""		SELECT *****s.name AS "Hardware Model",*****ts.firmwareversion AS "Firmware Version", *****es.dcwversion AS "DCW Version"
										FROM *****
										JOIN ***** ON e*****.endpointmodelid = en*****.hwmodelid
										JOIN ***** ON rf*****.endpointid = en*****.endpointid
										WHERE e*****.endpointmodelfamilyid in ('65550','65558')
										AND en*****.st***** in ('8','14','13','28','31','33','34','50','72')""")
		except Exception as error:
			print("""<h5> <span class= "glyphicon glyphicon-remove"> </span> Connection ERROR CODE 101 </h5> """)
			print("""{error_message} """.format(error_message=error))
			exit()

		############network devices
		df_networks = pd.DataFrame(db_query, columns = ['Hardware Model','Firmware Version','DCW Version'])
		df_networks = df_networks.replace(np.nan,'(blank)',regex=True)
		network_info = {}
		#####################################################################################################################
		# This part using the query to compute the pivot table to be return to the html page it was called for.
		#####################################################################################################################
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

		try:
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
				network_table.at[model_pos,'Router Model'] = key 
				network_table.at[total_pos,'Router Model'] = key + " Total:"
				network_table.at[total_pos,'Router Count'] = local_total
				


			network_table = network_table.replace(np.nan,'',regex=True)
			#print(network_table)
			print(network_table.to_html(index=False))
		except Exception as error:
			print("""{error_message} """.format(error_message=error))
			exit()

	elif sys.argv[7] == "mssql":
		try:
			server = sys.argv[1]
			database = sys.argv[3]
			username = ''
			password = ''
			cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

			df_networks = pd.read_sql_query("""SELECT *****ls.name AS "Hardware Model", *****.firmwareversion AS "Firmware Version", *****s.dcwversion AS "DCW Version"
										FROM *****
										JOIN ***** ON *****s.endpointmodelid = *****s.hwmodelid
										JOIN ***** ON *****s.endpointid = e*****s.endpointid
										WHERE e*****.endpointmodelfamilyid in ('65550','65558')
										AND e*****ts.statuscodeid in ('8','14','13','28','31','33','34','50','72')""", cnxn)
		except Exception as error:
			print("""<h5> <span class= "glyphicon glyphicon-remove"> </span> Connection ERROR 101 </h5> """)
			print("""{error_message} """.format(error_message=error))
			exit()
		
		#####################################################################################################################
		# This part using the query to compute the pivot table to be return to the html page it was called for.
		#####################################################################################################################
		############network devices
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

		try:
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
				network_table.at[model_pos,'Router Model'] = key 
				network_table.at[total_pos,'Router Model'] = key + " Total:"
				network_table.at[total_pos,'Router Count'] = local_total
				


			network_table = network_table.replace(np.nan,'',regex=True)
			#print(network_table)
			print(network_table.to_html(index=False))
		except Exception as error:
			print("""{error_message} """.format(error_message=error))
			exit()

except Exception as error:
	print("""<h5> <span class= "glyphicon glyphicon-remove"> </span> Connection ERROR 102 </h5> """)
	print("""{error_message} """.format(error_message=error))
	exit()