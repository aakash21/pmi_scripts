#!/usr/bin/python

import boto
from boto import ec2
from boto.ec2 import elb
from boto.ec2.elb.attributes import ConnectionDrainingAttribute
import csv

with open('elb-connectiondraining.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Region','ELB Name', 'Cross Zone Load Balancing Status'])


connection=ec2.connect_to_region('us-east-1')
regions = connection.get_all_regions()

for region in regions:
    print region.name
    lbconnection = boto.ec2.elb.connect_to_region(region.name)
    elbs = lbconnection.get_all_load_balancers()
    for elbi in elbs:
        print 'Load Balancer Name:' + str(elbi.name)
        lbconn = lbconnection.get_all_lb_attributes(elbi.name)
        status = lbconn.connection_draining.enabled
        print 'Connection Draining:' + str(status)
        #print "\n************\n"
        if status == True:
            with open('elb-connectiondraining.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name, elbi.name,'Enabled'])
        #    print 'Connection Draining Enabled'
        else:
            with open('elb-connectiondraining.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name, elbi.name,'Disabled'])
            #print 'Connection Draining Disabled'



