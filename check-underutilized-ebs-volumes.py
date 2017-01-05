#!/usr/bin/python
# Description: Script to check underutilized EBS volumes

import boto
from boto import ec2
from boto.ec2 import cloudwatch
import datetime
import dateutil
from datetime import timedelta
from boto.ec2.cloudwatch import CloudWatchConnection
import csv

cw = cloudwatch.connect_to_region('ap-southeast-1')

with open('underutilized_ebs.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Region','Volume ID','Size','Volume Status', 'Status', 'Volume Type','Count'])

connection=ec2.connect_to_region('ap-southeast-1')
regions = connection.get_all_regions()

for region in regions:
    connection = boto.ec2.connect_to_region(region.name)
    cw = cloudwatch.connect_to_region(region.name)
    volumes = connection.get_all_volumes()

    for volume in volumes:
        count = 0
        daystomonitor = [1,2,3,4,5,6,7]
        for day in daystomonitor:

            ebsreadresults = cw.get_metric_statistics(
                300, # Granularity
                datetime.datetime.utcnow()-datetime.timedelta(days=day), # Start
                datetime.datetime.utcnow()-datetime.timedelta(days=day-1), # End
                'VolumeIdleTime', # Metric name
                'AWS/EBS', # Namespace
                'Average', # Statistics
                dimensions={'VolumeId': volume.id} # Dimensions
            )

            if not ebsreadresults:
                count = count + 1
            else:
                print 'hell'
        if count == 7:
                with open('underutilized_ebs.csv', 'a') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow([region.name,volume.id,volume.size,volume.status, 'Underutilized', volume.type,count])
        else:
               print "Hello"
