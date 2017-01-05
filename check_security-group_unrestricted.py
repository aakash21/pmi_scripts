#!/usr/bin/python
import boto,csv
import boto.ec2
from boto.ec2.connection import EC2Connection
from boto import ec2



class securityLoopHoles:

    def printSecurityRules():
        with open('security_group.csv', 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(['GroupName', 'GroupId', 'VPCID', 'Protocol', 'Port', 'Instances', 'Permissions', 'Usability','Region Name'])

        conn = ec2.connect_to_region('us-east-1')
        regions = conn.get_all_regions()
        for region in regions:
            conn = ec2.connect_to_region(region.name)
            groups = conn.get_all_security_groups()

            for group in groups:
                for rule in group.rules:
                    for i in group.instances():
                        if i is not None and '0.0.0.0/0' in str(rule.grants):
                            with open('security_group.csv', 'a') as csvfile:
                                writer = csv.writer(csvfile, delimiter=',')
                                writer.writerow([group.name, group.id, group.vpc_id, rule.ip_protocol, rule.from_port, i, rule.grants, 'In use', region.name])


                    if not group.instances() and '0.0.0.0/0' in str(rule.grants):

                        with open('security_group.csv','a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow([group.name, group.id, group.vpc_id, rule.ip_protocol, rule.from_port,'instance not attached', rule.grants,'Not in use', region.name])

    if __name__ == "__main__":
        printSecurityRules()

