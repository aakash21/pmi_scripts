from boto import ec2
import csv


with open('rules_in_instance.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Instance Id', 'Region', 'Total Rules','VPC/Classic'])
    writer.writerow(['Allowed Limit:'])
    writer.writerow(['An Amazon EC2-VPC instance can have up to 50 security group rule'])
    writer.writerow(['An Amazon EC2-Classic instance can have up to 100 security group rules'])

conn = ec2.connect_to_region('us-east-1')
regions = conn.get_all_regions()
for region in regions:
    conn = ec2.connect_to_region(region.name)
    groups = conn.get_all_security_groups()
    reservations = conn.get_all_instances()
    for group in groups:
        if group.vpc_id:
            for res in reservations:
                for instance in res.instances:
                    sum=0
                    group_nums = len(instance.groups)
                    for z in range(group_nums):
                        group_id = instance.groups[z].id
                        sec_rules = conn.get_all_security_groups(group_ids=group_id)[0].rules
                        sum = sum + len(sec_rules)
                    if sum >= 50:
                        with open('rules_in_instance.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow([instance, region.name,  sum,'VPC'])
        if not group.vpc_id:
            for res in reservations:
                for instance in res.instances:
                    sum=0
                    group_nums = len(instance.groups)
                    for z in range(group_nums):
                        group_id = instance.groups[z].id
                        sec_rules = conn.get_all_security_groups(group_ids=group_id)[0].rules
                        sum = sum + len(sec_rules)
                    if sum >= 100:
                        with open('rules_in_instance.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerow([instance, region.name,  sum,'Classic'])




