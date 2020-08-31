import csv
import codecs
import xml.dom.minidom
import xml.etree.ElementTree 
from xml.etree import ElementTree as ET

class MendiFet:

  

   #Lehenengo Sortu Jarduerak
   #Jarduerak eta Murrizketak .fet fitxategian idatzi
   #Fitxategi horretatik taldeak eskuratu eta egitura sortu create_groups_XML
   #Taldeen egitura hori idatzi .fet fitxategian

   #Gelak bilatzen ditu, baina eraikinak falta dira. Garrantzitsua da gero murrizketak ezartzeko.

   #Berezitasunak: LAguntza duten ikasgaiak Tekno, plastika eta musika.
   #2. Batx tutore-Historia
   #Koldo eta Merche informatika aldi berean bada ez bada ere.   
   def __init__(self):
      self.fetxml=ET.fromstring("""   <fet version="5.18.0">
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
        <ConstraintStudentsSetNotAvailableTimes>
	<Weight_Percentage>100</Weight_Percentage>
	<Students>4</Students>
	<Number_of_Not_Available_Times>10</Number_of_Not_Available_Times>
	<Not_Available_Time>
		<Day>Astelehena</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Astelehena</Day>
		<Hour>14:30-15:20</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteartea</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteartea</Day>
		<Hour>14:30-15:20</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteazkena</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteazkena</Day>
		<Hour>14:30-15:20</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Osteguna</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Osteguna</Day>
		<Hour>14:30-15:20</Hour>
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
	<Comments></Comments>
</ConstraintStudentsSetNotAvailableTimes>
<ConstraintStudentsSetNotAvailableTimes>
	<Weight_Percentage>100</Weight_Percentage>
	<Students>1</Students>
	<Number_of_Not_Available_Times>10</Number_of_Not_Available_Times>
	<Not_Available_Time>
		<Day>Astelehena</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Astelehena</Day>
		<Hour>14:30-15:20</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteartea</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteartea</Day>
		<Hour>14:30-15:20</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteazkena</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteazkena</Day>
		<Hour>14:30-15:20</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Osteguna</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Osteguna</Day>
		<Hour>14:30-15:20</Hour>
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
	<Comments></Comments>
</ConstraintStudentsSetNotAvailableTimes>
<ConstraintStudentsSetNotAvailableTimes>
	<Weight_Percentage>100</Weight_Percentage>
	<Students>2</Students>
	<Number_of_Not_Available_Times>10</Number_of_Not_Available_Times>
	<Not_Available_Time>
		<Day>Astelehena</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Astelehena</Day>
		<Hour>14:30-15:20</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteartea</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteartea</Day>
		<Hour>14:30-15:20</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteazkena</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteazkena</Day>
		<Hour>14:30-15:20</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Osteguna</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Osteguna</Day>
		<Hour>14:30-15:20</Hour>
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
	<Comments></Comments>
</ConstraintStudentsSetNotAvailableTimes>
<ConstraintStudentsSetNotAvailableTimes>
	<Weight_Percentage>100</Weight_Percentage>
	<Students>3</Students>
	<Number_of_Not_Available_Times>10</Number_of_Not_Available_Times>
	<Not_Available_Time>
		<Day>Astelehena</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Astelehena</Day>
		<Hour>14:30-15:20</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteartea</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteartea</Day>
		<Hour>14:30-15:20</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteazkena</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteazkena</Day>
		<Hour>14:30-15:20</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Osteguna</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Osteguna</Day>
		<Hour>14:30-15:20</Hour>
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
	<Comments></Comments>
</ConstraintStudentsSetNotAvailableTimes>
<ConstraintStudentsSetNotAvailableTimes>
	<Weight_Percentage>100</Weight_Percentage>
	<Students>5-A</Students>
	<Number_of_Not_Available_Times>10</Number_of_Not_Available_Times>
	<Not_Available_Time>
		<Day>Astelehena</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Astelehena</Day>
		<Hour>14:30-15:20</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteartea</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteartea</Day>
		<Hour>14:30-15:20</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteazkena</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteazkena</Day>
		<Hour>14:30-15:20</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Osteguna</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Osteguna</Day>
		<Hour>14:30-15:20</Hour>
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
	<Comments></Comments>
</ConstraintStudentsSetNotAvailableTimes>
<ConstraintStudentsSetNotAvailableTimes>
	<Weight_Percentage>100</Weight_Percentage>
	<Students>5-B</Students>
	<Number_of_Not_Available_Times>10</Number_of_Not_Available_Times>
	<Not_Available_Time>
		<Day>Astelehena</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Astelehena</Day>
		<Hour>14:30-15:20</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteartea</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteartea</Day>
		<Hour>14:30-15:20</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteazkena</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteazkena</Day>
		<Hour>14:30-15:20</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Osteguna</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Osteguna</Day>
		<Hour>14:30-15:20</Hour>
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
	<Comments></Comments>
</ConstraintStudentsSetNotAvailableTimes>
<ConstraintStudentsSetNotAvailableTimes>
	<Weight_Percentage>100</Weight_Percentage>
	<Students>6-A</Students>
	<Number_of_Not_Available_Times>10</Number_of_Not_Available_Times>
	<Not_Available_Time>
		<Day>Astelehena</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Astelehena</Day>
		<Hour>14:30-15:20</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteartea</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteartea</Day>
		<Hour>14:30-15:20</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteazkena</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteazkena</Day>
		<Hour>14:30-15:20</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Osteguna</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Osteguna</Day>
		<Hour>14:30-15:20</Hour>
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
	<Comments></Comments>
</ConstraintStudentsSetNotAvailableTimes>
<ConstraintStudentsSetNotAvailableTimes>
	<Weight_Percentage>100</Weight_Percentage>
	<Students>6-B</Students>
	<Number_of_Not_Available_Times>10</Number_of_Not_Available_Times>
	<Not_Available_Time>
		<Day>Astelehena</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Astelehena</Day>
		<Hour>14:30-15:20</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteartea</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteartea</Day>
		<Hour>14:30-15:20</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteazkena</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteazkena</Day>
		<Hour>14:30-15:20</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Osteguna</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Osteguna</Day>
		<Hour>14:30-15:20</Hour>
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
	<Comments></Comments>
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
	<Comments></Comments>
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
	<Comments></Comments>
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
	<Comments></Comments>
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
	<Comments></Comments>
</ConstraintStudentsSetNotAvailableTimes>
<ConstraintStudentsSetNotAvailableTimes>
	<Weight_Percentage>100</Weight_Percentage>
	<Students>B</Students>
	<Number_of_Not_Available_Times>10</Number_of_Not_Available_Times>
	<Not_Available_Time>
		<Day>Astelehena</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Astelehena</Day>
		<Hour>14:30-15:20</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteartea</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteartea</Day>
		<Hour>14:30-15:20</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteazkena</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Asteazkena</Day>
		<Hour>14:30-15:20</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Osteguna</Day>
		<Hour>11:15-11:45</Hour>
	</Not_Available_Time>
	<Not_Available_Time>
		<Day>Osteguna</Day>
		<Hour>14:30-15:20</Hour>
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
	<Comments></Comments>
</ConstraintStudentsSetNotAvailableTimes>
         </Time_Constraints_List>
         <Space_Constraints_List>
            <ConstraintBasicCompulsorySpace>
               <Weight_Percentage>100</Weight_Percentage>
               <Active>true</Active>
               <Comments></Comments>
            </ConstraintBasicCompulsorySpace>
         </Space_Constraints_List>
   </fet>""")
      self.raw_data=[]
      
      self.contype=None
      self.con=None
      self.teacher=None
      self.subject=None
      self.group=None
      self.totalduration=None
      self.room=None
      self.year=None
      self.building=None
      
            
      self.rooms={}
      self.names = {"guard": "Zaintza","option":"h","meeting":"Bilera","help":"laguntza","indep":"independiente","con_type":"Tipo","conexion":"Loturak",
                      "teacher_name":"Irakaslea","subject":"Ikasgaia","group":"Taldea","total_duration":"Orduak","room":"Aula","year":"Maila","building":"Eraikina","con3":"ConexiónA3"}
   
   def set_field_name(self,name,cname):
        self.names[name] =  cname
   
   def set_hours(self,hours):
      HoursElement=self.fetxml.find('./Hours_List')
      NumberElement=ET.SubElement(HoursElement,'Number')
      NumberElement.text=str(len(hours))
      for hour in hours:
         HourElement=ET.SubElement(HoursElement,'Name')
         HourElement.text=hour

   def set_days(self,days):
      DaysElement=self.fetxml.find('./Days_List')
      NumberElement=ET.SubElement(DaysElement,'Number')
      NumberElement.text=str(len(days))
      for day in days:
         DayElement=ET.SubElement(DaysElement,'Name')
         DayElement.text=day

   def set_name(self,name):
      NameElement=self.fetxml.find('./Institution_Name')
      NameElement.text=name
   
   def set_comments(self,name):
      CommentsElement=self.fetxml.find('./Comments')
      CommentsElement.text=name
      
   def no_class_hours_mendillorri(self):
      #FIXME
      dena="""        <ConstraintStudentsSetNotAvailableTimes>
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
      TimeConstraintElement=self.fetxml.find('./Time_Constraints_List')
      TimeConstraintElement.append(ET.fromstring(dena))
      #dbh-bach=ET.fromstring("""<ConstraintStudentsSetNotAvailableTimes>
                #<Weight_Percentage>100</Weight_Percentage>
                #<Students></Students>
                #<Number_of_Not_Available_Times>6</Number_of_Not_Available_Times>
                #<Not_Available_Time>
                        #<Day>Astelehena</Day>
                        #<Hour>11:15-11:45</Hour>
                #</Not_Available_Time>
                #<Not_Available_Time>
                        #<Day>Asteartea</Day>
                        #<Hour>11:15-11:45</Hour>
                #</Not_Available_Time>
                #<Not_Available_Time>
                        #<Day>Asteazkena</Day>
                        #<Hour>11:15-11:45</Hour>
                #</Not_Available_Time>
                #<Not_Available_Time>
                        #<Day>Osteguna</Day>
                        #<Hour>11:15-11:45</Hour>
                #</Not_Available_Time>
                #<Not_Available_Time>
                        #<Day>Ostirala</Day>
                        #<Hour>11:15-11:45</Hour>
                #</Not_Available_Time>
                #<Not_Available_Time>
                        #<Day>Astelehena</Day>
                        #<Hour>14:30-15:20</Hour>
                #</Not_Available_Time>
                #<Not_Available_Time>
                        #<Day>Asteartea</Day>
                        #<Hour>14:30-15:20</Hour>
                #</Not_Available_Time>
                #<Not_Available_Time>
                        #<Day>Asteazkena</Day>
                        #<Hour>14:30-15:20</Hour>
                #</Not_Available_Time>
                #<Not_Available_Time>
                        #<Day>Osteguna</Day>
                        #<Hour>14:30-15:20</Hour>
                #</Not_Available_Time>
                #<Not_Available_Time>
                        #<Day>Ostirala</Day>
                        #<Hour>14:30-15:20</Hour>
                #</Not_Available_Time>
                #<Active>true</Active>
                #<Comments/>
        #</ConstraintStudentsSetNotAvailableTimes>""")
      #batx=ET.fromstring("""<ConstraintStudentsSetNotAvailableTimes>
                #<Weight_Percentage>100</Weight_Percentage>
                #<Students></Students>
                #<Number_of_Not_Available_Times>6</Number_of_Not_Available_Times>
                #<Not_Available_Time>
                        #<Day>Astelehena</Day>
                        #<Hour>11:15-11:45</Hour>
                #</Not_Available_Time>
                #<Not_Available_Time>
                        #<Day>Asteartea</Day>
                        #<Hour>11:15-11:45</Hour>
                #</Not_Available_Time>
                #<Not_Available_Time>
                        #<Day>Asteazkena</Day>
                        #<Hour>11:15-11:45</Hour>
                #</Not_Available_Time>
                #<Not_Available_Time>
                        #<Day>Osteguna</Day>
                        #<Hour>11:15-11:45</Hour>
                #</Not_Available_Time>
                #<Not_Available_Time>
                        #<Day>Ostirala</Day>
                        #<Hour>11:15-11:45</Hour>
                #</Not_Available_Time>
                #<Not_Available_Time>
                        #<Day>Ostirala</Day>
                        #<Hour>14:30-15:20</Hour>
                #</Not_Available_Time>
                #<Active>true</Active>
                #<Comments/>
        #</ConstraintStudentsSetNotAvailableTimes>""")
      #TimeConstraintElement=self.fetxml.find('./Time_Constraints_List')
      #for gr in list(set([b.text for b in self.fetxml.findall('.//Students_List/Year/Group/Name')])):
         #if gr[0]<5 | gr[1] not in ('H','I,','J'):
            #StudentsElement=dbh-bach.find('./Students')
         #else:
            #StudentsElement=batx.find('./Students')
            
         #StudentsElement.text=gr #Save to xmlfet...
         #TimeConstraintElement.append(StudentsElement)
         
   def printm(self):
      print(self.prettify(self.fetxml))

   def prettify(self,elem):
      """Return a pretty-printed XML string for the Element.
      """
      rough_string = ET.tostring(elem, 'utf-8')
      reparsed = xml.dom.minidom.parseString(rough_string)
      return reparsed.toprettyxml(indent="\t")

   def write(self,file='mendifetoutput.fet'):
      f=codecs.open(file,'w','utf-8')
      #f.write(ET.tostring(self.fetxml))
      f.write(self.prettify(self.fetxml))
      f.close()
   #f.write(ET.tostring(rot,encoding="utf-8"))
   #X Fitxategi:
   #1. Talde txikiekin
   #2. Hautazkoekin
   #---------Sortu funtzioak---------
   #3. Independiente direnak 
   #4. Bilerak...

   #activities=[[teacher.subject,hours,room,groups],[..]]
   #groups=['1-A-OM','1-B-OM','1-C-OM']
   #activities=[['Asier','OM',2,'1-A',['1-A-OM','1-B-OM','1-C-OM']],['Oskia','HA',2,'1-B',['1-A-HA','1-B-HA','1-C-HA']]]
   def generate_simultaneous_activities(self,activities,idm,tags=None):
      """
      Generates the necesary xml for geneateSimultaneousActivities: the activities,
      rooms,samestartingtime...
      input: 
      activities=[[teacher,subject,hours,room,groups],[..]]
      where: groups=['1-A-OM','1-B-OM','1-C-OM']
      """
      #print("generate_simultaneous_activities")
      #print(idm)
      #print(activities)
      #print("____")
      Id=int(idm)
      gid=Id
      TimeConstraintElement=self.fetxml.find('./Time_Constraints_List')
      if int(activities[0][2]) >= 1: #FIXME: I had problems with 1 hour activities, I don't even understand why this if is here
         if len(activities)>1:
             TimeConstraintElement.append(self.generate_min_days(Id,activities[0][2]))#?
         for a in self.generate_start_time(Id,len(activities),int(activities[0][2])):
            TimeConstraintElement.append(a)
      SpaceConstraintElement=self.fetxml.find('./Space_Constraints_List')
      #Generate Activities  
      ActivitiesElement=self.fetxml.find('./Activities_List')
      for j in range(len(activities)):
         for a in self.generate_room(Id,activities[j][3],activities[j][2]):
            SpaceConstraintElement.append(a)
         #TimeConstraintElement.append(self.generate_min_days(Id,activities[j][2]))
         activity=activities[j]
         for i in range(int(activity[2])):
            ActivitiesElement.append(self.generate_activity(activity,Id,gid,tags=tags))
            Id+=1
         gid=Id
                  
   def generate_independent_activities(self,activities,idm,tags=None):
      """
      Generates the necesary xml for geneateIndependentActivities: the activities,
      rooms,...
      input: 
      activities=[[teacher.subject,hours,room,[groups]]
      #FIXME Taldeak ez daude prozesatuta!!
      """
      #print("generate_independent_activities")
      #print(idm)
      #print(activities)
      #print("____")
      Id=int(idm)
      gid=Id
      duration=1
      days=5 #In case xml not ready
      TimeConstraintElement=self.fetxml.find('./Time_Constraints_List')
      ActivitiesElement=self.fetxml.find('./Activities_List')
      SpaceConstraintElement=self.fetxml.find('./Space_Constraints_List')
      days=len(self.fetxml.findall('./Days_List/Name'))
      hours=int(activities[2])
      if activities[3]=="Trinkete": duration=2  #FIXME: Dirty hack for Gorputz HEziketa in Trinekte
      if  hours>days:
         duration=2
         actamount=int(hours/duration)
         rest=hours%duration
         if actamount <= days: #If activities can be grouped in 2 hours less or equal than days, they 
            #should not be the same day
            TimeConstraintElement.append(self.generate_min_days(Id,actamount))
         else:#Else I create as they where diferrent each one with 2 hours
            activities[2]=2
         for a in self.generate_room(Id,activities[3],hours/duration+rest):
            SpaceConstraintElement.append(a)
         for j in range(actamount):
            ActivitiesElement.append(self.generate_activity(activities,Id,gid,duration,tags=tags))
            Id+=1
            if actamount>days:gid+=1
         if rest != 0:
            if actamount>days:activities[2]=rest
            duration=rest
            ActivitiesElement.append(self.generate_activity(activities,Id,gid,duration,tags=tags))
      else:
         if hours > duration:#Was hours>1, changed for an activity with duration=2?
            TimeConstraintElement.append(self.generate_min_days(Id,activities[2]))#?
         #Generate Activities  
         for a in self.generate_room(Id,activities[3],hours/duration):
            SpaceConstraintElement.append(a)
            #TimeConstraintElement.append(self.generate_min_days(Id,activities[j][2]))
         for i in range(int(hours/duration)):
            ActivitiesElement.append(self.generate_activity(activities,Id,gid,duration,tags=tags))
            Id+=1
#      if rest: ActivitiesElement.append(self.generate_activity(activities,Id,gid,tags=tags))
      
   def group_long_activities(self,hours):
      #FIXME 13 hours: 4,1 =>3-3-3-3-1
      number=None
      mod=None
      DaysElement=self.fetxml.findall('./Days_List/Name')
      for i in range(1,len(DaysElement)+1): #len(self
         print(i)
         number=hours/i
         if number <= 5:
            mod = hours%i
            break
      return number,mod
         
   
   def generate_laguntza_activities(self,activities,idm,tags=None):
      """
      Generates the necesary xml for (some) sessions with multiple teachers: the activities,
      rooms,...
      input: 
      activities=[[teacher,subject,hours,room,[group]],[teacher,subject,hours,room,[group]]]
      [[u'Mariaje Ruiz', u'Tecnolog\xeda (Apoyo)', '1', '', ['1-B']], [u'Pablo Garc\xeda', u'Tecnolog\xeda', '2', 'TailerraAintzira1', ['1-B']]]
      """
      #FIXME Only works for two activities
      #print("generate_laguntza_activities")
      #print(idm)
      #print(activities)
      #print("____")
      #main=[]
      sec=[]
      if activities[0][2]>activities[1][2]:
         main = activities[0]
         sec = activities[1]
      else:
         main = activities[1]
         sec = activities[0]
      Id=int(idm)
      gid=Id
      SpaceConstraintElement=self.fetxml.find('./Space_Constraints_List')
      roms=self.generate_room(Id,main[3],main[2])
      for rom in roms:
         SpaceConstraintElement.append(rom)
      ActivitiesElement=self.fetxml.find('./Activities_List')
      #Generate Activities
      for i in range(int(main[2])):
         ActivityElement=ET.SubElement(ActivitiesElement, "Activity")
         if i==0:
            for teacher in main[0],sec[0]:
               Teacher=ET.SubElement(ActivityElement,"Teacher")
               Teacher.text=teacher
         else:
            Teacher=ET.SubElement(ActivityElement,"Teacher")
            Teacher.text=main[0]
         Subject=ET.SubElement(ActivityElement,"Subject")
         Subject.text=main[1]
         if tags:
          for t in tags:
              Tag=ET.SubElement(ActivityElement,"Activity_Tag")
              Tag.text=t
         Group=ET.SubElement(ActivityElement,"Students")
         Group.text=main[4][0]#shoul be [0][1]
         Duration=ET.SubElement(ActivityElement,"Duration")
         Duration.text='1'
         TDuration=ET.SubElement(ActivityElement,"Total_Duration")
         TDuration.text=str(main[2])
         IdAct=ET.SubElement(ActivityElement,"Id")
         IdAct.text=str(Id)
         GroupId=ET.SubElement(ActivityElement,"Activity_Group_Id")
         GroupId.text=str(gid)
         Active=ET.SubElement(ActivityElement,"Active")
         Active.text='true'
         Comments=ET.SubElement(ActivityElement,"Comments")
         Comments.text=' '
         Id += 1
         
         #print(ET.dump(ActivityElement))
      #print(ET.dump(ActivitiesElement))
      
   def generate_multiple_teachers(self,activities,idm,tags=None):
      """
      Generates the necesary xml for sessions with multiple tfeachers: the activities,
      rooms,...
      input: 
      activities=[[subject,year,hours,room,group],[teachers-list]]
      [[u'Bizikidetza Bilera', u'b', u'1', u'BizikAintzira', u'b'], [u'Amaia Arrieta', u'Ana Astrain', u'Asun Carlos']]
      """
      #print("generate_multiple_teachers")
      #print(idm)
      #print(activities)
      #print("____")
      Id=int(idm)
      gid=0
      SpaceConstraintElement=self.fetxml.find('./Space_Constraints_List')
      #Generate Activities  
      ActivitiesElement=self.fetxml.find('./Activities_List')
      SpaceConstraintElement.append(self.generate_room(Id,activities[0][3],activities[0][2])[0])
      ActivityElement=ET.SubElement(ActivitiesElement, "Activity")
      for teacher in activities[1]:
         Teacher=ET.SubElement(ActivityElement,"Teacher")
         Teacher.text=teacher
      Subject=ET.SubElement(ActivityElement,"Subject")
      Subject.text=activities[0][0]
      if tags:
          for t in tags:
              Tag=ET.SubElement(ActivityElement,"Activity_Tag")
              Tag.text=t
      Group=ET.SubElement(ActivityElement,"Students")
      Group.text=activities[0][4]#FIXME gropus not generated??
      Duration=ET.SubElement(ActivityElement,"Duration")
      Duration.text='1'
      TDuration=ET.SubElement(ActivityElement,"Total_Duration")
      TDuration.text=str(activities[0][2])
      IdAct=ET.SubElement(ActivityElement,"Id")
      IdAct.text=str(Id)
      GroupId=ET.SubElement(ActivityElement,"Activity_Group_Id")
      GroupId.text=str(gid)
      Active=ET.SubElement(ActivityElement,"Active")
      Active.text='true'
      Comments=ET.SubElement(ActivityElement,"Comments")
      Comments.text=' '
               
   def generate_activity(self,activity,Id,gid,duration='1',tags=None):    
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
      ActivityElement=ET.Element("Activity")
      Teacher=ET.SubElement(ActivityElement,"Teacher")
      Teacher.text=activity[0]
      Subject=ET.SubElement(ActivityElement,"Subject")
      Subject.text=activity[1]
      if tags:
          for t in tags:
              Tag=ET.SubElement(ActivityElement,"Activity_Tag")
              Tag.text=t
      if not isinstance(activity[4], str):  #python2-> if not isinstance(activity[4], basestring):
         for group in activity[4]:
            Group=ET.SubElement(ActivityElement,"Students")
            Group.text=group   
      elif activity[4] != '':
         Group=ET.SubElement(ActivityElement,"Students")
         Group.text=activity[4]
      Duration=ET.SubElement(ActivityElement,"Duration")
      Duration.text=str(duration)
      TDuration=ET.SubElement(ActivityElement,"Total_Duration")
      TDuration.text=str(activity[2])
      IdAct=ET.SubElement(ActivityElement,"Id")
      IdAct.text=str(Id)
      GroupId=ET.SubElement(ActivityElement,"Activity_Group_Id")
      GroupId.text=str(gid)
      Active=ET.SubElement(ActivityElement,"Active")
      Active.text='true'
      Comments=ET.SubElement(ActivityElement,"Comments")
      Comments.text=' '
      return ActivityElement
         

   def generate_room(self,Id,room,number):
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
      r=[]
      for i in range(Id,Id+int(number)):
         RoomCElement=ET.Element("ConstraintActivityPreferredRoom")
         RWeight=ET.SubElement(RoomCElement,"Weight_Percentage")
         RWeight.text='100'
         RActivityId=ET.SubElement(RoomCElement,"Activity_Id")
         RActivityId.text=str(i)
         RActivityRoom=ET.SubElement(RoomCElement,"Room")
         RActivityRoom.text=room
         PLActive=ET.SubElement(RoomCElement,"Permanently_Locked")
         PLActive.text='true'
         RActive=ET.SubElement(RoomCElement,"Active")
         RActive.text='true'
         RComments=ET.SubElement(RoomCElement,"Comments")
         RComments.text=' '  
         r.append(RoomCElement)
      return r
         
         
   def generate_start_time(self,Id,activitiesnumber,activitiesduration):
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
      starttimelist=[]
      for i in range(activitiesduration):
         #Generate Starting time Constraint  
         Constraint=ET.Element("ConstraintActivitiesSameStartingTime")
         CWeight=ET.SubElement(Constraint,"Weight_Percentage")
         CWeight.text='100'
         CNumber=ET.SubElement(Constraint,"Number_of_Activities")
         CNumber.text=str(activitiesnumber)
         for a in range(Id,Id+activitiesnumber*activitiesduration,activitiesduration):
            Cact=ET.SubElement(Constraint,"Activity_Id")
            Cact.text=str(a)
         CActive=ET.SubElement(Constraint,"Active")
         CActive.text='true'
         CComments=ET.SubElement(Constraint,"Comments")
         CComments.text=' '  
         Id+=1
         starttimelist.append(Constraint)
      return starttimelist
   
   def generate_min_days(self,Id,number):
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
      Constraint=ET.Element("ConstraintMinDaysBetweenActivities")
      CWeight=ET.SubElement(Constraint,"Weight_Percentage")
      CWeight.text='100'
      CCons=ET.SubElement(Constraint,"Consecutive_If_Same_Day")
      CCons.text='true'
      CNumber=ET.SubElement(Constraint,"Number_of_Activities")
      CNumber.text=str(number)
      for a in range(Id,Id+int(number)):
         Cact=ET.SubElement(Constraint,"Activity_Id")
         Cact.text=str(a)
      CMinDays=ET.SubElement(Constraint,"MinDays")
      CMinDays.text='1'
      CActive=ET.SubElement(Constraint,"Active")
      CActive.text='true'
      CComments=ET.SubElement(Constraint,"Comments")
      CComments.text=' '  
      return Constraint

   def generate_independent(self,activities):
      """
      activities is a list with the following format:
      [[teacher.subject,year,group,hours,room],[..]] 
      teacher,subject,year,groups,hours,room
      returns a list where each element is a subject with formated group:year-group
      """
      #Saiatu dictionary erabiliz egiten
      s=[]
      for r in activities:
         v = [r[0],r[1],r[4],r[5],[r[2]+"-"+r[3]]]
         s.append(v)
      return s

   def generate_meetings_groups(self,activities):
      """
      activities is a list with the following format:
      teacher,subject,year,groups,hours,room,conexion
      returns a list where each element is a connection of teachers 
      that have a meeting a the same time, and in each connection wich are
      also list, each element has the format [[teacher.subject,hours,room,groups],[..]]
      output [[con1,[[subject,year,hours,room,group],[teachers-list]]],[...]]
        activities=[[subject,year,hours,room,group],[teachers-list]]
      """
      #Saiatu dictionary erabiliz egiten
      s=[]
      for r in activities:
         #FIXME: Saiatu bihurtzen jardueran normal bat irakasle askorekin
         #print(r)
         v = [r[-1],[[r[1],r[2],r[4],r[5],"B-"+r[1]],[r[0]]]]
         #v = [r[-1],[[r[1],r[2],r[4],r[5],r[2]+"-"+r[3]],[r[0]]]]
         #print(v)
         for i in range(len(s)):
            if s[i][0] == v[0]:
               s[i][1][1].append(v[1][1][0])
               break
            else:
               if i==len(s)-1:
                  s.append(v)
         if len(s)==0:
            s.append(v)
      return s


   def generate_laguntza_groups(self,activities):
      """
      #FIXME
      activities is a list with the following format:
      teacher,subject,year,groups,hours,room,conexion
      returns a list where each element is a connection of subject 
      that should be at least one session at the same time, 
      and in each connection wich are
      """
      #Saiatu dictionary erabiliz egiten
      s=[]
      for r in activities:
         v = [r[-1],r[0:-1]]
         if len(r[3])>1:
            Taldeak=[]
            for j in range(len(r[3])):
               Taldeak.append(r[2]+"-"+r[3][j]+"-"+r[1])
            v = [r[-1],[[r[0],r[1],r[4],r[5],Taldeak]]]
         else:
            v = [r[-1],[[r[0],r[1],r[4],r[5],[r[2]+"-"+r[3]]]]]
         for i in range(len(s)):
            if s[i][0] == v[0]:
               s[i][1].insert(len(s[i][1]),v[1][0])
               break
            else:
               if i==len(s)-1:
                  s.append(v)
         if len(s)==0:
            s.append(v)
      return s


   def generate_talde_txikiak(self,activities):
      """
      activities is a list with the following format:
      teacher,subject,year,groups,hours,room,conexion
      returns a list where each element is a connection of subject 
      that should be a the same time, and in each connection wich are
      also list, each element has the format [[teacher.subject,hours,room,groups],[..]]
      [[con1,[[teacher.subject,hours,room,[groups]],[..]],[con2,[[teacher.subject,hours,room,[groups]],[..]]],[...]]
      The groups generated follow this rule:
      If is a simple group (only one letter), the group name is year_letter_G
      If is a mixed group (two letters), groups are [[year-firstletter-P,year-secondletter-P]]
      """
      #Saiatu dictionary erabiliz egiten
      s=[]
      for r in activities:
         v = [r[-1],r[0:-1]]
         if len(r[3])>1:
            v = [r[-1],[r[0],r[1],r[4],r[5],[r[2]+"-"+r[3][0]+"-P",r[2]+"-"+r[3][1]+"-P"]]]
         else:
            v = [r[-1],[r[0],r[1],r[4],r[5],[r[2]+"-"+r[3]+"-G"]]]
         for i in range(len(s)):
            if s[i][0] == v[0]:
               s[i].insert(len(s[i]),v[1:][0])
               break
            else:
               if i==len(s)-1:
                  s.append(v)
         if len(s)==0:
            s.append(v)
      return s
      
   def generate_hautazkoak(self,activities):
      """
      Reads a csv file with the following format:
      department,teacher,subject,year,groups,hours,room,conexion
      returns a list where each element is a connection of subject 
      that should be a the same time, and in each connection wich are
      also list, each element has the format [[teacher.subject,hours,room,groups],[..]]
      [[con1,[[teacher.subject,hours,room,[groups]],[..]],[con2,[[teacher.subject,hours,room,[groups]],[..]]],[...]]
      The groups generated follow this rule:
      Groups are [[year-1letter-subject,year-2letter-subject,year-3letter-subject,...]]
      """
      #Saiatu dictionary erabiliz egiten
      s=[]
      for r in activities:
         v = [r[-1],r[0:-1]]
         Taldeak=[]
         for j in range(len(r[3])):
            Taldeak.append(r[2]+"-"+r[3][j]+"-"+r[1])
         v = [r[-1],[r[0],r[1],r[4],r[5],Taldeak]]
         for i in range(len(s)):
            if s[i][0] == v[0]:
               s[i].insert(len(s[i]),v[1:][0])
               break
            else:
               if i==len(s)-1:
                  s.append(v)
         if len(s)==0:
            s.append(v)
      return s
   
   def generate_hautazkoak_XML(self,CSVfile):
      #Saiatu dictionary erabiliz egiten
      with open(CSVfile,'rb') as csvfile: 
         s=[]
         reader = csv.reader(csvfile,delimiter=',')
         connections=ET.Element("connections")
         for r in reader:
            activity=ET.SubElement(connections,"activty")
            for j in range(len(r[4])):
               group=ET.SubElement(activity,"group")
               group.text=(r[3]+"-"+r[4][j]+"-"+r[2])
            v = [r[-1],[r[1],r[2],r[5],r[6],Taldeak]]
            for i in range(len(s)):
               if s[i][0] == v[0]:
                  s[i].insert(len(s[i]),v[1:][0])
                  break
               else:
                  if i==len(s)-1:
                     s.append(v)
            if len(s)==0:
               s.append(v)
      return s
   
   def max_activity_id(self):
      """
      Returns the max_activity_id that the fet xml has
      """
      try:
         return int(max([int(b.text) for b in self.fetxml.findall(".//Activity/Id")]))+1
      except:
         return 1


   def generate_groups_from_activities(self):
      """
      Returns the groups defined in activities from the suplied fet file
      """
      #Years:1,2,3,4,5,6 len=1
      #Groups:1-A,1-B,1-C,  3-Dib!! 3<=len<6
      #Subgroups: 1-A-CCSS,1-A-HA,1-A-LS  6<=len
      #FIXME 4-Div!!included as subgroup of 4-D
      groups = list(set([b.text for b in self.fetxml.findall(".//Activity/Students")]))
      groups.sort(key = len)
      d={}
      for g in groups:
         if len(g)==1 and not g in d:
            d[g]={}
         if len(g)>1 and len(g)<=4:
            if g[0] in d and not g in d[g[0]]:
               d[g[0]][g]=[]
            else:
               d[g[0]]={}
               d[g[0]][g]=[]
         if len(g)>4:
            if not g[0] in d:
               d[g[0]]={}
            if not g[0:3] in d[g[0]]:
               d[g[0]][g[0:3]]=[]
            if not g in g[0:3]:
               d[g[0]][g[0:3]].append(g)
      return d

   def create_groups_XML(self,groups):
      """
      Creates the Students section of the fet xml file
      from an fet xml file with activities, by extracting
      activities groups
      groups:{'1':{'1-k':{'1-k-Al','1-k-Fr'}}}...
      """
      Students=self.fetxml.find('./Students_List')
      for year in groups.keys():
         YearElement=ET.SubElement(Students,"Year")
         YName=ET.SubElement(YearElement,"Name")
         YName.text=year
         YNoS = ET.SubElement(YearElement,'Number_of_Students')
         YNoS.text = "0"
         if groups[year].keys()!=[]:
            for group in groups[year].keys():
               GroupElement=ET.SubElement(YearElement,"Group")
               GName=ET.SubElement(GroupElement,"Name")
               GName.text=group
               GNoS = ET.SubElement(GroupElement,'Number_of_Students')
               GNoS.text = "0"    
               if len(groups[year][group])>0:
                  for sg in groups[year][group]:
                     subgroup=ET.SubElement(GroupElement,'Subgroup')
                     sgname = ET.SubElement(subgroup,'Name')
                     sgname.text =  sg
                     sgNoS = ET.SubElement(subgroup,'Number_of_Students')
                     sgNoS.text = "0"
         
      return Students
      
   
   def generate_tags_from_activities(self):
      """
      Returns the tags defined in activities from the suplied fet file
      """
      TagList = self.fetxml.find('./Activity_Tags_List')
      for tag in  list(set([b.text for b in self.fetxml.findall('.//Activity/Activity_Tag')])):
         Tag = ET.SubElement(TagList,"Activity_Tag")
         TagName = ET.SubElement(Tag,"Name")
         TagName.text = tag
      
     
   def generate_teachers_from_activities(self):
      """
      Returns the teachers defined in activities from the suplied fet file
      """
      TeacherList=self.fetxml.find('./Teachers_List')
      for teacher in  list(set([b.text for b in self.fetxml.findall('.//Activity/Teacher')])):
         Teacher=ET.SubElement(TeacherList,"Teacher")
         TeacherName=ET.SubElement(Teacher,"Name")
         TeacherName.text=teacher

   def generate_subjects_from_activities(self):
      """
      Returns the teachers defined in activities from the suplied fet file
      """
      SubjectsList=self.fetxml.find('./Subjects_List')
      for subject in  list(set([b.text for b in self.fetxml.findall('.//Activity/Subject')])):
         Subjects=ET.SubElement(SubjectsList,"Subject")
         SubjectsName=ET.SubElement(Subjects,"Name")
         SubjectsName.text=subject


   def generate_rooms_from_activities(self):
      """
      Returns the teachers defined in activities from the suplied fet file
      """
      RoomsList=self.fetxml.find('./Rooms_List')
      for room in list(set([b.text for b in self.fetxml.findall('.//ConstraintActivityPreferredRoom/Room')])):#Eraikinak  -list(set([a.text for a in self.xmlfile.findall('./Room/Name')]))
         if room =='':
             continue
         Room=ET.SubElement(RoomsList,"Room")
         RoomName=ET.SubElement(Room,"Name")
         RoomName.text=room
         RoomBuilding=ET.SubElement(Room,"Building")
         RoomBuilding.text=room[0]#self.rooms[room]
      for room in list(set([b.text for b in self.fetxml.findall('.//ConstraintActivityPreferredRooms/Preferred_Room')])):
         if room =='':
             continue
         Room=ET.SubElement(RoomsList,"Room")
         RoomName=ET.SubElement(Room,"Name")
         RoomName.text=room
         RoomBuilding=ET.SubElement(Room,"Building")
         RoomBuilding.text=room[0]#self.rooms[room]

   def generate_buildings_from_rooms(self):
      """
      Caution,rooms could not have building text!!
      """
      BuildingsList=self.fetxml.find('./Buildings_List')
      for bulding in list(set([b.text for b in self.fetxml.findall('.//Rooms_List/Room/Building')])):
         print(bulding)
         Building=ET.SubElement(BuildingsList,"Building")
         BuildingName=ET.SubElement(Building,"Name")
         BuildingName.text=bulding

   def generate_guard_activity(self,zaintzak,tags=None):
                
        Id = self.max_activity_id()
        bulding1guards = 5 #FIXME: Not hardcoded
        bulding2guards = 5
        
        ActivitiesElement = self.fetxml.find('./Activities_List')
        SpaceConstraintElement = self.fetxml.find('./Space_Constraints_List')
       
        for zaintza in zaintzak:
            for i in range(int(zaintza[self.totalduration])):
                print(zaintza)

                ActivitiesElement.append(self.generate_activity([zaintza[6],zaintza[2],1,"","",zaintza[9]], Id, Id, 1,tags=["alumnado","guardia"]))
                #generate activity: [Teacher,Subject,Total_Duration,Room,[Group(s)]] 
                
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
                        PRElement.text = "1_Z"+str(i+1)
                elif zaintza[self.building] == '2':
                    NPerElement.text = str(bulding2guards)
                    for i in range(bulding2guards):
                        PRElement = ET.SubElement(RoomConstraintElement,'Preferred_Room')
                        PRElement.text = "2_Z"+str(i+1)
                elif zaintza[self.building] == '12':
                    NPerElement.text = str(bulding1guards + bulding2guards)
                    for i in range(bulding1guards):
                        PRElement = ET.SubElement(RoomConstraintElement,'Preferred_Room')
                        PRElement.text = "1_Z"+str(i+1)
                    for i in range(bulding2guards):
                        PRElement = ET.SubElement(RoomConstraintElement,'Preferred_Room')
                        PRElement.text = "2_Z"+str(i+1)
                        
                SpaceConstraintElement.append(RoomConstraintElement)
                Id = Id + 1
        

   def generate_all_laguntza(self,groups):
      for group in groups:
         Id=self.max_activity_id()
         self.generate_laguntza_activities(group[1],Id,tags=["alumnado","apoyo","clase"])
         
   def generate_all_meetings(self,groups):
      for group in groups:
         Id=self.max_activity_id()
         self.generate_multiple_teachers(group[1],Id,tags=["reunión"])
   
   def generate_all_little_groups(self,groups):
      for group in groups:
         Id=self.max_activity_id()
         activityroot=self.generate_simultaneous_activities(group[1:],Id,tags=["alumnado","clase"])
   #FIXME Both functions are equal, should be merged
   def generate_all_option_groups(self,groups):
      for group in groups:
         Id=self.max_activity_id()
         activityroot=self.generate_simultaneous_activities(group[1:],Id,tags=["alumnado","clase"])

   def generate_all_independent_activities(self,groups,tags=None):
      if tags == None:
          tags = ["alumnado","clase"]
      for group in groups:
         Id=self.max_activity_id()
         activityroot=self.generate_independent_activities(group,Id,tags)
      
   def read_csv_data(self,csvfile,separator=','):
      s=[line.rstrip().split(separator) for line in open(csvfile,'r')]
      
      
      self.contype=s[0].index(self.names['con_type'])
      self.con=s[0].index(self.names['conexion'])
      self.teacher=s[0].index(self.names['teacher_name'])
      self.subject=s[0].index(self.names['subject'])
      self.group=s[0].index(self.names['group'])
      self.totalduration=s[0].index(self.names['total_duration'])
      self.room=s[0].index(self.names['room'])
      self.year=s[0].index(self.names['year'])
      self.building=s[0].index(self.names['building'])
      
      self.raw_data=s[1:]
      
   def generate_from_raw_data(self):
      tt=[]
      haut=[]
      indep=[]
      con3 = []
      bilera=[]
      lag=[]
      zaintzak = []
      
      for activity in self.raw_data:
         self.rooms[activity[self.room]]=activity[self.building]
         #if activity[self.room]:
            #self.rooms[activity[self.room]]=activity[self.room][0]
         if activity[self.contype]=="tt":
            tt.append([activity[self.teacher],activity[self.subject],activity[self.year],activity[self.group],activity[self.totalduration],activity[self.room],activity[self.con]])
         if activity[self.contype]==self.names["option"]:
            haut.append([activity[self.teacher],activity[self.subject],activity[self.year],activity[self.group],activity[self.totalduration],activity[self.room],activity[self.con]])
         if activity[self.contype]==self.names["meeting"]:
            bilera.append([activity[self.teacher],activity[self.subject],activity[self.year],activity[self.group],activity[self.totalduration],activity[self.room],activity[self.con]])
         if activity[self.contype]==self.names["help"]:
            lag.append([activity[self.teacher],activity[self.subject],activity[self.year],activity[self.group],activity[self.totalduration],activity[self.room],activity[self.con]])
         if activity[self.contype]==self.names["indep"]:
            indep.append([activity[self.teacher],activity[self.subject],activity[self.year],activity[self.group],activity[self.totalduration],activity[self.room]])
         if activity[self.contype] == self.names["guard"]:
            zaintzak.append(activity)
         if activity[self.contype]==self.names["con3"]:
            con3.append([activity[self.teacher],activity[self.subject],activity[self.year],activity[self.group],activity[self.totalduration],activity[self.room]])

            
      lg=self.generate_all_little_groups(self.generate_talde_txikiak(tt))
      haug=self.generate_all_option_groups(self.generate_hautazkoak(haut))
      ind=self.generate_all_independent_activities(self.generate_independent(indep))
      c3=self.generate_all_independent_activities(self.generate_independent(con3),["alumnado","clase","C3"])
      bil=self.generate_all_meetings(self.generate_meetings_groups(bilera))
      lagun=self.generate_all_laguntza(self.generate_laguntza_groups(lag))
      zain = self.generate_guard_activity(zaintzak)
      #print(lg)
      #print(haut)
      #print(bil)
      
   def bilatu(self):
      d={}
      for a in  list(set(root.findall('./Students_List/Year/Group/Subgroup/Name'))) :
         if a.text[0]<'5':
            if a.text[0:3] not in d.keys(): d[a.text[0:3]]=[]
            d[a.text[0:3]].append(a.text[4:])
      return d
      
   #Functions for importing from a fet file:
   def TeacherssinFile(xmlfile):
      """
      Returns the teachers defined in activities from the suplied fet file
      """
      tree = ET.parse(xmlfile)
      root = tree.getroot()
      print(list(set([b.text for b in root.findall(".//Activity/Teacher")])))#bada ez bada, egin - list(set([a.text for a in self.xmlfile.findall('./Teachers_List')]))
   
   def RoomsinFile(xmlfile):
      """
      Returns the rooms defined in activities from the suplied fet file
      """
      tree = ET.parse(xmlfile)
      root = tree.getroot()
      print(list(set([b.text for b in root.findall(".//ConstraintActivityPreferredRoom/Room")])))

   def max_activity_id_from_file(xmlfile):
      """
      Returns the max_activity_id that the suplied fet xmlfile has
      """
      tree = ET.parse(xmlfile)
      root = tree.getroot()
      try:
         return max([b.text for b in root.findall(".//Activity/Id")])
      except:
         return "1"
     
   def groups_in_fet_file(xmlfile):
      """
      Returns the groups defined in activities from the suplied fet file
      """
      #Years:1,2,3,4,5,6 len=1
      #Groups:1-A,1-B,1-C,  3-Dib!! 3<=len<6
      #Subgroups: 1-A-CCSS,1-A-HA,1-A-LS  6<=len
      tree = ET.parse(xmlfile)
      root = tree.getroot()
      all = list(set([b.text for b in root.findall(".//Activity/Students")]))
      all.sort(key = len)
      d={}
      for g in all:
         if len(g)==1 and not g in d:
            d[g]={}
         if len(g)>1 and len(g)<4:
            if g[0] in d and not g in d[g[0]]:
               d[g[0]][g]=[]
            else:
               d[g[0]]={}
               d[g[0]][g]=[]
         if len(g)>=4:
            if not g[0] in d:
               d[g[0]]={}
            if not g[0:3] in d[g[0]]:
               d[g[0]][g[0:3]]=[]
            if not g in g[0:3]:
               d[g[0]][g[0:3]].append(g)
      return d

   #['Mintegia', 'Izena', 'Ikasgaia', 'Maila', 'Taldea', 'Orduak', 'Gela', 'Konexion', 'Eraikina', 'Mota']

   #<ConstraintStudentsSetNotAvailableTimes>
        #<Weight_Percentage>100</Weight_Percentage>
        #<Students>5-I</Students>
        #<Number_of_Not_Available_Times>6</Number_of_Not_Available_Times>
        #<Not_Available_Time>
                #<Day>Astelehena</Day>
                #<Hour>11:15-11:45</Hour>
        #</Not_Available_Time>
        #<Not_Available_Time>
                #<Day>Asteartea</Day>
                #<Hour>11:15-11:45</Hour>
        #</Not_Available_Time>
        #<Not_Available_Time>
                #<Day>Asteazkena</Day>
                #<Hour>11:15-11:45</Hour>
        #</Not_Available_Time>
        #<Not_Available_Time>
                #<Day>Osteguna</Day>
                #<Hour>11:15-11:45</Hour>
        #</Not_Available_Time>
        #<Not_Available_Time>
                #<Day>Ostirala</Day>
                #<Hour>11:15-11:45</Hour>
        #</Not_Available_Time>
        #<Not_Available_Time>
                #<Day>Ostirala</Day>
                #<Hour>14:30-15:20</Hour>
        #</Not_Available_Time>
        #<Active>true</Active>
        #<Comments></Comments>
#</ConstraintStudentsSetNotAvailableTimes>
