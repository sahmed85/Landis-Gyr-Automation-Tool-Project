#!c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe
############################################################################################
#File: currentDeviceCount.py
#Name: Shad Ahmed
#Date Created: 3/5/2020
#Last Modified: 04/29/2020 
#Usage: Internal | localhost -> to be used externally
#Overview: This file is a python script using CGI to compute a current device counts based on files uploaded.
#		   Current device count uses the Endpoint and Collector Extract to build a summation of all endpoint types. 
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
	df_collectors = pd.read_excel('C:/wamp64/www/upgradeplantool/uploads/{session_id}_collectors.xlsx'.format(session_id = sys.argv[1]))
	df_endpoints = pd.read_excel('C:/wamp64/www/upgradeplantool/uploads/{session_id}_endpoints.xlsx'.format(session_id = sys.argv[1]))

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
	try:
		this_file = open('C:/wamp64/www/upgradeplantool/session_files/{session}_excel_count.txt'.format(session = sys.argv[1]))
		html_content = this_file.read()
		print(html_content)
		this_file.close()
	except:
		endpoint_info = {}

		for ind in df_endpoints.index:
			metertype = str(df_endpoints["Hardware Model"][ind])
			if metertype not in endpoint_info.keys():
				endpoint_info[metertype] = 1
			else:
				endpoint_info[metertype] += 1

		df_endpointsTable = pd.DataFrame(columns= ['Meter Type','Count of Meter'])
		df_endpointsTable["Meter Type"] = endpoint_info.keys()
		df_endpointsTable["Count of Meter"] = endpoint_info.values()

		html_endpoint = df_endpointsTable.to_html(index=False)
		print(html_endpoint)
		
except Exception as error:
	print("""<h5> <span class= "glyphicon glyphicon-remove"> </span> Connection ERROR 202 </h5> """)
	print("""{error_message} """.format(error_message=error))
	exit()