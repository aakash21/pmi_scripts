#!/usr/bin/python
##Amazon EBS snapshot script##
##Conditions##
#Yellow: The most recent volume snapshot is between 7 and 30 days old.
#Red: The most recent volume snapshot is more than 30 days old.
#Red: The volume does not have a snapshot.
#########################################

import boto.ec2
import datetime
import time,datetime
from datetime import datetime
import dateutil
import csv

connection = boto.ec2.connect_to_region('us-east-1')
regions = connection.get_all_regions()

with open('ebsSnapshots.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Region','Volume ID','Snapshot ID','Snapshot Age','Status','Reason'])

for region in regions:
    conn = boto.ec2.connect_to_region(region.name)
    print conn
    snaps = conn.get_all_snapshots(owner="self")
    volumes = conn.get_all_volumes()

    for vol in volumes:
        snapid=[]
        snapshot=conn.get_all_snapshots(filters={"volume-id":vol.id})
        if snapshot:
            snapshots = conn.get_all_snapshots(owner="self",filters={"volume-id":vol.id})
            for snapshot in snapshots:
                snapid.append(snapshot)
            #print len(snapid)
            #print snapid[0]

            #for i in snapid[len(snapid)-1]:#
            z = snapid[len(snapid)-1].start_time
            a = datetime.strptime(z, '%Y-%m-%dT%H:%M:%S.%fZ')
            b = datetime.now()
            p = (b - a).days

                #print "Number of days Snapshot older = %s  "  %(p)
            if p>=7 and p<30:
                  with open('ebsSnapshots.csv', 'a') as csvfile:
                                            writer = csv.writer(csvfile, delimiter=',')
                                            writer.writerow([region.name, vol.id, snapid[len(snapid)-1],p,'Yellow','Age'])
              #    print "Snapshot older then 7 but not more than 30 days"
            if p>=30:
                  with open('ebsSnapshots.csv', 'a') as csvfile:
                                            writer = csv.writer(csvfile, delimiter=',')
                                            writer.writerow([region.name, vol.id, snapid[len(snapid)-1],p,'Red','Age'])
              #        print "Snapshot older than 30 days"
                  #print "Snapshot Found"
        else:
            with open('ebsSnapshots.csv', 'a') as csvfile:
                                    writer = csv.writer(csvfile, delimiter=',')
                                    writer.writerow([region.name, vol.id, '', '','Red','No Snapshot'])


        '''
          for i in snaps:
          snapid = i.id
          test = i.volume_id
          print "VolumeID = %s" %test
          print "SnapshotID = %s" %snapid
          z = i.start_time
          a = datetime.strptime(z, '%Y-%m-%dT%H:%M:%S.%fZ')
          b = datetime.now()
          p = (b - a).days

          #print "Number of days Snapshot older = %s  "  %(p)
          if p>=7 and p<30:
              with open('ebsSnapshots.csv', 'a') as csvfile:
                                        writer = csv.writer(csvfile, delimiter=',')
                                        writer.writerow([region.name, test, snapid, p,'Yellow'])
          #    print "Snapshot older then 7 but not more than 30 days"
          if p>=30:
              with open('ebsSnapshots.csv', 'a') as csvfile:
                                        writer = csv.writer(csvfile, delimiter=',')
                                        writer.writerow([region.name, test, snapid, p,'Red'])
          #        print "Snapshot older than 30 days"
          #print "==================================="

          '''
