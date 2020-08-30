#!c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe
############################################################################################
#File: test_oracleDB.py
#Name: Shad Ahmed
#Date Created: 3/11/2020
#Last Modified: Ongoing 
#Usage: Internal | localhost -> to be used externally
#Overview: This is a test python file to connect to a DB using cx_Oracle library.  
#Github/Git: sahmed85/ | *this is a private repo*
#Project: UpgradePlanTool
############################################################################################### 

import cx_Oracle
import sys

try:
	dsn_tns = cx_Oracle.makedsn(sys.argv[1], sys.argv[2], service_name= sys.argv[3])
	conn = cx_Oracle.connect(user = sys.argv[4], password = sys.argv[5], dsn= dsn_tns)
	print("""<h5> Connection Succeded </h5> """)
except Exception as error:
	print("""<h5> Connection Failure </h5> """)
	print("""{error_message} """.format(error_message=error))
	exit()

# c = conn.cursor()
# c.execute(' SELECT * FROM collectors')

# for row in c:
# 	print(row[2], '-', row[3])

# conn.close()
