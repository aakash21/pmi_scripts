#!/usr/bin/python
# Script to check EC2 Balance between Availability Zones
# Author: Neeraj Gupta

import boto
from boto import ec2
from boto import vpc
import csv

connection=ec2.connect_to_region('ap-southeast-1')
with open('ec2-az-balance.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Region','Availability Zone', 'No. of Instances'])

regions = connection.get_all_regions()
for region in regions:
    ec2conn = ec2.connect_to_region(region.name)
    az = ec2conn.get_all_zones()
    for a in az:
        print a.name
        reservations = connection.get_all_reservations(filters={'availability_zone':a.name})
        with open('ec2-az-balance.csv', 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([region.name,a.name,len(reservations)])

