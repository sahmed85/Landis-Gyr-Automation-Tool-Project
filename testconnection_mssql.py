#!c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe
############################################################################################
#File: testconnection_mssql.py
#Name: Shad Ahmed
#Date Created: 3/19/2020
#Last Modified: 04/29/2020 
#Usage: Internal | localhost -> to be used externally
#Overview: This is a python file to test a connection to a DB using pyodbc library.  
#Github/Git: sahmed85/ | *this is a private repo*
#Project: UpgradePlanTool
############################################################################################### 

import pyodbc
import sys
#############################################################################################################################
# This section of the script works on building a connection to the database based on command line arguments:
# sys.argv[1] = hostname
# sys.argv[2] = port 
# Returns a message if it works.
#############################################################################################################################
try:
	server = sys.argv[1]
	database = sys.argv[2]
	username = ''
	password = ''
	cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
	print("""<h5> <span class= "glyphicon glyphicon-ok"> </span> Connection Succeded </h5> """)
except Exception as error:
	print("""<h5> <span class= "glyphicon glyphicon-remove"> </span> Connection Failure ERROR 101 </h5> """)
	print("""{error_message} """.format(error_message=error))
	exit()
	