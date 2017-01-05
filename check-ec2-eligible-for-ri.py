#!/usr/bin/python

import boto
from boto import ec2
import datetime
import time,datetime
from datetime import datetime
import dateutil
import csv

connection = ec2.connect_to_region('us-east-1')

with open('RIeligible_ec2.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Region','Instance ID', 'Instance Name','Instance Type', 'Instance Age','Platform'])

regions = connection.get_all_regions()

for region in regions:
    conn = ec2.connect_to_region(region.name)
    reservations = conn.get_all_reservations()
    for reservation in reservations:
        for instance in reservation.instances:
            #print instance.platform
            z = instance.launch_time
            a = datetime.strptime(z, '%Y-%m-%dT%H:%M:%S.%fZ')
            b = datetime.now()
            p = (b - a).days
            if instance.state == 'running' and p > 60:
                with open('RIeligible_ec2.csv', 'a') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',')
                        writer.writerow([region.name, instance.id, instance.tags['Name'], instance.type, p, instance.platform])
            else:
                print 'Instance in Stop State'


