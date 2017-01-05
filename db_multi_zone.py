#!/usr/bin/python
######################################################################
## A DB instance is deployed in a Multi Availability Zone.         ##
##  ##
## ##
######################################################################
import boto
import boto.ec2
import boto.rds
import csv
import datetime
import dateutil
from datetime import timedelta
from boto.ec2 import cloudwatch
from boto.ec2.cloudwatch import CloudWatchConnection
cw = CloudWatchConnection()
print cw
connection = boto.ec2.connect_to_region("us-east-1")
regions = connection.get_all_regions()
with open('RDSmultiaz.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Region','Endpoint','Multi-Availability Zone'])
for region in regions:
	connection = boto.rds.connect_to_region(region.name)
	db = connection.get_all_dbinstances()
	for i in db:
		print check_multi_az
		with open('RDSmultiaz.csv', 'a') as csvfile:
        		writer = csv.writer(csvfile, delimiter=',')
           		writer.writerow([region.name,i.endpoint[0],i.multi_az])

