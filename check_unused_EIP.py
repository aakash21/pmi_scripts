#!/usr/bin/python

#This script will output all unused Elastic IP in every regions

import boto
import sys
from boto import ec2
import csv

with open('unused-eip.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Region','EIP'])

region=ec2.regions()

for reg in region:

    try:
        connection=ec2.connect_to_region(reg.name)

        if reg.name == "us-gov-west-1" or reg.name == "cn-north-1":
            #print "API call is not allowed in this regions:",".",reg.name
            continue

        elasticIpAddress=connection.get_all_addresses();

        for eIP in elasticIpAddress:
            if eIP.instance_id:
                print 'None'
            else:
                #print "Unused Elastic IP address is found"
                #print  eIP ,",", reg.name
                with open('unused-eip.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name, eIP])
    except:


        print sys.exc_info()


