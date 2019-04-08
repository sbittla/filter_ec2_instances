import boto3
#import requests
#import json
#import re

#######################################################################################################
###                             METHODS SECTION                                                     ###
#######################################################################################################
#----------------------------------------------------------------------------------------------------#
# GET THE ELBs  FROM A REGIONS WITH THE FILTERS                             #
#----------------------------------------------------------------------------------------------------#
def get_elb_instances(region_name):
  fh = open(region_name+"_elb.csv", "w")
  rdsclient = boto3.client('elb', region_name=region_name)
  response = rdsclient.describe_load_balancers()
  #print("LoadBalancerName,DNSName,CreatedTime")
  fh.write("LoadBalancerName,DNSName,CreatedTime\n")
  for instance in response["LoadBalancerDescriptions"]:    
    try:
        #print(instance["LoadBalancerName"],instance["DNSName"],instance["CreatedTime"].strftime('%m/%d/%Y'))
        fh.write(instance["LoadBalancerName"]+ "," +instance["DNSName"]+ "," +instance["CreatedTime"].strftime('%m/%d/%Y')+ "\n")
    except Exception as e:
        print (e)
        raise (e)
  fh.close()

#----------------------------------------------------------------------------------------------------#
# GET THE RDS  FROM A REGIONS WITH THE FILTERS						     #
#----------------------------------------------------------------------------------------------------#
def get_rds_instances(region_name):
  fh = open(region_name+"_rds.csv", "w")
  rdsclient = boto3.client('rds', region_name=region_name)
  response = rdsclient.describe_db_instances()#Filters=filters)
  fh.write("DBInstanceIdentifier,DBInstanceClass,Engine,MasterUsername,InstanceCreateTime,MasterUsername,DBInstanceStatus, AllocatedStorage in GB, BackupRetentionPeriod, StorageType \n")
  for instance in response["DBInstances"]:
    #print(instance["DBInstanceIdentifier"],instance["DBInstanceClass"],instance["Engine"],instance["MasterUsername"],instance["InstanceCreateTime"], instance["MasterUsername"], instance["DBInstanceStatus"], instance["AllocatedStorage"], instance["BackupRetentionPeriod"],instance["StorageType"])
    try:
        fh.write(instance["DBInstanceIdentifier"]+ "," +instance["DBInstanceClass"]+ "," +instance["Engine"]+ "," +instance["MasterUsername"]+ "," +instance["InstanceCreateTime"].strftime('%m/%d/%Y') + "," + instance["MasterUsername"]+ "," + instance["DBInstanceStatus"]+ "," + str(instance["AllocatedStorage"])+ "," + str(instance["BackupRetentionPeriod"])+ "," +instance["StorageType"] + "\n")
    except Exception as e:
        print (e)
        raise (e)
  fh.close()

#----------------------------------------------------------------------------------------------------#
# GET THE  AMAZON MACHINE IMAGES FROM A REGIONS WITH THE FILTERS                             #
#----------------------------------------------------------------------------------------------------#
def get_ami_instances(region_name):
  fh = open(region_name+"_amis.csv", "w")
  amiclient = boto3.client('ec2', region_name=region_name)
  response = amiclient.describe_images()#Filters=filters)
  fh.write("Name,OwnerId,ImageId, ImageType, CreationDate, RootDeviceType, VirtualizationType \n")
  #print("Name,OwnerId,ImageId, ImageType, CreationDate, RootDeviceType, VirtualizationType \n")
  for instance in response["Images"]:
    #print(instance["OwnerId"],instance["ImageId"],instance["ImageType"],instance["CreationDate"], instance["RootDeviceType"], instance["VirtualizationType"])
    tag_name= False
    tag_val = "No Name"
    try:
        #print(instance["KeyName"], ", ", instance["InstanceId"], ", ",  instance["ImageId"], ", ", instance["InstanceType"], ", ", instance["LaunchTime"])
        iKeys = instance.keys()
        #print(iKeys)
      
        if ("Tags" in iKeys):
            #print("Instance tags are: ", instance["Tags"])
            tags = instance["Tags"]
            for tag in tags:
                for key, val in tag.items():
                    #print(key, "=>", val)
                    tag_val = val
                    if (tag_val=='Name'):
                        tag_name = True
                        
                        
                if (tag_name==True):
                    #print("The host name is: ", tag_val)   
                    break

        if (tag_name):
            fh.write(tag_val + ", " + instance["OwnerId"] + ", " +  instance["ImageId"] + ", " +instance["ImageType"]+ ", "+ instance["CreationDate"] + ", " +instance["RootDeviceType"]+", " +instance["VirtualizationType"]+"\n")
        else:
            fh.write("No Name" + ", " + instance["OwnerId"] + ", " +  instance["ImageId"] + ", " +instance["ImageType"]+ ", "+ instance["CreationDate"] + ", " +instance["RootDeviceType"]+", " +instance["VirtualizationType"]+"\n")
                
    except Exception as e:
        print (e)
        raise (e)
  fh.close()
#######################################################################################################
###                             MAIN SECTION	                                                       ###
###         Get  the delta of rds running instances from a given criteria                           ###
#######################################################################################################



try:

  # Region us-west-2  Oregon
  get_rds_instances( 'us-west-2')
  get_ami_instances( 'us-west-2')
  get_elb_instances( 'us-west-2')
  
# Region us-east-1 - N. Virgenis
  get_rds_instances( 'us-east-1')
  get_ami_instances( 'us-east-1')
  get_elb_instances( 'us-east-1')
  
# Region eu-central-1 Frankfurt
  get_rds_instances( 'eu-central-1')
  get_ami_instances( 'eu-central-1')
  get_elb_instances( 'eu-central-1')
except Exception as e:
  print(e)
  raise e
