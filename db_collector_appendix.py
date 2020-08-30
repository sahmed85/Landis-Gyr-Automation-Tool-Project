#!c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe
############################################################################################
#File: db_collector_appendix.py
#Name: Shad Ahmed
#Date Created: 3/26/2020
#Last Modified: 04/15/2020
#Usage: Internal | localhost -> to be used externally
#Overview: This file is a python script using CGI to compute table of collector count using database connections. 
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
				## this try is for dbs that have the central services schema 
				db_query.execute(""" alter session set current_schema = centralservcies """)
				db_query.execute("""SELECT *****.name AS "Device Sub Type",  *****.confirmedname AS "Device Name"
								FROM ****
								JOIN **** ON *****.cltrsubtypid = *****.cltrsubtypid """)
			except:
				db_query.execute("""SELECT*****.name AS "Device Sub Type",  *****.confirmedname AS "Device Name"
								FROM collectors
								JOIN collectorsubtypes ON *****.cltrsubtypid = *****.cltrsubtypid """)
		except Exception as error:
			print("""<h5> <span class= "glyphicon glyphicon-remove"> </span> Connection ERROR 101 </h5> """)
			print("""{error_message} """.format(error_message=error))
			exit()
		#################collector devices
		#####################################################################################################################
		# This part using the query to compute the pivot table to be return to the html page it was called for.
		#####################################################################################################################
		df_collectors = pd.DataFrame(db_query, columns = ['Device Sub Type','Device Name'])
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

		try:
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
			#print(collector_table)
			print(collector_table.to_html(index=False))
		except Exception as error:
			print("""{error_message} """.format(error_message=error))
			print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
			exit()

	elif sys.argv[7] == "mssql":
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

			df_collectors = pd.read_sql_query("""SELECT *****.name AS "Device Sub Type", *****.confirmedname AS "Device Name"
								FROM *****
								JOIN ***** ON *****.cltrsubtypid = *****.cltrsubtypid """, cnxn)
		except Exception as error:
			print("""<h5> <span class= "glyphicon glyphicon-remove"> </span> Connection ERROR 101 </h5> """)
			print("""{error_message} """.format(error_message=error))
			exit()

		#################collector devices
		#####################################################################################################################
		# This part using the query to compute the pivot table to be return to the html page it was called for.
		#####################################################################################################################
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

		try:
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
			#print(collector_table)
			print(collector_table.to_html(index=False))
		except Exception as error:
			print("""{error_message} """.format(error_message=error))
			print ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
			exit()
			
except Exception as error:
	print("""<h5> <span class= "glyphicon glyphicon-remove"> </span> Connection ERROR 102 </h5> """)
	print("""{error_message} """.format(error_message=error))
	exit()

