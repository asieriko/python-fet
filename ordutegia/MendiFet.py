import csv
import codecs
import xml.dom.minidom

from collections import defaultdict 
from xml.etree import ElementTree as ET

class MendiFet:

  

    # Lehenengo Sortu Jarduerak
    # Jarduerak eta Murrizketak .fet fitxategian idatzi
    # Fitxategi horretatik taldeak eskuratu eta egitura sortu create_groups_XML
    # Taldeen egitura hori idatzi .fet fitxategian

    # Gelak bilatzen ditu, baina eraikinak falta dira. Garrantzitsua da gero murrizketak ezartzeko.

    # Berezitasunak: LAguntza duten ikasgaiak Tekno, plastika eta musika.
    # 2. Batx tutore-Historia
    # Koldo eta Merche informatika aldi berean bada ez bada ere.    
    def __init__(self):
        self.fetxml = ET.fromstring("""    <fet version="5.18.0">
            <Institution_Name></Institution_Name>
            <Comments></Comments>
            <Hours_List></Hours_List>
            <Days_List></Days_List>
            <Students_List></Students_List>
            <Teachers_List></Teachers_List>
            <Subjects_List></Subjects_List>
            <Activity_Tags_List></Activity_Tags_List>
            <Activities_List></Activities_List>
            <Buildings_List></Buildings_List>
            <Rooms_List></Rooms_List>
            <Time_Constraints_List>
                    <ConstraintBasicCompulsoryTime>
                    <Weight_Percentage>100</Weight_Percentage>
                    <Active>true</Active>
                    <Comments></Comments>
                </ConstraintBasicCompulsoryTime>
            </Time_Constraints_List>
            <Space_Constraints_List>
                <ConstraintBasicCompulsorySpace>
                    <Weight_Percentage>100</Weight_Percentage>
                    <Active>true</Active>
                    <Comments></Comments>
                </ConstraintBasicCompulsorySpace>
            </Space_Constraints_List>
    </fet>""")
        self.raw_data = []
        
        self.contype = None
        self.con = None
        self.teacher = None
        self.subject = None
        self.group = None
        self.totalduration = None
        self.room = None
        self.year = None
        self.building = None
        
        self.teachers = set()
        self.rooms = set()
        self.subjects = set()
        self.buildings = set()
        
        self.roombuilding = {}
        
        #FIXME: the function can check if the subjects ends with a number to avoid duplicates...
        self.incompatibilities = {"5":{"IKT 2":["IKT 1"],"IKT 1":["IKT 2"],
                                  "Fisika Kimika 1":["Fisika Kimika 2", "Historia 1", "Historia 2","Latina","Ekonomia 1", "Ekonomia 2","Matematika GGZZ I 1", "Matematika GGZZ I 2","Marrazketa Artistikoa"],
                                  "Fisika Kimika 2":["Fisika Kimika 1", "Historia 1", "Historia 2","Latina","Ekonomia 1", "Ekonomia 2","Matematika GGZZ I 1", "Matematika GGZZ I 2","Marrazketa Artistikoa"],
                                  "Bio Geo":["Tek Ind","Marrazketa Teknikoa","Historia 1", "Historia 2","Latina","Ekonomia 1", "Ekonomia 2","Matematika GGZZ I 1", "Matematika GGZZ I 2","Marrazketa Artistikoa"],
                                  "Tek Ind":["Anatomia Ap.","Bio Geo","Historia 1", "Historia 2","Latina","Ekonomia 1", "Ekonomia 2","Matematika GGZZ I 1", "Matematika GGZZ I 2","Marrazketa Artistikoa"],
                                  "Anatomia Ap.":["Tek Ind","Historia 1", "Historia 2","Latina","Ekonomia 1", "Ekonomia 2","Matematika GGZZ I 1", "Matematika GGZZ I 2","Marrazketa Artistikoa"],
                                  "Marrazketa Teknikoa":["Historia 1", "Historia 2","Bio Geo","Latina","Ekonomia 1", "Ekonomia 2","Matematika GGZZ I 1", "Matematika GGZZ I 2","Marrazketa Artistikoa"],
                                  "Matematika 1": ["Matematika 2", "Historia 1", "Historia 2","Latina","Ekonomia 1", "Ekonomia 2","Matematika GGZZ I 1", "Matematika GGZZ I 2","Marrazketa Artistikoa"],
                                  "Matematika 2": ["Matematika 1","Historia 1", "Historia 2","Latina","Ekonomia 1", "Ekonomia 2","Matematika GGZZ I 1", "Matematika GGZZ I 2","Marrazketa Artistikoa"],
                             "Historia 1":["Historia 2", "Fisika Kimika 1","Fisika Kimika 2","Matematika 1", "Matematika 2","Tek Ind", "Bio Geo", "Anatomia Ap.","Marrazketa Teknikoa"],
                             "Historia 2":["Historia 1", "Fisika Kimika 1","Fisika Kimika 2","Matematika 1", "Matematika 2","Tek Ind", "Bio Geo", "Anatomia Ap.","Marrazketa Teknikoa"],
                             "Latina":["Ekonomia 1", "Ekonomia 2","Fisika Kimika 1","Fisika Kimika 2","Matematika 1", "Matematika 2","Tek Ind", "Bio Geo", "Anatomia Ap.","Marrazketa Teknikoa"],
                             "Matematika GGZZ I 1":["Matematika GGZZ I 2", "Fisika Kimika 1","Fisika Kimika 2","Matematika 1", "Matematika 2","Tek Ind", "Bio Geo", "Anatomia Ap.","Marrazketa Teknikoa"],
                             "Matematika GGZZ I 2":["Matematika GGZZ I 1", "Fisika Kimika 1","Fisika Kimika 2","Matematika 1", "Matematika 2","Tek Ind", "Bio Geo", "Anatomia Ap.","Marrazketa Teknikoa"],
                             "Ekonomia 1":["Ekonomia 2", "Latina","Fisika Kimika 1","Fisika Kimika 2","Matematika 1", "Matematika 2","Tek Ind", "Bio Geo", "Anatomia Ap.","Marrazketa Teknikoa"],
                             "Ekonomia 2":["Ekonomia 1", "Latina","Fisika Kimika 1","Fisika Kimika 2","Matematika 1", "Matematika 2","Tek Ind", "Bio Geo", "Anatomia Ap.","Marrazketa Teknikoa"],
                             "Marrazketa Artistikoa":["Fisika Kimika 1","Fisika Kimika 2","Matematika 1", "Matematika 2","Tek Ind", "Bio Geo", "Anatomia Ap.","Marrazketa Teknikoa"]}}
        
        self.names = {"guard": "Zaintza","option":"h","meeting":"bilera","help":"laguntza","indep":"independiente","con_type":"Mota","conexion":"Konexion",
                      "teacher_name":"Izena","subject":"Ikasgaia","group":"Taldea","total_duration":"Orduak","room":"Gela","year":"Maila","building":"Eraikina"}
        
    def set_hours(self, hours):
        HoursElement = self.fetxml.find('./Hours_List')
        NumberElement = ET.SubElement(HoursElement, 'Number')
        NumberElement.text = str(len(hours))
        for hour in hours:
            HourElement = ET.SubElement(HoursElement, 'Name')
            HourElement.text = hour

    def set_days(self, days):
        DaysElement = self.fetxml.find('./Days_List')
        NumberElement = ET.SubElement(DaysElement, 'Number')
        NumberElement.text = str(len(days))
        for day in days:
            DayElement = ET.SubElement(DaysElement, 'Name')
            DayElement.text = day

    def set_name(self, name):
        NameElement = self.fetxml.find('./Institution_Name')
        NameElement.text = name
    
    def set_comments(self, name):
        CommentsElement = self.fetxml.find('./Comments')
        CommentsElement.text = name
        
    def no_class_hours_mendillorri(self):
        # FIXME
        dena = """          <ConstraintStudentsSetNotAvailableTimes>
                     <Weight_Percentage>100</Weight_Percentage>
                     <Students>bilera</Students>
                     <Number_of_Not_Available_Times>6</Number_of_Not_Available_Times>
                     <Not_Available_Time>
                                <Day>Astelehena</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteartea</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteazkena</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Osteguna</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Ostirala</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Astelehena</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteartea</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteazkena</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Osteguna</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Ostirala</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Active>true</Active>
                     <Comments/>
          </ConstraintStudentsSetNotAvailableTimes>
        <ConstraintStudentsSetNotAvailableTimes>
                     <Weight_Percentage>100</Weight_Percentage>
                     <Students>5-I</Students>
                     <Number_of_Not_Available_Times>6</Number_of_Not_Available_Times>
                     <Not_Available_Time>
                                <Day>Astelehena</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteartea</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteazkena</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Osteguna</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Ostirala</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Ostirala</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Active>true</Active>
                     <Comments/>
          </ConstraintStudentsSetNotAvailableTimes>
          <ConstraintStudentsSetNotAvailableTimes>
                     <Weight_Percentage>100</Weight_Percentage>
                     <Students>5-H</Students>
                     <Number_of_Not_Available_Times>6</Number_of_Not_Available_Times>
                     <Not_Available_Time>
                                <Day>Astelehena</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteartea</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteazkena</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Osteguna</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Ostirala</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Ostirala</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Active>true</Active>
                     <Comments/>
          </ConstraintStudentsSetNotAvailableTimes>
          <ConstraintStudentsSetNotAvailableTimes>
                     <Weight_Percentage>100</Weight_Percentage>
                     <Students>5-J</Students>
                     <Number_of_Not_Available_Times>6</Number_of_Not_Available_Times>
                     <Not_Available_Time>
                                <Day>Astelehena</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteartea</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteazkena</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Osteguna</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Ostirala</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Ostirala</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Active>true</Active>
                     <Comments/>
          </ConstraintStudentsSetNotAvailableTimes>
          <ConstraintStudentsSetNotAvailableTimes>
                     <Weight_Percentage>100</Weight_Percentage>
                     <Students>6-I</Students>
                     <Number_of_Not_Available_Times>6</Number_of_Not_Available_Times>
                     <Not_Available_Time>
                                <Day>Astelehena</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteartea</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteazkena</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Osteguna</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Ostirala</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Ostirala</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Active>true</Active>
                     <Comments/>
          </ConstraintStudentsSetNotAvailableTimes>
          <ConstraintStudentsSetNotAvailableTimes>
                     <Weight_Percentage>100</Weight_Percentage>
                     <Students>6-H</Students>
                     <Number_of_Not_Available_Times>6</Number_of_Not_Available_Times>
                     <Not_Available_Time>
                                <Day>Astelehena</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteartea</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteazkena</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Osteguna</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Ostirala</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Ostirala</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Active>true</Active>
                     <Comments/>
          </ConstraintStudentsSetNotAvailableTimes>
          <ConstraintStudentsSetNotAvailableTimes>
                     <Weight_Percentage>100</Weight_Percentage>
                     <Students>6-A</Students>
                     <Number_of_Not_Available_Times>6</Number_of_Not_Available_Times>
                     <Not_Available_Time>
                                <Day>Astelehena</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteartea</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteazkena</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Osteguna</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Ostirala</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Astelehena</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteartea</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteazkena</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Osteguna</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Ostirala</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Active>true</Active>
                     <Comments/>
          </ConstraintStudentsSetNotAvailableTimes>
          <ConstraintStudentsSetNotAvailableTimes>
                     <Weight_Percentage>100</Weight_Percentage>
                     <Students>6-B</Students>
                     <Number_of_Not_Available_Times>6</Number_of_Not_Available_Times>
                     <Not_Available_Time>
                                <Day>Astelehena</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteartea</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteazkena</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Osteguna</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Ostirala</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Astelehena</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteartea</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteazkena</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Osteguna</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Ostirala</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Active>true</Active>
                     <Comments/>
          </ConstraintStudentsSetNotAvailableTimes>
                     <ConstraintStudentsSetNotAvailableTimes>
                     <Weight_Percentage>100</Weight_Percentage>
                     <Students>6-C</Students>
                     <Number_of_Not_Available_Times>6</Number_of_Not_Available_Times>
                     <Not_Available_Time>
                                <Day>Astelehena</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteartea</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteazkena</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Osteguna</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Ostirala</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Astelehena</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteartea</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteazkena</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Osteguna</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Ostirala</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Active>true</Active>
                     <Comments/>
          </ConstraintStudentsSetNotAvailableTimes>
          <ConstraintStudentsSetNotAvailableTimes>
                     <Weight_Percentage>100</Weight_Percentage>
                     <Students>1</Students>
                     <Number_of_Not_Available_Times>6</Number_of_Not_Available_Times>
                     <Not_Available_Time>
                                <Day>Astelehena</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteartea</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteazkena</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Osteguna</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Ostirala</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Astelehena</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteartea</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteazkena</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Osteguna</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Ostirala</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Active>true</Active>
                     <Comments/>
          </ConstraintStudentsSetNotAvailableTimes>
          <ConstraintStudentsSetNotAvailableTimes>
                     <Weight_Percentage>100</Weight_Percentage>
                     <Students>2</Students>
                     <Number_of_Not_Available_Times>6</Number_of_Not_Available_Times>
                     <Not_Available_Time>
                                <Day>Astelehena</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteartea</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteazkena</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Osteguna</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Ostirala</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Astelehena</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteartea</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteazkena</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Osteguna</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Ostirala</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Active>true</Active>
                     <Comments/>
          </ConstraintStudentsSetNotAvailableTimes>
          <ConstraintStudentsSetNotAvailableTimes>
                     <Weight_Percentage>100</Weight_Percentage>
                     <Students>3</Students>
                     <Number_of_Not_Available_Times>6</Number_of_Not_Available_Times>
                     <Not_Available_Time>
                                <Day>Astelehena</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteartea</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteazkena</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Osteguna</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Ostirala</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Astelehena</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteartea</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteazkena</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Osteguna</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Ostirala</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Active>true</Active>
                     <Comments/>
          </ConstraintStudentsSetNotAvailableTimes>
          <ConstraintStudentsSetNotAvailableTimes>
                     <Weight_Percentage>100</Weight_Percentage>
                     <Students>4</Students>
                     <Number_of_Not_Available_Times>6</Number_of_Not_Available_Times>
                     <Not_Available_Time>
                                <Day>Astelehena</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteartea</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteazkena</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Osteguna</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Ostirala</Day>
                                <Hour>11:15-11:45</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Astelehena</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteartea</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Asteazkena</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Osteguna</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Not_Available_Time>
                                <Day>Ostirala</Day>
                                <Hour>14:30-15:20</Hour>
                     </Not_Available_Time>
                     <Active>true</Active>
                     <Comments/>
          </ConstraintStudentsSetNotAvailableTimes>"""
        TimeConstraintElement = self.fetxml.find('./Time_Constraints_List')
        TimeConstraintElement.append(ET.fromstring(dena))
        # dbh-bach=ET.fromstring("""<ConstraintStudentsSetNotAvailableTimes>
            # <Weight_Percentage>100</Weight_Percentage>
            # <Students></Students>
            # <Number_of_Not_Available_Times>6</Number_of_Not_Available_Times>
            # <Not_Available_Time>
                # <Day>Astelehena</Day>
                # <Hour>11:15-11:45</Hour>
            # </Not_Available_Time>
            # <Not_Available_Time>
                # <Day>Asteartea</Day>
                # <Hour>11:15-11:45</Hour>
            # </Not_Available_Time>
            # <Not_Available_Time>
                # <Day>Asteazkena</Day>
                # <Hour>11:15-11:45</Hour>
            # </Not_Available_Time>
            # <Not_Available_Time>
                # <Day>Osteguna</Day>
                # <Hour>11:15-11:45</Hour>
            # </Not_Available_Time>
            # <Not_Available_Time>
                # <Day>Ostirala</Day>
                # <Hour>11:15-11:45</Hour>
            # </Not_Available_Time>
            # <Not_Available_Time>
                # <Day>Astelehena</Day>
                # <Hour>14:30-15:20</Hour>
            # </Not_Available_Time>
            # <Not_Available_Time>
                # <Day>Asteartea</Day>
                # <Hour>14:30-15:20</Hour>
            # </Not_Available_Time>
            # <Not_Available_Time>
                # <Day>Asteazkena</Day>
                # <Hour>14:30-15:20</Hour>
                    # </Not_Available_Time>
                    # <Not_Available_Time>
                        # <Day>Osteguna</Day>
                        # <Hour>14:30-15:20</Hour>
                    # </Not_Available_Time>
                    # <Not_Available_Time>
                        # <Day>Ostirala</Day>
                        # <Hour>14:30-15:20</Hour>
                    # </Not_Available_Time>
                    # <Active>true</Active>
                    # <Comments/>
        # </ConstraintStudentsSetNotAvailableTimes>""")
        # batx=ET.fromstring("""<ConstraintStudentsSetNotAvailableTimes>
            # <Weight_Percentage>100</Weight_Percentage>
            # <Students></Students>
            # <Number_of_Not_Available_Times>6</Number_of_Not_Available_Times>
            # <Not_Available_Time>
                # <Day>Astelehena</Day>
                # <Hour>11:15-11:45</Hour>
            # </Not_Available_Time>
            # <Not_Available_Time>
                # <Day>Asteartea</Day>
                # <Hour>11:15-11:45</Hour>
            # </Not_Available_Time>
            # <Not_Available_Time>
                # <Day>Asteazkena</Day>
                # <Hour>11:15-11:45</Hour>
            # </Not_Available_Time>
            # <Not_Available_Time>
                # <Day>Osteguna</Day>
                # <Hour>11:15-11:45</Hour>
            # </Not_Available_Time>
            # <Not_Available_Time>
                # <Day>Ostirala</Day>
                # <Hour>11:15-11:45</Hour>
            # </Not_Available_Time>
            # <Not_Available_Time>
                # <Day>Ostirala</Day>
                # <Hour>14:30-15:20</Hour>
            # </Not_Available_Time>
            # <Active>true</Active>
            # <Comments/>
        # </ConstraintStudentsSetNotAvailableTimes>""")
        # TimeConstraintElement=self.fetxml.find('./Time_Constraints_List')
        # for gr in list(set([b.text for b in self.fetxml.findall('.//Students_List/Year/Group/Name')])):
            # if gr[0]<5 | gr[1] not in ('H','I,','J'):
                # StudentsElement=dbh-bach.find('./Students')
            # else:
                # StudentsElement=batx.find('./Students')
                
            # StudentsElement.text=gr #Save to xmlfet...
            # TimeConstraintElement.append(StudentsElement)
            
    def printm(self):
        print(self.prettify(self.fetxml))

    def prettify(self, elem):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = xml.dom.minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="\t")

    def write(self, file='mendifetoutput.fet'):
        f = codecs.open(file, 'w', 'utf-8')
        # f.write(ET.tostring(self.fetxml))
        f.write(self.prettify(self.fetxml))
        f.close()
    # f.write(ET.tostring(rot,encoding="utf-8"))
    # X Fitxategi:
    # 1. Talde txikiekin
    # 2. Hautazkoekin
    #---------Sortu funtzioak---------
    # 3. Independiente direnak 
    # 4. Bilerak...

    # activities=[[teacher.subject,hours,room,groups],[..]]
    # groups=['1-A-OM','1-B-OM','1-C-OM']
    # activities=[['Asier','OM',2,'1-A',['1-A-OM','1-B-OM','1-C-OM']],['Oskia','HA',2,'1-B',['1-A-HA','1-B-HA','1-C-HA']]]
    def generate_simultaneous_activities(self, activities, idm):
        """
        Generates the necesary xml for geneateSimultaneousActivities: the activities,
        rooms,samestartingtime...
        input: 
        activities=[[teacher.subject,hours,room,groups],[..]]
        where: groups=['1-A-OM','1-B-OM','1-C-OM']
        """
        # print("generate_simultaneous_activities")
        # print(idm)
        # print(activities)
        # print("____")
        Id = int(idm)
        gid = Id
        TimeConstraintElement = self.fetxml.find('./Time_Constraints_List')
        if int(activities[0][self.totalduration]) > 1:
            if len(activities) > 1:
                TimeConstraintElement.append(self.generate_min_days(Id, activities[0][self.totalduration]))  # ?
          #FIXME: Next two lines maybe are not needed, as new subgroups are exclusive
#         for a in self.generate_start_time(Id, len(activities), int(activities[0][self.totalduration])):
#             TimeConstraintElement.append(a)
        SpaceConstraintElement = self.fetxml.find('./Space_Constraints_List')
        # Generate Activities  
        ActivitiesElement = self.fetxml.find('./Activities_List')
        for j in range(len(activities)):
            for a in self.generate_room(Id, activities[j][self.room], activities[j][self.totalduration]):
                SpaceConstraintElement.append(a)
            # TimeConstraintElement.append(self.generate_min_days(Id,activities[j][2]))
            activity = activities[j]
            for _ in range(int(activity[self.totalduration])):
                ActivitiesElement.append(self.generate_activity(activity, Id, gid))
                Id += 1
            gid = Id
        
                        
    def generate_independent_activities(self, activities, idm):
        """
        Generates the necesary xml for geneateIndependentActivities: the activities,
        rooms,...
        input: 
        activities=[[teacher.subject,hours,room,[groups]]
        #FIXME Taldeak ez daude prozesatuta!!
        """
        # print("generate_independent_activities")
        # print(idm)
        # print(activities)
        # print("____")
        Id = int(idm)
        gid = Id
        duration = 1
        days = 5  # In case xml not ready
        TimeConstraintElement = self.fetxml.find('./Time_Constraints_List')
        ActivitiesElement = self.fetxml.find('./Activities_List')
        SpaceConstraintElement = self.fetxml.find('./Space_Constraints_List')
        days = len(self.fetxml.findall('./Days_List/Name'))
        hours = int(activities[self.totalduration])
        if (activities[self.room] == "Trinkete") and (activities[self.totalduration] >= 2): 
            duration = 2  # FIXME: Dirty hack for Gorputz HEziketa in Trinekte
        if  hours > days:
            distribution = self.group_long_activities(hours)
            duration = 2
            actamount = hours // duration
            rest = hours % duration
            if actamount <= days:  # If activities can be grouped in 2 hours less or equal than days, they 
                # should not be the same day
                TimeConstraintElement.append(self.generate_min_days(Id, actamount+rest)) #7//2 = 3 days, rest 1 hour, the fourth day
            else:  # Else I create as they where diferrent each one with 2 hours
                activities[self.totalduration] = 2
            for a in self.generate_room(Id, activities[self.room], hours // duration + rest):
                SpaceConstraintElement.append(a)
            for _ in range(actamount):
                ActivitiesElement.append(self.generate_activity(activities, Id, gid, duration))
                Id += 1
                if actamount > days:gid += 1
            if rest != 0:
                if actamount > days:
                    activities[self.totalduration] = rest
                duration = rest
                ActivitiesElement.append(self.generate_activity(activities, Id, gid, duration))
        else:
            if hours > duration:  # Was hours>1, changed for an activity with duration=2?
                TimeConstraintElement.append(self.generate_min_days(Id, activities[self.totalduration]))  # ?
            # Generate Activities  
            for a in self.generate_room(Id, activities[self.room], hours // duration):
                SpaceConstraintElement.append(a)
                # TimeConstraintElement.append(self.generate_min_days(Id,activities[j][2]))
            for _ in range(hours // duration):
                ActivitiesElement.append(self.generate_activity(activities, Id, gid, duration))
                Id += 1
#        if rest: ActivitiesElement.append(self.generate_activity(activities,Id,gid))
        
    def group_long_activities(self, hours,compact=True):
        # FIXME 13 hours: 4,1 =>3-3-3-3-1 Not used
        number = None
        mod = None
        DaysElement = self.fetxml.findall('./Days_List/Name')
        days = len(DaysElement)
        number = hours // days
        rest = hours % days
        
        if (number == 1) and compact:
            number = 2
            rest = hours % number
        
        grouped = []
        
        if rest == 0:
            for i in range(hours//number):
                grouped.append(number)
            for i in range(days-hours//number):
                grouped.append(0)
        else:
            for i in range(rest):
                grouped.append(number+1)
            for i in range(days -rest):
                grouped.append(number)
        return grouped
            
    
    def generate_laguntza_activities(self, activities, idm):
        """
        Generates the necesary xml for (some) sessions with multiple teachers: the activities,
        rooms,...
        input: 
        activities=[[teacher,subject,hours,room,[group]],[teacher,subject,hours,room,[group]]]
        [[u'Mariaje Ruiz', u'Tecnolog\xeda (Apoyo)', '1', '', ['1-B']], [u'Pablo Garc\xeda', u'Tecnolog\xeda', '2', 'TailerraAintzira1', ['1-B']]]
        """
        # FIXME Only works for two activities
        # print("generate_laguntza_activities")
        # print(idm)
        # print(activities)
        # print("____")
        # main=[]
        sec = []
        if activities[0][2] > activities[1][2]:
            main = activities[0]
            sec = activities[1]
        else:
            main = activities[1]
            sec = activities[0]
        Id = int(idm)
        gid = Id
        SpaceConstraintElement = self.fetxml.find('./Space_Constraints_List')
        roms = self.generate_room(Id, main[3], main[2])
        for rom in roms:
            SpaceConstraintElement.append(rom)
        ActivitiesElement = self.fetxml.find('./Activities_List')
        # Generate Activities
        for i in range(int(main[2])):
            ActivityElement = ET.SubElement(ActivitiesElement, "Activity")
            if i == 0:
                for teacher in main[0], sec[0]:
                    Teacher = ET.SubElement(ActivityElement, "Teacher")
                    Teacher.text = teacher
            else:
                Teacher = ET.SubElement(ActivityElement, "Teacher")
                Teacher.text = main[0]
            Subject = ET.SubElement(ActivityElement, "Subject")
            Subject.text = main[1]
            Group = ET.SubElement(ActivityElement, "Students")
            Group.text = main[4][0]  # shoul be [0][1]
            Duration = ET.SubElement(ActivityElement, "Duration")
            Duration.text = '1'
            TDuration = ET.SubElement(ActivityElement, "Total_Duration")
            TDuration.text = str(main[2])
            IdAct = ET.SubElement(ActivityElement, "Id")
            IdAct.text = str(Id)
            GroupId = ET.SubElement(ActivityElement, "Activity_Group_Id")
            GroupId.text = str(gid)
            Active = ET.SubElement(ActivityElement, "Active")
            Active.text = 'true'
            Comments = ET.SubElement(ActivityElement, "Comments")
            Comments.text = ' '
            Id += 1
            
            # print(ET.dump(ActivityElement))
        # print(ET.dump(ActivitiesElement))
        
    def generate_multiple_teachers(self, conexion, idm):
        """
        Generates the necesary xml for sessions with multiple tfeachers: the activities,
        rooms,...
        input: 
        activities=['R', ['MB', 'B', '', '1', '7', '2', 'R', 'bilera'], ['Teacher2', 'Teacher3', 'Teacher4']]
        [[u'Bizikidetza Bilera', u'b', u'1', u'BizikAintzira', u'b'], [u'Amaia Arrieta', u'Ana Astrain', u'Asun Carlos']]
        """
        # print("generate_multiple_teachers")
        # print(idm)
        # print(activities)
        # print("____")
        Id = int(idm)
        activity = conexion[1]
        SpaceConstraintElement = self.fetxml.find('./Space_Constraints_List')
        # Generate Activities  
        ActivitiesElement = self.fetxml.find('./Activities_List')
        SpaceConstraintElement.append(self.generate_room(Id, activity[self.room-1], activity[self.totalduration-1])[0])
        ActivityElement = ET.SubElement(ActivitiesElement, "Activity")
        for teacher in conexion[2]:
            Teacher = ET.SubElement(ActivityElement, "Teacher")
            Teacher.text = teacher
        Subject = ET.SubElement(ActivityElement, "Subject")
        Subject.text = activity[self.subject-1]
        Group = ET.SubElement(ActivityElement, "Students")
        Group.text = activity[self.year-1]  # FIXME gropus not generated??
        Duration = ET.SubElement(ActivityElement, "Duration")
        Duration.text = '1'
        TDuration = ET.SubElement(ActivityElement, "Total_Duration")
        TDuration.text = str(activity[self.totalduration-1])
        IdAct = ET.SubElement(ActivityElement, "Id")
        IdAct.text = str(Id)
        GroupId = ET.SubElement(ActivityElement, "Activity_Group_Id")
        GroupId.text = str(Id)
        Active = ET.SubElement(ActivityElement, "Active")
        Active.text = 'true'
        Comments = ET.SubElement(ActivityElement, "Comments")
        Comments.text = ' '
                    
    def generate_activity(self, activity, Id, gid, duration='1'):     
        """Generates a fet activity xml from a tuple formated as: [Teacher,Subject,Total_Duration,Room,[Group(s)]] 
        and the activity Id, and activities group Id
        Returns
        <Activity>
            <Teacher>Teacher</Teacher>
            <Subject>Subject</Subject>
            <Students>Group1</Students>
            <Students>Groupn</Students>
            <Total_Duration>Total_Duration</Total_Duration>
            <Id>Id<Id>
            <Activity_Group_Id>..</Activity_Group_Id>
            <Active>true</Active>
            <Comments>  </Comments>
        </Activity>     
        """
        ActivityElement = ET.Element("Activity")
        Teacher = ET.SubElement(ActivityElement, "Teacher")
        Teacher.text = activity[self.teacher]
        Subject = ET.SubElement(ActivityElement, "Subject")
        Subject.text = activity[self.subject]
        if not isinstance(activity[self.group], str):  # python2-> if not isinstance(activity[4], basestring):
            for group in activity[self.group]:
                Group = ET.SubElement(ActivityElement, "Students")
                Group.text = group
        else:
            Group = ET.SubElement(ActivityElement, "Students")
            Group.text = activity[self.group][0] #FIXME: What does this do?
        Duration = ET.SubElement(ActivityElement, "Duration")
        Duration.text = str(duration)
        TDuration = ET.SubElement(ActivityElement, "Total_Duration")
        TDuration.text = str(activity[self.totalduration])
        IdAct = ET.SubElement(ActivityElement, "Id")
        IdAct.text = str(Id)
        GroupId = ET.SubElement(ActivityElement, "Activity_Group_Id")
        GroupId.text = str(gid)
        Active = ET.SubElement(ActivityElement, "Active")
        Active.text = 'true'
        Comments = ET.SubElement(ActivityElement, "Comments")
        Comments.text = ' '
        return ActivityElement
            

    def generate_room(self, Id, room, number):
        """
        Generates the xml necesary for fet room assignement
        generate_room(3,'1.A',2)
        Id:Activity Id
        room:room name
        number: number of the same activity in that room (technology is twice
        a week in technology room, so two activities has to be forced in that room
        Returns a list where each item is a generated xml for a session
        <ConstraintActivityPreferredRoom>
            <Weight_Percentage>100</Weight_Percentage>
            <Activity_Id>4</Activity_Id>
            <Room>1A</Room>
            <Permanently_Locked>true</Permanently_Locked>
            <Active>true</Active>
            <Comments> </Comments>
        </ConstraintActivityPreferredRoom>
        """
        r = []
        for i in range(Id, Id + int(number)):
            RoomCElement = ET.Element("ConstraintActivityPreferredRoom")
            RWeight = ET.SubElement(RoomCElement, "Weight_Percentage")
            RWeight.text = '100'
            RActivityId = ET.SubElement(RoomCElement, "Activity_Id")
            RActivityId.text = str(i)
            RActivityRoom = ET.SubElement(RoomCElement, "Room")
            RActivityRoom.text = room
            PLActive = ET.SubElement(RoomCElement, "Permanently_Locked")
            PLActive.text = 'true'
            RActive = ET.SubElement(RoomCElement, "Active")
            RActive.text = 'true'
            RComments = ET.SubElement(RoomCElement, "Comments")
            RComments.text = ' '  
            r.append(RoomCElement)
        return r
            
            
    def generate_start_time(self, Id, activitiesnumber, activitiesduration):
        """
        Generates the xml necesary for fet to force several activities
        be at the same time
        Id: Id of the first activity (the activitites must be consecutive and alternative
        for 2 sessions of A,B,C ids should be A(1,2),B(3,4),C(5,6)
        activitiesnumber: number of activities that occurs at the same time
        activitiesduration: number of sessions of the activities
        Returns a list with generate conexions
        For input generate_start_time(1,3,2)
        Output: (a list with 2 elements like:
        <ConstraintActivitiesSameStartingTime>
            <Weight_Percentage>100</Weight_Percentage>
            <Number_of_Activities>3</Number_of_Activities>
            <Activity_Id>1</Activity_Id>
            <Activity_Id>3</Activity_Id>
            <Activity_Id>5</Activity_Id>
            <Active>true</Active>
            <Comments> </Comments>
        </ConstraintActivitiesSameStartingTime>
        """
        starttimelist = []
        for _i in range(activitiesduration):
            # Generate Starting time Constraint  
            Constraint = ET.Element("ConstraintActivitiesSameStartingTime")
            CWeight = ET.SubElement(Constraint, "Weight_Percentage")
            CWeight.text = '100'
            CNumber = ET.SubElement(Constraint, "Number_of_Activities")
            CNumber.text = str(activitiesnumber)
            for a in range(Id, Id + activitiesnumber * activitiesduration, activitiesduration):
                Cact = ET.SubElement(Constraint, "Activity_Id")
                Cact.text = str(a)
            CActive = ET.SubElement(Constraint, "Active")
            CActive.text = 'true'
            CComments = ET.SubElement(Constraint, "Comments")
            CComments.text = ' '  
            Id += 1
            starttimelist.append(Constraint)
        return starttimelist
    
    def generate_min_days(self, Id, number):
        """
        Forces activities not to be in the same day
        Id: Id of the first activity
        number:number of activities (Id must be consecutive)
        For input: generate_min_days(1,3)
        Output:
        <ConstraintMinDaysBetweenActivities>
            <Weight_Percentage>100</Weight_Percentage>
            <Consecutive_If_Same_Day>true</Consecutive_If_Same_Day>
            <Number_of_Activities>3</Number_of_Activities>
            <Activity_Id>1</Activity_Id>
            <Activity_Id>2</Activity_Id>
            <Activity_Id>3</Activity_Id>
            <Active>true</Active>
            <Comments> </Comments>
        </ConstraintMinDaysBetweenActivities>
        """
        Constraint = ET.Element("ConstraintMinDaysBetweenActivities")
        CWeight = ET.SubElement(Constraint, "Weight_Percentage")
        CWeight.text = '100'
        CCons = ET.SubElement(Constraint, "Consecutive_If_Same_Day")
        CCons.text = 'true'
        CNumber = ET.SubElement(Constraint, "Number_of_Activities")
        CNumber.text = str(number)
        for a in range(Id, Id + int(number)):
            Cact = ET.SubElement(Constraint, "Activity_Id")
            Cact.text = str(a)
        CMinDays = ET.SubElement(Constraint, "MinDays")
        CMinDays.text = '1'
        CActive = ET.SubElement(Constraint, "Active")
        CActive.text = 'true'
        CComments = ET.SubElement(Constraint, "Comments")
        CComments.text = ' '  
        return Constraint


    def generate_meetings_groups(self, activities):
        """
        activities is a list with the following format:
        teacher,subject,year,groups,hours,room,conexion
        returns a list where each element is a connection of teachers 
        that have a meeting a the same time, and in each connection wich are
        also list, each element has the format [[teacher.subject,hours,room,groups],[..]]
        output [[con1,[[subject,year,hours,room,group],[teachers-list]]],[...]]
          activities=[[subject,year,hours,room,group],[teachers-list]]
        """
        # Saiatu dictionary erabiliz egiten
        s = []
        for activity in activities:
            # FIXME: Saiatu bihurtzen jardueran normal bat irakasle askorekin
#            print(r)
            v = [activity[self.con], activity[1:],[activity[0]]]
            for i in range(len(s)):
                if s[i][0] == v[0]:
                    s[i][2].append(activity[self.teacher])
                    break
                else:
                    if i == len(s) - 1:
                        s.append(v)
            if len(s) == 0:
                s.append(v)
        return s


    def generate_laguntza_groups(self, activities):
        """
        #FIXME
        activities is a list with the following format:
        teacher,subject,year,groups,hours,room,conexion
        returns a list where each element is a connection of subject 
        that should be at least one session at the same time, 
        and in each connection wich are
        """
        # Saiatu dictionary erabiliz egiten
        s = []
        for r in activities:
            v = [r[-1], r[0:-1]]
            if len(r[3]) > 1:
                Taldeak = []
                for j in range(len(r[3])):
                    Taldeak.append(r[2] + "-" + r[3][j] + "-" + r[1])
                v = [r[-1], [[r[0], r[1], r[4], r[5], Taldeak]]]
            else:
                v = [r[-1], [[r[0], r[1], r[4], r[5], [r[2] + "-" + r[3]]]]]
            for i in range(len(s)):
                if s[i][0] == v[0]:
                    s[i][1].insert(len(s[i][1]), v[1][0])
                    break
                else:
                    if i == len(s) - 1:
                        s.append(v)
            if len(s) == 0:
                s.append(v)
        return s


            
    def generate_hautazkoak(self, activities):
        """
        Reads a csv file with the following format:
        department,teacher,subject,year,groups,hours,room,conexion
        returns a list where each element is a connection of subject 
        that should be a the same time, and in each connection wich are
        also list, each element has the format [[teacher,subject,year,groups,hours,room,building,conexion,type],[..]]
        [['Teacher2', 'Subject2', '1DBH', ['1-H-Subject10_1-Subject5-Subject2', '1-H-Subject10_1-Subject7-Subject2', '1-H-Subject10_1-Subject8-Subject2', '1-H-Subject10_2-Subject5-Subject2', '1-H-Subject10_2-Subject7-Subject2', '1-H-Subject10_2-Subject8-Subject2', '1-I-Subject10_2-Subject5-Subject2', '1-I-Subject10_2-Subject7-Subject2', '1-I-Subject10_2-Subject8-Subject2', '1-I-Subject10_3-Subject5-Subject2', '1-I-Subject10_3-Subject7-Subject2', '1-I-Subject10_3-Subject8-Subject2'], '2', '1', '2', 'A', 'h'], ['Teacher3', 'Subject3', '1DBH', ['1-H-Subject10_1-Subject5-Subject3', '1-H-Subject10_1-Subject7-Subject3', '1-H-Subject10_1-Subject8-Subject3', '1-H-Subject10_2-Subject5-Subject3', '1-H-Subject10_2-Subject7-Subject3', '1-H-Subject10_2-Subject8-Subject3', '1-I-Subject10_2-Subject5-Subject3', '1-I-Subject10_2-Subject7-Subject3', '1-I-Subject10_2-Subject8-Subject3', '1-I-Subject10_3-Subject5-Subject3', '1-I-Subject10_3-Subject7-Subject3', '1-I-Subject10_3-Subject8-Subject3'], '2', '2', '2', 'A', 'h'], ['Teacher5', 'Subject5', '1DBH', ['1-H-Subject10_1-Subject5-Subject2', '1-H-Subject10_1-Subject5-Subject3', '1-H-Subject10_2-Subject5-Subject2', '1-H-Subject10_2-Subject5-Subject3', '1-I-Subject10_2-Subject5-Subject2', '1-I-Subject10_2-Subject5-Subject3', '1-I-Subject10_3-Subject5-Subject2', '1-I-Subject10_3-Subject5-Subject3', '1-J-Subject5'], '3', '1', '2', 'B', 'h'], ['Teacher7', 'Subject7', '1DBH', ['1-H-Subject10_1-Subject7-Subject2', '1-H-Subject10_1-Subject7-Subject3', '1-H-Subject10_2-Subject7-Subject2', '1-H-Subject10_2-Subject7-Subject3', '1-I-Subject10_2-Subject7-Subject2', '1-I-Subject10_2-Subject7-Subject3', '1-I-Subject10_3-Subject7-Subject2', '1-I-Subject10_3-Subject7-Subject3', '1-J-Subject7'], '3', '2', '2', 'B', 'h'], ['Teacher8', 'Subject8', '1DBH', ['1-H-Subject10_1-Subject8-Subject2', '1-H-Subject10_1-Subject8-Subject3', '1-H-Subject10_2-Subject8-Subject2', '1-H-Subject10_2-Subject8-Subject3', '1-I-Subject10_2-Subject8-Subject2', '1-I-Subject10_2-Subject8-Subject3', '1-I-Subject10_3-Subject8-Subject2', '1-I-Subject10_3-Subject8-Subject3', '1-J-Subject8'], '3', '3', '2', 'B', 'h'], ['Teacher6', 'Subject10_1', '1DBH', ['1-H-Subject10_1-Subject5-Subject2', '1-H-Subject10_1-Subject5-Subject3', '1-H-Subject10_1-Subject7-Subject2', '1-H-Subject10_1-Subject7-Subject3', '1-H-Subject10_1-Subject8-Subject2', '1-H-Subject10_1-Subject8-Subject3'], '5', '1', '2', 'C', 'h'], ['Teacher8', 'Subject10_2', '1DBH', ['1-H-Subject10_2-Subject5-Subject2', '1-H-Subject10_2-Subject5-Subject3', '1-H-Subject10_2-Subject7-Subject2', '1-H-Subject10_2-Subject7-Subject3', '1-H-Subject10_2-Subject8-Subject2', '1-H-Subject10_2-Subject8-Subject3', '1-I-Subject10_2-Subject5-Subject2', '1-I-Subject10_2-Subject5-Subject3', '1-I-Subject10_2-Subject7-Subject2', '1-I-Subject10_2-Subject7-Subject3', '1-I-Subject10_2-Subject8-Subject2', '1-I-Subject10_2-Subject8-Subject3'], '5', '4', '2', 'C', 'h'], ['Teacher9', 'Subject10_3', '1DBH', ['1-I-Subject10_3-Subject5-Subject2', '1-I-Subject10_3-Subject5-Subject3', '1-I-Subject10_3-Subject7-Subject2', '1-I-Subject10_3-Subject7-Subject3', '1-I-Subject10_3-Subject8-Subject2', '1-I-Subject10_3-Subject8-Subject3'], '5', '2', '2', 'C', 'h']]
        The groups generated follow this rule:
        Groups are [[year-1letter-subject,year-2letter-subject,year-3letter-subject,...]]
        [['A', ['Teacher2', 'Subject2', '1DBH', ['1-H-Subject10_1-Subject5-Subject2', '1-H-Subject10_1-Subject7-Subject2', '1-H-Subject10_1-Subject8-Subject2', '1-H-Subject10_2-Subject5-Subject2', '1-H-Subject10_2-Subject7-Subject2', '1-H-Subject10_2-Subject8-Subject2', '1-I-Subject10_2-Subject5-Subject2', '1-I-Subject10_2-Subject7-Subject2', '1-I-Subject10_2-Subject8-Subject2', '1-I-Subject10_3-Subject5-Subject2', '1-I-Subject10_3-Subject7-Subject2', '1-I-Subject10_3-Subject8-Subject2'], '2', '1', '2', 'A', 'h'], 
               ['Teacher3', 'Subject3', '1DBH', ['1-H-Subject10_1-Subject5-Subject3', '1-H-Subject10_1-Subject7-Subject3', '1-H-Subject10_1-Subject8-Subject3', '1-H-Subject10_2-Subject5-Subject3', '1-H-Subject10_2-Subject7-Subject3', '1-H-Subject10_2-Subject8-Subject3', '1-I-Subject10_2-Subject5-Subject3', '1-I-Subject10_2-Subject7-Subject3', '1-I-Subject10_2-Subject8-Subject3', '1-I-Subject10_3-Subject5-Subject3', '1-I-Subject10_3-Subject7-Subject3', '1-I-Subject10_3-Subject8-Subject3'], '2', '2', '2', 'A', 'h']], 
        ['B', ['Teacher5', 'Subject5', '1DBH', ['1-H-Subject10_1-Subject5-Subject2', '1-H-Subject10_1-Subject5-Subject3', '1-H-Subject10_2-Subject5-Subject2', '1-H-Subject10_2-Subject5-Subject3', '1-I-Subject10_2-Subject5-Subject2', '1-I-Subject10_2-Subject5-Subject3', '1-I-Subject10_3-Subject5-Subject2', '1-I-Subject10_3-Subject5-Subject3', '1-J-Subject5'], '3', '1', '2', 'B', 'h'], 
              ['Teacher7', 'Subject7', '1DBH', ['1-H-Subject10_1-Subject7-Subject2', '1-H-Subject10_1-Subject7-Subject3', '1-H-Subject10_2-Subject7-Subject2', '1-H-Subject10_2-Subject7-Subject3', '1-I-Subject10_2-Subject7-Subject2', '1-I-Subject10_2-Subject7-Subject3', '1-I-Subject10_3-Subject7-Subject2', '1-I-Subject10_3-Subject7-Subject3', '1-J-Subject7'], '3', '2', '2', 'B', 'h'], 
              ['Teacher8', 'Subject8', '1DBH', ['1-H-Subject10_1-Subject8-Subject2', '1-H-Subject10_1-Subject8-Subject3', '1-H-Subject10_2-Subject8-Subject2', '1-H-Subject10_2-Subject8-Subject3', '1-I-Subject10_2-Subject8-Subject2', '1-I-Subject10_2-Subject8-Subject3', '1-I-Subject10_3-Subject8-Subject2', '1-I-Subject10_3-Subject8-Subject3', '1-J-Subject8'], '3', '3', '2', 'B', 'h']], 
        ['C', ['Teacher6', 'Subject10_1', '1DBH', ['1-H-Subject10_1-Subject5-Subject2', '1-H-Subject10_1-Subject5-Subject3', '1-H-Subject10_1-Subject7-Subject2', '1-H-Subject10_1-Subject7-Subject3', '1-H-Subject10_1-Subject8-Subject2', '1-H-Subject10_1-Subject8-Subject3'], '5', '1', '2', 'C', 'h'], 
              ['Teacher8', 'Subject10_2', '1DBH', ['1-H-Subject10_2-Subject5-Subject2', '1-H-Subject10_2-Subject5-Subject3', '1-H-Subject10_2-Subject7-Subject2', '1-H-Subject10_2-Subject7-Subject3', '1-H-Subject10_2-Subject8-Subject2', '1-H-Subject10_2-Subject8-Subject3', '1-I-Subject10_2-Subject5-Subject2', '1-I-Subject10_2-Subject5-Subject3', '1-I-Subject10_2-Subject7-Subject2', '1-I-Subject10_2-Subject7-Subject3', '1-I-Subject10_2-Subject8-Subject2', '1-I-Subject10_2-Subject8-Subject3'], '5', '4', '2', 'C', 'h'], 
              ['Teacher9', 'Subject10_3', '1DBH', ['1-I-Subject10_3-Subject5-Subject2', '1-I-Subject10_3-Subject5-Subject3', '1-I-Subject10_3-Subject7-Subject2', '1-I-Subject10_3-Subject7-Subject3', '1-I-Subject10_3-Subject8-Subject2', '1-I-Subject10_3-Subject8-Subject3'], '5', '2', '2', 'C', 'h']]]
        """
        # Saiatu dictionary erabiliz egiten
        conexions = []
        for activity in activities:
            v = [activity[self.con], activity]
            for i in range(len(conexions)):
                if conexions[i][0] == v[0]:
                    conexions[i].insert(len(conexions[i]), v[1:][0])
                    break
                else:
                    if i == len(conexions) - 1:
                        conexions.append(v)
            if len(conexions) == 0:
                conexions.append(v)
        return conexions
    
    
    def max_activity_id(self):
        """
        Returns the max_activity_id that the fet xml has
        """
        try:
            return int(max([int(b.text) for b in self.fetxml.findall(".//Activity/Id")])) + 1
        except:
            return 1


    def generate_groups_from_activities(self):
        """
        Returns the groups defined in activities from the suplied fet file
        """
        # Years:1,2,3,4,5,6 len=1
        # Groups:1-A,1-B,1-C,  3-Dib!! 3<=len<6
        # Subgroups: 1-A-CCSS,1-A-HA,1-A-LS  6<=len
        # FIXME 4-Div!!included as subgroup of 4-D
        groups = list(set([b.text for b in self.fetxml.findall(".//Activity/Students")]))
        groups.sort(key=len)
        d = {}
        for g in groups:
            if len(g) == 1 and not g in d:
                d[g] = {}
            if len(g) > 1 and len(g) <= 4:
                if g[0] in d and not g in d[g[0]]:
                    d[g[0]][g] = []
                else:
                    d[g[0]] = {}
                    d[g[0]][g] = []
            if len(g) > 4:
                if not g[0] in d:
                    d[g[0]] = {}
                if not g[0:3] in d[g[0]]:
                    d[g[0]][g[0:3]] = []
                if not g in g[0:3]:
                    d[g[0]][g[0:3]].append(g)
        return d

    def create_groups_XML(self, groups):
        """
        Creates the Students section of the fet xml file
        from an fet xml file with activities, by extracting
        activities groups
        groups:{'1':{'1-k':{'1-k-Al','1-k-Fr'}}}...
        """
        Students = self.fetxml.find('./Students_List')
        for year in groups.keys():
            YearElement = ET.SubElement(Students, "Year")
            YName = ET.SubElement(YearElement, "Name")
            YName.text = year
            YNoS = ET.SubElement(YearElement, 'Number_of_Students')
            YNoS.text = "0"
            if groups[year].keys() != []:
                for group in groups[year].keys():
                    GroupElement = ET.SubElement(YearElement, "Group")
                    GName = ET.SubElement(GroupElement, "Name")
                    GName.text = group
                    GNoS = ET.SubElement(GroupElement, 'Number_of_Students')
                    GNoS.text = "0"     
                    if len(groups[year][group]) > 0:
                        for sg in groups[year][group]:
                            subgroup = ET.SubElement(GroupElement, 'Subgroup')
                            sgname = ET.SubElement(subgroup, 'Name')
                            sgname.text = sg
                            sgNoS = ET.SubElement(subgroup, 'Number_of_Students')
                            sgNoS.text = "0"
            
        return Students
        
        
      
    def generate_teachers_from_activities(self):
        """
        Returns the teachers defined in activities from the suplied fet file
        """
        TeacherList = self.fetxml.find('./Teachers_List')
        for teacher in  list(set([b.text for b in self.fetxml.findall('.//Activity/Teacher')])):
            Teacher = ET.SubElement(TeacherList, "Teacher")
            TeacherName = ET.SubElement(Teacher, "Name")
            TeacherName.text = teacher

    def generate_subjects_from_activities(self):
        """
        Returns the teachers defined in activities from the suplied fet file
        """
        SubjectsList = self.fetxml.find('./Subjects_List')
        for subject in  list(set([b.text for b in self.fetxml.findall('.//Activity/Subject')])):
            Subjects = ET.SubElement(SubjectsList, "Subject")
            SubjectsName = ET.SubElement(Subjects, "Name")
            SubjectsName.text = subject


    def generate_rooms_from_activities(self):
        """
        Returns the teachers defined in activities from the suplied fet file
        """
        RoomsList = self.fetxml.find('./Rooms_List')
        for room in list(set([b.text for b in self.fetxml.findall('.//ConstraintActivityPreferredRoom/Room')])):  # Eraikinak  -list(set([a.text for a in self.xmlfile.findall('./Room/Name')]))
            Room = ET.SubElement(RoomsList, "Room")
            RoomName = ET.SubElement(Room, "Name")
            RoomName.text = room
            RoomBuilding = ET.SubElement(Room, "Building")
            RoomBuilding.text = self.roombuilding[room]
            
        for room in list(set([b.text for b in self.fetxml.findall('.//ConstraintActivityPreferredRooms/Preferred_Room')])):  # Eraikinak  -list(set([a.text for a in self.xmlfile.findall('./Room/Name')]))
            Room = ET.SubElement(RoomsList, "Room")
            RoomName = ET.SubElement(Room, "Name")
            RoomName.text = room
            RoomBuilding = ET.SubElement(Room, "Building")
            RoomBuilding.text = room[-1]

    def generate_buildings_from_rooms(self):
        """
        Caution,rooms could not have building text!!
        """
        BuildingsList = self.fetxml.find('./Buildings_List')
        for bulding in list(set([b.text for b in self.fetxml.findall('.//Rooms_List/Room/Building')])):
            Building = ET.SubElement(BuildingsList, "Building")
            BuildingName = ET.SubElement(Building, "Name")
            BuildingName.text = bulding

    def generate_all_laguntza(self, groups):
        for group in groups:
            Id = self.max_activity_id()
            self.generate_laguntza_activities(group[1], Id)
            
    def generate_all_meetings(self, groups):
        for group in groups:
            Id = self.max_activity_id()
            self.generate_multiple_teachers(group, Id)
    
    def generate_all_option_groups(self, groups):
        for group in groups:
            Id = self.max_activity_id()
            activityroot = self.generate_simultaneous_activities(group[1:], Id)

    def generate_all_independent_activities(self, groups):
        for group in groups:
            Id = self.max_activity_id()
            activityroot = self.generate_independent_activities(group, Id)
        
    def read_csv_data(self, csvfile, separator=','):
        s = [line.rstrip().split(separator) for line in open(csvfile, 'r')]
                
        self.contype = s[0].index(self.names["con_type"])
        self.con = s[0].index(self.names["conexion"])
        self.teacher = s[0].index(self.names["teacher_name"])
        self.subject = s[0].index(self.names["subject"])
        self.group = s[0].index(self.names["group"])
        self.totalduration = s[0].index(self.names["total_duration"])
        self.room = s[0].index(self.names["room"])
        self.year = s[0].index(self.names["year"])
        self.building = s[0].index(self.names["building"])
        
        self.raw_data = s[1:]
        
    def generate_from_raw_data(self):
        haut = []
        indep = []
        bilera = []
        lag = []
        zaintzak = []
        
    
        sg = self.generatesubgroups(self.raw_data)
        
        print("Subgroups: ",sg)
        activities = []
        for j in self.raw_data:
            if j[self.contype] in [self.names["meeting"]]:
                activities.append(j)
            else:
                nl = j[:3] + list([self.getgroups(j,sg)]) + j[4:]
                activities.append(nl)
        print("activities: ",activities)

            
        for activity in activities:
            self.roombuilding[activity[self.room]] = activity[self.building]
            self.teachers.add(activity[self.teacher])
            self.rooms.add(activity[self.room])
            self.subjects.add(activity[self.subject])
            self.buildings.add(activity[self.building])
            if activity[self.contype] == self.names["option"]:
                haut.append(activity)
            if activity[self.contype] == self.names["meeting"]:
                bilera.append(activity)
            if activity[self.contype] == self.names["help"]:
                lag.append([activity[self.teacher], activity[self.subject], activity[self.year], activity[self.group], activity[self.totalduration], activity[self.room], activity[self.con]])
            if activity[self.contype] == self.names["indep"]:
                indep.append(activity)
            if activity[self.contype] == self.names["guard"]:
                zaintzak.append(activity)
                
        haug = self.generate_all_option_groups(self.generate_hautazkoak(haut))
        ind = self.generate_all_independent_activities(indep)
        bil = self.generate_all_meetings(self.generate_meetings_groups(bilera))
        lagun = self.generate_all_laguntza(self.generate_laguntza_groups(lag))
        zain = self.generate_guard_activity(zaintzak)
        # print(lg)
        # print(haut)
        # print(bil)
    def generate_guard_activity(self,zaintzak):
                
        Id = self.max_activity_id()
        bulding1guards = 5
        bulding2guards = 5
        
        ActivitiesElement = self.fetxml.find('./Activities_List')
        SpaceConstraintElement = self.fetxml.find('./Space_Constraints_List')
       
        for zaintza in zaintzak:
            for i in range(int(zaintza[self.totalduration])):
                ActivitiesElement.append(self.generate_activity(zaintza, Id, Id, 1))
                
                RoomConstraintElement = ET.Element('ConstraintActivityPreferredRooms')
                WPerElement = ET.SubElement(RoomConstraintElement,'Weight_Percentage')
                WPerElement.text = "100"
                ActIdElement = ET.SubElement(RoomConstraintElement,'Activity_Id')
                ActIdElement.text = str(Id)
                NPerElement = ET.SubElement(RoomConstraintElement,'Number_of_Preferred_Rooms')
                ActiveRElement = ET.SubElement(RoomConstraintElement,'Active')
                ActiveRElement.text = "true"
                ComRElement = ET.SubElement(RoomConstraintElement,'Comments')
                #FIXME: Something more generic, configurable with number of guards and multiple buildins
                if zaintza[self.building] == '1':               
                    NPerElement.text = str(bulding1guards)
                    for i in range(bulding1guards):
                        PRElement = ET.SubElement(RoomConstraintElement,'Preferred_Room')
                        PRElement.text = "Z"+str(i+1)+"-1"
                elif zaintza[self.building] == '2':
                    NPerElement.text = str(bulding2guards)
                    for i in range(bulding2guards):
                        PRElement = ET.SubElement(RoomConstraintElement,'Preferred_Room')
                        PRElement.text = "Z"+str(i+1)+"-2"
                elif zaintza[self.building] == '12':
                    NPerElement.text = str(bulding1guards + bulding2guards)
                    for i in range(bulding1guards):
                        PRElement = ET.SubElement(RoomConstraintElement,'Preferred_Room')
                        PRElement.text = "Z"+str(i+1)+"-1"
                    for i in range(bulding2guards):
                        PRElement = ET.SubElement(RoomConstraintElement,'Preferred_Room')
                        PRElement.text = "Z"+str(i+1)+"-2"
                        
                SpaceConstraintElement.append(RoomConstraintElement)
                Id = Id + 1
        
    def generatesubgroups(self,activities):
        '''
        a = [['Teacher1','tekno','1DBH', '1H',  '3', '1A1', ''], [ 'Teacher2','BE','1DBH','1HI', '2', '1A2', 'x'], ['Teacher3','ERL','1DBH', '1HI',  '2', '1A3', 'x']]
        o = {'1-I': ['1-I-BE', '1-I-ERL'], '1-H': ['1-H-BE', '1-H-ERL']}
        '''
        connectedactivities = self.conexions(activities)
        d = {}
        for conexion in connectedactivities.values():
            group_subjects = self.extract(conexion)
            d = self.mergedics(d,group_subjects)
        subgroups = {}
        for k,v in d.items():
            a = v  #[['BE', 'ERL'], ['Natur', 'CCSS']]
            a.insert(0,[k]) #[['1-I'], ['BE', 'ERL'], ['Natur', 'CCSS']]
            subgroups[k] = self.combine(a) # { '1-I': ['1-I-BE-Natur', '1-I-BE-CCSS', '1-I-ERL-Natur', '1-I-ERL-CCSS']}
        return subgroups
     
    def mergedics(self,d1,d2):
        '''
        Merges two dictionaries
        d1 = {}
        d2 = {'5-I': ['IKT', 'ORAT', 'KulZ'], '5-J': ['IKT', 'ORAT', 'KulZ']}
        newsubgroups.mergedics(d1,d2)
        {'5-I': [['IKT', 'ORAT', 'KulZ']], '5-J': [['IKT', 'ORAT', 'KulZ']]}
     
        d1 = {'5-I': [['IKT', 'ORAT', 'KulZ'], ['tekno', 'FRA', 'ALE', 'MART', 'NAFAR']], '5-J': [['IKT', 'ORAT', 'KulZ'], ['tekno', 'FRA', 'ALE', 'MART', 'NAFAR']]}
        d2 = {'5-H': ['tekno', 'FRA', 'ALE', 'MART', 'NAFAR'], '5-J': ['tekno', 'FRA', 'ALE', 'MART', 'NAFAR'], '5-I': ['tekno', 'FRA', 'ALE', 'MART', 'NAFAR']}
        newsubgroups.mergedics(d1,d2)
        {'5-H': [['tekno', 'FRA', 'ALE', 'MART', 'NAFAR']], '5-I': [['IKT', 'ORAT', 'KulZ'], ['tekno', 'FRA', 'ALE', 'MART', 'NAFAR']], '5-J': [['IKT', 'ORAT', 'KulZ'], ['tekno', 'FRA', 'ALE', 'MART', 'NAFAR']]}
        '''
        if d2 == {}:
                d1,d2 = d2,d1
        k1 = d1.keys()
        k2 = d2.keys()
        d=defaultdict(list)
        for k in k1:
            d[k] = d1[k]
        for k in k2:
            if k not in k1:
                d[k] = [d2[k]]
            elif d2[k] not in d[k]:
                d[k].append(d2[k])
        return d
     
    def conexions(self,activities):
        '''
        takes all subjects and generates conexions
        activities = [['Teacher1','tekno','1DBH', '1H',  '3', '1A1', ''], ['BE', '1HI', 'Teacher2', '2', '1A2', 'x'], ['ERL', '1HI', 'Teacher3', '2', '1A3', 'x']]
        {'x': [['BE', '1HI', 'Teacher2', '2', '1A2', 'x'],['ERL', '1HI', 'Teacher3', '2', '1A3', 'x']]}
        '''
        con = defaultdict(list)
        for activity in activities:
            if (activity[self.con] != '') and (activity[self.contype] not in  ['bilera','zaintza']):
                if any(activity[self.subject] in i[self.subject] for i in  con[activity[self.con]]):
                    raise NameError("Same subject ({}) in a connection ({})".format(activity[self.subject],activity[self.con]))
                    #If this is not checked you get duplicates, for grupos pequeños...
                    #['Begoña', 'Natur', '1DBH', ['1-H-BE-Natur', '1-H-BE-Natur', '1-H-ERL-Natur', '1-H-ERL-Natur'], '4', '1A2', 'z']
                    #['Juanjo', 'Natur', '1DBH', ['1-H-BE-Natur', '1-H-BE-Natur', '1-H-ERL-Natur', '1-H-ERL-Natur', '1-I-BE-Natur', '1-I-ERL-Natur'], '4', '1A3', 'z']
                if any(activity[self.teacher] in i[self.teacher] for i in  con[activity[self.con]]):
                    raise NameError("Same teacher ({}) in a connection ({})".format(activity[self.teacher],activity[self.con]))
                if any(activity[self.room] in i[self.room] for i in  con[activity[self.con]]):
                    raise NameError("Same room ({}) in a connection ({})".format(activity[self.room],activity[self.con]))      
                con[activity[self.con]].append(activity)
        return con
        
    def getgroups(self,activity,sg):
        '''
        activity = ['BE', '1HI', 'Marilen', '2', '1A2', 'x']
        sg = {'1-H': ['1-H-BE', '1-H-ERL'], '1-I': ['1-I-BE', '1-I-ERL']}
        returns ['1-H-BE', '1-I-BE']
          
        Last if...
        activity = ['tekno', '1H', 'Asier', '3', '1A1', '']
        sg = {'1-H': ['1-H-BE', '1-H-ERL'], '1-I': ['1-I-BE', '1-I-ERL']}
        returns ['1-H-BE', '1-H-ERL']
          
        activity = ['Luisa', 'CCSS', '1DBH', '1I', '4', '1A4', 'z']
        sg = {'1-I': ['1-I-BE-Natur', '1-I-BE-CCSS', '1-I-ERL-Natur', '1-I-ERL-CCSS']}
        returns ['1-I-BE-CCSS', '1-I-ERL-CCSS']
        '''
        groups = []
        subgroups = []
        for groupleter in activity[self.group][1:]:
            groups.append(activity[self.group][0]+"-"+groupleter)
        for group in groups:
            for subgroup in sg[group]:
                if ("-"+activity[self.subject] in subgroup) or (activity[self.con]==''):
                    # second par of the or
                    #It's not connected so all subgroups of the group
                    subgroups.append(subgroup)
        return(subgroups)

    def combine(self,groups):
        '''
        Creates all combinations from two or more lists
        combine ([['h'],['erl','be'],['plas','fra','ale']])  
        ['h-erl-plas', 'h-erl-fra', 'h-erl-ale', 'h-be-plas', 'h-be-fra', 'h-be-ale']
        '''     
        l = len(groups)
        if l < 1:
            raise ValueError()
        if l == 1:
            return groups[0]
        c = []
        l1 = groups[0]
        for l2 in groups[1:]:
            for e1 in l1:
                for e2 in l2:
                    if not self.incompatiblegroups(e1[0],e2,e1.split("-"),self.incompatibilities):
                        c.append(str(e1)+"-"+str(e2))
            l1 = c
            c = []
        return l1
    
    def incompatiblegroups(self,course,group,combinations,incompatibilities):
        #returns True if there is an incompatibility among the groups (its not possible to do
        #4th course latin and biology-geology.
        #inputs are course, the subject-group, the list of combinations of subject-groupss
        #and the list of incompatible subjects
        #incompatiblegroups('5', 'Fisika Kimika', {'5', 'H', 'Historia'}, {"5":{"Fisika Kimika":["Historia","Latina","Ekonomia","Matematika GGZZ","Marrazketa Artistikoa"],"Matematika": ["Historia","Latina","Ekonomia","Matematika GGZZ","Marrazketa Artistikoa"]}})
        #print("IN:",course,group,combinations,incompatibilities)
        if course not in  incompatibilities.keys() or group not in incompatibilities[course].keys():
            return False
        if set(combinations).intersection(incompatibilities[course][group]) != set():
            return True
        return False


    def extract(self,activities):
        '''
        Takes connected subjects and returns a dict with the group and the subjects
        activities = [['Teacher6', 'MT', '1BATX', '5HIJ', '4', '1A4', 't'], ['Teacher8', 'BG', '1BATX', '5HIJ', '4', '1A4', 't'], ['Teacher4', 'Latin', '1BATX', '5HIJ', '4', '1A4', 't'], ['Teacher7', 'Ekonomia', '1BATX', '5HIJ', '4', '1A4', 't']]
        extract(b)
        {'5-J': ['MT', 'BG', 'Latin', 'Ekonomia'], '5-H': ['MT', 'BG', 'Latin', 'Ekonomia'], '5-I': ['MT', 'BG', 'Latin', 'Ekonomia']}
        '''
        groups = defaultdict(list)
        for activity in activities:
            if activity[self.con] != '':
                for leter in activity[self.group][1:]:
                    groups[activity[self.group][0]+"-"+leter].append(activity[self.subject])
        return groups
         
     
    def bilatu(self,xmlfile=None):
        d = {}
        if xmlfile:
            tree = ET.parse(xmlfile)
            root = tree.getroot()
        else:
            root = self.fetxml
        for a in  list(set(root.findall('./Students_List/Year/Group/Subgroup/Name'))) :
            if a.text[0] < '5':
                if a.text[0:3] not in d.keys(): d[a.text[0:3]] = []
                d[a.text[0:3]].append(a.text[4:])
        return d
        
    # Functions for importing from a fet file:
    def TeacherssinFile(self,xmlfile):
        """
        Returns the teachers defined in activities from the suplied fet file
        """
        tree = ET.parse(xmlfile)
        root = tree.getroot()
        print(list(set([b.text for b in root.findall(".//Activity/Teacher")])))  # bada ez bada, egin - list(set([a.text for a in self.xmlfile.findall('./Teachers_List')]))
    
    def RoomsinFile(self,xmlfile):
        """
        Returns the rooms defined in activities from the suplied fet file
        """
        tree = ET.parse(xmlfile)
        root = tree.getroot()
        print(list(set([b.text for b in root.findall(".//ConstraintActivityPreferredRoom/Room")])))

    def max_activity_id_from_file(self,xmlfile):
        """
        Returns the max_activity_id that the suplied fet xmlfile has
        """
        tree = ET.parse(xmlfile)
        root = tree.getroot()
        try:
            return max([b.text for b in root.findall(".//Activity/Id")])
        except:
            return "1"
      
    def groups_in_fet_file(self,xmlfile):
        """
        Returns the groups defined in activities from the suplied fet file
        """
        # Years:1,2,3,4,5,6 len=1
        # Groups:1-A,1-B,1-C,  3-Dib!! 3<=len<6
        # Subgroups: 1-A-CCSS,1-A-HA,1-A-LS  6<=len
        tree = ET.parse(xmlfile)
        root = tree.getroot()
        alls = list(set([b.text for b in root.findall(".//Activity/Students")]))
        alls.sort(key=len)
        d = {}
        for g in alls:
            if len(g) == 1 and not g in d:
                d[g] = {}
            if len(g) > 1 and len(g) < 4:
                if g[0] in d and not g in d[g[0]]:
                    d[g[0]][g] = []
                else:
                    d[g[0]] = {}
                    d[g[0]][g] = []
            if len(g) >= 4:
                if not g[0] in d:
                    d[g[0]] = {}
                if not g[0:3] in d[g[0]]:
                    d[g[0]][g[0:3]] = []
                if not g in g[0:3]:
                    d[g[0]][g[0:3]].append(g)
        return d