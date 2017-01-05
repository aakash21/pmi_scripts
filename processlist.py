#!/usr/bin/python

import psutil
import csv
found = 0
with open('whitelist.csv', 'rb') as f:
    reader = csv.reader(f)
    filter_list = list(reader)

#use the whitelist.csv to load the filters
processes = psutil.pids();
#prints the running processes on the local system.
for proc in processes:
    p=psutil.Process(proc)
    procName=p.name();



    for i in filter_list:
        for z in i:
            if   z in procName :
                found = 1

    if found == 0:
            procBin=p.exe();
            procStatus=p.status();
            procUser=p.username();
            print(procName+'|'+procBin+'|'+procStatus+'|'+procUser)

    found = 0
