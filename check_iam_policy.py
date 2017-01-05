
#!/usr/bin/python
#Description: Checks for your use of AWS Identity and Access Management (IAM). You can use IAM to create users, groups, and roles in AWS, and you can use permissions to control access to AWS resources.

import csv
import boto
from boto import iam
connection = iam.connect_to_region('us-east-1')

with open('IAMinuse.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['IAM - Users','IAM - Roles', 'IAM - Groups', 'IAM in use'])


### IAM User Check ###
iamuser_list=[]
iamusers = connection.get_all_users()
if not iamusers.users:
    print 'No User Found'
try:
    for user in iamusers.users:
        print user.user_name
        with open('IAMinuse.csv', 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([user.user_name])
except:
        print 'Error in IAM user checking'

### IAM Role Check ###
iam_list=[]
iamroles = connection.list_roles()
if not iamroles.roles:
    print 'No Role Found'
try:
    for roles in iamroles.roles:
        print roles.role_name
        with open('IAMinuse.csv', 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['',roles.role_name])
except:
        print 'Error in IAM role checking'




### IAM Group Check ###
iamgroup_list=[]
iamgroups = connection.get_all_groups()
if not iamgroups.groups:
    print 'No Group Found'
try:
    for groups in iamgroups.groups:
        print groups.group_name
        with open('IAMinuse.csv', 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['','',groups.group_name])
except:
        print 'Error in IAM group checking'



if iamusers.users and iamgroups.groups and iamroles.roles:

    with open('IAMinuse.csv', 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['','','', 'True'])

else:
<<<<<<< HEAD
    with open('IAMinuse.csv', 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['','','', 'False'])
=======
    print 'IAM not in Use'

