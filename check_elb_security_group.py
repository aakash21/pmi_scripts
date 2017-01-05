import boto
from boto import ec2
from boto.ec2 import elb
import csv

sec_list= []
lb_list= []
extra_security_rules = []

with open('elb_security.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Load Balancer Name','Region Name','Ports'])

connection=ec2.connect_to_region('us-east-1')
regions = connection.get_all_regions()
for region in regions:
    lbconnection = boto.ec2.elb.connect_to_region(region.name)
    elbs = lbconnection.get_all_load_balancers()
    try:
        for elb in elbs:
            group_id = elb.security_groups[0]
            sec_rules = connection.get_all_security_groups(group_ids=group_id)[0].rules
            for i in sec_rules:
                sec_list.append(int(i.from_port))
            for i in elb.listeners:
                z = i.load_balancer_port
                lb_list.append(z)
            for i in sec_list:
                if i not in lb_list:
                    extra_security_rules.append(i)
            if extra_security_rules:
                with open('elb_security.csv', 'a') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow([elb.name,region.name,extra_security_rules])
                    writer.writerow(['These ports of security group associated with a load balancer are not defined in the load balancer listener configuration'])
    except:
        with open('elb_security.csv', 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Alert: A security group associated with a load balancer does not exist'])

