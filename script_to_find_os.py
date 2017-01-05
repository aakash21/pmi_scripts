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
import numpy as np
import os
import subprocess


data = np.loadtxt('new.csv',dtype=np.str,delimiter='    ',skiprows=1)
print data
for i in data:
        var = str(i).split('\t')
        cmd = "sh /home/nainam/Downloads/hello.sh %s %s %s" %(var[5],var[2],var[3])
        os.system(cmd)
        file = open('/home/nainam/Downloads/test2.txt', 'r')
        read=file.read()
        osystem =str(read).strip(' \t\n\r')
        if not osystem:
            osystem = 'Login issue'
        with open('new.csv', 'a') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',')
                        writer.writerow([var[0], var[1], var[2], var[3], var[4],var[5],osystem])




