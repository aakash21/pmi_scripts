#!/usr/bin/python
#Description: Checks the password policy for your account and warns when a password policy is not enabled, or if password content requirements have not been enabled. Password content requirements increase the overall security of your AWS environment by enforcing the creation of strong user passwords. When you create or change a password policy, the change is enforced immediately for new users but does not require existing users to change their passwords.


import boto
from boto import iam
import csv
connection = iam.connect_to_region('us-east-1')

with open('IAMpasswordpolicy.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Password Policy','Uppercase','Lowercase','Number','Non-alphanumeric'])
try:
    passpolicy = connection.get_account_password_policy()
    with open('IAMpasswordpolicy.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(['Enabled',passpolicy.require_uppercase_characters,passpolicy.require_lowercase_characters,passpolicy.require_numbers,passpolicy.require_symbols, 'Enabled'])




except:
    with open('IAMpasswordpolicy.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(['Disabled',passpolicy.require_uppercase_characters,passpolicy.require_lowercase_characters,passpolicy.require_numbers,passpolicy.require_symbols, 'Disabled'])
