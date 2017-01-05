######################################################################
## A DB instance has the backup retention period set to 0 days.     ##
######################################################################
import boto
import boto.ec2
import boto.rds
import csv
import datetime
import dateutil
from datetime import timedelta
from boto.ec2 import cloudwatch
from boto.ec2.cloudwatch import CloudWatchConnection
cw = CloudWatchConnection()
print cw
connection = boto.ec2.connect_to_region("us-east-1")
regions = connection.get_all_regions()
with open('cloudtrail.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Region','Endpoint','Retention_policy','Status'])
for region in regions:
	connection = boto.rds.connect_to_region(region.name)
	print "#############################################"
	print "##",connection,"##"
	print  "############################################"
	with open('cloudtrail.csv', 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([connection,'False','False','False'])
	#print dir(connection)
	#print connection.debug
	#print connection.server_name()
	#print connection.profile_name

	db = connection.get_all_dbinstances()
	for d in db:
            print d.endpoint[0]
            retention_policy=d.backup_retention_period
            if retention_policy > 0:
                print "Backup Retention Policy more than Zero days"
                print "Number days Retention policy ::", retention_policy,"days\n"
                with open('cloudtrail.csv', 'a') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow([connection,d.endpoint[0],retention_policy,'Normal'])
            else:
                    print "Backup Retention Policy :: Zero days\n",
                    with open('cloudtrail.csv', 'a') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',')
                        writer.writerow([connection,d.endpoint[0],retention_policy,'Red'])




