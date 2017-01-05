import grp,pwd,os
from os.path import expanduser
import os
#Creates the file with the user detail in the current directory
destdir = '/home/ttnd'
destfile = 'newfile.txt'
appname = 'app name'
groupid = ''
userid = ''

#delete old feed file and create file
if os.path.exists(destfile):
        os.remove(destfile)
        print "file deleted...creating new file"
        output = open(destfile, 'w+')
        output.write('USER|GROUP' + '\n')
else:
        print "no file to delete...creating file"
        output = open(destfile, 'w+')
        output.write('USER|GROUP' + '\n')


#get user/group data for all users non primary groups
#documentation: https://docs.python.org/2/library/grp.html
groups = grp.getgrall()
for group in groups:
    groupid = group[2]
    for user in group[3]:
     #userid=os.system('id -u %s' user);
     cmd = "id -u %s"%(user);
     userid=os.system(cmd);
     output.write(user + '|'   + group[0] + '\n')
