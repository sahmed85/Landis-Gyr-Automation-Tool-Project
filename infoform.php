<!-- ############################################################################################
#File: infoform.php
#Name: Shad Ahmed
#Date Created: 2/25/2020
#Last Modified: 04/29/2020
#Usage: Internal | localhost -> to be used externally
#Overview: This file holds the php script for reading in the files from the upload and moving them to the appropiate dir.
		   This file also holds the html form builder that will be used to generate the plan
		   This files also has a dependency call for a python script in php to render what table data to be read in the next php file.     
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
	<title>	Build Plan : Form </title>
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

		@keyframes spinner {
			0% {
				transform: translate3d(-50%, -50%, 0) rotate(0deg);
			}
			100% {
				transform: translate3d(-50%, -50%, 0) rotate(360deg);
			}
		}

		.spin::before {
			animation: 1.5s linear infinite spinner;
			animation-play-state: inherit;
			border: solid 5px #cfd0d1;
			border-bottom-color: #1c87c9;
			border-radius: 50%;
			content: "";
			height: 70px;
			width: 70px;
			position: absolute;
			top: 50%;
			left: 50%;
			transform: translate3d(-50%, -50%, 0);
			will-change: transform;
		}

	</style>
</head>
<body>
	<?php
	///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	// This PHP script takes in the form information from the buildplan.php and stroes them into the SESSION global array so it 
	// can hold user information and carry forward it to other PHP scripts. 
	///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	session_start();
	?>
	<nav class = "nav navbar-default" style = "background-color:#8cba51" >
		<div class = "navbar-header"> 
			<a class = "navbar-brand" href = "home.html"; style = "color: white"> L+G Upgrade Plan Tool </a>
		</div>
		<ul class = "nav navbar-nav">
			<li> <a href= "home.html"> Home </a></li>
			<li class = "active"> <a href = "buildplan.php"> Build a Plan </a> </li>
		</ul>
		<ul class = "nav navbar-nav navbar-right">
			<li> <a href = "about.html"> <span class = "glyphicon glyphicon-exclamation-sign"></span> About </a> </li>
			<li> <a href="help.html"> <span class = "glyphicon glyphicon-user"></span> Help </a> </li>
		</ul>
	</nav>

	<div class="jumbotron text-center">
		<h2> Firmware Upgrade Plan Tool: </h2>
	</div>

	<?php
		

		if($_SERVER["REQUEST_METHOD"] == "POST"){
			
			///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
			// This PHP section deals with excel uploads from buildplan.php and checks to see if they are .xlsx. 
			// Throws errors if errors. 
			///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

			if((isset($_FILES["endpointextract"]) && $_FILES["endpointextract"]["error"] == 0) && (isset($_FILES["collectorextract"]) && $_FILES["collectorextract"]["error"] == 0) && (isset($_FILES["networkextract"]) && $_FILES["networkextract"]["error"] == 0)) {
				
				move_uploaded_file(($_FILES["endpointextract"]["tmp_name"]), "uploads/" .$_SESSION["id"]. "_endpoints.xlsx");
				move_uploaded_file(($_FILES["collectorextract"]["tmp_name"]), "uploads/" .$_SESSION["id"]. "_collectors.xlsx");
				move_uploaded_file(($_FILES["networkextract"]["tmp_name"]), "uploads/" .$_SESSION["id"]. "_network.xlsx");

			}
			else{
				echo "ERROR 201 is set check fail!";
				die();
			}
		}
		else {
			echo "ERROR 201 server post check fail!";
			die();
		}
	?> 

	<div class = "container-fluid text-center" style = "background-color: #abeda8">
		<h2 style="text-align: center"> Build a Plan </h2>
		<h4 style="text-align: center"> The upload has been received and being processed with python!</h4>
		<h4 style="text-align: center"> Let's get some more information to generate the plan: </h4>
		<br>
	</div>
	<br>
	<!-- Inserting form here that will be used to complete the report! -->
	<div class="container">

		<form class="form-horizontal" action = "report.php" method="POST" target="_blank" enctype="multipart/form-data">
			<div class="form-group">
				<label for="customerName">Customer Name:</label>
				<input type="text" class="form-control" id="customerName" placeholder="Customer" name="customerName">
			</div>

			<div class="form-group">
				<label for="customerName">Current CC Version:</label>
				<input type="text" class="form-control" id="ccVersion" placeholder="7.4 MR1" name="ccVersion">
			</div>

			<div class="form-group">
				<label> Maintenance Release Documentation For Current CC (http link): </label>
				<input type="text" class="form-control" id="docID" placeholder="DOC ID" name="docID">
				<input type="text" class="form-control" id="docID" placeholder="URL Here" name="docURL">
			</div>	

			<div class="form-group">
				<label> Target FW/DCW Version as per current CC version (below are the customer's meter type): </label>
				<div id = "target_info">
					<div class="spin">
					</div>
				</div>
			</div>

			<div class="form-group">
				<label for="networkMap">Network Map upload:</label>
				<input type="file" class="form-control" id="networkMap" name="networkMap">
			</div>

			<div class="form-group">
				<h5><strong> Based on the layer analysis provided <a href="layeranalysis.html" target="_blank">here</a>:</strong></h5>
				<label> For the initial group command test and small broadcast test, enter the collector name:</label>
				<input type="text" class="form-control" name="collector_name" placeholder="Collector Name">
				<label for="testhopsttl">For the small test of firmware and DCW broadcast (section 2.4 in template) enter the number of hops and TTL:</label>
				<input type="text" class="form-control" id="hopsttl" placeholder="number of hops" name="testhops">
				<input type="text" class= "form-control" id="hopsttl" placeholder="TTL number" name="testttl">
			</div>

			<div class="form-group">
				<h5><strong>Based on the layer analysis provided:</strong></h5>
				<label for="broadhopsttl">For the firmware and DCW broadcast (section 2.5 in template) enter the number of hops and TTL:</label>
				<input type="text" class="form-control" id="broadhopsttl" placeholder="number of hops" name="broadhops">
				<input type="text" class= "form-control" id="broadhopsttl" placeholder="TTL number" name="broadttl">
			</div>

			<button type="submit" class="btn btn-default">Generate Plan</button>
		</form>
	</div>

	<script type="text/javascript">
		/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		// This is a jQuery call to the server to call a python script. This is handled by the python_handler.php. 
		/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		jQuery.ajax ({
			type: "POST",
			url: 'python_handler.php',
			data: {functionname: 'callTarget_info'},
			success: function(data){
				document.getElementById("target_info").innerHTML = data;
			}
		})
	</script>

</body>
</html>

