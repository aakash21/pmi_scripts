__author__ = 'niraj'

import sys
import boto
from boto import ec2
connection=ec2.connect_to_region("us-east-1")



sgs=connection.get_all_instances()
for i in sgs:
    for z in i.instances:
        print dir(z.get_attribute)




#reservations = connection.get_all_instances()
#for reservation in reservations:
#    for instances in reservation.instances:
#        print instances.tags['Name']
#    print dir(instances)


