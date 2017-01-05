#!/usr/bin/python
import boto
from boto import ec2
from boto.ec2 import elb
from boto.ec2.elb.attributes import ConnectionDrainingAttribute
import csv

with open('elb-crosszone-lb.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Region','ELB Name', 'Cross Zone Load Balancing Status'])


connection=ec2.connect_to_region('us-east-1')
regions = connection.get_all_regions()

for region in regions:
    print "\n************\n"
    lbconnection = boto.ec2.elb.connect_to_region(region.name)
    elbs = lbconnection.get_all_load_balancers()
    if elbs > 0:
        for elbi in elbs:
            print "Load Balancer Name:" + str(elbi.name)
            print "Cross Zone Load Balancing:" + str(elbi.is_cross_zone_load_balancing())
            status = elbi.is_cross_zone_load_balancing()
            if status == True:
                 with open('elb-crosszone-lb.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name, elbi.name,'Enabled'])
            else:
                with open('elb-crosszone-lb.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name, elbi.name,'Disabled'])

    else:
        print "Error message"



