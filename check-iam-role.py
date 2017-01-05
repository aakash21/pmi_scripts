import boto
from boto import iam
import datetime
import time,datetime
from datetime import datetime
import csv

connection = iam.connect_to_region('us-east-1')

with open('iamRoles.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Role Name','Age','ARN','Status'])


print connection

#print dir(connection)

roles = connection.list_roles()
#print roles

#roles2 = connection.get_role_policy()
#print roles2

for role in roles['list_roles_response']['list_roles_result']['roles']:
    print role
    print role['create_date']
    z = role['create_date']
    #print datetime.datetime.date(role['create_date'])
    #print datetime.datetime.strptime(role['create_date'],'%Y-%m-%d')
    #print datetime.datetime.strftime(test,'%Y-%m-%d')
    #a = datetime.strptime(z, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d')
    #z = snapid[len(snapid)-1].start_time
    a = datetime.strptime(z, '%Y-%m-%dT%H:%M:%SZ')
    b = datetime.now()
    p = (b - a).days
    print p
    if p >= 90:
        with open('iamRoles.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow([role['role_name'],p,role['arn'],'Red'])
    else:
        with open('iamRoles.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow([role['role_name'],p,role['arn'],'Green'])
