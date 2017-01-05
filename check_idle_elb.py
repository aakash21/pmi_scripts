#!/usr/bin/python
# Description: Script to check sum of request on load balancer in last seven days. If number of request less then 700, then load balancer is idle

import boto
from boto import ec2
from boto.ec2 import cloudwatch
import datetime
from datetime import timedelta
from boto.ec2.cloudwatch import CloudWatchConnection
from boto.ec2 import elb
import sys
import csv

connection=ec2.connect_to_region('us-east-1')

with open('idleELB.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Region', 'ELB Name', 'Reason','Status'])


regions = connection.get_all_regions()
for region in regions:
    print region.name
    lbconnection = boto.ec2.elb.connect_to_region(region.name)
    elbs = lbconnection.get_all_load_balancers()
    if not elbs:
        print "No ELB in:" + str(region.name)
    else:
        for elbi in elbs:
            monitor=boto.ec2.cloudwatch.connect_to_region(region.name)
            print monitor
            print 'Load Balancer Name:' + str(elbi.name)
            results = monitor.get_metric_statistics(
                300, # Granularity
                datetime.datetime.utcnow()-datetime.timedelta(seconds=10080), # Start
                datetime.datetime.utcnow(), # End
                'RequestCount', # Metric name
                'AWS/ELB', # Namespace
                'Sum', # Statistics
                dimensions={'LoadBalancerName':elbi.name} # Dimensions
                )

            if not results:
                #print "No Attributes Found"
                with open('idleELB.csv', 'a') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow([region.name,elbi.name,'Low Request Count','Idle'])
                continue#switch = results.pop()
            else:
                #print results
                switch = results.pop()
                print(switch['Sum'])

            if switch['Sum'] <= 700:
                with open('idleELB.csv', 'a') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow([region.name,elbi.name,'Low Request Count','Idle'])
            else:
                print "Load Balancer is in use" + str(elbi.name), switch['Sum']


    ec2conn = ec2.connect_to_region(region.name)
    elbconn = elb.connect_to_region(region.name)

    abc= 'True'

    load_balancer = elbconn.get_all_load_balancers()
    #print load_balancer
    for lb in load_balancer:
        health = lb.get_instance_health()
        instances = ec2conn.get_only_instances(instance_ids=[instance.id for instance in lb.instances])
        #print instances
        for i in health:
            if i.state == 'InService':
                abc = 'False'
            else:
                i.state == 'OutOfService'
                abc= 'True'
        if abc == 'False':
            print "Active"
        if abc == 'True':
            with open('idleELB.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow([region.name,lb.name,'No Active Backend Instances','Idle'])
