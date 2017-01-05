#Description: For each MX resource record set, checks for a TXT resource record set that contains a corresponding SPF value. The SPF (Sender Policy Framework) value specifies the servers that are authorized to send email for your domain. This helps reduce spam by detecting and stopping email address spoofing. (Resource record sets that use the experimental SPF type are no longer recommended.)
#Alert Criteria
#Yellow: An MX resource record set does not have a TXT resource record set that contains a corresponding SPF value.

import boto
from boto import ec2
from boto import route53
import csv

conn = route53.connect_to_region('us-east-1')
hosted_zones = conn.get_all_hosted_zones()
zones = conn.get_zones()
mxRecors=""
print dir(conn)

with open('route53_mx_rrs.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Zone Name','SPF Record', 'SPF Status'])

# To listed Hosted Domains
for zone in hosted_zones['ListHostedZonesResponse']['HostedZones']:
    zone_name = zone['Name']
    zone_ids = zone['Id'].split("/")[2]
    print zone_name
    hosts = conn.get_all_rrsets(zone_ids)
    for host in hosts:

       if host.type == 'MX':
            mxRecors='true'

       if mxRecors and host.type == 'TXT':
        spf = host.resource_records[0]
        if zone_name[:-1] in spf[1:-1]:
            with open('route53_mx_rrs.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([zone_name, spf, 'True'])

        else:
            with open('route53_mx_rrs.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([zone_name, spf, 'False'])




