#!/usr/bin/python
import xml.etree.ElementTree as ET
import sys, getopt
import csv
import random
from collections import defaultdict


class evaluation():
    
    def init(self):
        pass
    
    def extractinfo(self,inputfile,forbiden):
        if inputfile[-4:] == ".csv":
            return self.extractinfoCSV(inputfile,forbiden)
        elif inputfile[-4:] == ".xml":
            return self.extractinfoXML(inputfile,forbiden)
        else:
            raise ValueError("File format is not .xml or .csv")
        

    def extractinfoXML(self,inputfile,forbiden):
        '''
        XML must be a FET's teachers.xml file
        <?xml version="1.0" encoding="UTF-8"?>
        <Teachers_Timetable>
            <Teacher name="Teacher1">
                <Day name="Astelehena">
                    <Hour name="08:30-9:25">
                        <Subject name="Euskara"></Subject><Students name="1-H"></Students><Room name="1H"></Room>
                    </Hour>
                    ...
                </Day>
                ...
            </Teacher>
            ...
        <Teachers_Timetable>
        only Teacher element and its attribute name are needed

        '''
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
                    #print("FFFF:",group.attrib.get('name')[:3])
                    continue
                if group.attrib.get('name')[:3] not in groups:
                    groups.append(group.attrib.get('name')[:3])
                if group.attrib.get('name')[:3] not in allgroups:
                    allgroups.append(group.attrib.get('name')[:3])
                if name not in gdic[group.attrib.get('name')[:3]]:
                    gdic[group.attrib.get('name')[:3]].append(name)
            tdic[name] = groups
        #print(tdic)
        #print(allgroups)
        print(gdic)
        return allgroups,gdic,tdic


    def extractinfoCSV(self,inputfile,forbiden,headers=False):
        '''
        CSV file must be a row for each group and a column for each teacher in the group
        1A;Teacher1;Teacher2;Teacher3
        1B;Teacher4;Teacher2;Teacher5
        '''
        tdic={}
        gdic= defaultdict(list)
        allgroups=[]
        with open(inputfile,'r') as results:
                reader = csv.reader(results,delimiter=",")
                if headers:
                    next(reader,None)
                for row in reader:
                    group = row[0]
                    if group in forbiden:
                        continue
                    allgroups.append(group)
                    for teacher in row[1:]:
                        if teacher != '':
                            gdic[group].append(teacher)
                            if teacher in tdic.keys():
                                tdic[teacher].append(group)
                            else:
                                tdic[teacher] = [group]
        print(allgroups,gdic,tdic)
        return allgroups,gdic,tdic
            
    def writeCSV(self,gdic):
        with open('eggs.csv', 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for group in gdic.keys():
                    teachers = list([group]) + gdic[group]
                    spamwriter.writerow(teachers)
     

    def mix(self,allgroups,simultaneous=4):
        '''
        creates the necesary partitions randomly with the simultaneous +/- 1 groups each
        FIXME Not sure if it works as it should
        '''
        l = len(allgroups)
        m = l%simultaneous
        d = l//simultaneous
        
        if m >= d:
            return self.mix2(allgroups,d+1)
        
        ##print("L =",len(groups),l,m,d)
        #result = []
        #i = 0
        #j = i + simultaneous
        #for p in range(d):
            ##print(i,j,p)
            #if p == d - 1:
                ##print("here")
                #j = len(allgroups)
            #result.append(sorted(groups[i:j]))
            #i = j
            #j = i + simultaneous
        ##print(result)
        #return result


    def mix2OLD(self,allgroups,sessions=12):
        '''
        creates sessions partitions randomly with the same +/- 1 groups each
        '''
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
                j = len(allgroups)
            result.append(sorted(groups[i:j]))
            i = j
            j = i + numbergroups
        #print(result,conf)
        return result

    def mix2(self,allgroups,sessions=12):
        '''
        creates sessions partitions randomly with the same +/- 1 groups each
        Manuel Zubieta: http://stackoverflow.com/a/14861842/1246747
        '''
        q, r = divmod(len(allgroups), sessions)
        indices = [q*i + min(i, r) for i in range(sessions+1)] 
        return [allgroups[indices[i]:indices[i+1]] for i in range(sessions)]


    def evaluatePartition(self,partition,gdic):
        '''
        input a set of groups and the list with each group's teachers
        [['1A','1B'],['2A','2B'],['3A','3B']]
        {'1A':["Teacher1","Teacher2"],'1B':["Teacher1","Teacher4"],'2A':["Teacher3","Teacher2"],'2B':["Teacher1","Teacher3"]},'3A':["Teacher1","Teacher2"],'3B':["Teacher1","Teacher4"]}
        ouput how many teachers repeat group for all partitions
        3
        '''
        conf = 0
        for group in partition:
            conf += self.evaluate(group,gdic)
        return conf

    def evaluate(self,groups,gdic):
        '''
        input a set of groups and the list with each group's teachers
        ['1A','1B']
        {'1A':["Teacher1","Teacher2"],'1B':["Teacher1","Teacher4"]}
        ouput how many teachers repeat group
        1
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
        

    def evaluateDay(self,groupspartition, gdic, teachers):
        '''
        input a set of groups organization and the list with each group's teachers
        [[['1A','1B'],['2A','2B']],[['3A','3B'],['4A','4B']]]
        {'1A':["Teacher1","Teacher2"],'1B':["Teacher1","Teacher4"],'2A':["Teacher1","Teacher2"],'2B':["Teacher1","Teacher4"],
        '3A':["Teacher5","Teacher2"],'3B':["Teacher4","Teacher4"],'4A':["Teacher6","Teacher2"],'4B':["Teacher5","Teacher4"]}
        ouput how many teachers repeat day
        2
        '''
        t = []
        conf = 0
        for p in groupspartition:
            tp = []
            groups = [item for sublist in p for item in sublist]
            for g in groups:
                for teacher in gdic[g]:
                    if teacher not in tp:
                        tp.append(teacher)
            #print(tp)
            t.append(tp)
        #print(t)
        for teacher in teachers.keys():
            tr = 0
            for i in range(len(t)):
                if teacher in t[i]:
                    tr += 1
            conf += tr
            #print(tr)
        #print(t)
        return conf
                


    def calculate(self,tfile="teachers.xml",forbiden=[],n=5000):
        '''
        iteratively searches the best groups/session organization in 
        order to maximize teachers presence and minimize teachers comming
        days
        '''
        a,g,t = self.extractinfo(tfile,forbiden)
        c = 999999999999
        c0 = c
        r = []
        p = []
        for i in range(n): #Select the best partition to maximize teachers comming
            partition = self.mix2(a,12) 
            c1 = self.evaluatePartition(partition,g)
            if c1 < c:
                r = partition
                c = c1
        for i in range(n): #select the best daily organization based on the previous to minimize teachers comming days
            partition = self.mix2(r,3) #3 days...
            c2 = self.evaluateDay(partition,g,t)
            if c2 < c0:
                p = partition
                c0 = c2
        return partition,c, c0
    
    
    def write(self,partition,conf,tdays):
        for d in partition:
            for g in d:
                print(g)
            print("----------")
        print("Conflicts: ",conf)
        print("Teacher-days: ",tdays)
        

    #self.calculate(forbiden=["M","B","6"])


    
def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print('teacher-eval.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('teacher-eval.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   eva = evaluation()
   eva.calculate(inputfile,['M','b','6'])

if __name__ == "__main__":
   main(sys.argv[1:])


 
