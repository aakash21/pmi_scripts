#!/usr/bin/python

import boto,csv
import boto.rds
from boto import ec2

with open('rds_security_group.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Region','RDSName','Security Group','Port','Global Access'])

conn = boto.ec2.connect_to_region('us-east-1')
regions = conn.get_all_regions()
for region in regions:
    conn = ec2.connect_to_region(region.name)
    connection = boto.rds.connect_to_region(region.name)
    db = connection.get_all_dbinstances()


    for i in db:
        groups = i.vpc_security_groups
        for group in groups:
            sec_rules = conn.get_all_security_groups(group_ids=group.vpc_group)[0].rules
            for rule in sec_rules:
                if '0.0.0.0/0' in str(rule.grants):
                    with open('rds_security_group.csv', 'a') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',')
                        writer.writerow([region.name,i.id,group.vpc_group,rule.from_port,rule.grants])