# Landis-Gyr-Automation-Tool-Project
**Please note that this is the redacted version of this project. NDA requires to remove confidential and sensitve information. This code has been uploaded as a showcase of my work in my internship with Landis+Gyr.**

1.1 About this Tool
The purpose of this tool is to help you create your firmware upgrade plan for your customer using this automated tool. The tool runs on WAMP stack server that uses JavaScript and Python to take user input to make guidelines and tables for an Upgrade Plan.
The tool allows a database connection to Oracle and MSSQL to handle larger customer data and offers a quicker execution time. Using a database connection allows you to filter for certain Firmware, if you do not want all firmware types into account. All queries used to fill a report can be found later in this documentation. 
The tool also allows Excel uploads (up to 1 GB) to handle reporting. For larger datasets, you can expect longer execution times due Read/Write and File IO times of Excel documents. For any errors in Oracle DB or MSSQL, excel uploads provides an alternative to creating reports.
# Landis-Gyr-Automation-Tool-Project
