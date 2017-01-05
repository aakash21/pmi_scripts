#!/usr/bin/python
# Script to check detailed monitoring status on EC2 instances
import boto
import boto.ec2
from boto import ec2
import csv

connection = ec2.connect_to_region('ap-southeast-1')

with open('cw-detailed-monitoring.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Region','Instance ID','Instance Name','CW Detailed Monitoring'])

regions = connection.get_all_regions()

for region in regions:
    reservations = connection.get_all_reservations()
    for reservation in reservations:
        for instance in reservation.instances:
            with open('cw-detailed-monitoring', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow([region.name,instance.id,instance.tags['Name'],instance.monitoring_state])
