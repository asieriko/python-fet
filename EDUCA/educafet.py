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
        dir_path = "/home/asier/Hezkuntza/python-hezkuntza/python-fet/16-17-data/"
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
        self.grdic = self.load_groups_rooms_file(os.path.join(dir_path, "subgroups.xml"))
        '''grdic - only with students
        'Elena Mugeta456B': {'Room': '1E5', 'Teacher': 'Elena Mugeta', 'Day': 4, 'Subject': 'Frantsesa', 'Group': ['6B'], 'Hour': 5},
        'Javier Beitia473A': {'Room': '2D9', 'Teacher': 'Javier Beitia', 'Day': 4, 'Subject': 'Alemaniera', 'Group': ['3A'], 'Hour': 7}
        '''
        self.adic = self.extract_asigf_from_groups()
        ''' adic
        '3CÁngel GálvezTutoretza2D9': {'Teacher': 'Ángel Gálvez', 'Subject': 'Tutoretza', 'Room': '2D9', 'Group': '3C', 'Count': 1},
        'Uxue MacuaZaintza63': {'Teacher': 'Uxue Macua', 'Count': 1, 'Group': 'b', 'Room': '', 'Subject': 'Zaintza'},
        '''
        # It seems that all the info in adic is already in grdic
        #print(self.teachers)
        wsdic, zdic = self.create_without_students_dict(os.path.join(dir_path, "teachers.xml"))
        self.adic.update(wsdic)
        self.groups = self.extract_taldeak_from_groups()
        '''groups
        '1L': {'ABREV': '1L', 'CURSO': '1', 'GRUPO': '1.L'},
        '6B': {'ABREV': '6B', 'CURSO': '6', 'GRUPO': '6.B'},
        '''
        agrdic = {**self.grdic, **zdic}
        self.saioak = agrdic
        '''Saioak # FIXME: The same as self.grdic plus activities without students
        'Javier Beitia473C': {'Room': '2D9', 'Teacher': 'Javier Beitia', 'Day': 4, 'Subject': 'Alemaniera', 'Group': ['3C'], 'Hour': 7},
        'Amaia Zubillaga325I': {'Room': '2E5', 'Teacher': 'Amaia Zubillaga', 'Day': 3, 'Subject': 'Oratoria', 'Group': ['5I'], 'Hour': 2},
        'Maite Pérez de CirizaZaintza41': {'Room': 'Z3-1', 'Teacher': 'Maite Pérez de Ciriza', 'Day': 1, 'Subject': 'Zaintza', 'Group': [''], 'Hour': 4},
        '''
        self.tree = ''
        self.create_educa_xml()
        self.root = self.tree.getroot()
        self.create_soluct_xml()
        self.create_asigt_xml()
        self.create_proft_xml()
        self.create_grupt_xml()
        self.create_aulat_xml()
        self.create_nomasigt_xml()
        self.write_educa_xml()

    # LOAD Data!
    def load_teacher_file(self, CSVfile="irakasle.csv", interactive=False):
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

    def load_groups_rooms_file(self, xmlfile='subgroups.xml'):
        # in: fet's subgroups.xml file
        # out: dic {u'M\xaa \xc1ngeles Mar466A': {'Group': [u'6A'], 'Room': '6.A', 'Hour': 6, 'Teacher': u'M\xaa \xc1ngeles Mar', 'Day': 4, 'Subject': u'F\xedsica'}}
        tree = ET.parse(xmlfile)
        root = tree.getroot()
        tgdic = {}
        for subbgroup in root.findall('.//Subgroup'):
            subbgroupname = subbgroup.get('name')[0] + subbgroup.get('name')[2]
            for day in subbgroup.findall('.//Day'):
                dayname = self.days[day.get('name')]
                for hour in day.findall('.//Hour'):
                    hourname = self.hours[hour.get('name')]
                    for teacher in hour.findall('.//Teacher'):
                        subject = hour.find('.//Subject').get('name')
                        room = hour.find('.//Room')
                        if room is not None:
                            room = room.get('name')
                        else:
                            room = ""
                        key = teacher.get('name') + str(dayname) + str(hourname) + subbgroupname  # +subbgroupname gabe, group=[1A, 1B]
                        if key not in tgdic.keys():
                            di = {'Teacher': teacher.get('name'), 'Subject': subject, 'Day': dayname, 'Hour': hourname, 'Room': room, 'Group': [subbgroupname]}
                            tgdic[key] = di
                        else:
                            if subbgroupname not in tgdic[key]['Group']:
                                tgdic[key]['Group'].append(subbgroupname)
        return tgdic

    def extract_asigf_from_groups(self):
        ''' 
        From a dic for each activity-hour, creates a new dict for each set-activity-group with the count of how many sessions are
        in dic:u'M\xaa \xc1ngeles Mar466A': {'Group': [u'6A'], 'Room': '6.A', 'Hour': 6, 'Teacher': u'M\xaa \xc1ngeles Mar', 'Day': 4, 'Subject': u'F\xedsica'}}
        out: dic: { u'3KIbai Go\xf1iHiritartasuna3.JK': {'Count': 1, 'Room': '3.JK', 'Group': '3K', 'Teacher': u'Ibai Go\xf1i', 'Subject': 'Hiritartasuna'}}
        what happens when a set-of-activities are hold in different rooms? Does EDUCA use room information in ASIGF, I don't think so even if it allows up to 4 rooms
        <ASIGF ID="1" ASIG="2NTP" AULA="201" AULA1="" AULA2="" AULA3="" AULA4="" EDIFICIO="2" GRUP="2H" NALUM="" PROF="BG01" TIPO="" HORASEM="3"/>
        '''
        asigdic = {}
        for key in self.grdic.keys():
            print(self.grdic[key])
            newkey = self.grdic[key]['Group'][0] + self.grdic[key]['Teacher'] + self.grdic[key]['Subject'] + self.grdic[key]['Room']
            if newkey not in asigdic.keys():
                if self.grdic[key]['Group'][0][0] not in ['1', '2', '3', '4', '5', '6']:
                    groupname = "NOGROUP"
                else:
                    groupname = self.grdic[key]['Group'][0]
                ad = {'Teacher': self.grdic[key]['Teacher'], 'Group': groupname, 'Subject': self.grdic[key]['Subject'], 
                    'Room': self.grdic[key]['Room'], 'Count': 1}
                asigdic[newkey] = ad
            else:
                asigdic[newkey]['Count'] += 1
            print(asigdic[newkey])
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

    def extract_taldeak_from_groups(self):
        # in grdic:u'M\xaa \xc1ngeles Mar466A': {'Group': [u'6A'], 'Room': '6.A', 'Hour': 6, 'Teacher': u'M\xaa \xc1ngeles Mar', 'Day': 4, 'Subject': u'F\xedsica'}}
        # out: {'5H': {'ABREV': '5H', 'GRUPO': '5.H', 'CURSO': '5'}}
        groups = {}
        for key in self.grdic.keys():
            group = {}
            ga = self.grdic[key]['Group'][0]  # FIXME: Working...
            if ga[0] not in ['1', '2', '3', '4', '5', '6']:
                continue
            group['ABREV'] = ga
            group['CURSO'] = ga[0]
            group['GRUPO'] = ga[0] + "." + ga[1] #FIXME: If I want to create groupings al name must be considered
            groups[ga] = group
            
        return groups

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
        # print(self.tree)
        self.tree.write(educafile, 
                xml_declaration=True, encoding='utf-8', 
                method="xml")  

    def create_proft_xml(self):
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
        # in: {'5H': {'ABREV': '5H', 'GRUPO': '5.H', 'CURSO': '5'}}
        grupt = ET.Element("GRUPT")
        for ID, key in enumerate(self.groups.keys()):
            if self.groups[key]['CURSO'] <= '4': 
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
                                        'GRUPO': self.groups[key]['GRUPO'][-1], #FIXME: If I want to create groupings all name must be considered
                                        'ID': str(ID),
                                        'MAXALUM': '0',
                                        'NIVEL': nivel,
                                        'TURNO': 'D',
                                        })
        self.indent(grupt)
        self.root.append(grupt)

    def create_asigt_xml(self):
        # ind: dic: { u'3KIbai Go\xf1iHiritartasuna3.JK': {'Count': 1, 'Room': '3.JK', 'Group': '3K', 'Teacher': u'Ibai Go\xf1i', 'Subject': 'Hiritartasuna'}}
        # out: educa's ASIGT element
        asigt = ET.Element("ASIGT")
        for ID, key in enumerate(self.adic.keys()):
            # if self.adic[key]['Room'] not in self.buildings.keys():  
            #    print(self.adic[key]['Room'])
            # self.buildings[self.adic[key]['Room']]='1'
            if self.adic[key]['Group'][0]=='b':  # FIXME: maybe =='b' isn't enough
                grup = ""
            else:
                grup = self.adic[key]['Group']
            if self.adic[key]['Room'] == "":
                aula = ""
                edificio = ""
            else:
                aula = self.buildings[self.adic[key]['Room']]['ABREV']
                edificio = self.buildings[self.adic[key]['Room']]['EDIFICIO']
            if self.adic[key]['Subject'] not in self.subjects.keys():  # self.teachers.keys()
                print(self.subjects[self.adic[key]['Subject']])
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

    def create_soluct_xml(self): 
        # print(self.saioak[self.saioak.keys()[0]])  # FIXME ezabatu
        # print(self.saioak)
        soluct = ET.Element("SOLUCT")
        for key in self.saioak.keys():
            if self.saioak[key]['Room'] not in self.buildings.keys():
                aula = ""
            else:
                aula = self.buildings[self.saioak[key]['Room']]['ABREV']
            # print(key)
            # if not adic[k]['Subject'] in subjects.keys():
            #    iz=input("Ikagaia: ["+adic[k]['Subject']+"]:")
            # print(key, ": ", self.saioak[key]['Group'])
            if self.saioak[key]['Group'] != ['']: 
                cur = self.saioak[key]['Group'][0][0]
            else:
                cur = ""
            if self.saioak[key]['Group'] != ['']: 
                grup = self.saioak[key]['Group'][0][1]
            else:
                grup = "" 
            if cur <= '4':
                nivel = 'ESO'
            elif cur > '4':
                nivel = 'BACH'
            else:
                nivel = ''
            if grup in ['P', 'Q']:
                nivel = 'DIV'
            if self.saioak[key]['Group'] != [''] and self.saioak[key]['Group'][0][0] in ['1', '2', '3', '4', '5', '6']:
                cgrup = self.saioak[key]['Group'][0]
            else:
                cgrup = ""
                nivel = ""
                cur = ""
                grup = ""
            ET.SubElement(soluct, 'SOLUCF',
                                    {'ASIG': self.subjects[self.saioak[key]['Subject']]['ABREV'],
                                        'AULA': aula,
                                        'CODGRUPO': cgrup,
                                        'CURSO': cur,
                                        'DIA': str(self.saioak[key]['Day']),
                                        'GRUPO': grup,
                                        'HORA': str(self.saioak[key]['Hour']),
                                        'NIVEL': nivel,
                                        'PROF': self.teachers[self.saioak[key]['Teacher']]['ABREV'],
                                        'SESIONES': '1',
                                        'TAREA': '',
                                        'TURNO': 'D',
                                        })
        self.indent(soluct)
        self.root.append(soluct)

    def create_nomasigt_xml(self):   
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

    def create_without_students_dict(self, teachersfile="teachers.xml"):
        tree = ET.parse(teachersfile)
        root = tree.getroot()
        # Ikaslerik gabeko jarduerak lortzeko.
        # FIXME:Zaintzak ez ditu hartzen!!
        # <Hour name="08:30-9:25">
        # <Subject name="1.ZaintzaAintzira"></Subject><Room name="1.ReflexionAintzira"></Room>
        # </Hour>
        t = {}
        d = {}
        for teacher in root.findall('.//Teacher'):
            teachername = teacher.get('name')
            print(teachername)
            if teachername not in self.teachers.keys():
                print(teachername)
                self.teachers[teachername]['ABREV'] = input("ABREV: ")
                self.teachers[teachername]['DEPART'] = input("Depart: ")
            
            for eg in teacher.findall('.//Day'):
                eguna = self.days[eg.get('name')]
                for ordu in eg.findall('.//Hour'):
                    hour = self.hours[ordu.get('name')]
                    subjects = ordu.findall('.//Subject')
                    students = ordu.findall(".//Students")
                    rooma = ordu.findall(".//Room")
                    if rooma != []:
                        room = rooma[0].get('name')
                    else:
                        room = ""
                    if students == [] and subjects != []:
                    # print(subjects[0].get('name'), hour, eguna, teachername)
                        if subjects[0].get('name') not in self.subjects.keys():
                            iz = input("Ikasgaia: [" + subjects[0].get('name') + "]:")
                            if iz != "": 
                                self.subjects[subjects[0].get('name')] = {'ABREV': iz}
                            else:
                                self.subjects[subjects[0].get('name')] = {'ABREV': subjects[0].get('name')}	    
                        t[teachername + subjects[0].get('name') + str(hour) + str(eguna)] = {'Teacher': teachername, 'Subject': subjects[0].get('name'), 'Room': "", 'Group': "NOGROUP", 'Count': 1}
                        d[teachername + subjects[0].get('name') + str(hour) + str(eguna)] = {'Teacher': teachername, 'Subject': subjects[0].get('name'), 'Room': room, 'Group': [""], 'Day': eguna, 'Hour': hour}
        return t, d

    def create_teacher_groups_dict2(self, root, orduak):
        t = {}
        for teacher in root.findall('.//Teacher'):
            teachername = teacher.get('name')
            for eg in teacher.findall('.//Day'):
                eguna = [eg.get('name')]
                for ordu in eg.findall('.//Hour'):
                    ordua = orduak[ordu.get('name')]
                    subjects = ordu.findall('.//Subject')
                    if subjects != []:
                        sub = subjects[0].get('name')
                        ikasgaia = sub
                        for a in ordu.findall(".//Students"):
                            if a != []:
                                group = str(a.get('name')[0]) + str(a.get('name')[2])
                                key = teachername + str(eguna) + str(ordua) + group
                            if key in t.keys():
                                t[key]['count'] = t[key]['count']+1
                            else:
                                d = {'teacher': teachername, 'group': group, 'subject': sub, 'day': eguna, 'hour': ordua, 'count': 1}  # FIXME count beti da bat, eguna eta ordua ezberdinuak direlako
                                t[key] = d
        return t

    def t_txikia(self, a):
        if a.get('name')[-1]=='P': 
            return 'P'
        else:
            return ''

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


# for k in tdic.keys():
  # print(tdic[k]['teacher'],tdic[k]['groups'],tdic[k]['subject'],tdic[k]['count'])

	  # if (gps in t.keys(): t[gps]=t[gps]+1
	# for ikas in ordu.findall('.//Students'):
	  # if ikas !=[] and (ikas.get('name'))[0]!='b': 
	    
	    
	    
	    
	    # ikasleak=ikas.get('name')[0]+ikas.get('name')[2]
	    # if ikas.get('name')[-1]=='P': ikasleak=ikasleak+'P'
	    # print(teachername,eguna,ordua,ikasleak,ikasgaia)
    # print(t)
    


# for a in root.findall(".//ASIGT/ASIGF[@ASIG='2FRA']"): print(a.attrib)
# Lortu ikasgaien izenak for a in root.findall(".//Students"): print(a.get('name')[0:3])
# list(set([a.get('name')[0:3] for a in root.findall(".//Students")]))
# taldeak=sorted(list(set([a.get('name')[0:3] for a in root.findall(".//Students")])))

	      

# Parseatu feten irteera *teachers.xml
# Irakurri, ikasgai, gela eta irakasleen ALIASAK BG01...
# Egin HASH,DIctionary bat horiekin
# Taldeen izenak moldatu <Students name="1 -H -Frantsesa -HA"> -> 1H (Ikusi errepikatzen diren, talde gehiago diren.. (egin behar da ASIGT bat talde bakoitzarako)
# Zenbatu ikasgai bera ikasle talde berekin zenbat ordu dituen
# ASIG,AULA,GRUP eta PROF dictionary hori erabiliz ezarri
# ASIG=ikasgaiak["IKT"], AULA=gelak["InformatikaGela1"], GRUP=taldeak["1H"], PROF=Irakasleak["Asier Urio"]... 
    def load_ikasgaiak_from_fet(self,root): # FIXME: Agian hau ez da erabiltzen
        ikasgaiak = sorted(list(set([a.get('name')[0:3] for a in root.findall(".//Subject")])))
        for a in root.findall(".//Subject"):
            if a.get('name')[-2] == "_": a.set('name',a.get('name')[0:-2])
            if "aintza" in a.get('name'): a.set('name','Zaintza')    
            if "uardia" in a.get('name'): a.set('name','Zaintza')    
            if "Tutore Bilera" in a.get('name'): a.set('name','Tutore Bilera')    
        asigfall = []                             
        asigf = []   
        for a in t[1].findall('.//Hour'):# t, teacher??
            b =  a.findall('.//Students')
            c =  a.findall('.//Subject')
        #    for d in c:
        #      print(d.get('name'))
            for x in b:
        #      print(x.get('name')[0:3])
                year = x.get('name')[0]
                group = x.get('name')[0] + x.get('name')[2]
                if x.get('name')[-1] == "P": 
                    subject = d.get('name')[0:3] + "P"
                else:
                    subject = d.get('name')[0:3]
                print('ASIG=' + year + d.get('name')[0:3] + ' GRUP=' + group)
                asigfall.append('ASIG=' + year + subject + ' GRUP=' + group)
        # Talde txikiak, talde normaltzat hartzen ditu, bihurtzen dudalako 2-k-p eta 2-k-h 2-k
        count = {}
        for asig in asigfall:
            if asig in asigf: count[asig] = int(count[asig]) + 1
            else:
                asigf.append(asig)
                count[asig] = 1
                            
                            
              
educasample="""<?xml version="1.0" encoding="utf-8"?>
<SERVICIO autor="KRONOWIN" fecha="2014/04/17 10:27:44" modulo="HORARIOS">
        <ASIGT>
                <ASIGF ASIG="2NTP" AULA="201" AULA1="" AULA2="" AULA3="" AULA4="" EDIFICIO="2" GRUP="2H" HORASEM="3" ID="1" NALUM="" PROF="BG01" TIPO=""/>
                <ASIGF ASIG="2FRA" AULA="202" AULA1="" AULA2="" AULA3="" AULA4="" EDIFICIO="2" GRUP="2H" HORASEM="2" ID="20" NALUM="" PROF="FR02" TIPO=""/>
                <ASIGF ASIG="2FRA" AULA="202" AULA1="" AULA2="" AULA3="" AULA4="" EDIFICIO="2" GRUP="2I" HORASEM="2" ID="22" NALUM="" PROF="FR02" TIPO=""/>
        </ASIGT>
        <NOMASIGT>
                <NOMASIGF ABREV="1ALE" ACTIV="1" ID="1" NOMBRE="1_ALEMAN"/>
        </NOMASIGT>
        <PROFT>
                <PROFF ABREV="AL01" DEPART="Aleman" ID="1" NOMBRE="Javier Beitia"/>
                <PROFF ABREV="FK03" DEPART="Fisica y Quimica" ID="19" NOMBRE="Jose Donazar"/>
        </PROFT>
        <GRUPT>
                <GRUPF ABREV="1A" CURSO="1" DESCRIP="" GRUPO="A" ID="1" MAXALUM="0" NIVEL="ESO" TURNO="D"/>
                <GRUPF ABREV="4H" CURSO="4" DESCRIP="ZIENTZIAK 1" GRUPO="H" ID="35" MAXALUM="0" NIVEL="ESO" TURNO="D"/>
                <GRUPF ABREV="UCE" CURSO="2" DESCRIP="UCE" GRUPO="V" ID="46" MAXALUM="0" NIVEL="ESO" TURNO="D"/>
                <GRUPF ABREV="4K" CURSO="4" DESCRIP="LETRAK TEKNOLOGIA" GRUPO="K" ID="47" MAXALUM="0" NIVEL="ESO" TURNO="D"/>
                <GRUPF ABREV="PR1B" CURSO="1" DESCRIP="PROA 1B" GRUPO="Q" ID="48" MAXALUM="0" NIVEL="ESO" TURNO="D"/>
        </GRUPT>
        <AULAT>
                <AULAF ABREV="107" EDIFICIO="2" ID="1" MAXALUM="0" NOMBRE="1A"/>
        </AULAT>
        <SOLUCT>
                <SOLUCF ASIG="RMGO" AULA="" CODGRUPO="" CURSO="" DIA="1" GRUPO="" HORA="1" NIVEL="" PROF="" SESIONES="1" TAREA="" TURNO=""/>
        </SOLUCT>
</SERVICIO>"""


subgroupsxml=  """<?xml version="1.0" encoding="UTF-8"?>
<Students_Timetable>
  <Subgroup name="1-A-P">
   <Day name="Astelehena">
    <Hour name="08:30-9:25">
      <Teacher name="Eugenio Miranda"></Teacher><Subject name="Ciencias Naturales"></Subject><Room name="1.AB"></Room>
    </Hour>
    <Hour name="09:25-10:20">
      <Teacher name="Angel Galvez"></Teacher><Subject name="Ingles"></Subject><Room name="1.AB"></Room>
    </Hour>
    <Hour name="10:20-11:15">
      <Teacher name="Javier Perez"></Teacher><Subject name="Lengua Castellana"></Subject><Room name="1.AB"></Room>
    </Hour>
    <Hour name="11:15-11:45">
     
    </Hour>
    <Hour name="11:45-12:40">
      <Teacher name="Pedro Gomez"></Teacher><Subject name="Musica"></Subject><Room name="MusikaAintzira"></Room>
    </Hour>
    <Hour name="12:40-13:35">
      <Teacher name="Luisa Rodriguez Itinerante"></Teacher><Subject name="CCSS"></Subject><Room name="1.AB"></Room>
    </Hour>
    <Hour name="13:35-14:30">
      <Teacher name="Mariaje Ruiz"></Teacher> <Teacher name="Merche Ansa"></Teacher><Subject name="Tecnologia"></Subject><Room name="TailerraAintzira1"></Room>
    </Hour>
    <Hour name="14:30-15:20">"""
    
f2e = Fet2EDUCA()    
f2e.generate_all()
