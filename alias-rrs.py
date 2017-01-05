#Description: Checks for resource record sets that route DNS queries to AWS resources; these can be changed to alias resource record sets. An alias resource record set is a special Amazon Route 53 record type that routes DNS queries to an AWS resource (for example, an Elastic Load Balancing load balancer or an Amazon S3 bucket) or to another Route 53 resource record set. When you use alias resource record sets, Route 53 routes your DNS queries to AWS resources free of charge.
#Alert Criteria
#Yellow: A resource record set is a CNAME to an Amazon S3 website.
#Yellow: A resource record set is a CNAME to an Amazon CloudFront distribution.
#Yellow: A resource record set is a CNAME to an Elastic Load Balancing load balancer.

import boto
from boto import ec2
from boto import route53
import csv

conn = route53.connect_to_region('us-east-1')
hosted_zones = conn.get_all_hosted_zones()
zones = conn.get_zones()

with open('alias-rrs-route53.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Host Name','End Point', 'Record Type','Category', 'Status'])

print dir(conn)
# To listed Hosted Domains
for zone in hosted_zones['ListHostedZonesResponse']['HostedZones']:
    zone_name = zone['Name']
    zone_ids = zone['Id'].split("/")[2]
    print zone_name
    hosts = conn.get_all_rrsets(zone_ids,)
    for host in hosts:
        if host.type == 'CNAME':
            if 's3' in host.resource_records[0]:
                with open('alias-rrs-route53.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([host.name, host.resource_records[0],host.type, 'Amazon S3', 'Yellow'])

            elif 'cloudfront.net' in host.resource_records[0]:
                with open('alias-rrs-route53.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([host.name, host.resource_records[0],host.type, 'Amazon Cloudfront', 'Yellow'])

            elif 'rds.amazonaws.com' in host.resource_records[0]:
                with open('alias-rrs-route53.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([host.name, host.resource_records[0],host.type, 'Amazon RDS', 'Yellow'])




