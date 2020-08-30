#!c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe
############################################################################################
#File: db_layeranalysis.py
#Name: Shad Ahmed
#Date Created: 3/23/2020
#Last Modified: Ongoing 
#Usage: Internal | localhost -> to be used externally
#Overview: This file is a python script using CGI to compute a layer analysis based on files uploaded.
#		   Layer Analysis uses the DB connection to build a layer analysis and run a summation calculation. 
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
			layer_file = open('C:/wamp64/www/upgradeplantool/session_files/{session}_layer.txt'.format(session = sys.argv[7]))
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
					db_query.execute("""SELECT *****.layer, *****ts.endpointid, e*****s.serialnumber  
									FROM *****
									JOIN ***** ON ****s.endpointid =*****s.endpointid
									JOIN ***** ON *****ls.endpointmodelid = *****ts.hwmodelid
									WHERE *****.firmwareversion LIKE {firmware} 
									AND *****s.statuscodeid in ('8','14','13','28','31','33','34','50','72')
									AND e*****s.endpointmodelid not in ('65560','65579','65569')""".format(firmware = firmware_str))
				except:
					db_query.execute("""SELECT r*****.layer, *****s.endpointid, e*****ts.serialnumber  
									FROM endpoints
									JOIN rfendpointproperties ON *****s.endpointid = *****nts.endpointid
									JOIN endpointModels ON e*****s.endpointmodelid = e*****s.hwmodelid
									WHERE en*****s.firmwareversion LIKE {firmware} 
									AND e*****s.statuscodeid in ('8','14','13','28','31','33','34','50','72')
									AND en*****s.endpointmodelid not in ('65560','65579','65569')""".format(firmware = firmware_str))
			except Exception as error:
				print("""<h5> <span class= "glyphicon glyphicon-remove"> </span> Connection ERROR 101 </h5> """)
				print("""{error_message} """.format(error_message=error))
				exit()

			#####################################################################################################################
			# This part using the query to compute the pivot table to be return to the html page it was called for.
			#####################################################################################################################
			df_endpoints = pd.DataFrame(db_query, columns=['Layer','EndpointID','SerialNumber'])

			layer_count = {-1:0}
			totalmeter_count = 0

			for ind in df_endpoints.index:
				#print(df_endpoints["Layer"][ind])
				
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

	elif sys.argv[8] == "mssql":
		try:
			layer_file = open('C:/wamp64/www/upgradeplantool/session_files/{session}_layer.txt'.format(session = sys.argv[7]))
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

				df_endpoints = pd.read_sql_query("""SELECT *****.layer AS "Layer", *****s.endpointid AS "Endpoint ID", *****s.serialnumber  
									FROM endpoints
									JOIN ***** ON *****s.endpointid = e*****s.endpointid
									JOIN e***** ON *****ls.endpointmodelid = *****s.hwmodelid
									WHERE *****ts.firmwareversion LIKE {firmware} 
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

			for ind in df_endpoints.index:
				#print(df_endpoints["Layer"][ind])
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
			
except Exception as error:
	print("""<h5> <span class= "glyphicon glyphicon-remove"> </span> Connection ERROR 102 </h5> """)
	print("""{error_message} """.format(error_message=error))
	exit()
