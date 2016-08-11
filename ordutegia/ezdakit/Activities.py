import csv
import xml.etree.ElementTree 
from xml.etree import ElementTree as ET
import Students

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
def gsa(activities,idm):
   """
   Generates the necesary xml for geneateSimultaneousActivities: the activities,
   rooms,samestartingtime...
   input: 
   activities=[[teacher.subject,hours,room,groups],[..]]
   where: groups=['1-A-OM','1-B-OM','1-C-OM']
   """
   root=ET.Element("root")
   id=int(idm)
   gid=id
   TimeConstraintElement=ET.SubElement(root,"Time_Constraints_List")
   for a in generateStartTime(id,len(activities),int(activities[0][2])):
      TimeConstraintElement.append(a)
   SpaceConstraintElement=ET.SubElement(root,"Space_Constraints_List")
   #Generate Activities  
   ActivitiesElement=ET.SubElement(root,"Activities_List")
   for j in range(len(activities)):
      for a in generateRoom(id,activities[j][3],activities[j][2]):
         SpaceConstraintElement.append(a)
      TimeConstraintElement.append(generateMinDays(id,activities[j][2]))
      activity=activities[j]
      for i in range(int(activity[2])):
         ActivitiesElement.append(generateActivity(activity,id,gid,i,j))
         id+=1
       
   return root


def generateActivity(activity,id,gid,i,j):    
   """Generates a fet activity xml from a tuple formated as: [Teacher,Subject,Total_Duration,Room,[Group(s)]] 
   and the activity id, and activities group id
   Returns
   <Activity>
      <Teacher>Teacher</Teacher>
      <Subject>Subject</Subject>
      <Students>Group1</Students>
      <Students>Groupn</Students>
      <Total_Duration>Total_Duration</Total_Duration>
      <Id>id<Id>
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
   if not isinstance(activity[4], basestring):
      for group in activity[4]:
         Group=ET.SubElement(ActivityElement,"Students")
         Group.text=group   
   else:
      Group=ET.SubElement(ActivityElement,"Students")
      Group.text=activity[4]
   Duration=ET.SubElement(ActivityElement,"Duration")
   Duration.text='1'
   TDuration=ET.SubElement(ActivityElement,"Total_Duration")
   TDuration.text=str(activity[2])
   Id=ET.SubElement(ActivityElement,"Id")
   Id.text=str(id)
   GroupId=ET.SubElement(ActivityElement,"Activity_Group_Id")
   GroupId.text=str(gid+j*int(activity[2]))
   Active=ET.SubElement(ActivityElement,"Active")
   Active.text='true'
   Comments=ET.SubElement(ActivityElement,"Comments")
   Comments.text=' '
   return ActivityElement
       
generateActivity(['Asier','OM',2,'1-A',['1-A-OM','1-B-OM','1-C-OM']],3)

def generateRoom(id,room,number):
   """
   Generates the xml necesary for fet room assignement
   generateRoom(3,'1.A',2)
   id:Activity id
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
   for i in range(id,id+int(number)):
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
       
       
def generateStartTime(id,activitiesnumber,activitiesduration):
   """
   Generates the xml necesary for fet to force several activities
   be at the same time
   id: Id of the first activity (the activitites must be consecutive and alternative
   for 2 sessions of A,B,C ids should be A(1,2),B(3,4),C(5,6)
   activitiesnumber: number of activities that occurs at the same time
   activitiesduration: number of sessions of the activites
   Returns a list with generate conexions
   For input generateStartTime(1,3,2)
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
      for a in range(id,id+activitiesnumber*activitiesduration,activitiesduration):
         Cact=ET.SubElement(Constraint,"Activity_Id")
         Cact.text=str(a)
      CActive=ET.SubElement(Constraint,"Active")
      CActive.text='true'
      CComments=ET.SubElement(Constraint,"Comments")
      CComments.text=' '  
      id+=1
      starttimelist.append(Constraint)
   return starttimelist
 
def generateMinDays(id,number):
   """
   Forces activities not to be in the same day
   id: id of the first activity
   number:number of activities (id must be consecutive)
   For input: generateMinDays(1,3)
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
   for a in range(id,id+int(number)):
      Cact=ET.SubElement(Constraint,"Activity_Id")
      Cact.text=str(a)
   CActive=ET.SubElement(Constraint,"Active")
   CActive.text='true'
   CComments=ET.SubElement(Constraint,"Comments")
   CComments.text=' '  
   return Constraint

#Order and elements in each value of s should match input to geneateSimultaneousActivities
def generateTaldeTxikiak(CSVfile):
   """
   Reads a csv file with the following format:
   department,teacher,subject,year,groups,hours,room,conexion
   returns a list where each element is a connection of subject 
   that should be a the same time, and in each connection wich are
   also list, each element has the format [[teacher.subject,hours,room,groups],[..]]
   [[con1,[[teacher.subject,hours,room,[groups]],[..]],[con2,[[teacher.subject,hours,room,[groups]],[..]]],[...]]
   The groups generated follow this rule:
   If is a simple group (only one letter), the group name is year_letter_G
   If is a mixed group (two letters), groups are [[year-firstletter-P,year-secondletter-P]]
   """
   #Saiatu dictionary erabiliz egiten
   with open(CSVfile,'rb') as csvfile: 
      s=[]
      reader = csv.reader(csvfile,delimiter=',')
      for r in reader:
         v = [r[-1],r[0:-1]]
         if len(r[4])>1:
            v = [r[-1],[r[1].decode('utf-8'),r[2].decode('utf-8'),r[5],r[6],[r[3]+"-"+r[4][0]+"-P",r[3]+"-"+r[4][1]+"-P"]]]
         else:
            v = [r[-1],[r[1].decode('utf-8'),r[2].decode('utf-8'),r[5],r[6],[r[3]+"-"+r[4]+"-G"]]]
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


def generateHautazkoak(CSVfile):
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
   with open(CSVfile,'rb') as csvfile: 
      s=[]
      reader = csv.reader(csvfile,delimiter=',')
      for r in reader:
         v = [r[-1],r[0:-1]]
         Taldeak=[]
         for j in range(len(r[4])):
            Taldeak.append(r[3]+"-"+r[4][j]+"-"+r[2].decode('utf-8'))
         v = [r[-1],[r[1].decode('utf-8'),r[2].decode('utf-8'),r[5],r[6],Taldeak]]
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
     

def generateHautazkoakXML(CSVfile):
   #Saiatu dictionary erabiliz egiten
   with open(CSVfile,'rb') as csvfile: 
      s=[]
      reader = csv.reader(csvfile,delimiter=',')
      connections=ET.Element("connections")
      for r in reader:
         activity=ET.SubElement(connections,"activty")
         for j in range(len(r[4])):
            group=ET.SubElement(activity,"group")
            group.text=(r[3]+"-"+r[4][j]+"-"+r[2].decode('utf-8')
         v = [r[-1],[r[1].decode('utf-8'),r[2].decode('utf-8'),r[5],r[6],Taldeak]]
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
  
def maxActivityId(xmlfile):
   """
   Returns the maxActivityId that the fet xmlfile has
   """
   tree = ET.parse(xmlfile)
   root = tree.getroot()
   try:
      return max([b.text for b in root.findall(".//Activity/Id")])
   except:
      return "1"

def GroupsinFile(xmlfile):
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
      a={}
      if len(g)==1 and not g in d:
         d[g]={}
      if len(g)>=3 and len(g)<6:
         if g[0] in d and not g in d[g[0]]:
            d[g[0]][g]=[]
         else:
            d[g[0]]={}
            d[g[0]][g]=[]
      if len(g)>=6:
         if not g[0] in d:
            d[g[0]]={}
         if not g[0:3] in d[g[0]]:
            d[g[0]][g[0:3]]=[]
         if not g in g[0:3]:
            d[g[0]][g[0:3]].append(g)
   return d

def createGroupsXML(xmlfile):
   """
   Creates the Students section of the fet xml file
   from an fet xml file with activities, by extracting
   activities groups
   """
   groups=GroupsinFile(xmlfile)
   Students=ET.Element("Students_List")
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
    
    
def TeacherssinFile(xmlfile):
   """
   Returns the teachers defined in activities from the suplied fet file
   """
   tree = ET.parse(xmlfile)
   root = tree.getroot()
   print(list(set([b.text for b in root.findall(".//Activity/Teacher")])))
  
def RoomsinFile(xmlfile):
   """
   Returns the rooms defined in activities from the suplied fet file
   """
   tree = ET.parse(xmlfile)
   root = tree.getroot()
   print(list(set([b.text for b in root.findall(".//ConstraintActivityPreferredRoom/Room")])))
  
def generateAllLittleGroups(cvsfile):
   groups=generateTaldeTxikiak(cvsfile)
   id=1#ordeztu fet fitxategikoarekin bada ez bada,  maxActivityId(...fet)
   root=ET.Element("root")
   ActivitiesElement=ET.SubElement(root,"Activities_List")
   TimeConstraintElement=ET.SubElement(root,"Time_Constraints_List")
   SpaceConstraintElement=ET.SubElement(root,"Space_Constraints_List")
   for group in groups:
      print(group)
      activityroot=gsa(group[1:],id)
      for activity in activityroot.findall('.//Activity'):
         ActivitiesElement.append(activity)
      for prefroom in activityroot.findall('.//ConstraintActivityPreferredRoom'):
         SpaceConstraintElement.append(prefroom)
      for sametime in activityroot.findall('.//ConstraintActivitiesSameStartingTime'):
         TimeConstraintElement.append(sametime)
      for mindays in activityroot.findall('.//ConstraintMinDaysBetweenActivities'):
         TimeConstraintElement.append(mindays)
      id+=1
      
   return root

def generateAllChoices(cvsfile):
   groups=generateHautazkoak(cvsfile)
   id=1#ordeztu fet fitxategikoarekin bada ez bada,  maxActivityId(...fet)
   root=ET.Element("root")
   ActivitiesElement=ET.SubElement(root,"Activities_List")
   TimeConstraintElement=ET.SubElement(root,"Time_Constraints_List")
   SpaceConstraintElement=ET.SubElement(root,"Space_Constraints_List")
   for group in groups:
      print(group)
      activityroot=gsa(group[1:],id)
      for activity in activityroot.findall('.//Activity'):
         ActivitiesElement.append(activity)
      for prefroom in activityroot.findall('.//ConstraintActivityPreferredRoom'):
         SpaceConstraintElement.append(prefroom)
      for sametime in activityroot.findall('.//ConstraintActivitiesSameStartingTime'):
         TimeConstraintElement.append(sametime)
      for mindays in activityroot.findall('.//ConstraintMinDaysBetweenActivities'):
         TimeConstraintElement.append(mindays)
      id+=1
      
   return root


def generateAll(hautazkoak,taldetxikiak):
   groups=generateHautazkoak(hautazkoak)+generateTaldeTxikiak(taldetxikiak)
   id=1#ordeztu fet fitxategikoarekin bada ez bada,  maxActivityId(...fet)
   root=ET.Element("root")
   ActivitiesElement=ET.SubElement(root,"Activities_List")
   TimeConstraintElement=ET.SubElement(root,"Time_Constraints_List")
   SpaceConstraintElement=ET.SubElement(root,"Space_Constraints_List")
   for group in groups:
      print(group)
      activityroot=gsa(group[1:],id)
      for activity in activityroot.findall('.//Activity'):
         ActivitiesElement.append(activity)
      for prefroom in activityroot.findall('.//ConstraintActivityPreferredRoom'):
         SpaceConstraintElement.append(prefroom)
      for sametime in activityroot.findall('.//ConstraintActivitiesSameStartingTime'):
         TimeConstraintElement.append(sametime)
      for mindays in activityroot.findall('.//ConstraintMinDaysBetweenActivities'):
         TimeConstraintElement.append(mindays)
      id+=1
      
   return root
   
maxActivityId('/home/asier/Hezkuntza/Irakasle-Ikasgai-Gela-Taldebatzuk.fet')
GroupsinFile('/home/asier/Hezkuntza/Irakasle-Ikasgai-Gela-Taldebatzuk.fet')
RoomsinFile('/home/asier/Hezkuntza/Irakasle-Ikasgai-Gela-Taldebatzuk.fet')
TeacherssinFile('/home/asier/Hezkuntza/Irakasle-Ikasgai-Gela-Taldebatzuk.fet')
createGroupsXML('/home/asier/Hezkuntza/Irakasle-Ikasgai-Gela-Taldebatzuk.fet')

#Lehenengo Sortu Jarduerak
#Jarduerak eta Murrizketak .fet fitxategian idatzi
#Fitxategi horretatik taldeak eskuratu eta egitura sortu createGroupsXML
#Taldeen egitura hori idatzi .fet fitxategian

#Gelak bilatzen ditu, baina eraikinak falta dira. Garrantzitsua da gero murrizketak ezartzeko.

#Berezitasunak: LAguntza duten ikasgaiak Tekno, plastika eta musika.
#2. Batx tutore-Historia
#Koldo eta Merche informatika aldi berean bada ez bada ere.

generateTaldeTxikiak('taldetxikiak.csv') 
generateSimultaneousActivities(generateTaldeTxikiak('taldetxikiak3.csv')[0][1:],5)

 
 
generateSimultaneousActivities(activities,89)

[['a', ['Bego\xc3\xb1a Izquierdo', 'Ciencias Naturales', '3', '1.B', '1-B-G'], ['Eugenio Miranda', 'Ciencias Naturales', '3', '1.AB', '1-AB'], ['Marcelo Otsoa de Etxaguen', 'CCSS', '3', '1.A', '1-A-G']], ['b', ['Eugenio Miranda', 'Ciencias Naturales', '3', '1.A', '1-A-G'], ['Laura Berm\xc3\xbadez', 'CCSS', '3', '1.B', '1-B-G'], ['Luisa Rodr\xc3\xadguez Itinerante', 'CCSS', '3', '1.AB', '1-AB']]]



activities=[['Asier','OM',2,'1-A',['1-A-OM','1-B-OM','1-C-OM']],['Oskia','HA',2,'1-B',['1-A-HA','1-B-HA','1-C-HA']],['Javi','KK',2,'1-C',['1-A-KK','1-B-KK','1-C-KK']]]
generateSimultaneousActivities(activities,8)
activities=[['Asier','OM',2,'1-A',['1-A-OM']],['Oskia','HA',2,'1-B',['1-B-HA']],['Javi','KK',2,'1-C',['1-C-KK']]]
generateSimultaneousActivities(activities,8)

#Fet fitxategiaren hasiera:
#<fet version="5.18.0">

#<Institution_Name>IES Mendillorri BHI</Institution_Name>

#<Comments>Algún comentario</Comments>

#<Hours_List>
	#<Number>8</Number>
	#<Name>08:30-9:25</Name>
	#<Name>09:25-10:20</Name>
	#<Name>10:20-11:15</Name>
	#<Name>11:15-11:45</Name>
	#<Name>11:45-12:40</Name>
	#<Name>12:40-13:35</Name>
	#<Name>13:35-14:30</Name>
	#<Name>14:30-15:20</Name>
#</Hours_List>

#<Days_List>
	#<Number>5</Number>
	#<Name>Astelehena</Name>
	#<Name>Asteartea</Name>
	#<Name>Asteazkena</Name>
	#<Name>Osteguna</Name>
	#<Name>Ostirala</Name>
#</Days_List>
