# Script to check EC2 Classic Instances running in all the regions
#__author__ = 'niraj'

#!/usr/bin/pythom
import boto
from boto import ec2
import csv


connection =  ec2.connect_to_region('eu-west-1')

regions = connection.get_all_regions()
for region in regions:

    try:
            print "\n*************************************\n"
            print region.name
            conn =  ec2.connect_to_region(region.name)
            reservations2 = conn.get_all_classic_link_instances()

            for reservation in reservations2:
                for instances in reservation.instances:
                    print "%s , , %s" % (instances.tags['Name'], instances.ip_address)

    except:
        print "Not Found"

