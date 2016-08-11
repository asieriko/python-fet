import csv
import codecs
import xml.dom.minidom
import xml.etree.ElementTree 
from xml.etree import ElementTree as ET


class zaintzak:
   
   def __init__(self):      
      self.teacher = None
      self.zaintzakop = None
      self.building = None
   
            
   def printm(self,elem):
      print self.prettify(elem)

   def prettify(self,elem):
      """Return a pretty-printed XML string for the Element.
      """
      rough_string = ET.tostring(elem, 'utf-8')
      reparsed = xml.dom.minidom.parseString(rough_string)
      return reparsed.toprettyxml(indent="\t")
   
   
   def read_csv_data(self,csvfile,separator=','):
      s = [line.rstrip().split(separator) for line in open(csvfile,'r')]
      
      self.teacher = s[0].index("irakaslea")
      self.zaintzakop = s[0].index("zaintzak")
      self.building = s[0].index("eraikina")
      self.maxactivity = 1680
      
      self.raw_data = s[1:]
      tree = ET.Element("all")
      zaintzak = ET.SubElement(tree,"zaintzak")
      zaintzagelak = ET.SubElement(tree,"zaintzagelak")
      for zaintza in s[1:]:
         for i in range(int(zaintza[self.zaintzakop])):
            ActivityElement = ET.SubElement(zaintzak,'Activity')
            TeacherElement = ET.SubElement(ActivityElement,'Teacher')
            TeacherElement.text = zaintza[self.teacher].decode('utf-8')
            ZaintzaElement = ET.SubElement(ActivityElement,'Subject')
            ZaintzaElement.text = "Zaintza"
            DurationElement = ET.SubElement(ActivityElement,'Duration')
            DurationElement.text = "1"
            TDurationElement = ET.SubElement(ActivityElement,'Total_Duration')
            TDurationElement.text = "1"
            IdElement = ET.SubElement(ActivityElement,'Id')
            IdElement.text = str(self.maxactivity)
            AGroupElement = ET.SubElement(ActivityElement,'Activity_Group_Id')
            AGroupElement.text = "0"
            ActiveElement = ET.SubElement(ActivityElement,'Active')
            ActiveElement.text = "true"
            CommentsElement = ET.SubElement(ActivityElement,'Comments')
            
            RoomConstraintElement = ET.SubElement(zaintzagelak,'ConstraintActivityPreferredRooms')
            WPerElement = ET.SubElement(RoomConstraintElement,'Weight_Percentage')
            WPerElement.text = "100"
            ActIdElement = ET.SubElement(RoomConstraintElement,'Activity_Id')
            ActIdElement.text = str(self.maxactivity)
            NPerElement = ET.SubElement(RoomConstraintElement,'Number_of_Preferred_Rooms')
            ActiveRElement = ET.SubElement(RoomConstraintElement,'Active')
            ActiveRElement.text = "true"
            ComRElement = ET.SubElement(RoomConstraintElement,'Comments')
            if zaintza[self.building] == '1':               
               NPerElement.text = "5"
               for i in range(5):
                  PRElement = ET.SubElement(RoomConstraintElement,'Preferred_Room')
                  PRElement.text = "Z"+str(i+1)+"-1"
            elif zaintza[self.building] == '2':
               NPerElement.text = "5"
               for i in range(5):
                  PRElement = ET.SubElement(RoomConstraintElement,'Preferred_Room')
                  PRElement.text = "Z"+str(i+1)+"-2"
            elif zaintza[self.building] == '12':
               NPerElement.text = "10"
               for i in range(5):
                  PRElement = ET.SubElement(RoomConstraintElement,'Preferred_Room')
                  PRElement.text = "Z"+str(i+1)+"-1"
               for i in range(5):
                  PRElement = ET.SubElement(RoomConstraintElement,'Preferred_Room')
                  PRElement.text = "Z"+str(i+1)+"-2"
            self.maxactivity = self.maxactivity+1
      f=codecs.open('outputfile.xml','w','utf-8')
      f.write(self.prettify(tree))
      f.close()
      self.printm(tree)      
      
z = zaintzak()
z.read_csv_data("/home/asier/Hezkuntza/SGCC-Erregistroak-16-17/PR01 Matriculacion y planificacion docente y servicios complementarios/PR0102 Planificacion/Horarios/zaintzak1617.csv")