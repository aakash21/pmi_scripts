#!/usr/bin/python
#Description: Checks for Amazon Route 53 failover resource record sets that are misconfigured. When Amazon Route 53 health checks determine that the primary resource is unhealthy, Amazon Route 53 responds to queries with a secondary, backup resource record set. You must create correctly configured primary and secondary resource record sets for failover to work.
#Alert Criteria
#Yellow: A primary failover resource record set does not have a corresponding secondary resource record set.
#Yellow: A secondary failover resource record set does not have a corresponding primary resource record set.
#Yellow: Primary and secondary resource record sets that have the same name are associated with the same health check.

__author__ = 'niraj'

import boto
from boto import ec2
from boto import route53
import csv

with open('route53-failover-routes.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Host Name','Failover Status', 'Health Check','Status'])

conn = route53.connect_to_region('us-east-1')
hosted_zones = conn.get_all_hosted_zones()
zones = conn.get_zones()
hosts=[]
print dir(conn)
# To listed Hosted Domains
for zone in hosted_zones['ListHostedZonesResponse']['HostedZones']:
    zone_name = zone['Name']
    zone_ids = zone['Id'].split("/")[2]
    #print zone_name
    hosts = conn.get_all_rrsets(zone_ids)

    for host in hosts:
        #print dir(host)
        if host.type == 'NS' or host.type == 'SOA':
            continue
        else:
            if not host.failover:
                with open('route53-failover-routes.csv', 'a') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow([host.name,host.failover,host.health_check,'Not Found'])

            else:
                with open('route53-failover-routes.csv', 'a') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow([host.name,host.failover,host.health_check,'Found'])