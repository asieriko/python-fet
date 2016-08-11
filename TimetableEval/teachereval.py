#!/usr/bin/python
import xml.etree.ElementTree as ET
import csv


def evaluate(inputfile):
  tree = ET.parse(inputfile)
  root = tree.getroot()
  teachers = root.findall(".//Teacher")
  tdic={}
  sumdic={}
  for teacher in teachers:
    totalpre=0
    totalpost=0
    total1and6=0
    total1and7=0
    totalgaps=0
    name=teacher.attrib.get('name')
    days = teacher.findall(".//Day")
    for day in days:
      hours=day.findall(".//Hour")
      prefirst=-1#1. hutsunea?
      activities=0
      lastactivity=6
      first=False
      last6=False
      last7=False
      atsedenaldi=0
      gaps=0
      for i in range(len(hours)):
        subject=hours[i].findall(".//Subject")
        if subject == [] and i-1 == prefirst: prefirst=i
        if subject == [] and i==3 and prefirst == 2: atsedenaldi = -1
        if subject == [] and i-1 != prefirst: gaps += 1
        if subject != []: activities += 1
        if subject != []: lastactivity = i
        if subject != [] and i==0: first=True
        if subject != [] and i==6: last6=True
        if subject != [] and i==7:
          last7=True
          last6=False
      if prefirst<6:
        totalpre += prefirst+1+atsedenaldi #+1 hasten delako 0n, eta <6, bestela esan nahi duelako egun osoa 7 orduak libre dituela, bestela atsedenaldia hutsune bezala hartzen du
        if lastactivity>3 and prefirst<3:
          totalgaps += lastactivity - activities - prefirst - 1
        else:
          totalgaps += lastactivity - activities - prefirst
      #if prefirst<6: totalgaps = gaps - (6-lastactivity)
      if lastactivity<6: totalpost += 6-lastactivity
      if lastactivity<=3:totalpost -= 1 #atsedenaldia hutsune bezlaa ez hartzeko
      if first and last6: total1and6 += 1
      if first and last7: total1and7 += 1
    tdic[name.encode('utf-8')]=(name.encode('utf-8'),totalpre,totalpost,totalgaps,total1and6,total1and7,total1and6+total1and7)
    if total1and6+total1and7 in sumdic.keys():
      sumdic[total1and6+total1and7] += 1
    else:
      sumdic[total1and6+total1and7] = 1

  return tdic, sumdic

def write(tdic,sumdic,outputfile):
  with open(outputfile, 'w') as f:
    writer = csv.writer(f)
    header=('irakaslea','goizeko hutsuenak','eguerdiko hutsuneak','erdiko hutsuneak','1 eta 6','1 eta 7','1 eta azkena')
    writer.writerow(', '.join(header))
    writer.writerows(tdic[key] for key in tdic.keys())
    header=sumdic.keys()
    print(sumdic)
    writer.writerow(('Resumen: Numero de personas con x dias completos',''))
    writer.writerow(', '.join(str(h) for h in header))
    writer.writerow(list(str(sumdic[key]) for key in sumdic.keys()))
    print("Resumen archivo:  (Escrito en "+ outputfile+")")

