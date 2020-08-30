#!c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe
############################################################################################
#File: table_test.py
#Name: Shad Ahmed
#Date Created: 3/11/2020
#Last Modified: Ongoing 
#Usage: Internal | localhost -> to be used externally
#Overview: This is a test file.
#Github/Git: sahmed85/ | *this is a private repo*
#Project: UpgradePlanTool
############################################################################################### 

import pandas as pd 
from openpyxl import load_workbook
import numpy as numpy

df_endpoints = pd.read_excel('test_endpoints.xlsx')
endpoint_names = []

for ind in df_endpoints.index:
	hardware_model = str(df_endpoints["Hardware Model"][ind])
	if hardware_model not in endpoint_names and hardware_model != "Inventory Device":
		endpoint_names.append(hardware_model)
	else:
		continue

#print(endpoint_names)

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
											<input type = "text" class = "form-control" name = "fw_version" id= "fw_version" placeholder="13.54">
										</td>

										<td> 
											<input type = "text" class = "form-control" name = "dcw_version" id= "dcw_version" placeholder="240D.13.53.0014">
										</td>

										<td>
											<input type = "text" class = "form-control" name = "dcw_filename" id= "dcw_filename" placeholder="FAXG.13.53.hex">
										</td>

										<td>
											<input type = "text" class = "form-control" name = "metrology" id= "metrology" placeholder="5.70">
										</td>
										
										<td>
											<input type = "text" class = "form-control" name = "zigbee" id= "zigbee" placeholder="2.04.15">
										</td>

									</tr>
								""".format(hardwaremodel=hardware_model)

html_table = html_table + """ </tbody> </tbale> """

print(html_table)




