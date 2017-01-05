#!/usr/bin/python
import boto,csv
import boto.ec2
from boto.ec2.connection import EC2Connection
from boto import ec2

class largeNoOfRules_SG:

    def printSecurityRules():

        with open('largeNumber_vpc.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['GroupName', 'GroupId', 'No. of Rules','Usability', 'Region Name'])

        with open('largeNumber_classic.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['GroupName', 'GroupId', 'No. of Rules','Usability', 'Region Name'])


        conn = ec2.connect_to_region('us-east-1')
        regions = conn.get_all_regions()
        for region in regions:
            conn = ec2.connect_to_region(region.name)
            groups = conn.get_all_security_groups()
            for group in groups:
                if group.vpc_id:
                    length = len(group.rules)
                    if group.instances() and length >= 50:
                        with open('largeNumber_vpc.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow([group.name, group.id, length,'In Use', region.name])


                    if not group.instances() and length >= 50:
                        with open('largeNumber_vpc.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow([group.name, group.id, length,'Not in Use',region.name])

                if not group.vpc_id:
                    length = len(group.rules)
                    if group.instances() and length >= 100:
                        with open('largeNumber_classic.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow([group.name, group.id, length,'In Use',region.name])


                    if not group.instances() and length >= 100:
                        with open('largeNumber_classic.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow([group.name, group.id, length,'Not in Use',region.name])



    if __name__ == "__main__":
        printSecurityRules()

