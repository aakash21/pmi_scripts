#!/usr/bin/python
#Description: Examines the health check configuration for Auto Scaling groups. If Elastic Load Balancing is being used for an Auto Scaling group, the recommended configuration is to enable an Elastic Load Balancing health check. If an Elastic Load Balancing health check is not used, Auto Scaling can only act upon the health of the Amazon Elastic Compute Cloud (Amazon EC2) instance and not on the application that is running on the instance.
#Alert Criteria
#Yellow: An Auto Scaling group has an associated load balancer, but the Elastic Load Balancing health check is not enabled.
#Yellow: An Auto Scaling group does not have an associated load balancer, but the Elastic Load Balancing health check is enabled.

import boto
from boto import ec2
from boto.ec2 import autoscale
from boto.ec2 import elb
import csv

connection =  ec2.connect_to_region('ap-southeast-1')


with open('asg_healthcheck.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter='')
            writer.writerow(['Region','Auto Scaling Group Name','Load Balancer Associated','Health Check','Status'])

regions = connection.get_all_regions()
for region in regions:
    conn = autoscale.connect_to_region(region.name)
    asg = conn.get_all_groups()
    #print asg
    for a in asg:
        #print dir(a)
        if not a.autoscaling_group_arn == 0:
            if len(a.load_balancers) == 0:
                #print "ELB Deleted"
                if a.health_check_type == 'EC2':
                    with open('asg_healthcheck.csv', 'a') as csvfile:
                        writer = csv.writer(csvfile, delimiter='')
                        writer.writerow([region.name,a.name, 'No', a.health_check_type, 'Green'])
            else:
                #print 'Found'
                if  a.health_check_type == 'ELB':
                   with open('asg_healthcheck.csv', 'a') as csvfile:
                        writer = csv.writer(csvfile, delimiter='')
                        writer.writerow([region.name,a.name, 'Yes', a.health_check_type, 'Green'])
                else:
                    #print "ELB health check missing"
                    #print a.health_check_type
                    with open('asg_healthcheck.csv', 'a') as csvfile:
                       writer = csv.writer(csvfile, delimiter='')
                       writer.writerow([region.name,a.name, 'Yes', a.health_check_type, 'Yellow'])
