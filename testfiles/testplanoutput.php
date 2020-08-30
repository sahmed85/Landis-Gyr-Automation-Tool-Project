<!-- ############################################################################################
#File: testplanoutput.php
#Name: Shad Ahmed
#Date Created: 2/25/2020
#Last Modified: Ongoing 
#Usage: Internal | localhost -> to be used externally
#Overview: This file holds the php script calling the python script that calls the appendix.py to generate all the 					tables used in firmware upgrade plan. This is a test file. 
#Github/Git: sahmed85/ | *this is a private repo*
#Project: UpgradePlanTool
############################################################################################### -->
<!DOCTYPE HTML>
<html>
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<!-- These headers are for linking the Bootstrap objects into this webpackage -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
	<title>	Layer Analysis </title>
	<style>
		
		h3 {
			color: black ;
		}

		.logo {
			font-size: 200px;
		}

		.col-sm-4 {
			text-align: center;
			margin: 25px 0;
		}

		.classWithPad {
			margin: 10px;
			padding: 10px;
		}

		div.bodycolor {
			background-color: #abeda8
		}

		input, textarea{
			background-color: #ebe6e6;	
		}

		table {
			border-collapse: collapse;
			width: 60%;
		}

		th, td {
			text-align: left;
			padding: 5px;
		}

		tr:nth-child(even) {
			background-color: #f2f2f2;
		}
</style>
<body>
<?php
function callAppendix(){
		$output = system("c:/Users/ahmeds/AppData/local/Programs/Python/Python35/python.exe c:/wamp64/www/upgradeplantool/appendix.py", $retval);
	}
callAppendix();
?>
</body>
</head>
</html>
