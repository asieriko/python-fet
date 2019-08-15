import csv
import os
import time
import xml.dom.minidom
from xml.etree import ElementTree as ET
from datetime import datetime
from itertools import chain
# import datuak
# educaren soluziotik, dictionary bat egin(irakasle-talde-gela) eta zenbatu, hori izango da ikasgaian jarri behar den balioa.
# agina interaktiboki izen batzuk jarri

# buildings=datuak.buildings
# teachers=datuak.irakasleak
# orduak=datuak.orduak
# egunak=datuak.egunak
# ikasgaiak=datuak.ikasgaiak


class Fet2EDUCA():

    def generate_all(self):
        self.DIV_GROUPS = ['2-P','2P','3-L','3L','3-D', '3D']
        dir_path = "/home/asier/Hezkuntza/python-hezkuntza/python-fet/17-18-data/"
        self.teachers = self.load_teacher_file(os.path.join(dir_path, "irakasle.csv"))
        '''teachers
        'Koldo Bermejo': {'ABREV': 'TK_03', 'DEPART': 'Teknologia', 'NOMBRE': 'Koldo Bermejo'},
        'Andoni Tolosa': {'ABREV': 'MA_01', 'DEPART': 'Matematika', 'NOMBRE': 'Andoni Tolosa'},
        '''
        self.buildings = self.load_rooms_file(os.path.join(dir_path, "gelak.csv"))
        '''buildings
        '0D6': {'ABREV': '0D6', 'EDIFICIO': '1', 'NOMBRE': '30000'},
        '203': {'ABREV': '203', 'EDIFICIO': '2', 'NOMBRE': '30000'},
        '''
        self.subjects = self.load_subjects_file(os.path.join(dir_path, "subjects.csv"))
        '''subjects
        'Mintegi Bilera FK': {'ABREV': 'MB', 'NOMBRE': 'Mintegi Bilera'},
        'Artearen Hª': {'ABREV': 'ARTH', 'NOMBRE': 'Artearen Historia'},
        '''
        self.hours = {'08:30-9:25': 1, '09:25-10:20': 2, '10:20-11:15': 3, '11:15-11:45': 4, '11:45-12:40': 5, '12:40-13:35': 6, '13:35-14:30': 7,  '14:30-15:20': 8}
        self.days = {'Astelehena': 1, 'Asteartea': 2, 'Asteazkena': 3, 'Osteguna': 4, 'Ostirala': 5}
        
        
        self.groups,self.teacherSession, self.teacherGroup = self.extract_teachers_file(os.path.join(dir_path, "teachers.xml"))
        '''groups
        '1L': {'ABREV': '1L', 'CURSO': '1', 'GRUPO': '1.L'},
        '6B': {'ABREV': '6B', 'CURSO': '6', 'GRUPO': '6.B'},
        '''
        
        
        self.adic = self.extract_asigf_from_groups(self.teacherSession)
        ''' adic
        '3CÁngel GálvezTutoretza2D9': {'Teacher': 'Ángel Gálvez', 'Subject': 'Tutoretza', 'Room': '2D9', 'Group': '3C', 'Count': 1},
        'Uxue MacuaZaintza63': {'Teacher': 'Uxue Macua', 'Count': 1, 'Group': 'b', 'Room': '', 'Subject': 'Zaintza'},
        '''
        # It seems that all the info in adic is already in grdic
        
        
        self.tree = ''
        self.create_educa_xml()
        self.root = self.tree.getroot()
        self.create_soluct_xml(self.teacherSession)
        self.create_asigt_xml()
        self.create_proft_xml()
        self.create_grupt_xml()
        self.create_aulat_xml()
        self.create_nomasigt_xml()
        self.write_educa_xml()

    # LOAD Data!
    def load_teacher_file(self, CSVfile="irakasle.csv", interactive=False):
        print("loading teachers names and posts from: ",CSVfile)
        # Besterik gabe, irakasleen hiztegia egiteko.
        # FIXME: Uste dut ez dela erabiltzen...
        teachers = {}
        with open(CSVfile, 'rt') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for r in reader:
                teacher = {}
                if interactive:
                    iz = input("Izena: [" + r[0] + "]:")
                    if iz != "":
                        teacher['NOMBRE'] = iz
                else:
                    teacher['NOMBRE'] = r[0]
                teacher['ABREV'] = r[2]
                teacher['DEPART'] = r[1]
                teachers[r[0]] = teacher
        return teachers

    def load_rooms_file(self, CSVfile="gelak.csv", interactive=False):
        print("loading rooms names and buildings from: ",CSVfile)
        # FIXME: Uste dut ez dela erabiltzen...
        rooms = {}
        with open(CSVfile, 'rt') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for r in reader:
                room = {}
                room['EDIFICIO'] = r[2]
                room['ABREV'] = r[0]
                room['NOMBRE'] = r[1]
                rooms[r[0]] = room
        return rooms

    def load_subjects_file(self, CSVfile="subjects.csv", interactive=False):
        print("loading subjects names and data from: ",CSVfile)
        # FIXME: Uste dut ez dela erabiltzen...
        subjects = {}
        with open(CSVfile, 'rt') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for r in reader:
                subject = {}
                subject['ABREV'] = r[2]
                subject['NOMBRE'] = r[1]
                subjects[r[0]] = subject
        return subjects

    

    def extract_asigf_from_groups(self,grdic):
        ''' 
        From a dic for each activity-hour, creates a new dict for each set-activity-group with the count of how many sessions are
        in dic:u'M\xaa \xc1ngeles Mar466A': {'Group': [u'6A'], 'Room': '6.A', 'Hour': 6, 'Teacher': u'M\xaa \xc1ngeles Mar', 'Day': 4, 'Subject': u'F\xedsica'}}
        out: dic: { u'3KIbai Go\xf1iHiritartasuna3.JK': {'Count': 1, 'Room': '3.JK', 'Group': '3K', 'Teacher': u'Ibai Go\xf1i', 'Subject': 'Hiritartasuna'}}
        what happens when a set-of-activities are hold in different rooms? Does EDUCA use room information in ASIGF, I don't think so even if it allows up to 4 rooms
        <ASIGF ID="1" ASIG="2NTP" AULA="201" AULA1="" AULA2="" AULA3="" AULA4="" EDIFICIO="2" GRUP="2H" NALUM="" PROF="BG01" TIPO="" HORASEM="3"/>
        '''
        print("Extracting subject info from teachers and groups...")
        asigdic = {}
        for key in grdic.keys():
            #print(grdic[key])
            newkey = grdic[key]['Group'][0] + grdic[key]['Teacher'] + grdic[key]['Subject'] + grdic[key]['Room']
            if newkey not in asigdic.keys():
                #print("grdic[key]: ",key," value: ",grdic[key])
                if grdic[key]['Group'] == [''] or grdic[key]['Group'][0][0] not in ['1', '2', '3', '4', '5', '6']:
                    groupname = ""
                else:
                    groupname = grdic[key]['Group'][0]
                ad = {'Teacher': grdic[key]['Teacher'], 'Group': groupname, 'Subject': grdic[key]['Subject'], 
                    'Room': grdic[key]['Room'], 'Count': 1}
                asigdic[newkey] = ad
            else:
                asigdic[newkey]['Count'] += 1
            #print("asigdic[newkey]: ",newkey," value: ",asigdic[newkey])
        return asigdic

    def get_asigf_abrev(self, adic):
        # DIC bat sortu, baina eskuz esan ikasgai izen bakoitzaren laburdura
        subjects = {}
        for k in adic.keys():
            if not adic[k]['Subject'] in subjects.keys():
                iz = input("Ikagaia: [" + adic[k]['Subject'] + "]:")
            if iz != "":
                subjects[adic[k]['Subject']] = {'ABREV': iz}
            else:
                subjects[adic[k]['Subject']] = {'ABREV': adic[k]['Subject']}
        return subjects


    # Create XML for educa
    def create_educa_xml(self):
        self.tree = ET.ElementTree()
        now = datetime.now()
        # root=ET.Element("xml", 
                        # {'encoding': 'utf-8', 
                            # 'version'='1.0', 
                            # })
        # educa=ET.SubElement(root, "SERVICIO", 
        educa = ET.Element("SERVICIO", 
                                    {'autor': "Asier Urio's Fet Importer", 
                                        'fecha': now.strftime('%Y/%m/%d %H:%M:%S'), 
                                        'modulo': "Ordutegiak",  # Horarios?
                                        }) 
        self.tree._setroot(educa)
  
    def write_educa_xml(self, educafile="educa.xml"):
        print("Writing educa file: ",educafile)
        # print(self.tree)
        self.tree.write(educafile, 
                xml_declaration=True, encoding='utf-8', 
                method="xml")  

    def create_proft_xml(self):
        print("Creating PROFT xml...")
        proft = ET.Element("PROFT")
        for ID, teacher in enumerate(self.teachers.keys()):
            ET.SubElement(proft, 'PROFF',
                                    {'ABREV': self.teachers[teacher]['ABREV'],
                                        'DEPART': self.teachers[teacher]['DEPART'],
                                        'ID': str(ID),
                                        'NOMBRE': teacher, # self.irakasleak[teacher]['NOMBRE'],
                                        })
        self.indent(proft)
        self.root.append(proft)

    def create_aulat_xml(self):
        print("Creating AULAT xml...")
        aulat = ET.Element("AULAT")
        for ID, room in enumerate(self.buildings.keys()):
            ET.SubElement(aulat, 'AULAF',
                                    {'ABREV': self.buildings[room]['ABREV'],
                                        'EDIFICIO': self.buildings[room]['EDIFICIO'],
                                        'ID': str(ID),
                                        'MAXALUM': '0',
                                        'NOMBRE': self.buildings[room]['NOMBRE'],
                                        })   
        self.indent(aulat)
        self.root.append(aulat)

    def create_grupt_xml(self):
        print("Creating GROUPT xml...")
        # in: {'5H': {'ABREV': '5H', 'GRUPO': '5.H', 'CURSO': '5'}}
        grupt = ET.Element("GRUPT")
        for ID, key in enumerate(self.groups.keys()):
            if self.groups[key]['GRUPO'] == '1_UCE':
                nivel = 'UCE'
            elif self.groups[key]['CURSO'] <= '4': 
                nivel = 'ESO'
            elif self.groups[key]['CURSO'] > '4': 
                nivel = 'BACH'
            else: 
                nivel = ''
            if self.groups[key]['GRUPO'] in self.DIV_GROUPS:
                nivel = 'DIV'  
            if key[0] != 'b': ET.SubElement(grupt, 'GRUPF',
                                    {'ABREV': self.groups[key]['ABREV'],
                                        'CURSO': self.groups[key]['CURSO'],
                                        'DESCRIP': '',
                                        'GRUPO': self.groups[key]['GRUPO'], #FIXME: If I want to create groupings all name must be considered
                                        'ID': str(ID),
                                        'MAXALUM': '0',
                                        'NIVEL': nivel,
                                        'TURNO': 'D',
                                        })
        self.indent(grupt)
        self.root.append(grupt)

    def create_asigt_xml(self):
        print("Creating ASIGT xml...")
        # ind: dic: { u'3KIbai Go\xf1iHiritartasuna3.JK': {'Count': 1, 'Room': '3.JK', 'Group': '3K', 'Teacher': u'Ibai Go\xf1i', 'Subject': 'Hiritartasuna'}}
        # out: educa's ASIGT element
        asigt = ET.Element("ASIGT")
        for ID, key in enumerate(self.adic.keys()):
            # if self.adic[key]['Room'] not in self.buildings.keys():  
            #    print(self.adic[key]['Room'])
            # self.buildings[self.adic[key]['Room']]='1'
            #print("crate_asig_xml: ",self.adic[key],self.adic[key]['Group'])
            if self.adic[key]['Group'] != '' and self.adic[key]['Group'][0]=='b':  # FIXME: maybe =='b' isn't enough
                grup = ""
            else:
                grup = self.adic[key]['Group']
            if self.adic[key]['Room'] == "":
                #print(self.adic[key])
                aula = ""
                edificio = ""
            else:
                aula = self.buildings[self.adic[key]['Room']]['ABREV']
                edificio = self.buildings[self.adic[key]['Room']]['EDIFICIO']
            if self.adic[key]['Subject'] not in self.subjects.keys():  # self.teachers.keys()
                #print(self.subjects[self.adic[key]['Subject']])
                self.subjects[self.adic[key]['Subject']]['ABREV'] = input("ABREV: ")
                self.subjects[self.adic[key]['Subject']]['NOMBRE'] = input("NOMBRE: ")
            ET.SubElement(asigt, 'ASIGF',
                                    {'ASIG': self.subjects[self.adic[key]['Subject']]['ABREV'],
                                        'AULA': aula,
                                        'AULA1': '',
                                        'AULA2': '',
                                        'AULA3': '',
                                        'AULA4': '',
                                        'EDIFICIO': edificio,
                                        'GRUP': grup,
                                        'HORASEM': str(self.adic[key]['Count']),
                                        'ID': str(ID),
                                        'NALUM': '',
                                        'PROF': self.teachers[self.adic[key]['Teacher']]['ABREV'],
                                        'TIPO': '',
                                        })
        self.indent(asigt)
        self.root.append(asigt)

    def create_soluct_xml(self,teacherSession): 
        print("Creating SOLUCT xml...")
        # print(teacherSession[teacherSession.keys()[0]])  # FIXME ezabatu
        # print(teacherSession)
        soluct = ET.Element("SOLUCT")
        for key in teacherSession.keys():
            if teacherSession[key]['Room'] not in self.buildings.keys():
                aula = ""
            else:
                aula = self.buildings[teacherSession[key]['Room']]['ABREV']
            # print(key)
            # if not adic[k]['Subject'] in subjects.keys():
            #    iz=input("Ikagaia: ["+adic[k]['Subject']+"]:")
            # print(key, ": ", teacherSession[key]['Group'])
            if teacherSession[key]['Group'] != ['']: 
                cur = teacherSession[key]['Group'][0][0]
            else:
                cur = ""
            if teacherSession[key]['Group'] != ['']: 
                grup = teacherSession[key]['Group'][0]  # FIXME: All name  remove [1]
            else:
                grup = "" 
            if cur <= '4':
                nivel = 'ESO'
            elif cur > '4':
                nivel = 'BACH'
            else:
                nivel = ''
            if grup in ['2-P','3-D', '3-L','3-P']:
                nivel = 'DIV'
            if teacherSession[key]['Group'] != [''] and teacherSession[key]['Group'][0][0] in ['1', '2', '3', '4', '5', '6']:
                cgrup = teacherSession[key]['Group'][0]
            else:
                cgrup = ""
                nivel = ""
                cur = ""
                grup = ""
            ET.SubElement(soluct, 'SOLUCF',
                                    {'ASIG': self.subjects[teacherSession[key]['Subject']]['ABREV'],
                                        'AULA': aula,
                                        'CODGRUPO': cgrup,
                                        'CURSO': cur,
                                        'DIA': str(teacherSession[key]['Day']),
                                        'GRUPO': grup,
                                        'HORA': str(teacherSession[key]['Hour']),
                                        'NIVEL': nivel,
                                        'PROF': self.teachers[teacherSession[key]['Teacher']]['ABREV'],
                                        'SESIONES': '1',
                                        'TAREA': '',
                                        'TURNO': 'D',
                                        })
        self.indent(soluct)
        self.root.append(soluct)

    def create_nomasigt_xml(self):   
        print("Creating NOMASIGT element...")
        nomasigt = ET.Element("NOMASIGT")
        keys = []
        for ID, key in enumerate(self.adic.keys()):
            if self.subjects[self.adic[key]['Subject']]['ABREV'] in keys:
                continue
            # print(key)
            keys.append(self.subjects[self.adic[key]['Subject']]['ABREV'])
            ET.SubElement(nomasigt, 'NOMASIGF',
                                    {'ABREV': self.subjects[self.adic[key]['Subject']]['ABREV'],
                                        'ACTIV': '1',
                                        'ID': str(ID),
                                        'NOMBRE': self.adic[key]['Subject'],
                                        })
        self.indent(nomasigt)
        self.root.append(nomasigt)

   
    def extract_teachers_file(self, teachersfile): #new
        print("reading teachers file: ",teachersfile)
        teacherGroup = {}
        teacherSession = {}
        gd = {}
        groups = {}
        tree = ET.parse(teachersfile)
        root = tree.getroot()
        for teacher in root.findall('.//Teacher'):
            teachername = teacher.get('name')
            #print(teachername)
            for eg in teacher.findall('.//Day'):
                eguna = self.days[eg.get('name')]
                #print(eg.get('name'),eguna)
                for ordu in eg.findall('.//Hour'):
                    hour = self.hours[ordu.get('name')]
                    #print(hour,ordu.get('name'))
                    subjects = ordu.findall('.//Subject')
                    #print(subjects)
                    subject = ''
                    if len(subjects)>0:
                        subject = subjects[0].get('name')
                    students = ordu.findall(".//Students")
                    #print(students)
                    students_name = ''
                    if len(students) >= 1:
                        #print(">=1")
                        students_name = students[0].get('name')
                        #print(students_name)
                        for st in students[1:]:
                            students_name = students_name[0:3] + st.get('name')[1:3] + students_name[3:]
                        keystr = teachername+subject+students_name
                        if keystr not in gd.keys():
                                gd[keystr] = students_name
                                #print("new:", students_name)
                        #print(students_name)
                        
                                                
                        group = {}
                        ga = students_name[0]
                        if ga not in ['1', '2', '3', '4', '5', '6']:
                            continue
                        group['ABREV'] = students_name
                        group['CURSO'] = ga[0]
                        group['GRUPO'] = students_name
                        groups[students_name] = group
                            
#                         if students_name == '':
#                             print(keystr)
#                     if students == [] and subjects != []:
#                     # print(subjects[0].get('name'), hour, eguna, teachername)
#                         if subject not in self.subjects.keys():
#                             iz = input("Ikasgaia: [" + subject + "]:")
#                             if iz != "": 
#                                 self.subjects[subject] = {'ABREV': iz}
#                             else:
#                                 self.subjects[subject] = {'ABREV': subject}
                    rooma = ordu.findall(".//Room")
                    #print(rooma)
                    if rooma != []:
                        room = rooma[0].get('name')
                    else:
                        room = ""   
                    
                    if subject != '':   
                        teacherGroup[teachername + subject + str(hour) + str(eguna)] = {'Teacher': teachername, 'Subject': subject, 'Room': room, 'Group': students_name, 'Count': 1}
                        teacherSession[teachername + subject + str(hour) + str(eguna)] = {'Teacher': teachername, 'Subject': subject, 'Room': room, 'Group': [students_name], 'Day': eguna, 'Hour': hour}
                    #print(teacherSession)
        #print(groups)
        return groups,teacherSession,teacherGroup


    def indent(self, elem, level=0):
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def prettify(self, elem):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = xml.dom.minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="\t")


         

# Parseatu feten irteera *teachers.xml
# Irakurri, ikasgai, gela eta irakasleen ALIASAK BG01...
# Egin HASH,DIctionary bat horiekin
# Taldeen izenak moldatu <Students name="1 -H -Frantsesa -HA"> -> 1H (Ikusi errepikatzen diren, talde gehiago diren.. (egin behar da ASIGT bat talde bakoitzarako)
# Zenbatu ikasgai bera ikasle talde berekin zenbat ordu dituen
# ASIG,AULA,GRUP eta PROF dictionary hori erabiliz ezarri
# ASIG=ikasgaiak["IKT"], AULA=gelak["InformatikaGela1"], GRUP=taldeak["1H"], PROF=Irakasleak["Asier Urio"]... 
   
if __name__=="__main__":
    f2e = Fet2EDUCA()
    f2e.generate_all()
