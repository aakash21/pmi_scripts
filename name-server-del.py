#Description: Checks for Amazon Route 53 hosted zones for which your domain registrar or DNS is not using the correct Route 53 name servers. When you create a hosted zone, Route 53 assigns a delegation set of four name servers. The names of these servers are ns-###.awsdns-##.com, .net, .org, and .co.uk, where ### and ## typically represent different numbers. Before Route 53 can route DNS queries for your domain, you must update your registrar's name server configuration to remove the name servers that the registrar assigned and add all four name servers in the Route 53 delegation set. For maximum availability, you must add all four Route 53 name servers.
#Alert Criteria
#Yellow: A hosted zone for which the registrar for your domain does not use all four of the Route 53 name servers in the delegation set.

import boto
from boto import ec2
from boto import route53
import csv

with open('NS_delegation.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Hosted Zone', 'Status'])


conn = route53.connect_to_region('us-east-1')
hosted_zones = conn.get_all_hosted_zones()
zones = conn.get_zones()

print dir(conn)
# To listed Hosted Domains
for zone in hosted_zones['ListHostedZonesResponse']['HostedZones']:
    zone_name = zone['Name']
    zone_ids = zone['Id'].split("/")[2]
    print zone_name
    hosts = conn.get_all_rrsets(zone_ids)

    for host in hosts:
        if host.type == 'NS':
            print host.name, host.resource_records
            if len(host.resource_records) == 4:
                with open('NS_delegation.csv', 'a') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',')
                        writer.writerow([host.name, 'Green'])
            else:
                with open('NS_delegation.csv', 'a') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',')
                        writer.writerow([host.name, 'Yellow'])

            #print dir(host.failover)
#    print "\n********************************************************************\n"