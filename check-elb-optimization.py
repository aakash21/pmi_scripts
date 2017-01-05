import boto,csv,sys,datetime
from boto import ec2
from boto.ec2 import cloudwatch
from datetime import timedelta
from boto.ec2.cloudwatch import CloudWatchConnection
from boto.ec2 import elb

with open('ELB.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['ELB Name', 'No. Of Instances','Zone a','Zone b ','Zone c','Zone d', 'Zone e','Status','Region Name'])



def list(placement):
    if placement =='a':
        lista.append(i.placement)

    if placement =='b':
        listb.append(i.placement)

    if placement =='c':
        listc.append(i.placement)

    if placement =='d':
        listd.append(i.placement)

    if placement =='e':
        liste.append(i.placement)



connection=ec2.connect_to_region('us-east-1')
regions = connection.get_all_regions()
for region in regions:
    lbconnection = boto.ec2.elb.connect_to_region(region.name)
    ec2conn = ec2.connect_to_region(region.name)
    elbconn = elb.connect_to_region(region.name)
    elbs = lbconnection.get_all_load_balancers()
    if not elbs:
        with open('ELB.csv', 'a') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',')
                        writer.writerow(['ELB does not exists','','','','','','','',region.name])

    else:
        for lb in elbs:
                number= len(lb.instances)
                if lb.instances:
                    lista = []
                    listb = []
                    listc = []
                    listd = []
                    liste = []

                    instances = ec2conn.get_only_instances(instance_ids=[instance.id for instance in lb.instances])
                    for i in instances:
                        list(i.placement[-1])
                    with open('ELB.csv', 'a') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',')
                        writer.writerow([lb,len(lb.instances),len(lista),len(listb),len(listc),len(listd),len(liste),region.name])







