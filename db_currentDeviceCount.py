#!c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe
############################################################################################
#File: db_currentDeviceCount.py
#Name: Shad Ahmed
#Date Created: 3/5/2020
#Last Modified: 04/26/2020
#Usage: Internal | localhost -> to be used externally
#Overview: This file is a python script using CGI to compute a current device counts based on files uploaded.
#		   Current device count uses the Endpoint and Collector DB query to build a summation of all endpoint types. 
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
	if sys.argv[8] == "oracle":
		try:
			dsn_tns = cx_Oracle.makedsn(sys.argv[1], sys.argv[2], service_name= sys.argv[3])
			conn = cx_Oracle.connect(user = sys.argv[4], password = sys.argv[5], dsn = dsn_tns)
			db_query_endpoint = conn.cursor()
			db_query_collector = conn.cursor()
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
				db_query_endpoint.execute(""" alter session set current_schema = centralservcies """)
				db_query_endpoint.execute("""SELECT DISTINCT (*****.name) AS "model", COUNT (*****s.endpointid) AS "meter"
										FROM ******
										JOIN **** ON *****.endpointmodelid = *****.hwmodelid
										WHERE *****.firmwareversion LIKE {firmware}
										AND e*****.statuscodeid in ('8','14','13','28','31','33','34','50','72')
										AND *****.endpointmodelid not in ('65560','65579','65569')
										group by *****.name""".format(firmware = firmware_str))
				db_query_collector.execute(""" alter session set current_schema = centralservcies """)
				db_query_collector.execute("""SELECT *****.name AS "Device Sub Type",  *****.confirmedname AS "Device Name"
										FROM ****
										JOIN **** ON *****.cltrsubtypid = *****.cltrsubtypid""")
			except:
				db_query_endpoint.execute("""SELECT DISTINCT (endpointModels.name) AS "model", COUNT (endpoints.endpointid) AS "meter"
										FROM ******
										JOIN ***** ON *****.endpointmodelid = *****s.hwmodelid
										WHERE *****.firmwareversion LIKE {firmware}
										AND e*****s.statuscodeid in ('8','14','13','28','31','33','34','50','72')
										AND *****s.endpointmodelid not in ('65560','65579','65569')
										group by *****""".format(firmware = firmware_str))
				db_query_collector.execute("""SELECT c*****s.name AS "Device Sub Type",  *****.confirmedname AS "Device Name"
										FROM *****
										JOIN ***** ON *****s.cltrsubtypid = *****.cltrsubtypid""")
		except Exception as error:
			print("""<h5> <span class= "glyphicon glyphicon-remove"> </span> Connection ERROR 101 </h5> """)
			print("""{error_message} """.format(error_message=error))
			exit()

		df_collectors = pd.DataFrame(db_query_collector, columns = ['Device Sub Type','Device Name'])
		df_endpoints = pd.DataFrame(db_query_endpoint, columns = ['Hardware Model','Meter Count'])

		#collector info
		collector_info = {}

		for ind in df_collectors.index:
			devicetype = str(df_collectors["Device Sub Type"][ind])
			if  devicetype not in collector_info.keys():
				collector_info[devicetype] = 1
			else:
				collector_info[devicetype] += 1

		df_collectorsTable = pd.DataFrame(columns = ['Collector', 'Count of Collector ID'])
		df_collectorsTable["Collector"] = collector_info.keys()
		df_collectorsTable["Count of Collector ID"] = collector_info.values()

		html_collectors = df_collectorsTable.to_html(index=False)
		print(html_collectors)
		print("""<br>""")
		#endpoint info
		html_endpoint = df_endpoints.to_html(index=False)
		print(html_endpoint)

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

			df_collectors = pd.read_sql_query("""SELECT *****.name AS "Device Sub Type",  *****.confirmedname AS "Device Name"
										FROM *****
										JOIN ***** ON *****.cltrsubtypid =*****.cltrsubtypid""", cnxn)

			df_endpoints = pd.read_sql_query("""SELECT DISTINCT (*****.name) AS "Hardware Model", COUNT (e*****s.endpointid) AS "Meter Count"
										FROM *****
										JOIN ***** ON e******s.endpointmodelid = *****ts.hwmodelid
										WHERE *****s.firmwareversion LIKE {firmware}
										AND e*****ts.statuscodeid in ('8','14','13','28','31','33','34','50','72')
										AND e*****s.*****id not in ('65560','65579','65569')
										group by *****s.name""".format(firmware = firmware_str), cnxn)

		except Exception as error:
			print("""<h5> <span class= "glyphicon glyphicon-remove"> </span> Connection ERROR 101 </h5> """)
			print("""{error_message} """.format(error_message=error))
			exit()

		#collector info
		collector_info = {}

		for ind in df_collectors.index:
			devicetype = str(df_collectors["Device Sub Type"][ind])
			if  devicetype not in collector_info.keys():
				collector_info[devicetype] = 1
			else:
				collector_info[devicetype] += 1

		df_collectorsTable = pd.DataFrame(columns = ['Collector', 'Count of Collector ID'])
		df_collectorsTable["Collector"] = collector_info.keys()
		df_collectorsTable["Count of Collector ID"] = collector_info.values()

		html_collectors = df_collectorsTable.to_html(index=False)
		print(html_collectors)
		print("""<br>""")
		
		#endpoint info
		html_endpoint = df_endpoints.to_html(index=False)
		print(html_endpoint)
except Exception as error:
			print("""<h5> <span class= "glyphicon glyphicon-remove"> </span> Connection ERROR 102 </h5> """)
			print("""{error_message} """.format(error_message=error))
			exit()