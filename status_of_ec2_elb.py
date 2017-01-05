import boto.ec2
import boto.ec2.elb

conn = boto.ec2.connect_to_region(
'us-west-1',
aws_access_key_id = key,
aws_secret_access_key = sk,
)

# get all instances
instances = []

def cleanupDNS(ip):
return 
ip.replace('-','.').replace('ec2.','').replace('ip.','').replace('.us.west.1.compute.internal','').replace('.us.west.1.compute.amazonaws.com','')

for r in conn.get_all_instances():
instances.extend(r.instances)

lookup = {}# used to put a friendlier face on the load balancer entries.

print "All Instances"
print "ID\tPrivate IP\tPublic IP\tInstance Type\tRole"
for item in instances:
pub_dns = cleanupDNS(item.public_dns_name)
role = item.tags.get("Role")
lookup[item.id] = pub_dns, role
print '%s\t%s\t%s\t%s\t%s' %
(item.id,cleanupDNS(item.private_dns_name),pub_dns
,item.instance_type,role)


regs = boto.ec2.elb.regions()

elb_conn = regs[1].connect( # specific to my region, your milage may vary.
aws_access_key_id = key,
aws_secret_access_key = sk)

health = elb_conn.describe_instance_health('ias')

print "Load Balancer"
for instance in health:
print '%s\t%s\t%s' %
(lookup[instance.instance_id][0],lookup[instance.instance_id][1],instance.state)
