#!/usr/bin/python
#An Amazon EC2 instance that can be EBS-optimized has an attached Provisioned IOPS (SSD) volume but the instance is not EBS-optimized.

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

connection = boto.ec2.connect_to_region('ap-southeast-1')

ebsoptimized = ['c1.xlarge','c3.xlarge','c3.2xlarge','c3.4xlarge','c4.large','c4.xlarge','c4.2xlarge','c4.4xlarge','c4.8xlarge','d2.xlarge','d2.2xlarge','d2.4xlarge','d2.8xlarge','g2.2xlarge','i2.xlarge','i2.2xlarge','i2.4xlarge','m1.large','m1.xlarge','m2.2xlarge','m2.4xlarge','m3.xlarge','m3.2xlarge','m4.large','m4.xlarge','m4.2xlarge','m4.4xlarge','m4.10xlarge','r3.xlarge','r3.2xlarge','r3.4xlarge'
]


with open('Volumes_Attached_EBS_Optimized.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Instance Id', 'EBS Optimized Status', 'Storage Type', 'Region Name'])
regions = connection.get_all_regions()
for region in regions:
    connection = boto.ec2.connect_to_region(region.name)
    reservations = connection.get_all_reservations()
    for reservation in reservations:
        for instance in reservation.instances:
            ebsreadsum=0
            ebswritesum=0
            ebsreadcount = 0
            ebswritecount = 0
            if not instance.instance_type in ebsoptimized:
                continue#print "Support EBS Optimization: False", instance.id
            else:
                volumes = connection.get_all_volumes(filters={'attachment.instance-id': instance.id})
                for volume in volumes:
                    if volume.type == 'io1':
                        #print 'Instance Id', instance.id, 'EBS Optimized Status', instance.ebs_optimized, 'Storage Type', volume.type
                        with open('Volumes_Attached_EBS_Optimized.csv', 'a') as csvfile:
                                writer = csv.writer(csvfile, delimiter=',')
                                writer.writerow([instance.id, instance.ebs_optimized, volume.type, region.name])
                    else:
                        print "Other Volumes"




            #print "Support EBS Optimization: True", instance.id
            #print "EBS Optimization Status:", instance.ebs_optimized






