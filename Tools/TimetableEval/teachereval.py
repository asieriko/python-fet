#!/usr/bin/python
import xml.etree.ElementTree as ET
from collections import defaultdict, OrderedDict
import csv


def evaluate(inputfile):
  '''
  This function recives an teacher.xml file from fet and evaluates each teacher's timetable
  
  output
  tdic: A dictionary with every teacher and the following results: Same of sumtotal for each teacher
  sumdicNew: A dictionary with how many teachers have full days (NO:how many 0 full, 1 full,...) and days starting at first until 7th
  sumtotal: A list with the following data (sum for all teachers):
    totalgapsmorning
    totalgapsevening
    totalgapsweek
    totalgapsweek - weekdays + playtimeguard
    totalhoursweek
    totalhoursweek - weekdays
    totalhoursweek - weekdays + playtimeguard
    totalfulldays
    total17days
  '''
  tree = ET.parse(inputfile)
  root = tree.getroot()
  teachers = root.findall(".//Teacher")
  tdic={}
  sumtotal  = [0,0,0,0,0,0,0,0]
  sumdicNew = defaultdict(int)
  for teacher in teachers:
    weekdays = 5
    playtimeguard = 0
    totalgapsweek = 0
    totalgapsmorning = 0
    totalgapsevening = 0
    totalhoursweek = 0
    totalfulldays = 0
    total17days = 0
    name=teacher.attrib.get('name')
    days = teacher.findall(".//Day")
    for day in days:
      hours=day.findall(".//Hour")
      lasthour = 0
      firsthour = 10
      hoursday = 0
      activitiesday = 0
      gapsday = 0
      for i in range(len(hours)):
        subject=hours[i].findall(".//Subject")
        if subject != []: 
            lasthour = i
            activitiesday += 1
            if i == 3:
                playtimeguard += 1
        if subject != [] and i < firsthour: 
            firsthour = i
      if firsthour == 10: 
          firsthour = 0 #I've to find what is the first hour, but if a teacher doesn't have any clasess in a day it takes firsthour as 10
          weekdays -= 1
      hoursday = lasthour - firsthour + 1
      gapsday = hoursday - activitiesday
      if hoursday >= 7:
        totalfulldays += 1
      if firsthour == 0 and lasthour == 7:
        total17days += 1
      totalgapsweek += gapsday
      totalhoursweek += hoursday
      totalgapsmorning += firsthour
      totalgapsevening += max(6-lasthour,0) #FIXME: Having the last hour only some teachers, and being like an extaordinary hour, it can also be negative...
    tdic[name]=(name,totalgapsmorning,totalgapsevening,totalgapsweek,totalgapsweek - weekdays + playtimeguard,totalhoursweek,totalhoursweek - weekdays, totalhoursweek - weekdays + playtimeguard,totalfulldays,total17days)
    sumtotal = [sum(x) for x in zip(sumtotal, [totalgapsmorning,totalgapsevening,totalgapsweek,totalgapsweek - weekdays + playtimeguard,totalhoursweek,totalhoursweek - weekdays, totalhoursweek - weekdays + playtimeguard,totalfulldays,total17days])]
    sumdicNew[totalfulldays] += 1
    sumdicNew["1-7"] += total17days

  return OrderedDict(sorted(tdic.items())), sumdicNew, sumtotal

def write(tdic,sumdic,sumtotal, outputfile):
  with open(outputfile, 'w') as f:
    writer = csv.writer(f)
    header=(['irakaslea','goizeko hutsuenak','eguerdiko hutsuneak','erdiko hutsuneak','erdiko hutsuneak atsedenaldia kanpo','Asteko orduak atsedenaldia barne', 'Asteko orduak atsedenaldia kanpo', 'Asteko orduak atsedenaldia kanpo - zaintzak barne','Egun oso kopurua','1-7 kopurua'])
    writer.writerow(header)
    writer.writerows(tdic[key] for key in tdic.keys())
    sumtotal = [['Total:']+ [str(x) for x in sumtotal]]
    print(sumtotal)
    writer.writerows(sumtotal)
    print(sumdic)
    writer.writerow((['Resumen: Numero de personas con x dias completos']))
    writer.writerow(sumdic.keys())
    writer.writerow(list(str(sumdic[key]) for key in sumdic.keys()))
    print("Resumen archivo:  (Escrito en "+ outputfile+")")

