    #!/usr/bin/python
# Script to check detailed monitoring status on EC2 instances
import boto
import boto.ec2
from boto.ec2 import cloudwatch
from boto import ec2
import csv

with open('cloudwatch-custom.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Region','Namespace', 'Dimensions','Metric Name','Usage'])


connection = ec2.connect_to_region('us-east-1')

regions = connection.get_all_regions()

for region in regions:
    cw = cloudwatch.connect_to_region(region.name)
    #print cw.list_metrics()
    a = cw.list_metrics()

    for i in a:
        if i.namespace == 'System/Linux':
            with open('cloudwatch-custom.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow([region.name,i.namespace,i.dimensions['InstanceId'][0],'','Memory Utilization'])
                print i.namespace,i.dimensions['InstanceId']
                try:
                    if i.dimensions['Filesystem'] == 0:
                        print "Hello"
                        #with open('cloudwatch-custom.csv', 'a') as csvfile:
                        #    writer = csv.writer(csvfile, delimiter=',')
                        #    writer.writerow([region.name,i.namespace,i.dimensions['InstanceId'][0],'','Memory Utilization'])
                         #   print i.namespace,i.dimensions['InstanceId']
                    else:
                        with open('cloudwatch-custom.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow([region.name,i.namespace,i.dimensions['InstanceId'][0],i.dimensions['Filesystem'][0],'Disk Utilization'])
                        #print i.namespace,i.dimensions['Filesystem'][0]
                except:
                    print "Error"