#!/usr/bin/python
# Script to check usage of EC2, VPC, ELB, RDS and EBS volumes
# Script requires hard coding limits

import math
import boto
from boto import ec2
from boto import vpc
from boto import iam
from boto import support
from boto import rds
from boto.ec2 import elb
import csv


#Constant#
accountId = 442793157362
defaultvpc=5
defaultigw=5
defaulteip=5
defaultvolumes=5000
defaultsnapshots=10000
defaultrdssg=25
defaultrdspg=50
defaultrdssnapshot=50
defaultec=20
defaultelb=20


with open('servicelimits.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Region','Service', 'Limit Name','Limit Amount','Current Usage','Status'])


connection=ec2.connect_to_region('us-east-1')

regions = connection.get_all_regions()

'''
autoscaling
ebs
vpc
eip
elb
rds'''

def getlimits(reg,category):
    for region in regions:
        if reg == region.name:
            print reg
            connection = ec2.connect_to_region(reg)
            attributes = connection.describe_account_attributes()
            limits = {}
            for attribute in attributes:
                limits[str(attribute.attribute_name)]= attribute.attribute_values
            return limits[category][0]
        else:
            print "None"

def check_vpc(str):
        conn = vpc.connect_to_region(str)
        noOfVPCs = conn.get_all_vpcs()
        noOfIGW = conn.get_all_internet_gateways()
        noOfEIP = conn.get_all_addresses()
        print "VPC", len(noOfVPCs)
        print "IGW", len(noOfIGW)
        print "EIP", len(noOfEIP)

        #### For VPCs###
        if len(noOfVPCs) >= defaultvpc*0.8:
            with open('servicelimits.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name, 'VPC','VPCs',defaultvpc,len(noOfVPCs),'Red'])
        else:
            with open('servicelimits.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name, 'VPC','VPCs',defaultvpc,len(noOfVPCs),'Green'])

        ### For IGW###
        if len(noOfIGW) >= defaultigw*0.8:
            with open('servicelimits.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name, 'VPC','IGW',defaultigw,len(noOfIGW),'Red'])
        else:
            with open('servicelimits.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name, 'VPC','IGW',defaultigw,len(noOfIGW),'Green'])

        ### For EIP###
        if len(noOfEIP) >= float(getlimits(str,'vpc-max-elastic-ips'))*0.8:
            with open('servicelimits.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name, 'VPC','EIP',getlimits(str,'vpc-max-elastic-ips'),len(noOfEIP),'Red'])
        else:
            with open('servicelimits.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name, 'VPC','EIP',getlimits(str,'vpc-max-elastic-ips'),len(noOfEIP),'Green'])


def check_ebs_volumes(str):

        conn = ec2.connect_to_region(str)
        #noOfEBSSnapshots = conn.get_all_snapshots(owner=accountId)
        noOfEBSVolumes = conn.get_all_volumes()
        print "EBS in use", len(noOfEBSVolumes)
        #print "EBS Snapshot in use", len(noOfEBSSnapshots)
        ### For EBS###
        if len(noOfEBSVolumes) >= defaultvolumes*0.8:
            with open('servicelimits.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name, 'EBS','Active Volumes',defaultvolumes,len(noOfEBSVolumes),'Red'])
        else:
            with open('servicelimits.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name, 'EBS','Active Volumes',defaultvolumes,len(noOfEBSVolumes),'Green'])


def check_rds(str):
        defaultvpc=5
        conn = rds.connect_to_region(str)
        RDSsg = conn.get_all_dbsecurity_groups()
        snaps = conn.get_all_dbsnapshots()
        manualsnaps = []
        for snap in snaps:
            if snap.snapshot_type == 'manual':
                manualsnaps.append(snap.id)
        RDSparameter = conn.get_all_dbparameter_groups()
        #defaultRDSsg = conn.get
        print "RDS SG", len(RDSsg)
        print "RDS Snapshot", len(manualsnaps)
        print "RDS Parameter", len(RDSparameter)
        ### For RDS SG###
        if len(RDSsg) >= defaultrdssg*0.8:
            with open('servicelimits.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name, 'RDS','Security Groups',defaultrdssg,len(RDSsg),'Red'])
        else:
            with open('servicelimits.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name, 'RDS','Security Groups',defaultrdssg,len(RDSsg),'Green'])

        ### For RDS Snapshot###
        if len(manualsnaps) >= defaultrdssnapshot*0.8:
            with open('servicelimits.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name, 'RDS','Snapshot',defaultrdssnapshot,len(manualsnaps),'Red'])
        else:
            with open('servicelimits.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name, 'RDS','Snapshot',defaultrdssnapshot,len(manualsnaps),'Green'])

        ### For RDS Parameter Group###
        if len(RDSparameter) >= defaultrdspg*0.8:
            with open('servicelimits.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name, 'RDS','Parameter Group',defaultrdspg,len(RDSparameter),'Red'])
        else:
            with open('servicelimits.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name, 'RDS','Parameter Group',defaultrdspg,len(RDSparameter),'Green'])




def check_ec2(str):
    conn = ec2.connect_to_region(str)
    noOfEC2 = conn.get_all_instances()
    print "Instances:", len(noOfEC2)

    ### For EC2###
    if len(noOfEC2) >= float(getlimits(str,'max-instances'))*0.8:
            with open('servicelimits.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name,'EC2','Instances', getlimits(str,'max-instances'),len(noOfEC2),'Red'])
    else:
            with open('servicelimits.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name,'EC2','Instances',getlimits(str,'max-instances'),len(noOfEC2),'Green'])

def check_elb(str):
    conn = elb.connect_to_region(str)
    noOfELB = conn.get_all_load_balancers()
    print "ELB:", len(noOfELB)

     ### For ELB###
    if len(noOfELB) >= defaultelb*0.8:
            with open('servicelimits.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name,'ELB','Active Load Balancers',defaultelb,len(noOfELB),'Red'])
    else:
            with open('servicelimits.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name,'ELB','Active Load Balancers',defaultelb,len(noOfELB),'Green'])

for region in regions:
    print region.name
    check_vpc(region.name)
    check_ebs_volumes(region.name)
    #check_ebs_snapshots(region.name)
    check_rds(region.name)
    check_ec2(region.name)
    check_elb(region.name)
