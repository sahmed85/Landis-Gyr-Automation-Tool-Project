#!c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe
############################################################################################
#File: target_info.py
#Name: Shad Ahmed
#Date Created: 3/11/2020
#Last Modified: Ongoing 
#Usage: Internal | localhost -> to be used externally
#Overview: This is test python file to add to target info to the report. 
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
pos_i = 0
for hardware_model in endpoint_names:
	html_table = html_table + """ <tr>
										<td> {hardwaremodel} </td>
										
										<td> 
											<?php echo $fw_version[{pos}];?>
										</td>

										<td> 
											<?php echo $dcw_version[{pos}];?>
										</td>

										<td>
											<?php echo $dcw_filename[{pos}];?>
										</td>

										<td>
											<?php echo $metrology[{pos}];?>
										</td>
										
										<td>
											<?php echo $zigbee[{pos}];?>
										</td>

									</tr>
								""".format(hardwaremodel=hardware_model, pos=pos_i)
	pos_i += 1

html_table = html_table + """ </tbody> </tale> """

print(html_table)




