#!c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe
############################################################################################
#File: db_target_info.py
#Name: Shad Ahmed
#Date Created: 3/24/2020
#Last Modified: Ongoing 
#Usage: Internal | localhost -> to be used externally
#Overview: This is python file to add to infoform.php to add allow user to fill target fw/dcw info for the specific meter
#		   using a DB connection. 
#Github/Git: sahmed85/ | *this is a private repo*
#Project: UpgradePlanTool
############################################################################################### 

import pandas as pd 
from openpyxl import load_workbook
import numpy as numpy
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
				db_query.execute("""SELECT DISTINCT*****s.name AS "Hardware Model"
								FROM *****
								JOIN ***** ON e*****s.endpointmodelid = *****s.hwmodelid
								WHERE *****ts.firmwareversion LIKE {firmware}
								AND *****.statuscodeid in ('8','14','13','28','31','33','34','50','72')
								AND *****.endpointmodelid not in ('65560','65579','65569')""".format(firmware = firmware_str))
			except:
				db_query.execute("""SELECT DISTINCT *****.name AS "Hardware Model"
								FROM *****
								JOIN e***** ON e*****ls.endpointmodelid = *****s.hwmodelid
								WHERE en*****.firmwareversion LIKE {firmware}
								AND e*****.statuscodeid in ('8','14','13','28','31','33','34','50','72')
								AND e*****.endpointmodelid not in ('65560','65579','65569')""".format(firmware = firmware_str))
		except Exception as error:
			print("""<h5> <span class= "glyphicon glyphicon-remove"> </span> Connection ERROR CODE 101 </h5> """)
			print("""{error_message} """.format(error_message=error))
			exit()

		df_endpoints = pd.DataFrame(db_query, columns = ['Hardware Model'])
		endpoint_names = []
		#####################################################################################################################
		# This part using the query to compute the pivot table to be return to the html page it was called for.
		#####################################################################################################################
		for ind in df_endpoints.index:
			hardware_model = str(df_endpoints["Hardware Model"][ind])
			if hardware_model not in endpoint_names and hardware_model != "Inventory Device":
				endpoint_names.append(hardware_model)
			else:
				continue

		fo = open("C:/wamp64/www/upgradeplantool/session_files/{session_id}_target_model.txt".format(session_id = sys.argv[7]), "w")

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

			df_endpoints = pd.read_sql_query("""SELECT DISTINCT *****s.name AS "Hardware Model"
								FROM *****
								JOIN ***** ON *****s.endpointmodelid = *****s.hwmodelid
								WHERE *****s.firmwareversion LIKE {firmware}
								AND e*****.statuscodeid in ('8','14','13','28','31','33','34','50','72')
								AND *****s.endpointmodelid not in ('65560','65579','65569')""".format(firmware = firmware_str),cnxn)
		except Exception as error:
			print("""<h5> <span class= "glyphicon glyphicon-remove"> </span> Connection ERROR CODE 101 </h5> """)
			print("""{error_message} """.format(error_message=error))
			exit()

		#####################################################################################################################
		# This part using the query to compute the pivot table to be return to the html page it was called for.
		#####################################################################################################################
		endpoint_names = []

		for ind in df_endpoints.index:
			hardware_model = str(df_endpoints["Hardware Model"][ind])
			if hardware_model not in endpoint_names and hardware_model != "Inventory Device":
				endpoint_names.append(hardware_model)
			else:
				continue

		fo = open("C:/wamp64/www/upgradeplantool/session_files/{session_id}_target_model.txt".format(session_id = sys.argv[7]), "w")

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
		
except Exception as error:
	print("""<h5> <span class= "glyphicon glyphicon-remove"> </span> Connection ERROR 102 </h5> """)
	print("""{error_message} """.format(error_message=error))
	exit()


