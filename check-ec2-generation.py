#!/usr/bin/python

# Script to check EC2 instance generations


import boto
from boto import ec2
from boto import vpc
import csv

connection = ec2.connect_to_region('us-east-1')

instanceTypes = {'m1.medium','m1.small','m1.large','m1.xlarge','c1.medium','c1.xlarge','t1.micro','m2.xlarge','m2.2xlarge','m2.4xlarge','cr1.8xlarge'}
new = {'m1.medium':'m3.medium','m1.small':'t2.small','m1.large':'m3.large','m1.xlarge':'m3.xlarge','c1.medium':'c3.medium','c1.xlarge':'c3.xlarge','t1.micro':'t2.micro'}

with open('ec2generations.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Region','Instance Name','Instance Id','Current Instance Type','Suggested Instance Type'])


regions = connection.get_all_regions()

for region in regions:
    print region.name

    ec2conn = ec2.connect_to_region(region.name)
    reservations = ec2conn.get_all_reservations()
    for reservation in reservations:
        for instance in reservation.instances:
            if instance.instance_type in instanceTypes:
                with open('ec2generations.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name,instance.tags['Name'],instance.id,instance.instance_type,new[instance.instance_type]])
                print instance.instance_type
                print new[instance.instance_type]
            else:
                #print "upgrade instance", instance.instance_type
                print "dog"
            #print dir(instance)

