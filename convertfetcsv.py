import xml.etree.ElementTree as ET
from collections import defaultdict
import csv

class convertfetcsv():

    def __init__(self):
        self.tdic = {}
        self.gdic = defaultdict(list)
        self.allgroups = []
        self.forbidden = []

    def read_FET(self,inputfile):
            '''
            gets the groups and teachers data from a fet teachers.xml file
            '''
            tree = ET.parse(inputfile)
            root = tree.getroot()
            teachers = root.findall(".//Teacher")
            for teacher in teachers:
                groups=[]
                name=teacher.attrib.get('name')
                #print(name)
                students = teacher.findall(".//Students")
                for group in students:
                    #print(group.attrib.get('name')[:3])
                    if group.attrib.get('name')[0] in self.forbidden:
                        #print("FFFF:",group.attrib.get('name')[:3])
                        continue
                    if group.attrib.get('name')[:3] not in groups:
                        groups.append(group.attrib.get('name')[:3])
                    if group.attrib.get('name')[:3] not in self.allgroups:
                        self.allgroups.append(group.attrib.get('name')[:3])
                    if name not in self.gdic[group.attrib.get('name')[:3]]:
                        self.gdic[group.attrib.get('name')[:3]].append(name)
                self.tdic[name] = groups
                
                
    def write_CSV(self,outputfile):
        with open(outputfile, 'w') as f:
            writer = csv.writer(f)
            groups = [self.gdic[key] for key in self.gdic.keys()]
            writer.writerow(groups)
            print("csv file written in: ", outputfile)


                
if __name__ == "__main__":
    cfc = convertfetcsv()                
    inputfile = "/home/asier/Hezkuntza/python-hezkuntza/python-fet/EDUCA/teachers.xml"
    cfc.read_FET(inputfile)
    outputfile = inputfile[:-3]  + "csv"
    cfc.write_CSV(outputfile)
