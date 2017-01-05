#!/usr/bin/python
######################################################################
## An active DB instance has not had a connection in the last 7 days##
######################################################################
import boto
import boto.ec2
import boto.rds
from boto import ec2
import datetime
import csv
import dateutil
from datetime import timedelta
from boto.ec2 import cloudwatch
from boto.ec2.cloudwatch import CloudWatchConnection

connection = ec2.connect_to_region("us-west-2")
regions = connection.get_all_regions()
with open('publicRDS.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Region','Endpoint','Publicly Accessability'])
for region in regions:
    connection = boto.rds.connect_to_region(region.name)#
    db = connection.get_all_dbinstances()
    for i in db:
            with open('publicRDS.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow([region.name,i.endpoint[0],i.PubliclyAccessible])
