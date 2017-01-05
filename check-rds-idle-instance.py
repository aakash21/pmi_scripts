######################################################################
## An active DB instance has not had a connection in the last 7 days##
######################################################################
import boto
import boto.ec2
import boto.rds
import datetime
import csv
import dateutil
from datetime import timedelta
from boto.ec2 import cloudwatch
from boto.ec2.cloudwatch import CloudWatchConnection
cw = CloudWatchConnection()
print cw
connection = boto.ec2.connect_to_region("us-east-1")
regions = connection.get_all_regions()
with open('idleRDS.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Region','Endpoint','Status'])
for region in regions:
    connection = boto.rds.connect_to_region(region.name)
    with open('cloudtrail.csv', 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([connection,'False','False'])
#print dir(connection)
    rdssum=0
    db = connection.get_all_dbinstances()
 #print dir(db)
    for i in db:
        rdscount = 0
        print i.endpoint[0]


        daystomonitor = [1,2,3,4,5,6,7]
        for day in daystomonitor:

            retention_policy = i.backup_retention_period
            availability_zone = i.availability_zone
            rdsresults = cw.get_metric_statistics(
            3600, # Granularity
            datetime.datetime.utcnow()-datetime.timedelta(days=day), # Start
            datetime.datetime.utcnow()-datetime.timedelta(days=day-1), # End
            'DatabaseConnections', # Metric name
            'AWS/RDS', # Namespace
            'Average', # Statistics
            dimensions={'DBInstanceIdentifier':i.id} # Dimensions
        )

        if not rdsresults:
            print "No data exist"
            continue
        else:
            rdsread = rdsresults.pop()
            if rdsread['Average'] > 1:
                rdscount = rdscount + 1
             #print rdssum
        if rdscount < 1:
                print "RDS Idle"
                with open('idleRDS.csv', 'a') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow([region.name,i.endpoint[0],'Idle'])
        else:
            print "USE"
            #print rdsread['Average']












