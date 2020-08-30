#!c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe
############################################################################################
#File: testconnection_oracleDB.py
#Name: Shad Ahmed
#Date Created: 3/19/2020
#Last Modified: 04/29/2020 
#Usage: Internal | localhost -> to be used externally
#Overview: This is a python file to test a connection to a DB using cx_Oracle library.  
#Github/Git: sahmed85/ | *this is a private repo*
#Project: UpgradePlanTool
############################################################################################### 

import cx_Oracle
import sys

#############################################################################################################################
# This section of the script works on building a connection to the database based on command line arguments:
# sys.argv[1] = hostname
# sys.argv[2] = port 
# sys.argv[3] = sid/db name
# sys.argv[4] = password
# sys.argv[5] = current Firmware filter
# sys.argv[6] = session id for FILE IO 
# sys.argv[7] = db type 
# Returns a message if it works.
#############################################################################################################################
try:
	dsn_tns = cx_Oracle.makedsn(sys.argv[1], sys.argv[2], service_name= sys.argv[3])
	conn = cx_Oracle.connect(user = sys.argv[4], password = sys.argv[5], dsn= dsn_tns)
	print("""<h5> <span class= "glyphicon glyphicon-ok"> </span> Connection Succeded </h5> """)
except Exception as error:
	print("""<h5> <span class= "glyphicon glyphicon-remove"> </span> Connection Failure ERROR 101 </h5> """)
	print("""{error_message} """.format(error_message=error))
	exit()

