<!--  ############################################################################################
#File: db_handler.php
#Name: Shad Ahmed
#Date Created: 3/19/2020
#Last Modified: 04/29/2020
#Usage: Internal |
#Overview: This is a PHP file to call to python files with cml arguments. PHP system call to send input from forms to python script.
#Github/Git: sahmed85/ | *this is a private repo*
#Project: UpgradePlanTool
###############################################################################################  -->
<?php
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// This file holds all the calls to python files which have command line arguments from SESSIONS global array and POST array.
// Switch statement below handles the jQuery calls to this script and returns the appropiate information from the python scripts. 
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
session_start();

function test_DB_oracle(){
	$output = system("c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe c:/wamp64/www/upgradeplantool/testconnection_oracleDB.py " .$_POST["db_hostname"]. " " .$_POST["db_portnumber"]. " " .$_POST["db_servicename"]. " " .$_POST["db_username"]. " " .$_POST["db_password"], $retval);
}

function test_DB_mssql(){
	$output = system("c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe c:/wamp64/www/upgradeplantool/testconnection_mssql.py " .$_POST["db_hostname"]. " " .$_POST["db_servicename"], $retval);
}

function callLayerAnalysis(){
	$output = system("c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe c:/wamp64/www/upgradeplantool/db_layeranalysis.py " .$_SESSION["db_hostname"]. " " .$_SESSION["db_port"]. " " .$_SESSION["db_sid"]. " " .$_SESSION["db_username"]. " " .$_SESSION["db_password"]. " " .$_SESSION["currentFirmware"]. " " .$_SESSION["id"]. " " .$_SESSION["type"], $retval);
}

function callTarget_info(){
	$output = system("c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe c:/wamp64/www/upgradeplantool/db_target_info.py " .$_SESSION["db_hostname"]. " " .$_SESSION["db_port"]. " " .$_SESSION["db_sid"]. " " .$_SESSION["db_username"]. " " .$_SESSION["db_password"]. " " .$_SESSION["currentFirmware"]. " " .$_SESSION["id"]. " " .$_SESSION["type"], $retval);
}

function callRouter(){
	$output = system("c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe c:/wamp64/www/upgradeplantool/db_router_appendix.py " .$_SESSION["db_hostname"]. " " .$_SESSION["db_port"]. " " .$_SESSION["db_sid"]. " " .$_SESSION["db_username"]. " " .$_SESSION["db_password"]. " " .$_SESSION["currentFirmware"]. " " .$_SESSION["type"], $retval);
}

function callCollector(){
	$output = system("c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe c:/wamp64/www/upgradeplantool/db_collector_appendix.py " .$_SESSION["db_hostname"]. " " .$_SESSION["db_port"]. " " .$_SESSION["db_sid"]. " " .$_SESSION["db_username"]. " " .$_SESSION["db_password"]. " " .$_SESSION["currentFirmware"]. " " .$_SESSION["type"], $retval);
}

function callLayerAnalysis_infoform(){
	$output = system("c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe c:/wamp64/www/upgradeplantool/db_layeranalysis_infoform.py " .$_SESSION["db_hostname"]. " " .$_SESSION["db_port"]. " " .$_SESSION["db_sid"]. " " .$_SESSION["db_username"]. " " .$_SESSION["db_password"]. " " .$_SESSION["currentFirmware"]. " " .$_SESSION["id"]. " " .$_SESSION["type"], $retval);
}

function callEndpoint(){
	$output = system("c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe c:/wamp64/www/upgradeplantool/db_endpoint_appendix.py " .$_SESSION["db_hostname"]. " " .$_SESSION["db_port"]. " " .$_SESSION["db_sid"]. " " .$_SESSION["db_username"]. " " .$_SESSION["db_password"]. " " .$_SESSION["currentFirmware"]. " " .$_SESSION["id"]. " " .$_SESSION["type"], $retval);
}

function callCount(){
	$output = system("c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe c:/wamp64/www/upgradeplantool/db_currentDeviceCount.py " .$_SESSION["db_hostname"]. " " .$_SESSION["db_port"]. " " .$_SESSION["db_sid"]. " " .$_SESSION["db_username"]. " " .$_SESSION["db_password"]. " " .$_SESSION["currentFirmware"]. " " .$_SESSION["id"]. " " .$_SESSION["type"], $retval);
}

switch($_POST["functionname"]){
	
	case 'test_connection_oracle':
	test_DB_oracle();
	break;

	case 'test_connection_mssql':
	test_DB_mssql();
	break;

	case 'callLayerAnalysis':
	callLayerAnalysis();
	break;

	case 'callTarget_info':
	callTarget_info();
	break;

	case 'callRouter':
	callRouter();
	break;

	case 'callCollector':
	callCollector();
	break;

	case 'callLayerAnalysis_infoform':
	callLayerAnalysis_infoform();
	break;

	case 'callEndpoint':
	callEndpoint();
	break;

	case 'callCount':
	callCount();
	break;

	default:
	echo "Error in AJAX http request to server.";
}

?> 	
