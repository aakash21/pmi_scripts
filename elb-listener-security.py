import boto
from boto import ec2
from boto.ec2 import elb
import csv


with open('elb_security.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Listeners that do not use secure protocols(HTTPS/SSL)'])
    writer.writerow(['Load Balancer Name','Region Name','Protocol','Ports'])

conn = boto.ec2.connect_to_region('us-east-1')
regions = conn.get_all_regions()
for region in regions:
    conn = ec2.connect_to_region(region.name)
    lbconnection = boto.ec2.elb.connect_to_region(region.name)
    elbs = lbconnection.get_all_load_balancers()

    for elb in elbs:
            try:

                group_id = elb.security_groups[0]
                sec_rules = conn.get_all_security_groups(group_ids=group_id)[0].rules
                for rule in sec_rules:
                    if rule.ip_protocol not in ('https','ssl','HTTPS','SSL'):
                        with open('elb_security.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow([elb,region.name,rule.ip_protocol,rule.from_port])

            except:
                with open('elb_security.csv', 'a') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow(['Alert: A security group associated with a load balancer does not exist'])
                    writer.writerow([elb,region.name])