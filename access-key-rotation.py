#!/usr/bin/python
# Script to check IAM for active access keys
# Author: Neeraj Gupta

import boto
from boto import iam
import csv
import datetime
import time,datetime
from datetime import datetime

connection = iam.connect_to_region('us-east-1')

with open('AccessKeyRotation.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Username','Access Key ID', 'Age', 'Active/Disable','Status' ])


print connection.gs_access_key_id
users = connection.get_all_users('/')['list_users_response']['list_users_result']['users']
for user in users:
    print connection.get_all_access_keys(user.user_name)['list_access_keys_response']['list_access_keys_result']['access_key_metadata']
    for al in connection.get_all_access_keys(user.user_name)['list_access_keys_response']['list_access_keys_result']['access_key_metadata']:
        z = al.create_date
        a = datetime.strptime(z, '%Y-%m-%dT%H:%M:%SZ')
        b = datetime.now()
        p = (b - a).days
        print p
        if p >= 90:
            with open('AccessKeyRotation.csv', 'a') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow([al.user_name,al.access_key_id, p, al.status,'Age than 90 days'])
        else:
            with open('AccessKeyRotation.csv', 'a') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow([al.user_name,al.access_key_id, p, al.status,'Green'])