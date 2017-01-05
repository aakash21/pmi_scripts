#!/usr/bin/python
# Script to check active VPN connections in all the regions
# Author: Neeraj Gupta


import boto
from boto import ec2
from boto import vpc
import csv

connection=ec2.connect_to_region('us-east-1')

with open('vpnConnection.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Region','VPN Connection Name','VPN Id','Tunel 1','Tunnel 2', 'VPN Type', 'Status'])

regions = connection.get_all_regions()
for region in regions:
    vpnconn = vpc.connect_to_region(region.name)
    allvpn = vpnconn.get_all_vpn_connections()
    if len(allvpn) == 0:
        with open('vpnConnection.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow([region.name,'VPN Connection Not Found'])
    else:
        for vpn in allvpn:
            with open('vpnConnection.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow([region.name,vpn.tags['Name'],vpn.id,vpn.tunnels[0],vpn.tunnels[1], vpn.type, vpn.state])
