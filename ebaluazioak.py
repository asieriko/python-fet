#!/usr/bin/python
import xml.etree.ElementTree as ET
import sys, getopt
import csv
import random
from collections import defaultdict


def extractinfo(inputfile,forbiden):
  tree = ET.parse(inputfile)
  root = tree.getroot()
  teachers = root.findall(".//Teacher")
  tdic={}
  gdic= defaultdict(list)
  allgroups=[]
  for teacher in teachers:
    groups=[]
    name=teacher.attrib.get('name')
    #print(name)
    students = teacher.findall(".//Students")
    for group in students:
        #print(group.attrib.get('name')[:3])
        if group.attrib.get('name')[0] in forbiden:
            break
        if group.attrib.get('name')[:3] not in groups:
            groups.append(group.attrib.get('name')[:3])
        if group.attrib.get('name')[:3] not in allgroups:
            allgroups.append(group.attrib.get('name')[:3])
        if name not in gdic[group.attrib.get('name')[:3]]:
            gdic[group.attrib.get('name')[:3]].append(name)
    tdic[name] = groups
  #print(tdic)
  #print(allgroups)
  #print(gdic)
  return allgroups,gdic,tdic
        

def mix(allgroups,simultaneous=4):
    groups = []
    for gr in allgroups:
        if gr[0] != '6' and gr[0] != 'b':
            groups.append(gr)
    random.shuffle(groups)
    l = len(allgroups)
    m = l%simultaneous
    d = l//simultaneous
    #print("L =",len(groups))
    result = []
    i = 0
    j = i + simultaneous
    for p in range(d-1):
        if p == d - 1:
            j = len(a)
        result.append(groups[i:j])
        i = j
        j = i + simultaneous
    #print(result,conf)
    return result


def mix2(allgroups,sessions=16):
    groups = []
    for gr in allgroups:
        if gr[0] != '6' and gr[0] != 'b':
            groups.append(gr)
    random.shuffle(groups)
    l = len(allgroups)
    m = l%sessions
    d = l//sessions
    
    small = big = sessions
    
    if m != 0 and m < sessions:
        small = sessions - m
        big = m
    
    #print("L =",len(groups))
    result = []
    numbergroups = d
    i = 0
    j = i + numbergroups
    for p in range(sessions):
        if p > small-2:
            numbergroups = d + 1
        if p == sessions - 1:
            j = len(a)
        result.append(groups[i:j])
        i = j
        j = i + numbergroups
    #print(result,conf)
    return result


for n in range(1,19):
   print("----------",n,"-----------")
   for i in mix2(a,n):
     print(len(i)) 

def evaluatePartition(partition,gdic):
    conf = 0
    for group in partition:
        conf += evaluate(group,gdic)
    return conf

def evaluate(groups,gdic):
    '''
    input a set of groups and the list with each group's teachers
    ouput how many teachers repeat group
    '''
    t=[]
    conf = 0
    for g in groups:
        for teacher in gdic[g]:
            if teacher in t:
                conf += 1
            else:
                t.append(teacher)
    return conf
    
        

def calculate(tfile="teachers.xml",forbiden=[],n=5000):
    a,g,t = extractinfo(tfile,forbiden)
    c = 999999999999
    r = []
    for i in range(n):
        partition = mix(a)
        c1 = evaluatePartition(partition,g)
        if c1 < c:
            r = partition
            c = c1
    print(r,c)



def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'teacher-eval.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'teacher-eval.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   calculate(inputfile,['M','b','6'])

if __name__ == "__main__":
   main(sys.argv[1:])


 
