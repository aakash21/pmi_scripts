import boto,csv,os
from boto.s3.connection import S3Connection
from boto import s3
from boto.s3.connection import OrdinaryCallingFormat

all_users = 'http://acs.amazonaws.com/groups/global/AllUsers'
conn = S3Connection()
buckets = conn.get_all_buckets()
print buckets
with open('s3bucket_logging.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Bucket name, Logging Status'])

for bucket in buckets:
        try:
            bucket = conn.get_bucket(bucket.name,validate=True)
            status = bucket.get_logging_status()
            s = str(status)
            if s.__contains__('Disabled'):
                with open('s3bucket_logging.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow([bucket.name,'Disabled'])

            else:
                    try:
                        with open('s3bucket_logging.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow(['Source Bucket  name'])
                            writer.writerow([bucket.name])
                        source_owner=bucket.get_acl().owner.display_name

                        with open('s3bucket_logging.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow(['Source Bucket owner name:'])
                            writer.writerow([bucket.get_acl().owner.display_name])

                        s3conn = S3Connection()
                        target_bucket = s3conn.get_bucket(status.target)

                        with open('s3bucket_logging.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow(['Target Bucket  name:'])
                            writer.writerow([target_bucket.name])

                        target_owner=target_bucket.get_acl().owner.display_name
                        with open('s3bucket_logging.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow(['Target Bucket owner name:'])
                            writer.writerow([target_bucket.name])
                        if not source_owner == target_owner:
                            with open('s3bucket_logging.csv', 'a') as csvfile:
                                writer = csv.writer(csvfile, delimiter=',')
                                writer.writerow(['Target Bucket owner name:'])
                                writer.writerow([target_bucket.name])
                    except:
                        with open('s3bucket_logging.csv', 'a') as csvfile:
                                writer = csv.writer(csvfile, delimiter=',')
                                writer.writerow([bucket.name,'This bucket does not exists'])
        except:
            os.environ['S3_USE_SIGV4']='True'
            s3conn = S3Connection(is_secure=False,host='s3.eu-central-1.amazonaws.com',calling_format=OrdinaryCallingFormat())
            try:
                bucket = s3conn.get_bucket(bucket.name,validate=True)
                status = bucket.get_logging_status()
                s=str(status)
                if s.__contains__('Disabled'):
                    with open('s3bucket_logging.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow([bucket.name,'Disabled'])
                else:
                    try:
                        with open('s3bucket_logging.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow(['Source Bucket  name'])
                            writer.writerow([bucket.name])
                        source_owner=bucket.get_acl().owner.display_name
                        with open('s3bucket_logging.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow(['Source Bucket owner name:'])
                            writer.writerow([bucket.get_acl().owner.display_name])

                        s3conn = S3Connection()
                        target_bucket = s3conn.get_bucket(status.target)
                        with open('s3bucket_logging.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow(['Target Bucket  name:'])
                            writer.writerow([target_bucket.name])

                        target_owner=target_bucket.get_acl().owner.display_name
                        with open('s3bucket_logging.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow(['Target Bucket owner name:'])
                            writer.writerow([target_bucket.name])
                        if not source_owner == target_owner:
                            with open('s3bucket_logging.csv', 'a') as csvfile:
                                writer = csv.writer(csvfile, delimiter=',')
                                writer.writerow(['Target Bucket owner name:'])
                                writer.writerow([target_bucket.name])
                    except:
                        with open('s3bucket_logging.csv', 'a') as csvfile:
                                writer = csv.writer(csvfile, delimiter=',')
                                writer.writerow([bucket.name,'This bucket does not exists'])


            except:
                connection = s3.connect_to_region('us-east-1',calling_format=OrdinaryCallingFormat())
                try:
                    bucket = connection.get_bucket(bucket.name,validate=True)
                    status = bucket.get_logging_status()
                    s = str(status)
                    if s.__contains__('Disabled'):
                        with open('s3bucket_logging.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow([bucket.name,'Disabled'])
                    else:
                        with open('s3bucket_logging.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow(['Source Bucket  name'])
                            writer.writerow([bucket.name])
                        source_owner=bucket.get_acl().owner.display_name
                        with open('s3bucket_logging.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow(['Source Bucket owner name:'])
                            writer.writerow([bucket.get_acl().owner.display_name])

                        s3conn = S3Connection()
                        target_bucket = s3conn.get_bucket(status.target)
                        with open('s3bucket_logging.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow(['Target Bucket  name:'])
                            writer.writerow([target_bucket.name])

                        target_owner=target_bucket.get_acl().owner.display_name
                        with open('s3bucket_logging.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow(['Target Bucket owner name:'])
                            writer.writerow([target_bucket.name])
                        if not source_owner == target_owner:
                            with open('s3bucket_logging.csv', 'a') as csvfile:
                                writer = csv.writer(csvfile, delimiter=',')
                                writer.writerow(['Target Bucket owner name:'])
                                writer.writerow([target_bucket.name])
                except:
                        with open('s3bucket_logging.csv', 'a') as csvfile:
                                writer = csv.writer(csvfile, delimiter=',')
                                writer.writerow([bucket.name,'This bucket is empty'])
            del os.environ['S3_USE_SIGV4']





