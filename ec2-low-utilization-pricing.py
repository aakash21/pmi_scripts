#!/usr/bin/python
# Description: An instance had 10% or less daily average CPU utilization and 5 MB or less network I/O on at least 4 of the previous 14 days.

import boto
from boto import ec2
from boto.ec2 import cloudwatch
import datetime
import dateutil
from datetime import timedelta
from boto.ec2.cloudwatch import CloudWatchConnection
import csv
import urllib2
import json,re
import math

jsontoec2 = {
    "us-east" : "us-east-1",
    "us-east-1" : "us-east-1",
    "us-west" : "us-west-1",
    "us-west-1" : "us-west-1",
    "us-west-2" : "us-west-2",
    "eu-ireland" : "eu-west-1",
    "eu-west-1" : "eu-west-1",
    "eu-central-1" : "eu-central-1",
    "apac-sin" : "ap-southeast-1",
    "ap-southeast-1" : "ap-southeast-1",
    "ap-southeast-2" : "ap-southeast-2",
    "apac-syd" : "ap-southeast-2",
    "apac-tokyo" : "ap-northeast-1",
    "ap-northeast-1" : "ap-northeast-1",
    "sa-east-1" : "sa-east-1",
    "us-gov-west-1" : "us-gov-west-1"
}

ec2recommend = {
    "c3.large" : "m3.medium",
    "c3.xlarge" : "c3.large",
    "c3.2xlarge" : "c3.large",
    "c3.4xlarge" : "c3.large",
    "m3.large" : "m3.medium",
    "m3.xlarge" : "m3.medium",
    "m3.2xlarge" : "m3.large",
    "m3.4xlarge" : "m3.large",
    "m3.medium" : "t2.small",
    "r3.large" : "m3.medium",
    "r3.xlarge" : "m3.large",
    "r3.2xlarge" : "m3.large",
    "r3.4xlarge" : "m3.xlarge",
}


with open('ec2pricing.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Region','OS','Instance ID', 'Instance Type', 'Instance Pricing'])


linux='http://a0.awsstatic.com/pricing/1/ec2/linux-od.min.js'
rhel='http://a0.awsstatic.com/pricing/1/ec2/rhel-od.min.js'
windows='http://a0.awsstatic.com/pricing/1/ec2/mswin-od.min.js'



def get_json(var):
        jsonp_string = urllib2.urlopen(var).read()
        json_string = re.sub(r"(\w+):", r'"\1":', jsonp_string[jsonp_string.index('callback(') + 9 : -2])
        pricing = json.loads(json_string)
        return pricing

def extract(a,b,c):
    for i in a['config']['regions']:
        if c == 'us-gov-west-1':
            continue
        elif c == jsontoec2[i['region']]:
            print i['region']
            defaultinstances={}
            for z in i['instanceTypes']:
                j=0
                print len(z['sizes'])
                while j < len(z['sizes']):
                    instancetype = z['sizes'][j]['size']
                    instanceprice = z['sizes'][j]['valueColumns'][0]['prices']['USD']
                    defaultinstances[str(instancetype)]= str(instanceprice)
                    j = j + 1
                    #ec2conn = ec2.connect_to_region(jsontoec2[i['region']])
            #reservations = ec2conn.get_all_reservations()
            #for reservation in reservations:
            #    for instance in reservation.instances:
             #       print instance, instance.instance_type
            if b in defaultinstances:
                    if b in ec2recommend:
                        print 'hello'
                        hourly = defaultinstances[b]
                        diff=float(hourly)-float(defaultinstances[ec2recommend[b]])
                        with open('ec2pricing.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow([jsontoec2[i['region']],b,hourly,ec2recommend[b],defaultinstances[ec2recommend[b]],diff])
                    else:
                        with open('ec2pricing.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow([jsontoec2[i['region']],b,defaultinstances[b],'','',''])


with open('ec2instances.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        print row[0],row[1], row[2]

        if row[2] == 'linux':
            pricing_linux = get_json(linux)
            extract(pricing_linux,row[1],row[0])
        elif row[2] == 'windows':
            pricing_windows=get_json(windows)
            extract(pricing_windows,row[1],row[0])
        elif row[2] == 'rhel':
             pricing_rhel=get_json(rhel)
             extract(pricing_rhel,row[1],row[0])

