#Description: Checks for resource record sets that can benefit from having a lower time-to-live (TTL) value. TTL is the number of seconds that a resource record set is cached by DNS resolvers. When you specify a long TTL, DNS resolvers take longer to request updated DNS records, which can cause unnecessary delay in rerouting traffic (for example, when DNS Failover detects and responds to a failure of one of your endpoints).
#Alert Criteria
#Yellow: A resource record set whose routing policy is Failover has a TTL greater than 60 seconds.
#Yellow: A resource record set with an associated health check has a TTL greater than 60 seconds.

__author__ = 'niraj'

import boto
from boto import ec2
from boto import route53
import csv

conn = route53.connect_to_region('us-east-1')
hosted_zones = conn.get_all_hosted_zones()
zones = conn.get_zones()

with open('high-ttl.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Host Name','Failover', 'Health Check','TTL','STATUS'])



print dir(conn)
# To listed Hosted Domains
for zone in hosted_zones['ListHostedZonesResponse']['HostedZones']:
    zone_name = zone['Name']
    zone_ids = zone['Id'].split("/")[2]
    print zone_name
    hosts = conn.get_all_rrsets(zone_ids)

    for host in hosts:
        print host.name, host.failover, host.health_check
        if host.failover:
            if host.ttl > 60:
                with open('high-ttl.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([host.name, host.failover, host.health_check, host.ttl,'Red'])

                #print "FailOver TTL High", host.ttl
            else:
                with open('high-ttl.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([host.name, host.failover, host.health_check, host.ttl,'Green'])

                #print "FailOver TTL OK", host.ttl

        if host.health_check:
            if host.ttl > 60:
                with open('high-ttl.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([host.name, host.failover, host.health_check, host.ttl,'Red'])

                #print "Health TTL High", host.ttl
            else:
                with open('high-ttl.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([host.name, host.failover, host.health_check, host.ttl,'Green'])

                #print "Health TTL OK", host.ttl
    '''

        print host.name, host.identifier, host.failover, host.health_check, host.type, host.alias_dns_name, host.resource_records, host.ttl
        #print dir(host)
    print "\n********************************************************************\n"
    '''

