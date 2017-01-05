######################################################################
## A DB instance is deployed in a single Availability Zone.         ##
## A DB instance has the backup retention period set to 0 days.     ##
## An active DB instance has not had a connection in the last 7 days##
######################################################################
import boto
import boto.ec2
import boto.rds
import datetime
import dateutil
from datetime import timedelta
from boto.ec2 import cloudwatch
from boto.ec2.cloudwatch import CloudWatchConnection
cw = CloudWatchConnection()
print cw
connection = boto.ec2.connect_to_region("us-east-1")
regions = connection.get_all_regions()
for region in regions:
    connection = boto.rds.connect_to_region(region.name)
    print "#############################################"
    print "##",connection,"##"
    print  "############################################"
#print dir(connection)
    rdssum=0
    db = connection.get_all_dbinstances()
 #print dir(db)
    for i in db:
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
            print "========================="
            print "Day:", day
            if not rdsresults:
             print "No data exist"
             continue
            else:
                rdsread = rdsresults.pop()
                print i.id, "Database Connections:", rdsread['Average']
                rdssum = rdssum + rdsread['Average']
             #print rdssum
        if rdssum==0:
                print "==============================================================="
                print "DB instance has not had a connection in the last 7 days", rdssum/7
                print "==============================================================="
        else:
                print "Have connections"
                #print rdsread['Average']

                print "Availability_zone :",availability_zone
        if retention_policy > 0:
                 print "Backup Retention Policy more than Zero days"
                 print "Number days Retention policy ::", retention_policy,"days\n"
        else:
                    print "Backup Retention Policy :: Zero days\n",

                    check_multi_az = i.multi_az
        if check_multi_az == True:
                 print "Multi-AZ:", check_multi_az
        else:
            print "Multi-AZ:", check_multi_az
            print "============================================="


