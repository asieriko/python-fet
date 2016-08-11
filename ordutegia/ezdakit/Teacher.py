import xml.etree.ElementTree 
from xml.etree import ElementTree as ET

class Teacher:
  def setName(self, name):
    self.name = name
  def setShortName(self, shortname):
    self.shortname = shortname
  def setID(self, idt):
    self.idt = idt
  def setDepartment(self, dept):
    self.department = dept
  def getName(self):
    return self.name
  def getCode(self):
    return self.idt
  def getDepartment(self):
    return self.department
  
  def addTeacher(self,idt,name,shortname,dept):
    self.name = name
    self.shortname = shortname
    self.idt = idt
    self.department = dept
  
  def printTeacher(self):
    print self.shortname + ": " + self.name + " ("  + self.department + ")"

  def fromEducaXML2(self,xml):
    teacher = xml
    self.idt = teacher.get('ID')
    self.shortName = teacher.get('ABREV')
    self.name = teacher.get('NOMBRE')
    self.department = teacher.get('DEPART')
  
  def fromEducaXML(self,xml):
    teacher = ET.fromstring(xml)
    self.idt = teacher.get('ID')
    self.shortName = teacher.get('ABREV')
    self.name = teacher.get('NOMBRE')
    self.department = teacher.get('DEPART')
    
  def toEducaXML(self):
    subject=ET.Element('PROFF')
    subject.set('ID',self.idt)
    subject.set('ABREV',self.shortName)
    subject.set('NOMBRE',self.name)
    subject.set('DEPART',self.department)
    return ET.dump(subject)
        
  def toFetXML(self):
    teacher=ET.Element('Teacher')
    nteachername = ET.SubElement(teacher,'Name')#,teacher.attrib)
    nteachername.text =  self.name
    return ET.dump(teacher)
  
class Subject:
  def setName(self,name):
    self.name = name
  def setId(self,idr):
    self.idr = idr
  def setAula(self,aula):
    self.aula = aula
  def setAula1(self,a1):
    self.aula1 = a1
  def setAula2(self,a2):
    self.aula2 = a2
  def setAula3(self,a3):
    self.aula3 = a3
  def setAula4(self,a4):
    self.aula4 = a4
  def setBuilding(self,building):
    self.building = building
  def setGrup(self,group):
    self.grup = group
  def setNalum(self,nalum):
    self.nalum = nalum
  def setTeacher(self,teacher):
    self.teacher = teacher
  def setType(self,subjtype):
    self.subjtype = subjtype
  def setHours(self,hours):
    self.hours = hours
  
  def fromEducaXML(self,xml):
    subject = ET.fromstring(xml)
    self.idr = subject.get('ID')
    self.name = subject.get('ASIG')
    self.aula = subject.get('AULA')
    self.building = subject.get('EDIFICIO')
    self.teacher = subject.get('PROF')
    self.subjtype = subject.get('TIPO')
    self.hours = subject.get('HORASEM')
    self.nalum = subject.get('NALUM')
    self.grup = subject.get('GRUP')
    self.aula1 = subject.get('AULA1')
    self.aula2 = subject.get('AULA2')
    self.aula3 = subject.get('AULA3')
    self.aula4 = subject.get('AULA4')
  
  
  def fromEducaXML2(self,xml):
    subject = xml
    self.idr = subject.get('ID')
    self.name = subject.get('ASIG')
    self.aula = subject.get('AULA')
    self.building = subject.get('EDIFICIO')
    self.teacher = subject.get('PROF')
    self.subjtype = subject.get('TIPO')
    self.hours = subject.get('HORASEM')
    self.nalum = subject.get('NALUM')
    self.grup = subject.get('GRUP')
    self.aula1 = subject.get('AULA1')
    self.aula2 = subject.get('AULA2')
    self.aula3 = subject.get('AULA3')
    self.aula4 = subject.get('AULA4')
    
  def toEducaXML(self):
    subjects=ET.Element('ASIGF')
    subjects.set('ID',self.idr)
    subjects.set('ASIG',self.name)
    subjects.set('AULA',self.aula)
    subjects.set('AULA1',self.aula1)
    subjects.set('AULA2',self.aula2)
    subjects.set('AULA3',self.aula3)
    subjects.set('AULA4',self.aula4)
    subjects.set('EDIFICIO',self.building)
    subjects.set('GRUP',self.grup)
    subjects.set('NALUM',self.nalum)
    subjects.set('PROF',self.teacher)
    subjects.set('TIPO',self.subjtype)
    subjects.set('HORASEM',self.hours)
    return ET.dump(subjects)
        
        
class SubjectNames:
  def setName(self,name):
    self.name = name
  def setId(self,ids):
    self.ids = ids
  def setShortName(self,shortname):
    self.shortname = shortname
  def setActive(self,active):
    self.active = active
    
  def fromEducaXML(self,xml):
    subject = ET.fromstring(xml)
    self.ids = subject.get('ID')
    self.shortName = subject.get('ABREV')
    self.name = subject.get('NOMBRE')
    self.active = subject.get('ACTIV')
    
  def toEducaXML(self):
    subject=ET.Element('ASIGF')
    subject.set('ID',self.ids)
    subject.set('ABREV',self.shortName)
    subject.set('NOMBRE',self.name)
    subject.set('ACTIV',self.active)
    return ET.dump(subject)
        
 
 
class Groups:
  def setName(self,name):
    self.name = name
  def setId(self,ids):
    self.ids = ids
  def setShortName(self,shortname):
    self.shortname = shortname
  def setActive(self,active):
    self.active = active
    
  def fromEducaXML(self,xml):
    group = ET.fromstring(xml)
    self.ids = group.get('ID')
    self.shortName = group.get('ABREV')
    self.name = group.get('NOMBRE')
    self.active = group.get('ACTIV')
    
  def toEducaXML(self):
    group=ET.Element('GROUPF')
    group.set('ID',self.idg)
    group.set('ABREV',self.shortName)
    group.set('CURSO',self.course)
    group.set('GRUPO',self.group)
    group.set('MAXALUM',self.maxsutdents)
    group.set('NIVEL',self.level)
    group.set('TURNO',self.lang)
    group.set('DESCRIP',self.desc)
    return ET.dump(group)
  
  
class timetable:
  def __init__(self):
    self.teachers = []
    self.subjects = []
    self.subjectnames = []
    self.rooms = []
    self.groups = []
  
  def importEducaXML(self,xmlfile):
    tree = ET.parse(xmlfile)
    for teacher in tree.iter('PROFF'):
      t = Teacher()
      t.fromEducaXML2(teacher)
      self.teachers.append(t)
    for subject in tree.iter('PROFF'):
      s = Subject()
      s.fromEducaXML2(subject)
      self.subjects.append(s)
    print self.teachers[0].getName()
    
  def printFet(self):
    newteachers=ET.Element('Teachers_List')
    for teacher in self.teachers:
      nteacher = ET.SubElement(newteachers, 'Teacher')
      nteachername = ET.SubElement(nteacher,'Name')#,teacher.attrib)
      nteachername.text = teacher.getName()
      
    newsubjects=ET.Element('Subjects_List')
    for teacher in self.subjects:
      nteacher = ET.SubElement(newsubjects, 'Subject')
      nteachername = ET.SubElement(nteacher,'Name')#,teacher.attrib)
      nteachername.text = teacher.name
      
    ET.dump(newteachers)
    ET.dump(newsubjects)
    
    
class result():
  def __init__(self):
    self.solucion = []
  def loadFetTeachersFile(self,teachersFile):
    tree = ET.parse(teachersFile)
    root = tree.getroot()
    for teacher in root:
      name = teacher.get('name')
      for day in teacher:
	dayn = day.get('name')
	for hour in day:
	  if len(hour)>0:
	    hourn= hour.get('name')
	    for value in hour.iter():
	      if value.tag=='Subject':
		sub=value.get('name')
	      if value.tag=='Students':
		group=value.get('name')
	      if value.tag=='Room':
		room=value.get('name')
	    self.solucion.append(dict([('ASIG', sub),('AULA', room),('CODGRUPO', group),('DIA', dayn), ('HORA', hourn), ('PROF', name),('SESIONES','1' ),('TAREA','')]))
  def printList(self):
    for activity in self.solucion:
      print activity
      
  def printEducaXML(self):
    xmlsolucion=ET.Element('SOLUCT')
    for solf in self.solucion:
      solucf = ET.SubElement(xmlsolucion,'SOLUCF')
      solucf.attrib = solf
      
    return ET.dump(xmlsolucion)
   

r=result()    
r.loadFetTeachersFile('/home/asier/fet-results/timetables/untitled-single/untitled_teachers.xml')
r.printList()
r.printEducaXML()

subj='<Subject name="1ING"></Subject><Students name="1BH"></Students><Room name="1B(108)"></Room>'
	  
	  
	  
    #teachers = tree.find('/Teachers_Timetable')
    #for teacher in teachers:
      
      
      #tree=ET.parse('/home/asier/fet-results/timetables/untitled-single/untitled_teachers.xml')
    
    #def getBuildings(tree):
    #rooms = tree.find('/AULAT')
    #buildings = set([child.get('EDIFICIO') for child in rooms])
    #newbuildings=ET.Element('Buildings_List')
    
sol='<SOLUCF ASIG="2TEK" AULA="220" CODGRUPO="2I" CURSO="2" DIA="1" GRUPO="I" HORA="4" NIVEL="ESO" PROF="TK01" SESIONES="1" TAREA="" TURNO="D"/>'    
#for teacher in solution, ... badago lerro bat saio bakoitzeko, eta bikoizketa bada bi
mbilera='<SOLUCF ASIG="RMTK" AULA="" CODGRUPO="" CURSO="" DIA="5" GRUPO="" HORA="5" NIVEL="" PROF="TK01" SESIONES="1" TAREA="" TURNO=""/>'
kpb='<SOLUCF ASIG="RCCP" AULA="" CODGRUPO="" CURSO="" DIA="3" GRUPO="" HORA="5" NIVEL="" PROF="MA02" SESIONES="1" TAREA="" TURNO=""/>'
g='<GRUPF ID="1" ABREV="1A" CURSO="1" GRUPO="A" MAXALUM="0" NIVEL="ESO" TURNO="D" DESCRIP=""/>'
      
Asier = Teacher()         
Asier.addTeacher("Asier Urio","TK-09","Teknologia","")
Asier.printTeacher()

asig = '<ASIGF ID="1" ASIG="2NTP" AULA="201" AULA1="" AULA2="" AULA3="" AULA4="" EDIFICIO="2" GRUP="2H" NALUM="" PROF="BG01" TIPO="" HORASEM="3"/>'
a=Subject()
a.fromEducaXML('<ASIGF ID="1" ASIG="2NTP" AULA="201" AULA1="" AULA2="" AULA3="" AULA4="" EDIFICIO="2" GRUP="2H" NALUM="" PROF="BG01" TIPO="" HORASEM="3"/>')
print a.toEducaXML()

sa='<NOMASIGF ID="1" ABREV="1ALE" NOMBRE="1_ALEMAN" ACTIV="1"/>'        
sn=SubjectNames()
sn.fromEducaXML('<NOMASIGF ID="1" ABREV="1ALE" NOMBRE="1_ALEMAN" ACTIV="1"/>')
sn.toEducaXML()

te='  <PROFF ID="1" ABREV="AL01" NOMBRE="Javier Beitia" DEPART="Aleman"/>'
Asier.fromEducaXML('<PROFF ID="1" ABREV="AL01" NOMBRE="Javier Beitia" DEPART="Aleman"/>')
Asier.toEducaXML()

tt=timetable()
tt.importEducaXML("../../educapolita.xml")
tt.printFet()