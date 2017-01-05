#!/usr/bin/python
#Description: Checks for resource record sets that are associated with health checks that have been deleted. Amazon Route 53 does not prevent you from deleting a health check that is associated with one or more resource record sets. If you delete a health check without updating the associated resource record sets, the routing of DNS queries for your DNS failover configuration will not work as intended.
#Alert Criteria
#Yellow: A resource record set is associated with a health check that has been deleted.

__author__ = 'niraj'

import boto
from boto import ec2
from boto import route53
from boto.route53 import healthcheck
import csv

conn = route53.connect_to_region('us-east-1')

hosted_zones = conn.get_all_hosted_zones()
zones = conn.get_zones()

with open('deleted_R53health_checks.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Hosted Zone Name','Hosted Zone ID', 'RRS ID', 'Type','Health Check Id','Status'])


print dir(conn)
# To listed Hosted Domains
for zone in hosted_zones['ListHostedZonesResponse']['HostedZones']:
    zone_name = zone['Name']
    zone_ids = zone['Id'].split("/")[2]
    print zone_name
    hosts = conn.get_all_rrsets(zone_ids,)

    for host in hosts:
        hcs = conn.get_list_health_checks()
        for hc in hcs['ListHealthChecksResponse']['HealthChecks']:
            print hc['Id']
            if host.health_check == hc['Id']:
                with open('deleted_R53health_checks.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([host.name, host.identifier, host.type,hc['Id'],'Found'])
                #print "Health Check Exist", host.name
            else:
                with open('deleted_R53health_checks.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([host.name, host.identifier,host.type,hc['Id'],'Not Found'])
                #print "Health Check Doesnt Exit", host.name
            #print host.name, host.health_check, host.type, host.resource_records, host.alias_evaluate_target_health
        #print dir(host)
    print "\n********************************************************************\n"


