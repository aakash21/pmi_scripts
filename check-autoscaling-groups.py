#!/usr/bin/python
#Description: Checks the availability of resources associated with launch configurations and your Auto Scaling groups. Auto Scaling groups that point to unavailable resources cannot launch new Amazon Elastic Compute Cloud (Amazon EC2) instances. When properly configured, Auto Scaling causes the number of Amazon EC2 instances to increase seamlessly during demand spikes and decrease automatically during demand lulls. Auto Scaling groups and launch configurations that point to unavailable resources do not operate as intended.
#Alert Criteria
#Red: An Auto Scaling group is associated with a deleted load balancer.
#Red: A launch configuration is associated with a deleted Amazon Machine Image (AMI).

import boto
from boto import ec2
from boto.ec2 import autoscale
import csv

connection =  ec2.connect_to_region('ap-southeast-1')


with open('asg_AutoScaling_loadBalancer.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Region','Auto Scaling Group Name','Launch Configuration Name','Load Balancer Name','Status','Reason'])

with open('asg_launcConfiguration_ami.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Region','Auto Scaling Group Name','Launch Configuration Name','Resource Type','Resource Name','Status','Reason'])


regions = connection.get_all_regions()
for region in regions:
    conn = autoscale.connect_to_region(region.name)
    asg = conn.get_all_groups()
    print asg
    for a in asg:
        if not a.autoscaling_group_arn == 0:
            if len(a.load_balancers) == 0:
                print "ELB Deleted"
                with open('asg_AutoScaling_loadBalancer.csv', 'a') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow([region.name,a.name, a.launch_config_name, a.load_balancers, 'Red', 'ELB Deleted'])
            else:
                print 'Not found'
                    #   print a.name, a.launch_config_name
        #print dir(a)
    lc = conn.get_all_launch_configurations()
    ec2conn = ec2.connect_to_region(region.name)


    for l in lc:
        if not l.image_id == 0:
            ami=ec2conn.get_image(l.image_id)

            if ami == None:
                 with open('asg_launcConfiguration_ami.csv', 'a') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow([region.name,a.name, a.launch_config_name,'AMI',l.image_id, 'RED','AMI Not Found'])
            else:
                print 'not found'

