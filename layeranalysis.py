#!c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe
############################################################################################
#File: layeranalysis.py
#Name: Shad Ahmed
#Date Created: 3/3/2020
#Last Modified: 04/29/2020  
#Usage: Internal | localhost -> to be used externally
#Overview: This file is a python script using CGI to compute a layer analysis based on files uploaded.
#		   Layer Analysis uses the Endpoint Extract to build a layer analysis and run a summation calculation. 
#Github/Git: sahmed85/ | *this is a private repo*
#Project: UpgradePlanTool
############################################################################################### 
import pandas as pd 
from openpyxl import load_workbook
import numpy as np
import sys
try:
	try:
	###############################################################################################################################
	# This reads in the excel file and computes a pivot table to be returned to the appropiate html. Throws an error if failed to 
	# read the file.
	###############################################################################################################################
		this_file = open('C:/wamp64/www/upgradeplantool/session_files/{session}_excel_layer.txt'.format(session = sys.argv[1]))
		html_content = this_file.read()
		print(html_content)
		this_file.close()
	except:
		df_endpoints = pd.read_excel('C:/wamp64/www/upgradeplantool/uploads/{session_id}_endpoints.xlsx'.format(session_id = sys.argv[1]))

		layer_count = {-1:0}
		totalmeter_count = 0

		for ind in df_endpoints.index:
			#print(df_endpoints["Layer"][ind])
			if df_endpoints["Status Code"][ind] in ["Normal", "Discovered", "Installed"]:
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
			else:
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
	print("""<h5> <span class= "glyphicon glyphicon-remove"> </span> Connection ERROR 202 </h5> """)
	print("""{error_message} """.format(error_message=error))
	exit()