#!/usr/bin/python
# Description: Script to check

import boto
from boto import ec2
from boto.ec2 import cloudwatch
import datetime
import dateutil
from datetime import timedelta
from boto.ec2.cloudwatch import CloudWatchConnection
import csv

cw = CloudWatchConnection()
print cw

connection = boto.ec2.connect_to_region('us-east-1')

ebsoptimized = ['c1.xlarge','c3.xlarge','c3.2xlarge','c3.4xlarge','c4.large','c4.xlarge','c4.2xlarge','c4.4xlarge','c4.8xlarge','d2.xlarge','d2.2xlarge','d2.4xlarge','d2.8xlarge','g2.2xlarge','i2.xlarge','i2.2xlarge','i2.4xlarge','m1.large','m1.xlarge','m2.2xlarge','m2.4xlarge','m3.xlarge','m3.2xlarge','m4.large','m4.xlarge','m4.2xlarge','m4.4xlarge','m4.10xlarge','r3.xlarge','r3.2xlarge','r3.4xlarge'
]

with open('overutilized_ebs.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Region','Instance ID','Instance Support EBS Optimized','Volume Id','Days Overutilized','Status','Volume Type'])

regions = connection.get_all_regions()
for region in regions:
    print "\n*************************************\n"
    print region.name
    connection = boto.ec2.connect_to_region(region.name)
    #reservations = connection.get_all_reservations(filters={"instance-state-name":"running"})
    reservations = connection.get_all_reservations()
#reservations = connection.get_all_reservations()

    for reservation in reservations:
        for instance in reservation.instances:
                    volumes = connection.get_all_volumes(filters={'attachment.instance-id': instance.id})
                    for volume in volumes:
                        ebsreadsum=0
                        ebswritesum=0
                        ebsreadcount = 0
                        ebswritecount = 0
                        if volume.type == 'standard':
                            print volume.id, volume.type
                            status = volume.status
                            volume_id =volume.id

                            daystomonitor = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
                            for day in daystomonitor:
                                ebsreadresults = cw.get_metric_statistics(
                                    3600, # Granularity
                                    datetime.datetime.utcnow()-datetime.timedelta(days=day), # Start
                                    datetime.datetime.utcnow()-datetime.timedelta(days=day-1), # End
                                    'VolumeReadOps', # Metric name
                                    'AWS/EBS', # Namespace
                                    'Average', # Statistics
                                    dimensions={'VolumeId': volume.id} # Dimensions
                                )

                                if not ebsreadresults:
                                    #print "No Attributes Found"
                                    continue
                                else:
                                    ebsread = ebsreadresults.pop()
                                    #print volume.id, "Day:", day, "Read Ops:", ebsread['Average']
                                    #ebsreadsum = ebsreadsum + ebsread['Average']
                                    if ebsread['Average'] > 95:
                                        ebsreadcount = ebsreadcount + 1
                                    #print ebsreadsum

                        # Check Write Ops
                            daystomonitor = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
                            for day in daystomonitor:
                                ebswriteresults = cw.get_metric_statistics(
                                    3600, # Granularity
                                    datetime.datetime.utcnow()-datetime.timedelta(days=day), # Start
                                    datetime.datetime.utcnow()-datetime.timedelta(days=day-1), # End
                                    'VolumeWriteOps', # Metric name
                                    'AWS/EBS', # Namespace
                                    'Average', # Statistics
                                    dimensions={'VolumeId':volume.id} # Dimensions
                                )

                                if not ebswriteresults:
                                            #print "No Attributes Found"
                                            continue
                                else:
                                    ebswrite = ebswriteresults.pop()
                                    #print volume.id, "Day:", day, "Write Ops:", ebswrite['Average']
                                    #ebswritesum = ebswritesum + ebswrite['Average']
                                    if ebswrite['Average'] > 95:
                                        ebswritecount = ebswritecount + 1
                                    #print ebswritesum

                            if ebsreadcount > 6 or ebswritecount > 6:
                                with open('overutilized_ebs.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name,instance.id,instance.ebs_optimized,volume.id,ebsreadcount,'Overutilized',volume.type])
                            else:
                                print "Normal"
                                with open('overutilized_ebs.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name,instance.id,instance.ebs_optimized,volume.id,ebsreadcount,'Green',volume.type])



