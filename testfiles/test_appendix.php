<!-- ############################################################################################
#File: appendix.php
#Name: Shad Ahmed
#Date Created: 3/3/2020
#Last Modified: Ongoing 
#Usage: Internal | localhost -> to be used externally
#Overview: This file is meant to call the python script using CGI to compute the tables for appendix.
#Github/Git: sahmed85/ | *this is a private repo*
#Project: UpgradePlanTool
############################################################################################### -->
<?php

function callCollector(){
		$output = system("c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe c:/wamp64/www/upgradeplantool/collector_appendix.py", $retval);
	}

function callRouter(){
		$output = system("c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe c:/wamp64/www/upgradeplantool/router_appendix.py", $retval);
	}

function callEndpoint(){
		$output = system("c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe c:/wamp64/www/upgradeplantool/endpoint_appendix.py", $retval);
	}

function callTable_test(){
		$output = system("c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe c:/wamp64/www/upgradeplantool/table_test.py", $retval); 
	}

switch($_POST["functionname"]){ 

	case 'callCollector': 
		callCollector();
		break;

	case 'callRouter':
		callRouter();
		break;

	case 'callEndpoint':
		callEndpoint();
		break;

	case 'callTabletest':
		callTable_test();
		break;

	default:
		echo "Error in AJAX http request to server.";

} 

?>
