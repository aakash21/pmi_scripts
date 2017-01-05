#!/usr/bin/python
## Script to find the cloudtrail configuration in each region with details and to check logging is enabled or not  ##
##CloudTrail reports log delivery errors for a region ###############################################################
##Cloudtrail csv will be generated###################################################################################
import boto
import boto.ec2
import boto.cloudtrail
import boto.cloudtrail.layer1
import boto.cloudtrail.exceptions
from boto.cloudtrail.layer1 import CloudTrailConnection
import json
import csv

connection = boto.ec2.connect_to_region("us-east-1")

regions = connection.get_all_regions()

#print regions

with open('cloudtrail.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Region','CloudTrail Status', 'Log Delivery Error'])

for region in regions:
    connection1 = boto.cloudtrail.connect_to_region(region.name)
    print region
    print region.name
    ctstatus = connection1.describe_trails()
    test = connection1
    print "==================================================="
    print test
    print "==================================================="
    pc = ctstatus['trailList']
    if len(ctstatus['trailList']) == 0:
           print 'A trail has not been created for a region\n'
           with open('cloudtrail.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow([region.name, 'False', 'False'])

    else:
        print 'A trail has  been created for a region'
        #print ctstatus['trailList']
        dc = ctstatus['trailList']
        abc = dc[0]
        logg = abc['Name']
        tc = connection1.get_trail_status(logg)
        print "Logging for this Cloudtrail :: ",tc['IsLogging']
        try:
             rf = tc['LatestDeliveryError']
             rg = boto.cloudtrail.exceptions.CloudWatchLogsDeliveryUnavailableException(status=rf,reason='LatestDeliveryError',body=None)
             #print "CloudTrail reports log delivery errors for this region : EXIST    Error Details::",rg

             with open('cloudtrail.csv', 'a') as csvfile:
                                                 writer = csv.writer(csvfile, delimiter=',')
                                                 writer.writerow([region.name, tc['IsLogging'], 'True'])

        except KeyError as rg:
            #print "CloudTrail reports log delivery errors for this region : NOT EXIST", rg
              with open('cloudtrail.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name, tc['IsLogging'], 'False'])

