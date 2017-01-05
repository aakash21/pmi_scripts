import boto
from boto import ec2
import csv

connection =  ec2.connect_to_region('us-east-1')


with open('ec2classic_instances.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Region','Instance Name', 'Instance ID', 'Instance Type'])

regions = connection.get_all_regions()
for region in regions:
    conn = ec2.connect_to_region(region.name)
    reservations = conn.get_all_reservations()
    for reservation in reservations:
        for instances in reservation.instances:
            if instances.vpc_id == None:
                print "EC2 Classic Instanec", instances.id
        #        print "%s \t \t %s \t \t %s" % (instances.tags['Name'], instances.ip_address, instances.vpc_id)
                with open('ec2classic_instances.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name, instances.tags['Name'], instances.id, instances.instance_type])
            else:
                     print "Nothing Found"

            #print dir(instances)
