#!/usr/bin/env python
# Author - Vivek Ramachandran
#
# Website - http://securitytube.net
#
# Python for Hackers: http://securitytube-training.com/online-courses/securitytube-python-scripting-expert/
#
# License: Use as you please for non-commercial purposes.
#
 
 
from boto.s3.connection import S3Connection
import sys
 
new_connection = S3Connection(ACCESS_KEY, SECRET_KEY)
 
print "[+] Connecting to bucket %s " %sys.argv[1]
 
bucket = new_connection.get_bucket(sys.argv[1])
 
print "[+] Setting ACL : %s" %sys.argv[2]
 
bucket.set_acl(sys.argv[2])
 
print "[+] Fetching Permissons for %s " %sys.argv[1]
 
for grant in bucket.get_acl().acl.grants :
  print grant.permission, grant.display_name
 
