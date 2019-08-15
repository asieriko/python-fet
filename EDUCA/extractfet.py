import xml.etree.ElementTree as ET
from datetime import datetime
import pandas as pd
import sys, getopt
import csv
import random
from collections import defaultdict

class createAskabi():
    
    def create_lan_postu_ikasg(self,lpi):
        lpidf = pd.DataFrame()
        id = 18190000
        for row in lpi.itertuples():
            if row.subject in complementarias:
                lektiv = 'C'
            if row.acode[0] == 'Z':
                lektiv = 'Z'
            #FALTAN
            else:
                lektiv = 'D'
            #print(id,'1819',row.code,row.acode,row.students,0,0,lektiv)
            row = pd.Series([id,'1819',row.code,row.acode,row.students,0,0,lektiv,row.grouping],['id','ikast','postu','ikasg_kode','t_l','subtl','h_t','lektiv','grouping'])
            lpidf = lpidf.append(row,ignore_index=True)
            id += 1
        return lpidf
        
    def create_lan_postu_talde(self,lpt):
        lptdf = pd.DataFrame()
        id = 18190000
        for row in lpt.itertuples():
            if row.subject not in complementarias and row.students != '':
                for talde in row.students:
                    row2 = pd.Series([id,row.code,row.grade+talde,'1819'],['id','postu','talde','ikast'])
                    lptdf = lptdf.append(row2,ignore_index=True)
                    id += 1
        return lptdf
        
    def createOrdutegia(self,lpt,lpidf):
        id = 18190000
        ordutegia = pd.DataFrame()
        for row in lpt.itertuples():
            try:
                print(row.code,row.acode,row.students)
                print(lpidf[(lpidf.postu==row.code) & (lpidf.ikasg_kode==row.acode) & (lpidf.grouping==row.grouping)].id.item())
                piid = int(lpidf[(lpidf.postu==row.code) & (lpidf.ikasg_kode==row.acode) & (lpidf.grouping==row.grouping)].id.item())
                #type(piid)
                row = pd.Series([id,'1819',row.code,int(piid),row.day,row.hour,row.room,'','D'],['id','ikast','postu','postu_ikasg_id','astegun','saio','areto','areto2','tipoa'])
                ordutegia = ordutegia.append(row,ignore_index=True)
                id += 1
            except:
                print(row.code,row.acode,row.students)
        return ordutegia
        

class createEDUCA():
    
    def __init__(self):
        self.tree = ''
        self.create_educa_xml()
        self.root = self.tree.getroot()
        
        
    
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
    
    def create_proft_xml(self,teachers):
            proft = ET.Element("PROFT")
            for row in teachers.iterrows():
                ET.SubElement(proft, 'PROFF',
                                        {'ABREV': row[1].code,
                                            'DEPART': row[1].code[0:1],
                                            'ID': str(row[0]),
                                            'NOMBRE': row[1].teacher,
                                            })
            self.indent(proft)
            self.root.append(proft)

    def create_grupt_xml(self,groups):
        # in: {'5H': {'ABREV': '5H', 'GRUPO': '5.H', 'CURSO': '5'}}
        grupt = ET.Element("GRUPT")
        for row in groups.iterrows():
            if row[1].c != '': ET.SubElement(grupt, 'GRUPF',
                                    {'ABREV': row[1].grouping,
                                        'CURSO': row[1].grade,
                                        'DESCRIP': '',
                                        'GRUPO': row[1].grouping, #FIXME: If I want to create groupings all name must be considered remove [-1]
                                        'ID': str(row[0]),
                                        'MAXALUM': '0',
                                        'NIVEL': row[1].c,
                                        'TURNO': 'D',
                                        })
        self.indent(grupt)
        self.root.append(grupt)

    def create_asigt_xml(self,lect):
        # ind: pandas DataFrame: 
        #type   code            grouping grade students     subject   room  acode  hours
        #4     AL_01  1-ABCDE-Alemaniera     1    ABCDE  Alemaniera  2_108  1_ALE   3
        # out: educa's ASIGT element
        asigt = ET.Element("ASIGT")
        for row in lect.iterrows():
            if row[1].grade == 'U':
                continue
            ET.SubElement(asigt, 'ASIGF',
                                    {'ASIG': row[1].acode,
                                        'AULA': row[1].room,
                                        'AULA1': '',
                                        'AULA2': '',
                                        'AULA3': '',
                                        'AULA4': '',
                                        'EDIFICIO': row[1].room[0],
                                        'GRUP': row[1].grouping,
                                        'HORASEM': str(int(row[1].hours)),
                                        'ID': str(int(row[0])),
                                        'NALUM': '',
                                        'PROF': row[1].code,
                                        'TIPO': '',
                                        })
        self.indent(asigt)
        self.root.append(asigt)
        

    def create_soluct_xml(self,dt): 
        soluct = ET.Element("SOLUCT")
        for row in dt.itertuples():
            ET.SubElement(soluct, 'SOLUCF',
                                    {'ASIG': row.subject,
                                        'AULA': row.room,
                                        'CODGRUPO': row.grouping,
                                        'CURSO': row.grade,
                                        'DIA': row.day,
                                        'GRUPO': row.grouping,
                                        'HORA': row.hour,
                                        'NIVEL': row.c,
                                        'PROF': row.code,
                                        'SESIONES': '1',
                                        'TAREA': '',
                                        'TURNO': 'D',
                                        })
        self.indent(soluct)
        self.root.append(soluct)

    def create_nomasigt_xml(self,subjects):   
        nomasigt = ET.Element("NOMASIGT")
        for row in subjects.iterrows():
            ET.SubElement(nomasigt, 'NOMASIGF',
                                    {'ABREV': row[1].acode,
                                        'ACTIV': '1',
                                        'ID': str(row[0]),
                                        'NOMBRE': row[1].subject,
                                        })
        self.indent(nomasigt)
        self.root.append(nomasigt)

complementarias = ['Zaintza',
'MintegiBurutzaOrduak',
'Ibiltaritza',
'TutoretzaOsagarriOrduak',
'TutoretzaLektiboOrduak',
'AdinMurrizketaOrduak',
'TTBB',
'EOIDNA',
'ZuzendaritzaLektibo',
'ZuzendaritzaOsagarri',
'KalitateOrduak',
'KPB',
'Zuzendaritza',
'Coeducación',
'Bizikidetza',
'MBTeknologia',
'MBPlastika',
'MBOrientazioa',
'MBMusika',
'MBMatematika',
'MBKultura Klasikoa',
'MBIngelesa',
'MBGorputz Heziketa',
'MBGizarte',
'MBGaztelania',
'MBFrantsesa',
'MBFisika Kimika',
'MBFilosofia',
'MBEuskara',
'MBBio Geo',
'MBAleman',
'TutBilera56D',
'TutBilera56AG',
'TutBilera4D',
'TutBilera4AG',
'TutBilera3D',
'TutBilera3AG',
'TutBilera2D',
'TutBilera2AG',
'TutBilera1D',
'TutBilera1AG',
'SSBB',
'Plan Eco.']

def extractinfoXML(inputfile,fet_askabi,postu):
    df = pd.read_csv(fet_askabi)
    df3 = pd.read_csv(postu)
    df2 = pd.DataFrame()
    tree = ET.parse(inputfile)
    root = tree.getroot()
    teachers = root.findall(".//Teacher")
    tdic={}
    gdic= defaultdict(list)
    allgroups=[]
    for teacher in teachers:
        groups=[]
        name=teacher.attrib.get('name')
        postu = df[df.FET==name].postu.item()
        days = teacher.findall(".//Day")
        for day in days:
            dn = day.attrib.get('name')
            hours = day.findall(".//Hour")
            for hour in hours:
                students = ''
                subject = None
                sn = ''
                room = None
                rn = ''
                gt = []
                sg = ''
                grade = ''
                hn = hour.attrib.get('name')
                subject = hour.findall(".//Subject")
                if subject:
                    sn = subject[0].attrib.get('name')
                room = hour.findall(".//Room")
                if room:
                    rn = room[0].attrib.get('name')
                if sn in complementarias:
                    scode = sn
                    if sn == 'Zaintza':
                        grade=rn[0]
                        if hn == "11:15-11:45":
                            sn = 'ZaintzaR'
                        else:
                            sn = 'Zaintza'
                        scode = grade+"_"+sn
                    grouping = ''
                    kode = df3[df3.scode==scode].kode.item()
                    row = pd.Series([name,postu,dn,hn,'',sg,sn,grouping,scode,kode,rn,'C'],["teacher","code","day","hour","grade","students","subject","grouping","scode","acode",'room','type'])
                    df2 = df2.append(row,ignore_index=True)
                    continue
                students = hour.findall(".//Students")
                #print(name,dn,hn,students)
                if len(students)>0:
                    gt = students[0].attrib.get('name').split("-")
                    sg = ''
                    grade = gt[0]
                    if grade == 'B':
                        sg = 'B'
                    else:
                        if len(students) > 1:
                            for group in students:
                                gt = group.attrib.get('name').split("-")
                                #print(gt,gt[1])
                                sg += gt[1]
                            sg = ''.join(sorted(sg))
                            grouping = grade+"-"+sg+"-"+sn
                        else:
                            if gt[0] == 'UCE':
                                grade = 'U'
                                sg = 'U'
                            else:
                                sg = gt[1]
                            grouping = grade+"_"+sg
                    #print(name,dn,hn,grade,sg,sn,grade+"-"+sg+"-"+sn)
                    #print(name,df[df.FET==name].postu.item(),dn,hn,grade,sg,sn,grade+"-"+sg+"-"+sn,grade+"_"+sn)
                    scode = grade+"_"+sn
                    #print(scode)
                    #print(df3.scode.unique())
                    #print(df3[df3.scode==scode])
                    #print("Kode: ", df3[df3.scode==scode].kode.item())
                    
                    kode = df3[df3.scode==scode].kode.item()
                    row = pd.Series([name,postu,dn,hn,grade,sg,sn,grouping,scode,kode,rn,'L'],["teacher","code","day","hour","grade","students","subject","grouping","scode","acode",'room','type'])
                    df2 = df2.append(row,ignore_index=True)
    #for sc in df2.scode.unique():
        #print(sc)
    return df2
               
               
def course(x):
    if x == '':
        return x
    elif x[0]>='5':
        return "BACH"
    elif x in ['2_P','3_D','3_L']:
        return "DIV"
    elif x[0] in ['1','2','3','4']:
        return "ESO"
    return ''

def day(x):
    d = {'Astelehena':'1', 'Asteartea':'2', 'Asteazkena':'3', 'Osteguna':'4', 'Ostirala':'5'}
    return d[x]

def hour(x):
    d = {'08:30-9:25':'1', '09:25-10:20':'2', '10:20-11:15':'3', '11:15-11:45':'4', '11:45-12:40':'5', '12:40-13:35':'6', '13:35-14:30':'7', '14:30-15:20':'8'}
    return d[x]

f = "/home/asier/Hezkuntza/python-hezkuntza/17-18/timetables/Horario-18-19-Version7_data_and_timetable_DefinitivoComplementario-single/Horario-18-19-Version7_data_and_timetable_DefinitivoComplementario_teachers.xml"
f2 = "/home/asier/Hezkuntza/SGCC-Erregistroak-18-19/PR01 Matriculacion y planificacion docente y servicios complementarios/PR0102 Planificacion/Horarios/askabi-fet-postu.csv"
f3 =  "/home/asier/Hezkuntza/SGCC-Erregistroak-18-19/PR01 Matriculacion y planificacion docente y servicios complementarios/PR0102 Planificacion/Horarios/lan_postu_ikasg.csv"

timetable_dataframe = extractinfoXML(f,f2, f3)
timetable_dataframe['c'] = [course(x) for x in timetable_dataframe['grouping']]
timetable_dataframe['day'] = [day(x) for x in timetable_dataframe['day']]
timetable_dataframe['hour'] = [hour(x) for x in timetable_dataframe['hour']]
uni = timetable_dataframe.drop_duplicates(['code','grade','students'])
groups = timetable_dataframe.drop_duplicates(['grouping'])
teachers = timetable_dataframe.drop_duplicates(['code'])
subjects = timetable_dataframe[timetable_dataframe.c!=''].drop_duplicates(['subject','grade'])
subjects = timetable_dataframe.drop_duplicates(['subject','grade'])


#for t in uni.code.unique():
    #for r in timetable_dataframe[timetable_dataframe.code==t].iterrows():
        #if r[1].grade not in ['B',' ',None]:
            #for s in r[1].students:
                #print(t,r[1].grade+s,'1819')



tt = timetable_dataframe.groupby(['code','grouping','grade','students','subject','room','acode','type'],as_index=False).size()
grouping_subject_hours_df = tt.unstack().reset_index()


#comp no hace falta!!
compt = grouping_subject_hours_df.dropna(subset=['C'])
compt = compt.drop(['L'], axis=1)
compt = compt.rename(columns={ compt.columns[-1]: "hours" })

lect = grouping_subject_hours_df.dropna(subset=['L'])
lect = lect.drop(['C'], axis=1)
lect = lect.rename(columns={ lect.columns[-1]: "hours" })

#educa = createEDUCA()
#educa.create_proft_xml(teachers)
#educa.create_grupt_xml(groups)
#educa.create_nomasigt_xml(subjects)
#educa.create_asigt_xml(lect)
#educa.create_soluct_xml(timetable_dataframe)

#educa.tree.write('educa.xml',encoding='utf-8',method='xml')



askabi = createAskabi()
ab = askabi.create_lan_postu_ikasg(grouping_subject_hours_df)
ab2 = askabi.create_lan_postu_talde(grouping_subject_hours_df)
ab3 = askabi.createOrdutegia(timetable_dataframe,ab)
#for row in timetable_dataframe.iterrows():
    #print(row[1].code)
##the same
#for row in timetable_dataframe.itertuples():
    #print(row.code)    

#for row in lect.itertuples():
    #print(row.code, row.grade)       
    
ab[(ab.postu=='TK_01') & (ab.ikasg_kode=='6_IKT') & (ab.t_l=='HIJ')].id.item()
ab[(ab.postu=='FK_05') & (ab.ikasg_kode=='Z_1') & (ab.t_l=='')].id.item()
