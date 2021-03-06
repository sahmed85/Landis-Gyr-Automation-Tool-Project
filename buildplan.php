<!-- ############################################################################################
#File: buildplan.php
#Name: Shad Ahmed
#Date Created: 2/18/2020
#Last Modified: 04/29/2020 
#Usage: Internal | localhost -> to be used externally
#Overview: This file is a dev file to create a firmware/network upgrade plan for customers.  
#Github/Git: sahmed85/ | *this is a private repo*
#Project: UpgradePlanTool
############################################################################################### -->
<?php
	///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	// This part of the script starts a session for the current user on the server. This allows to use SESSION global array to carry 
	// data across PHP files.
 	///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	session_start();
	$_SESSION["id"] = session_id();
?>
<!DOCTYPE HTML>
<html>
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<!-- These headers are for linking the Bootstrap objects into this webpackage -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
	<title>	Upgrade Plan Tool Home </title>
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

	</style>
</head>
<body>
	<nav class = "nav navbar-default" style = "background-color:#8cba51" >
		<div class = "navbar-header"> 
			<a class = "navbar-brand" href = "home.html"; style = "color: white"> L+G Upgrade Plan Tool </a>
		</div>
		<ul class = "nav navbar-nav">
			<li> <a href= "home.html"> Home </a></li>
			<li class = "active"> <a href = "#"> Build a Plan </a> </li>
		</ul>
		<ul class = "nav navbar-nav navbar-right">
			<li> <a href = "about.html"> <span class = "glyphicon glyphicon-exclamation-sign"></span> About </a> </li>
			<li> <a href="help.html"> <span class = "glyphicon glyphicon-user"></span> Help </a> </li>
		</ul>
	</nav>

	<div class="jumbotron text-center">
		<h2> Firmware Upgrade Plan Tool: </h2>
	</div>

	<div class = "container-fluid text-center" style = "background-color: #abeda8">
		<h2 style="text-align: center"> Build a Plan </h2>
		<h4 style="text-align: center"> Let's get some information on your customer in order to generate a plan!</h4>
		<br>
	</div>
	<div class="row content row-no-gutters" style = "background-color: #abeda8">
		<div class="col-sm-6 classWithPad">
			<h4> Enter the databse information so the application can connect authenticate to the database: </h4>
			<h5> Note: MSSQL connection will not need all fields, simply add the DB URL, Database Name and Firmware Version and test the connection </h5>
			<h5> <i>If your are unable to login using the database credentials for the customer or a self-hosted customer, use the option below to upload a XLS file.</i> </h5>
			
			<form action="db_infoform.php" method = "POST" target="_self" id="login">
				<h4> Select the databse type the customer is supported on (select one): </h4>
				<div class="form-group">
					<input type="radio" value= "oracle" name="dbtype" onclick="reenable()" required>
					<label> Oracle </label>
					<br>
					<input type="radio" value="mssql" name="dbtype" onclick="disable()">
					<label> Microsoft SQL </label>
				</div>

				<h4> Enter the user information for authentication to DB: </h4>
				<div class="form-group">
					<label for="username"> Username: </label>
					<br>
					<input type="text" id="username" name="username" placeholder="Oracle Username" disabled>
				</div>

				<div class="form-group">
					<label for="password"> Password: </label>
					<br>
					<input type="password" name="password" id="password" disabled>
				</div>

				<h4> Enter the details to the DB: </h4>
				<div class="form-group">
					<label for="hostname"> Hostname: </label>
					<input type="text" name="hostname" id="hostname" placeholder="DB url" class="form-control">
				</div>

				<div class="form-group">
					<label for="port"> Port Number: </label>
					<input type="text" name="port" id="port" placeholder="1521" class="form-control" disabled>
				</div>

				<div class="form-group">
					<label for="SID"> SID/Database Name: </label>
					<input type="text" name="sid" id="sid" placeholder="SID" class="form-control">
				</div>

				<div class="form-group">
					<label for="currentFirmware"> Current Firmware Version(s) to be upgraded: (Comma Seperate if multiple versions or type All for all types) </label>
					<input type="text" name="currentFirmware" id="currentFirmware" placeholder="6.17, 9.18 or All" class="form form-control">
				</div>

				<button onclick="testDBresponse()" class="btn btn-inverse"> Test Database Connection </button>

				<div id="connectionTest">
					<h5> *Click to Test Connection*</h5>
				</div>

				<input type="submit" value="Submit" class="btn btn-inverse">

			</form>
		</div>
	</div>
	<hr>
	<div class="row content row-no-gutters" style = "background-color: #abeda8"> 
		<div class="col-sm-6 classWithPad">
			<h4> Upload a excel file (.xlsx):  </h4>
			<h5> Upload endpoint extract, collector extract and network device extract from the customer CC. </h5>
			<br>
			<form action="infoform.php" method="POST" enctype="multipart/form-data" target="_self">
				Select Endpoint Extract to upload:
				<input type="file" name="endpointextract" id = "file1">
				<br>
				Select Collector Extract to upload:
				<input type="file" name="collectorextract" id = "file2">
				<br>
				Select Network Device Extract to upload:
				<input type="file" name="networkextract" id="file3">
				<br>
				<input type="submit" value ="Upload Data" name = "Upload" class="btn btn-inverse" >
			</form>
		</div>
	</div>

	<script type="text/javascript">
		////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		// These Javascript calls work on click events of either clicking Oracle or MSSQL. This helps disable certain form inputs
		// if Oracle or MSSQL is chosen. This part also has a function for testing a database connection which in turn has a jQuery
		// call which in turn call a python file to test a connection for either Oracle or MSSQL. 
		////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		var type;

		function disable(){
			document.getElementById("username").setAttribute("disabled","True");
			document.getElementById("password").setAttribute("disabled","True");
			document.getElementById("port").setAttribute("disabled","True");
			type = "mssql";

		}
		function reenable(){
			document.getElementById("username").removeAttribute("disabled");
			document.getElementById("password").removeAttribute("disabled");
			document.getElementById("port").removeAttribute("disabled");
			type = "oracle";
		}

		function testDBresponse(){
			if (type == "oracle"){
				event.preventDefault();
				var hostname = document.getElementById("hostname").value;
				var portnumber =document.getElementById("port").value;
				var service_name = document.getElementById("sid").value;
				var username = document.getElementById("username").value;
				var password = document.getElementById("password").value;
				jQuery.ajax ({
					type: "POST",
					url: 'db_handler.php',
					data: {functionname:'test_connection_oracle',db_hostname: hostname, db_portnumber: portnumber, db_servicename: service_name,db_username: username, db_password: password},
					success: function(data){
						document.getElementById("connectionTest").innerHTML = data;
					}
				});
			} 

			else if (type == "mssql"){
				event.preventDefault();
				var hostname = document.getElementById("hostname").value;
				var service_name = document.getElementById("sid").value;
				jQuery.ajax ({
					type: "POST",
					url: 'db_handler.php',
					data: {functionname:'test_connection_mssql',db_hostname: hostname,db_servicename: service_name},
					success: function(data){
						document.getElementById("connectionTest").innerHTML = data;
					}
				});
			}

		}
	</script>
</body>                                