<!-- ############################################################################################
#File: actiontest.php
#Name: Shad Ahmed
#Date Created: 2/18/2020
#Last Modified: Ongoing 
#Usage: Internal | localhost -> to be used externally
#Overview: This file is a test file to test php forms and forms validation.  
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
			<li class = "active"> <a href = "buildplan.html"> Build a Plan </a> </li>
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
		$databasename = $_POST["option1"];
		echo $databasename;
	?>
</body>
</html>
