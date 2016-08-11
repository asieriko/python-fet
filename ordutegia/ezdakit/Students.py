import csv
import xml.etree.ElementTree 
from xml.etree import ElementTree as ET

#years=[[1, ['A', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']], ['B', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']], ['C', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']], ['D', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']]], [2, ['A', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']], ['B', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']], ['C', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']], ['D', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']]], [3, ['A', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']], ['B', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']], ['C', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']], ['D', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']]], [4, ['A', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']], ['B', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']], ['C', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']], ['D', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']]], [5, ['A', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']], ['B', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']], ['C', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']], ['D', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']]], [6, ['A', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']], ['B', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']], ['C', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']], ['D', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']]]]
def GenerateStudents(Years):
  Students = ET.Element("Students_List")
  for year in Years:
    Students.append(GenerateYear(year))
  
  print ET.dump(Students)
      
#Year=[1, ['A', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']], ['B', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']], ['C', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']], ['D', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']]]
def GenerateYear(Year):
  YearElement=ET.Element("Year")
  YName=ET.SubElement(YearElement,"Name")
  YName.text=str(Year[0])
  YNoS = ET.SubElement(YearElement,'Number_of_Students')
  YNoS.text = "0"
  for groups in Year[1:]:
    YearElement.append(GenerateGroups(Year[0],groups))
#  print ET.dump(YearElement)    
  return YearElement

#group=['A', ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']] 
def GenerateGroups(Year,Group):  
  GroupElement=ET.Element("Group")
  GName=ET.SubElement(GroupElement,"Name")
  GName.text=str(Year)+" "+Group[0]
  GNoS = ET.SubElement(GroupElement,'Number_of_Students')
  GNoS.text = "0"  
  if len(Group)>1:
     for option in Group[1]:
       GroupElement.append(GenerateSubGroups(Year,Group[0],option))
  
  return GroupElement

#1 A ['LS', 'OM', 'Fr', 'Al', 'Eus', 'HA', 'Erl', 'HRel']
#1-A-LS...
def GenerateSubGroups(Year,Group,Option):
  subgroup=ET.Element('Subgroup')
  sgname = ET.SubElement(subgroup,'Name')
  sgname.text =  str(Year)+"-"+Group+"-"+Option
  sgNoS = ET.SubElement(subgroup,'Number_of_Students')
  sgNoS.text = "0"
  return subgroup

def generateFromCSV(CSVfile):
   with open(CSVfile,'rb') as csvfile: 
       s=[]
       reader = csv.reader(csvfile,delimiter=',')
       for r in reader:
         if len(r)<3:
            v = [r[0],[r[1]]]
         else:
             v = [r[0],[r[1],r[2:]]] 
         for i in range(len(s)):
             if s[i][0] == v[0]:
	        s[i].insert(len(s[i]),v[1:][0])
                break
             else:
	        if i==len(s)-1:
                   s.append(v)
         if len(s)==0:
	    s.append(v)
   GenerateStudents(s)


generateFromCSV('taldea.csv')
