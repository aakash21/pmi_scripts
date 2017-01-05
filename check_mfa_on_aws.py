#!/usr/bin/python
#import boto
#from boto import iam
#connection = iam.connect_to_region('us-east-1')
#iammfa = connection.get_all_mfa_devices('neeraj.gupta')
#print(iammfa)

import boto
from boto import iam
import csv

#connection=iam.IAMConni()
connection = iam.connect_to_region('us-east-1')

with open('MFAstatus.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['MFA','Status'])

root = connection.get_account_summary()
print root
if root['AccountMFAEnabled']:
    with open('MFAstatus.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow(['Root Account','Enabled'])
else:
    with open('MFAstatus.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow(['Root Account','Disabled'])

iamProfiles=connection.get_all_users();

for user in iamProfiles.users:

    mfaDevices = connection.get_all_mfa_devices(user.user_name)


    if mfaDevices.mfa_devices:
        #print "User --->",user.user_name , " MFA : Enabled"
        with open('MFAstatus.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([user.user_name,'Enabled'])
    else:
        print "User ---> ",user.user_name , "MFA : Disabled"
        with open('MFAstatus.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([user.user_name,'Disabled'])
