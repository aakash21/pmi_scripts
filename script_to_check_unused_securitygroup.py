import boto
import boto.ec2
EC2_REGION='ap-southeast-2'
ec2region = boto.ec2.get_region(EC2_REGION)
ec2 = boto.connect_ec2(region=ec2region)
sgs = ec2.get_all_security_groups()
for sg in sgs:
    if len(sg.instances()) == 0:
        print ("{0},{1}".format(sg.id, sg.name))
