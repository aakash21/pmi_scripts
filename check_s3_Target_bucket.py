##The target bucket does not exist##########################################
import boto
import boto.ec2
import boto.s3
import boto.s3.bucket
import boto.s3.acl
import boto.s3.bucketlistresultset
import csv


connection = boto.ec2.connect_to_region("us-east-1")
print connection
with open('s3.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['S3 List','Target Bucket'])
connection1 = boto.s3.connect_to_region("us-east-1")
test = connection1.get_all_buckets()
print dir(test)
for i in test :
    #print dir(i)
    print i.name
    p = i.name

    log_status = i.get_logging_status()
    print "Logging Status",log_status
    print "The target bucket exist status  ::",log_status.target
    '''with open('s3.csv', 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([p,log_status.target])'''
    if log_status.target == None:
        with open('s3.csv', 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([p,'Not Exist'])
    else:
        with open('s3.csv', 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([p,'Exist'])



