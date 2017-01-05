#!/usr/bin/python

import boto,csv,os
from boto.s3.connection import S3Connection
from boto import s3
from boto.s3.connection import OrdinaryCallingFormat
all_users = 'http://acs.amazonaws.com/groups/global/AllUsers'
conn = S3Connection(is_secure=False)
buckets = conn.get_all_buckets()

with open('s3bucket.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['S3BucketName','Owner','Permissions owned'])
            
for bucket in buckets:
        try:
            bucket = conn.get_bucket(bucket.name,validate=True)
            acl = bucket.get_acl()
            for grant in acl.acl.grants:
                if grant.uri == all_users:
                    if grant.permission in ('READ','WRITE','WRITE_ACP','READ_ACP'):
                        with open('s3bucket.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow([bucket.name,'Everyone',grant.permission])
        except:
            os.environ['S3_USE_SIGV4']='True'
            s3conn = S3Connection(is_secure=False,host='s3.eu-central-1.amazonaws.com')
            try:
                bucket = s3conn.get_bucket(bucket.name,validate=True)
                acl = bucket.get_acl()
                for grant in acl.acl.grants:
                    if grant.uri == all_users:
                        if grant.permission in ('READ','WRITE','WRITE_ACP','READ_ACP'):
                            with open('s3bucket.csv', 'a') as csvfile:
                                writer = csv.writer(csvfile, delimiter=',')
                                writer.writerow([bucket.name,'Everyone',grant.permission])

            except:
                connection = s3.connect_to_region('us-east-1',calling_format=OrdinaryCallingFormat())
                bucket = connection.get_bucket(bucket.name,validate=True)
                acl = bucket.get_acl()
                for grant in acl.acl.grants:
                    if grant.uri == all_users:
                        if grant.permission in ('READ','WRITE','WRITE_ACP','READ_ACP'):
                            with open('s3bucket.csv', 'a') as csvfile:
                                writer = csv.writer(csvfile, delimiter=',')
                                writer.writerow([bucket.name,'Everyone',grant.permission])


            del os.environ['S3_USE_SIGV4']