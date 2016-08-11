import MendiFet as MF
import csv
import codecs
import xml.dom.minidom
import xml.etree.ElementTree 
from xml.etree import ElementTree as ET
import unittest

class TestMendiFet(unittest.TestCase):


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

  def test_generate_activity_one_group(self):
      a=MF.MendiFet()
      activity = ["Teacher","Subject","Total_Duration","Room",["Group"]] 
      ag = a.generate_activity(activity,1,1,1)
      at = ET.fromstring("<Activity><Teacher>Teacher</Teacher><Subject>Subject</Subject><Students>Group</Students><Duration>1</Duration><Total_Duration>Total_Duration</Total_Duration><Id>1</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity>")
      self.assertEqual(ET.tostring(at), ET.tostring(ag))

  def test_generate_activity_two_groups(self):
      a=MF.MendiFet()
      activity = ["Teacher","Subject","Total_Duration","Room",["Group1","Group2"]] 
      ag = a.generate_activity(activity,1,1,1)
      at = ET.fromstring("<Activity><Teacher>Teacher</Teacher><Subject>Subject</Subject><Students>Group1</Students><Students>Group2</Students><Duration>1</Duration><Total_Duration>Total_Duration</Total_Duration><Id>1</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity>")
      self.assertEqual(ET.tostring(at), ET.tostring(ag))


  def test_generate_room(self):
      a = MF.MendiFet()
      rg = a.generate_room(1,"room1",1)
      rt = ET.fromstring("<ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>1</Activity_Id><Room>room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom>")
      self.assertEqual(ET.tostring(rt), ET.tostring(rg[0]))
     
  def test_generate_room_2(self):
      a = MF.MendiFet()
      rg = a.generate_room(1,"room1",2)
      rt1 = ET.fromstring("<ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>1</Activity_Id><Room>room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom>")
      rt2 = ET.fromstring("<ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>2</Activity_Id><Room>room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom>")
      rt = [rt1,rt2]
      self.assertEqual(ET.tostring(rt[0]), ET.tostring(rg[0]))   
      self.assertEqual(ET.tostring(rt[1]), ET.tostring(rg[1]))
 
         
         
  def generate_start_time(self,Id,activitiesnumber,activitiesduration):
      a = MF.MendiFet()
      stg = a.generate_start_time(1,3,1)
      stt = ET.fromstring("<ConstraintActivitiesSameStartingTime><Weight_Percentage>100</Weight_Percentage><Number_of_Activities>3</Number_of_Activities><Activity_Id>1</Activity_Id><Activity_Id>3</Activity_Id><Activity_Id>5</Activity_Id><Active>true</Active><Comments> </Comments></ConstraintActivitiesSameStartingTime>")
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
      
      """

   
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
      >>> generate_independent(1,[["t","s","1","AB",2,"1c3"]])
      [[u't', u's', 2, u'1c3', ['1-AB']]]
      """
      #Saiatu dictionary erabiliz egiten
      s=[]
      for r in activities:
         v = [r[0].decode('utf-8'),r[1].decode('utf-8'),r[4],r[5].decode('utf-8'),[r[2]+"-"+r[3]]]
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
#         print r
         v = [r[-1],[[r[1].decode('utf-8'),r[2].decode('utf-8'),r[4].decode('utf-8'),r[5].decode('utf-8'),r[2].decode('utf-8')+"-"+r[3].decode('utf-8')],[r[0].decode('utf-8')]]]
#         print v
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




if __name__ == '__main__':
    unittest.main()