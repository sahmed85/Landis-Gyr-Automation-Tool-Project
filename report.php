<!-- ############################################################################################
#File: report.php
#Name: Shad Ahmed
#Date Created: 3/9/2020
#Last Modified: 04/29/2020 
#Usage: Internal | localhost -> to be used externally
#Overview: This file holds the html tags for outputting the report. Using AJAX it calls a php script which calls the 	 layeranalysis and appendix python scripts for tables.  
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
	<title>	Upgrade Report </title>
	<style>
		
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
			table-layout: auto;
  			width: 650px;
		}

		th, td {
			text-align: left;
			padding: 1px;
		}

		tr:nth-child(even) {
			background-color: #f2f2f2;
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

		thead   {display: table-header-group;   }

		tfoot   {display: table-footer-group;   }

	</style>
</head>
<body>
	
	<?php
		
		/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		// This PHP script is used to create global variables which are used inside the html tags to fulfill information inside the
		// template. This data is the POST from the db_infoform.php and used throughout this file. 
		////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		
		session_start();
		$customer_name = $_POST["customerName"];
		$cc_version = $_POST["ccVersion"];
		$fw_version = $_POST["fw_version"];
		$dcw_version = $_POST["dcw_version"];
		$dcw_filename = $_POST["dcw_filename"];
		$metrology = $_POST["metrology"];
		$zigbee = $_POST["zigbee"];
		$collector_name = $_POST["collector_name"];
		$test_hops = $_POST["testhops"];
		$test_ttl = $_POST["testttl"];
		$broad_hops = $_POST["broadhops"];
		$broad_ttl = $_POST["broadttl"];
		$doc_id = $_POST["docID"];
		$doc_url = $_POST["docURL"];

		/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		// This part sets the filename for the network map upload and set it to a global variable to used in the html tag. 
		////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		
		if($_SERVER["REQUEST_METHOD"] == "POST"){
				if(isset($_FILES["networkMap"]) && $_FILES["networkMap"]["error"] == 0){
					$image_ext = pathinfo($_FILES["networkMap"]["tmp_name"], PATHINFO_EXTENSION);
					move_uploaded_file(($_FILES["networkMap"]["tmp_name"]), "uploads/" .$_SESSION["id"]. "_networkmap.png");
					$image_src = "/upgradeplantool/uploads/" .$_SESSION["id"]. "_networkmap.png";
				}
				else{
					$image_src = "/upgradeplantool/uploads/null.jpeg";
				}
			}
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
		<h2> Firmware Upgrade Plan Report: </h2>
		<p> Simply Click 'Copy Report' and Paste it into the downloadable LG Template!</p>
		<button class = "btn btn-default" onclick="CopyToClipboard('report')">Copy Report</button>
		<button class = "btn btn-default"> <a href="/upgradeplantool/download/template.docx" download> Download Template </a></button>
	</div>

	<div class="container" id = "report">
		<h2> 1 Summary </h2>
		<h5> This guide will outline the steps needed to the upgrade of Integrated Enhanced Focus AX meters. The goal firmware version is shown in the target firmware table below (Section 1.3). The customer is currently using Command Center <?php echo $cc_version;?>. </h5>
		<h5> Landis+Gyr will facilitate the update of the Enhanced Integrated Focus AX meters. The customer will be responsible for upgrading the rest of the network devices. Landis+Gyr will provide an upgrade plan for the rest of the network if the customer would like. </h5>
		<h5> This document is a recommendation. All update processes should follow L+G’s official RF Network Device Upgrade Guide (<a href="http://connection.am.bm.net/departments/Sales/Shared%20Documents/Technical%20Sales/Tools/Documentation/98-1290.pdf">98-1290</a>). </h5>
		<h5>It will likely take several weeks to complete the update of firmware and DCW but the majority should be done in 2-3 weeks.</h5>  

		<h3> 1.1 Reference Documents </h3>
		<h5> <a href = "http://connection.am.bm.net/departments/Sales/Shared%20Documents/Technical%20Sales/Tools/Documentation/98-1290.pdf">98-1290</a> : Gridstream RF Network Device Upgrade Guide <br>
			 <a href="<?php echo $doc_url;?>"><?php echo $doc_id;?></a> : CC <?php echo $cc_version;?> Maintenance Release Notes
		</h5>

		<h3> 1.2 Current Device Type Counts </h3>
		<div id = 'insert_count' style="padding-left: 5px">
			<div class="spin"></div>
		</div>

		<h3> 1.3 Target Firmware/DCW Versions </h3>
		<h5> <i> Per Command Center <?php echo $cc_version; ?> Release Notes </i> </h5>
		<div id="targetTable" style="padding-left:5px">
			<table broder="1" class="dataframe">
					<thead>
						<tr style = "text-align: center;">
							<th> Meter </th>
							<th> Firmware Version </th>
							<th> DCW Version </th>
							<th> DCW Filename </th>
							<th> Metrology </th>
							<th> Zigbee </th>
						</tr>
					</thead>
					<tbody> 
			<?php 
				
				////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
				// This part of the scripts utilizes file IO of PHP to check if the hardware model types are saved in the 
				// directory.
				////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

				$target_file = fopen("C:/wamp64/www/upgradeplantool/session_files/" .$_SESSION["id"]. "_target_model.txt", "r");
				$pos = 0;
				while(!feof($target_file)) {
					echo "<tr>
						<td>" .fgets($target_file). "</td>
						<td>" .$fw_version[$pos]. "</td>
						<td>" .$dcw_version[$pos]."</td>
						<td>" .$dcw_filename[$pos]. "</td>
						<td>" .$metrology[$pos]. "</td>
						<td>" .$zigbee[$pos]. "</td>
					</tr>";
					$pos = $pos + 1;
				}
				fclose($target_file);
			?>
				</tbody>
			</table>
		</div>

		<h3> 1.4 Broadcast Plan </h3>
		<h5> Below is a map showing <?php echo $customer_name;?>'s network architecture. </h5>
		<!-- Insert Picture of Network design map here -->
		<img src="<?php echo $image_src;?>" style="padding-left: 5px; width:700px;height:500px;" alt="Network Map should be Here">
		<p> <i> Figure 1. Broadcast Plan Map </i> </p>

		<h3> 1.5 Scheduling </h3>
		<h5> It is important not to schedule broadcasts during scheduled maintenance of the system. </h5>

		<h2> 2 Upgrade Steps </h2>
		<h3> 2.1 Request Firmware Files </h3>
		<ul> 
			<li> <h5> Request <?php echo $fw_version[0]; ?> firmware files specifically for <?php echo $customer_name; ?>. </h5></li>
			<li> <h5>Both the <strong>current </strong> and <strong>target</strong> versions of firmware must be loaded into Command Center</h5></li>
		</ul>

		<h3> 2.2 Meter Shop Test </h3>
		<ul>
			<li> <h5> At least one meter of each type and Program ID that will be receiving a Firmware upgrade should be tested in the Meter Shop for validation purposes prior to beginning field upgrades.</h5></li>
			<li> <h5> This will help to ensure that no major issues occur in the broadcast.</h5></li>
		</ul> 

		<h3> 2.3 Initial Group Test </h3>
		<ul>
			<li> <h5> Select 25 meters on the Collector <?php echo $collector_name; ?> and upgrade them in Command Center individually using a Group Command.</h5></li>
				<ul>
					<li> <h5> Send the 25 meters a Get Endpoint Information command to the 25 meters to confirm it took the firmware.</h5></li>
					<li> <h5> Then upgrade the DCW and metrology using Group Commands. </h5></li>
				</ul>
			<li> <h5> Verify that all upgraded meters are reading properly and can send/receive data.</h5></li>
		</ul>

		<h3> 2.4 Small Broadcast Test </h3>
		<ul>
			<li> <h5> Run a small broadcast from the Collector <?php echo $collector_name; ?>, <strong> set maximum hops to <?php echo $test_hops; ?> and TTL to <?php echo $test_ttl; ?> </strong>. </h5> </li>
				<ul> 
					<li> <h5> Broadcast a DCW update with the same settings. </h5> </li>
				</ul>
			<li> <h5> Verify that all meters are operating properly or have assignable cause for error that is not due to the broadcast of new firmware. </h5> </li>
			<li> <h5> Evaluate the distance travelled by the packets in the broadcast. If necessary, maximum hops can be increased. </h5> </li>
		</ul>

		<h3> 2.5 Firmware and DCW Broadcast </h3>
		<ul>
			<li> <h5> Now, update all the meters’ firmware via broadcast. </h5> </li>
			<li> <h5> Start with broadcasting on the Collectors in Red above; with settings of <?php echo $test_hops;?> hops and TTL of <?php echo $test_ttl;?></strong>. </h5> </li>
			<li> <h5> After each broadcast finishes, run Endpoint Extracts from Command Center to determine effectiveness of broadcast. </h5></li>
			<ul>
				<li> <h5> After each broadcast finishes, run Endpoint Extracts from Command Center to determine effectiveness of broadcast. </h5></li>
				<li> <h5> Evaluate remaining meters needing update after each broadcast and design future broadcasts according to the quantity of meters remaining on each Collector; i.e. – broadcast on Collectors with highest number meters remaining.</h5></li>
				<li> <h5> After  more than 97% of the meters were updated, users usually use a Group Command from CC to update remaining meters. </h5></li>
				<li> <h5> If less than 97% of Group Command meters were updated, consider running an additional Repeat Group Command.</h5></li>
				<li> <h5> If more than 97% of meters from the Group Command were updated and meters are, upgrade the stragglers through RadioShop.</h5></li>
			</ul>
			<li> <h5> After the firmware download is complete, broadcast DCWs with the same broadcast settings and general upgrade plan as above for firmware.</h5></li>
			<ul>
				<li> <h5> Upgrade DCW stragglers with Command Center Group Commands or through RadioShop. </h5></li>
				<li> <h5> Be sure to only broadcast to meters with the correct firmware version.</h5></li>
			</ul>
			<li> <h5> Verify that all meters are running correctly. </h5></li>
		</ul>

		<h2> 3 Information on Broadcasting Process </h2>
		<h3> 3.1 General Information </h3>
		<h5> Broadcasting is a tool that Command Center allows us to use to update groups of meters at one time. When using this tool, it is important to understand the process, and to understand the possible risks. </h5>
		<h5> The first step is uploading both the <strong> current </strong> and <strong> target </strong> firmware files into Command Center.</h5>
		<h5> Each broadcast update must target a specific combination of endpoint device type, firmware, and DCW. Any endpoints with DCWs below 9.5X upgrading to the target versions need to follow the broadcast practices in the “Command Center Broadcast Deviation” best practice document. Meters upgrading from 9.X to 10.X firmware should be sorted into separate categories by meter type, Tariff ID, and Misc ID.</h5>
		<h5> For all other meters, one meter of each type, form and program should be upgraded via P2P or Radioshop prior to ANY broadcast updates and a GEC should be sent to each of them. Landis+Gyr will run a query to define each of these meter combinations. For example, if the customer has Focus AX Enhanced Integrated 2S meters with 3 different meter program IDs, then they would need to seed and then issue a GEC to 3 meters, one of each type.</h5>
		<h5> A Layer Analysis is conducted in order to reach at least 98% of meters in as few hops as possible. A broadcast should never exceed 10 hops unless L+G recommends it based on the network architecture. </h5>
		<h5> Firmware broadcasts can take approximately 3 days to complete for one round. If any meters fail to update via broadcast after 2 rounds of broadcast, they must be updated point to point (P2P). This can be done in Command Center, or in RadioShop.</h5>
		<h5> After firmware upgrade is verified as successful, DCW and Metrology can be updated. In the case of Integrated meters, metrology is automatically updated with firmware and only DCW needs to be upgraded. DCW upgrades are sent out via broadcast in the same design as firmware upgrades. DCW and Metrology broadcasts usually take 2-3 hours to complete. Any DCW broadcast failures must be upgraded P2P via Command Center or RadioShop.</h5>

		<h3> 3.2 How to Issue a Broadcast Command </h3>
		<h5> To broadcast upgrade commands to network devices, perform the following steps:</h5>
		<img src="/upgradeplantool/images/img1.png" style="padding-left: 5px">  
		<ol>
			<li><h5> Navigate to the <strong> Network > Endpoints > Broadcast Commands </strong> page and select the <strong> Endpoint Firmware Download </strong> command. </h5></li>
			<li><h5> Select the desired device from the <strong> Endpoint Model </strong> drop-down list: Enhanced Integrated Focus AX. </h5></li>
			<li><h5> Select the filter <strong> Zigbee Capable: </strong>Yes. </h5></li>
			<li><h5> Select the filter <strong> Module Firmware</strong> version: All. </h5></li>
			<li><h5> Select the filter <strong> DCW Version</strong>: All.</h5></li>
			<li><h5> Select the <strong> Collector(s)</strong>.</h5> </li>
			<li><h5> Set the target <strong> New Firmware to Send</strong> version.</h5></li>
			<li><h5> Set <strong> Maximum Hops to <?php echo $broad_hops;?> (see Layer Analysis) and Maximum TTL to <?php echo $broad_ttl;?> </strong></h5></li>
			<li><h5> Take a screenshot of the settings used for personal records to track exact specifications.</h5></li>
			<li><h5> Select <strong> Send</strong> button.</h5></li>
		</ol>

		<h3> 3.3 How to Issue a Group Command</h3>
		<h5> To send upgrade commands to groups of network devices in Command Center, perform the following steps:</h5>
		<ol>
			<li><h5> Navigate to the <strong> Network > Endpoints > Electric Group Commands</strong> page to send firmware to one or multiple virtual addressing groups. </h5></li>
			<li><h5> Select the <strong> Virtual Addressing Group</strong> or enter a comma separated value (CSV) list of meter numbers.</h5></li>
			<li><h5> Select the <strong> Endpoint Firmware Download</strong> command.</h5></li>
			<li><h5> Select the <strong> Module Firmware </strong> version from the drop-down list.</h5></li>
			<li><h5> Select the <strong> Send</strong> button. </h5></li>
		</ol>
		<h5> Do not attempt to send a Group Command to more than 25 endpoints per collector or 500 endpoints total.</h5>

		<h3> 3.4 How to Issue a Point to Point Command: RadioShop</h3>
		<h5> To perform point-to-point updates (one at a time) to a single network device in RadioShop perform the following steps:</h5>
		<ol>
			<li> <h5> Unless already completed, add intended Collector to <strong> Connections </strong> by clicking <strong> Add </strong>. A successfully started Collector will have its radios listed under <strong>NetworkID </strong> on the <strong> Nodes </strong> side of the screen. </h5></li>
			<img src="/upgradeplantool/images/img2.png">
			<li> <h5> Click on <strong> NetworkID </strong>. A radio icon will illuminate in the top left-hand corner. Click the radio icon. </h5></li>
			<img src="/upgradeplantool/images/img3.png">
			<li> <h5>A dialogue box will pop up. Enter the LAN Address of the intended device, and the <strong> Name </strong> and <strong> Radio Name </strong> boxes should automatically be populated. Paste the device’s WAN Address into the box labeled <strong> Encoded </strong> Value and press <strong> OK </strong>. The device will now be visible below <strong> NetworkID </strong>. </h3></li>
			<li> <h5> Click the dropdown arrow next to the illuminated key icon near the top of the screen. Select <strong> Discover Key </strong>. If the key is discovered, a <strong> Radio Configuration </strong> tab will open within one minute. If not, repeat this step. </h5></li>
			<li> <h5> Starting in the bar at the top of the screen, click <strong> Configure>Firmware>Download New Image </strong>.</h5></li>
			<li> <h5> Within one minute a NMP Configuration dialogue box will pop up. Confirm that the device is using the intended Collector in the first box. Set <strong> Download Rate </strong> to 1 second, <strong>Mood </strong> to Quick and <strong> Priority </strong> to 0. Click <strong> OK </strong>, and in the two following pop-ups, click no.</h5></li>
			<li> <h5> The download progress can be tracked using the <strong> Firmware Download </strong> tab. If the download is indicated to have failed, retry steps 5 and 6.</h5></li>
			<img src="/upgradeplantool/images/img4.png">
		</ol>

		<h2> Appendix </h2>
		<h3> i. Current Collector Count </h3>
		<div id= 'collectortable' style = "padding-left:5px">
			<div class = "spin"></div>
		</div>

		<h3> ii. Current Router Count </h3>
		<div id="routertable" style="padding-left:5px">
			<div class="spin">
			</div>
		</div> 

		<h3> iii. Current Endpoint Count </h3>
		<div id="endpointtable" style="padding-left:5px">
			<div class="spin">
			</div>
		</div>

		<h3> iv. Layer Analysis </h3>
		<div id="layeranalysistable" style="padding-left: 5px">
			<div class="spin">
			</div>
		</div>
	</div>


	<script type="text/javascript">
		
		/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		// These jQuery call are sent to the db_handler.php to get tables returned to this page from python scripts.
		/////////////////////////////////////////////////////////////////////////////////////////////////////////////////

		jQuery.ajax ({
			type: "POST",
			url: 'python_handler.php',
			data: {functionname:'callCount'},
			success: function(data){
				document.getElementById("insert_count").innerHTML = data;
			}
		});

		jQuery.ajax ({
			type: "POST",
			url: 'python_handler.php',
			data: {functionname:'callCollector'},
			success: function(data){
				document.getElementById("collectortable").innerHTML = data;
			}
		});

		jQuery.ajax ({
			type: "POST",
			url: 'python_handler.php',
			data: {functionname:'callRouter'},
			success: function(data){
				document.getElementById("routertable").innerHTML = data;
			}
		});

		jQuery.ajax ({
			type: "POST",
			url: 'python_handler.php',
			data: {functionname:'callEndpoint'},
			success: function(data){
				document.getElementById("endpointtable").innerHTML = data;
			}
		});

		jQuery.ajax ({
			type: "POST",
			url: 'python_handler.php',
			data: {functionname: 'callLayerAnalysis'},
			success: function(data){
				document.getElementById("layeranalysistable").innerHTML = data;
			}
		});

		function CopyToClipboard(containerid) {
			if (document.selection) {
				var range = document.body.createTextRange();
				range.moveToElementText(document.getElementById(containerid));
				range.select().createTextRange();
				document.execCommand("copy");
			} else if (window.getSelection) {
				var range = document.createRange();
				range.selectNode(document.getElementById(containerid));
				window.getSelection().addRange(range);
				document.execCommand("copy");
				alert("Text has been copied, now paste in the text-area")
			}
		}	

	</script>

</body>
</html>
