#!/usr/bin/python
import boto,csv
import boto.ec2
from boto.ec2.connection import EC2Connection
from boto import ec2


class unused_SGs:

    def unusedSG():
        with open('empty_security_group.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['GroupName', 'GroupId', 'Region Name', 'Usability'])
        conn = ec2.connect_to_region('us-east-1')
        regions = conn.get_all_regions()
        for region in regions:
            conn = ec2.connect_to_region(region.name)
            groups = conn.get_all_security_groups()
            for group in groups:
                if not group.instances():
                    for rule in group.rules:
                        with open('empty_security_group.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow([group.name, group.id,region.name,'Not in Use'])

    if __name__ == "__main__":
        unusedSG()
