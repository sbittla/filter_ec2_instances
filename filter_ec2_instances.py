import boto3
import requests
import json
import re

#######################################################################################################
###                             METHODS SECTION                                                     ###
#######################################################################################################

#----------------------------------------------------------------------------------------------------#
# GET THE EC2 INSTANCES FROM A REGIONS WITH THE FILTERS						     #
#----------------------------------------------------------------------------------------------------#
def get_ec2_instances(region_name, filters):
  ec2client = boto3.client('ec2', region_name=region_name)
  response = ec2client.describe_instances(Filters=filters)
  instances=[]
  for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
      #If the Pltaform is windows the key will be present. Otherwise, platform key will not be present
      #Right now the windows agents, in jenkins are not appended with the instance id. Once this is fixed, remove the if condition
      #if ("Platform" not in instance.keys()):
      instances.append(instance["InstanceId"])
      # This will print will output the value of the Dictionary key 'InstanceId'
      #print(instance["InstanceId"],instance["InstanceType"], instance["LaunchTime"], instance["State"])
  #print (instances)
  return response, instances



#----------------------------------------------------------------------------------------------------#
# THE DELTA BETWEEN ACTIVE JENKINS LABELS VS EC2 INSTANCES   #
#----------------------------------------------------------------------------------------------------#
def check_for_non_jenkins_instances(ec2_instances, jenkins_nodes, aws_region):
  if (((set(ec2_instances)==set(jenkins_nodes)) and (len(ec2_instances)==len(jenkins_nodes)))):
    print('No non jenkins instances in ', aws_region)
    return
  else:
    #print ("jenkins", aws_region, sorted(set(jenkins_nodes)))
    #print ("ec2", aws_region, sorted(set(ec2_instances)))	
    non_jenkins_set = set(ec2_instances).difference(set(jenkins_nodes)) 
    if (non_jenkins_set):
      print ('Non jenkins instances found for ', aws_region)
      return non_jenkins_set
    else:
      un_non_jenkins_set = set(jenkins_nodes).difference(set(ec2_instances))
      print(aws_region, "uncleaned instances are: ", un_non_jenkins_set)
      return
    return

def print_non_jenkins_ec2_instances(ec2_response, non_jenkins_instances, aws_region):
    # Open file  
    fh = open(aws_region+".csv", "w")  

    fh.write("The instances for the region: " +  aws_region + "\n")
    fh.write("KeyName, Instance id, ImageId, InstanceType, LaunchTime \n")
    for reservation in ec2_response["Reservations"]:
        for instance in reservation["Instances"]:
            if(instance["InstanceId"] in non_jenkins_instances):
                try:
                    #print(instance["KeyName"], ", ", instance["InstanceId"], ", ",  instance["ImageId"], ", ", instance["InstanceType"], ", ", instance["LaunchTime"])
                    fh.write(instance["KeyName"]+ ", " + instance["InstanceId"] + ", " +  instance["ImageId"] + ", " +instance["InstanceType"]+ ", "+ instance["LaunchTime"].strftime('%m/%d/%Y') + "\n")
        
              
                except Exception as e:
                    #print("No Key", ", ", instance["InstanceId"], ", ",  instance["ImageId"], ", ", instance["InstanceType"], ", ", instance["LaunchTime"])
                    fh.write("No Key" + ", " + instance["InstanceId"] + ", " +  instance["ImageId"] + ", " +instance["InstanceType"]+ ", "+ instance["LaunchTime"].strftime('%m/%d/%Y')+ "\n")
                    #instance["Status"], instance["OwnerId"]
    fh.close()

#######################################################################################################
### 				VARIABLES SECTION						    ###
#######################################################################################################

j1_filters=[
           {'Name': 'instance-state-name', 'Values': ['running']},
           {'Name': 'tag:Name', 'Values': ['j1*','j2*','j3*']},
           {'Name': 'tag:server', 'Values': ['jenkins1','jenkins2','jenkins3']}
	]

ec2_filters=[
           {'Name': 'instance-state-name', 'Values': ['running']}
    ]


#######################################################################################################
###                             MAIN SECTION	                                                       ###
###         Get  the delta of ec2 running instances from a given criteria                           ###
#######################################################################################################



try:

  # Region us-west-2  Oregon
  j1_response, jenkins_instances = get_ec2_instances( 'us-west-2', j1_filters)
  us_west2_ec2_response, us_west2_ec2_instances = get_ec2_instances( 'us-west-2', ec2_filters)

  non_jenkins_instances = check_for_non_jenkins_instances(us_west2_ec2_instances, jenkins_instances, 'us-west-2')
  print_non_jenkins_ec2_instances(us_west2_ec2_response, non_jenkins_instances, 'us-west-2')
  
# Region us-east-1 - N. Virgenis
  j2_response, jenkins_instances = get_ec2_instances( 'us-east-1', j1_filters)
  us_east1_ec2_response, us_east1_ec2_instances = get_ec2_instances( 'us-east-1', ec2_filters)

  non_jenkins_instances = check_for_non_jenkins_instances(us_east1_ec2_instances, jenkins_instances, 'us-east-1')
  print_non_jenkins_ec2_instances(us_east1_ec2_response, non_jenkins_instances, 'us-east-1')

# Region eu-central-1 Frankfurt
  j2_response, jenkins_instances = get_ec2_instances( 'eu-central-1', j1_filters)
  eu_central1_ec2_response, eu_central1_ec2_instances = get_ec2_instances( 'eu-central-1', ec2_filters)

  non_jenkins_instances = check_for_non_jenkins_instances(eu_central1_ec2_instances, jenkins_instances, 'eu-central-1')
  print_non_jenkins_ec2_instances(eu_central1_ec2_response, non_jenkins_instances, 'eu-central-1')
except Exception as e:
  print(e)
  raise e
