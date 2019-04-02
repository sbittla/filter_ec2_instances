# Fetch EC2 instances delta
This  program is useful if you want to fetch difference between running EC2 instances and a filter criteria 

For the current program it will create a csv file for each region and diplays the data in uw-west-2.csv, u-east-1.csv, eu-central1.csv. And each csv file will have the columns:

*** Instance Name, KeyName, Instance id, ImageId, InstanceType, LaunchTime ***

## Prerequisites To run this program from localhost
Install python3<br/>
Install pip3<br/>
Install the python3 packages boto3, requests, json and re.<br/>
Before running this command, you should be authenticated as a AWS user on the command prompt<br/>

## Run the command
'''
python3 list_ec2_instances_by_age.py

'''