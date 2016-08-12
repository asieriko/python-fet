#!/usr/bin/python
import xml.etree.ElementTree as ET
import sys, getopt
import csv
from collections import defaultdict


def evaluate(inputfile,outputfile):
  tree = ET.parse(inputfile)
  root = tree.getroot()
  teachers = root.findall(".//Teacher")
  tdic={}
  gdic= defaultdict(list)
  allgroups=[]
  for teacher in teachers:
    groups=[]
    name=teacher.attrib.get('name')
    print(name)
    students = teacher.findall(".//Students")
    for group in students:
        print(group.attrib.get('name')[:3])
        if group.attrib.get('name')[:3] not in groups:
            groups.append(group.attrib.get('name')[:3])
        if group.attrib.get('name')[:3] not in allgroups:
            allgroups.append(group.attrib.get('name')[:3])
        if name not in gdic[group.attrib.get('name')[:3]]:
            gdic[group.attrib.get('name')[:3]].append(name)
    tdic[name] = groups
  print(tdic)
  print(allgroups)
  print(gdic)
        
        

        
evaluate("teachers.xml","")

    tdic[name.encode('utf-8')]=(name.encode('utf-8'),totalpre,totalpost,totalgaps,total1and6,total1and7,total1and6+total1and7)
    if total1and6+total1and7 in sumdic.keys():
      sumdic[total1and6+total1and7] += 1
    else:
      sumdic[total1and6+total1and7] = 1

  
  with open(outputfile, 'wb') as f:

    writer = csv.writer(f)
    header=('irakaslea','goizeko hutsuenak','eguerdiko hutsuneak','erdiko hutsuneak','1 eta 6','1 eta 7','1 eta azkena')
    writer.writerow(header)
    writer.writerows(tdic[key] for key in tdic.keys())
    header=sumdic.keys()
    print "Resumen archivo: " + inputfile + "  (Escrito en "+ outputfile+")"
    print sumdic
    writer.writerow(('Resumen: Numero de personas con x dias completos',''))
    writer.writerow(header)
    writer.writerow(list(sumdic[key] for key in sumdic.keys()))

  #print "irakaslea,goizeko hutsuenak,eguerdiko hutsuneak,1 eta 6,1 eta 7."
  #for key in tdic.keys():
    #(goiz,eguerdi,firstand6last,firstandlast)=tdic[key]
    #print key,',',goiz,',',eguerdi,',',firstand6last,',',firstandlast



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
   evaluate(inputfile,outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])


 
