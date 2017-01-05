#!/usr/bin/python
# Author: Neeraj Gupta

import boto
import boto.ec2
import boto.rds
import boto.rds2.layer1
from boto.rds2.layer1 import RDSConnection
from boto import ec2
import csv

with open('notificationsRDS.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Region','Source Type','Event Category List','Status','Enabled/Disabled','SNS URL'])

conn = boto.ec2.connect_to_region("us-east-1")
regions = conn.get_all_regions()

for region in regions:
    connection = boto.rds2.connect_to_region(region.name)
    db = connection.describe_event_subscriptions()
    if len(db['DescribeEventSubscriptionsResponse']['DescribeEventSubscriptionsResult']['EventSubscriptionsList']) == 0:
        with open('notificationsRDS.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow([region.name,'No Event Subscriptions Found'])
    else:
        for i in db['DescribeEventSubscriptionsResponse']['DescribeEventSubscriptionsResult']['EventSubscriptionsList']:
            print i
            print len(i)
            if len(i) != 0:
                with open('notificationsRDS.csv', 'a') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow([region.name,i['SourceType'],i['EventCategoriesList'],i['Status'],i['Enabled'],i['SnsTopicArn']])

