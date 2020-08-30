<!-- ############################################################################################
#File: python_handler.php
#Name: Shad Ahmed
#Date Created: 3/3/2020
#Last Modified: 04/29/2020
#Usage: Internal | localhost -> to be used externally
#Overview: This file is meant to call the python script using CGI to compute all calls requested from AJAX calls in html files. 
#Github/Git: sahmed85/ | *this is a private repo*
#Project: UpgradePlanTool
############################################################################################### -->
<?php

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// This file holds all the calls to python files which have command line arguments from SESSIONS global array and POST array.
// Switch statement below handles the jQuery calls to this script and returns the appropiate information from the python scripts. 
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

session_start();

function callCollector(){
	$output = system("c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe c:/wamp64/www/upgradeplantool/collector_appendix.py " .$_SESSION["id"], $retval);
}

function callRouter(){
	$output = system("c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe c:/wamp64/www/upgradeplantool/router_appendix.py " .$_SESSION["id"], $retval);
}

function callEndpoint(){
	$output = system("c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe c:/wamp64/www/upgradeplantool/endpoint_appendix.py " .$_SESSION["id"], $retval);
}

function callTarget_info(){
	$output = system("c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe c:/wamp64/www/upgradeplantool/target_info.py " .$_SESSION["id"], $retval); 
}

function callCount(){
	$output = system("c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe c:/wamp64/www/upgradeplantool/currentDeviceCount.py " .$_SESSION["id"], $retval);
}

function callLayerAnalysis(){
	$output = system("c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe c:/wamp64/www/upgradeplantool/layeranalysis.py " .$_SESSION["id"], $retval);
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

	case 'callTarget_info':
	callTarget_info();
	break;

	case 'callCount':
	callCount();
	break;

	case 'callLayerAnalysis':
	callLayerAnalysis();
	break;
	
	default:
	echo "Error in AJAX http request to server.";

} 

?>
