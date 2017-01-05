#An instance had more than 90% daily average CPU utilization on at least 4 of the previous 14 days.
#!/usr/bin/python
#An instance had more than 90% daily average CPU utilization on at least 4 of the previous 14 days.

import boto
from boto import ec2
from boto.ec2 import cloudwatch
import datetime
import dateutil
from datetime import timedelta
from boto.ec2.cloudwatch import CloudWatchConnection
import csv

# Constants
daystomonitor = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]


cw = CloudWatchConnection()
print cw

with open('high_utilization_ec2.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Region/AZ','Instance ID','Instance Name','Instance Type','Number of days High Utilized','Status','Criteria'])



connection = boto.ec2.connect_to_region('us-east-1')

regions = connection.get_all_regions()

for region in regions:
    ec2conn = boto.ec2.connect_to_region(region.name)
    print region.name
    #reservations = ec2conn.get_all_reservations(filters={"instance-state-name":"stopped"})
    reservations = ec2conn.get_all_reservations()
    cw = boto.ec2.cloudwatch.connect_to_region(region.name)
    print cw
    count=0
    for reservation in reservations:
        for instance in reservation.instances:
            print instance.id
            print dir(instance)
            cpusum=0

            for day in daystomonitor:
                ec2results = cw.get_metric_statistics(
                    3600, # Granularity

                    datetime.datetime.utcnow()-datetime.timedelta(days=day), # Start
                    datetime.datetime.utcnow()-datetime.timedelta(days=day-1), # End
                    'CPUUtilization', # Metric name
                    'AWS/EC2', # Namespace
                    'Average', # Statistics
                    dimensions={'InstanceId':instance.id} # Dimensions
                )
                if not ec2results:
                    #print "No Data Found"
                    continue
                else:
                    ec = ec2results.pop()
                    cpusum = cpusum + ec['Average']
                    if ec['Average'] >= 90:
                        count = count + 1
                    else:
                        print "Normal"
                    #print ec['Average']
                    #print "Day:", day, "CPU Sum:", cpusum
                    #print "\n******************\n"

            if (count >= 4):
                #print "Instance Overutilized"
                #print "CPU Sum:", (cpusum/7)
                #print "Count:", count
                with open('high_utilization_ec2.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name, instance.id, instance.tags['Name'], instance.instance_type, count,'Overutilized','CPU Utilization >90% for atleast 4 days in last 2 weeks'])
                        #print region.name, instance.id, instance.tags['Name'], instance.instance_type, count,'Overutilized'


            else:
                    print "Instance is optimized"
                #print "CPU Sum:", cpusum/7
                #print "Count:", count
                #with open('high_utilization_ec2.csv', 'a') as csvfile:
                 #                   writer = csv.writer(csvfile, delimiter=',')
                  #                  writer.writerow([region.name, instance.id, instance.tags['Name'], instance.instance_type, count,'Normal'])


