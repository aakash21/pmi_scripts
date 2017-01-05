#!/usr/bin/python
import boto,csv,os
from boto import s3
from boto.s3.connection import S3Connection
from boto.s3.connection import OrdinaryCallingFormat

with open('bucket_policy.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Bucket Name','Lifecycle Configuration'])

conn = S3Connection(is_secure=False)
buckets = conn.get_all_buckets()
print buckets

for bucket in buckets:
    try:
        bucket = conn.get_bucket(bucket.name)
        try:
            policy = bucket.get_policy()
            if 's3:x-amz-server-side-encryption' in policy:
                with open('bucket_policy.csv', 'a') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow([bucket.name,'Bucket is encrypted'])
            else:
                with open('bucket_policy.csv', 'a') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow([bucket.name,'Bucket is not encrypted'])
        except:
            with open('bucket_policy.csv', 'a') as csvfile:
                 writer = csv.writer(csvfile, delimiter=',')
                 writer.writerow([bucket.name,'No Policy is attached to the bucket'])


    except:
         os.environ['S3_USE_SIGV4']='True'
         s3conn = S3Connection(is_secure=False,host='s3.eu-central-1.amazonaws.com')
         try:
            bucket = s3conn.get_bucket(bucket.name,validate=True)
            try:
                policy = bucket.get_policy()
                if 's3:x-amz-server-side-encryption' in policy:
                    with open('bucket_policy.csv', 'a') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',')
                        writer.writerow([bucket.name,'Bucket is encrypted'])
                else:
                    with open('bucket_policy.csv', 'a') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',')
                        writer.writerow([bucket.name,'Bucket is not encrypted'])

            except:
                with open('bucket_policy.csv', 'a') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow([bucket.name,'No Policy is attached to the bucket'])
            del os.environ['S3_USE_SIGV4']

         except:
            connection = s3.connect_to_region('us-east-1',calling_format=OrdinaryCallingFormat())
            bucket = connection.get_bucket(bucket.name,validate=True)
            try:
                bucket = s3conn.get_bucket(bucket.name,validate=True)
                try:
                    policy = bucket.get_policy()
                    if 's3:x-amz-server-side-encryption' in policy:
                        with open('bucket_policy.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow([bucket.name,'Bucket is encrypted'])
                    else:
                        with open('bucket_policy.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow([bucket.name,'Bucket is not encrypted'])


                except:
                    with open('bucket_policy.csv', 'a') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',')
                        writer.writerow([bucket.name,'The lifecycle configuration does not exist'])

            except:
                print "Something bad has happened"

