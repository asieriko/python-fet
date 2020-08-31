#!/usr/bin/python
import sys, getopt,os
import json,csv

from collections import defaultdict

teachersgroups = "/media/asier/Erregeton/python-horarios/grupos-profesores.csv"

groupses = defaultdict(dict)
groupseu = defaultdict(dict)
with open(teachersgroups,newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    next(spamreader)
    for row in spamreader:
        groupses[row[0]][row[1]]=row[3]
        groupseu[row[0]][row[2]]=row[3]

with open('teachergroups-es.json', 'w') as json_file:
  json.dump(groupses, json_file)
  
with open('teachergroups-eu.json', 'w') as json_file:
  json.dump(groupseu, json_file)
