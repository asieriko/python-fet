import csv
import time
import xml.dom.minidom
from xml.etree import ElementTree as ET
from datetime import datetime
from itertools import chain
#import datuak
#educaren soluziotik, dictionary bat egin(irakasle-talde-gela) eta zenbatu, hori izango da ikasgaian jarri behar den balioa.
#agina interaktiboki izen batzuk jarri 

#buildings=datuak.buildings
#teachers=datuak.irakasleak
#orduak=datuak.orduak
#egunak=datuak.egunak
#ikasgaiak=datuak.ikasgaiak

def generate_all():
  teachers = load_irakasle_file("/home/asier/Hezkuntza/python-hezkuntza/python-fet/15-16/irakasle.csv")
  buildings = load_gelak_file("/home/asier/Hezkuntza/python-hezkuntza/python-fet/15-16/gelak.csv")
  ikasgaiak = load_subjects_file("/home/asier/Hezkuntza/python-hezkuntza/python-fet/15-16/subjects.csv")
  orduak = {'10:20-11:15': 3, '13:35-14:30': 6, '11:45-12:40': 4, '11:15-11:45': 0, '08:30-9:25': 1, '14:30-15:20': 8, '12:40-13:35': 5, '09:25-10:20': 2}
  egunak = {'Asteartea': 2, 'Ostirala': 5, 'Asteazkena': 3, 'Astelehena': 1, 'Osteguna': 4}
  grdic = load_groups_rooms_file(egunak,orduak,"/home/asier/Hezkuntza/python-hezkuntza/python-fet/15-16/subgroups.xml")
  adic = extract_asigf_from_groups(grdic)
  print(teachers)
  wsdic,zdic = create_without_students_dict(teachers,ikasgaiak,egunak,orduak,"/home/asier/Hezkuntza/python-hezkuntza/python-fet/15-16/teachers.xml")
  adic.update(wsdic)
  gdic = extract_taldeak_from_groups(grdic)
  agrdic = {**grdic, **zdic}
  soluct = create_soluct_xml(agrdic,teachers,ikasgaiak,buildings)
  asigt = create_asigt_xml(adic,buildings,teachers,ikasgaiak)
  proft = create_proft_xml(teachers)
  grupt = create_grupt_xml(gdic)
  aulat = create_aulat_xml(buildings)
  nomasigt = create_nomasigt_xml(adic,ikasgaiak)
  tree = create_educa_xml()
  root = tree.getroot()
  root.append(asigt)
  root.append(nomasigt)
  root.append(proft)
  root.append(grupt)
  root.append(aulat)
  root.append(soluct)
  write_educa_xml(tree)
  
#LOAD Data!
def load_irakasle_file(CSVfile="irakasle.csv",interactive=False):
  #Besterik gabe, irakasleen hiztegia egiteko.
  #FIXME: Uste dut ez dela erabiltzen...
  irakasleak={}
  with open(CSVfile,'rt') as csvfile: 
    reader = csv.reader(csvfile,delimiter=',')
    for r in reader:
      irakasle={}
      if interactive:
        iz=input("Izena: ["+r[2]+"]:")
        if iz != "": irakasle['NOMBRE']=iz
      else:
        irakasle['NOMBRE']=r[2]
      irakasle['ABREV']=r[1]
      irakasle['DEPART']=r[3]
      irakasleak[r[0]]=irakasle
  return irakasleak

def load_gelak_file(CSVfile="gelak.csv",interactive=False):
  #FIXME: Uste dut ez dela erabiltzen...
  gelak={}
  with open(CSVfile,'rt') as csvfile: 
    reader = csv.reader(csvfile,delimiter=',')
    for r in reader:
      gela={}
      gela['EDIFICIO']=r[2]
      gela['ABREV']=r[0]
      gela['NOMBRE']=r[1]
      gelak[r[0]]=gela
  return gelak

def load_subjects_file(CSVfile="subjects.csv",interactive=False):
  #FIXME: Uste dut ez dela erabiltzen...
  subjects={}
  with open(CSVfile,'rt') as csvfile: 
    reader = csv.reader(csvfile,delimiter=',')
    for r in reader:
      subject={}
      subject['ABREV']=r[2]
      subject['NOMBRE']=r[1]
      subjects[r[0]]=subject
  return subjects


def load_groups_rooms_file(egunak,orduak,xmlfile='subgroups.xml'):
  #in: fet's subgroups.xml file
  #out: dic {u'M\xaa \xc1ngeles Mar466A': {'Group': [u'6A'], 'Room': '6.A', 'Hour': 6, 'Teacher': u'M\xaa \xc1ngeles Mar', 'Day': 4, 'Subject': u'F\xedsica'}}
  tree = ET.parse(xmlfile)
  root = tree.getroot()
  tgdic = {}
  for sb in root.findall('.//Subgroup'):
    sbg = sb.get('name')[0]+sb.get('name')[2]
    for eg in sb.findall('.//Day'):
      eguna = egunak[eg.get('name')]
      for ordu in eg.findall('.//Hour'):
        ordua = orduak[ordu.get('name')]
        for teacher in ordu.findall('.//Teacher'):
          sub = ordu.find('.//Subject').get('name')
          room = ordu.find('.//Room')
          if room != None:
            room = room.get('name')
          else:
            room = ""
          key = teacher.get('name')+str(eguna)+str(ordua)+sbg#+sbg gabe, group=[1A,1B]
          if not key in tgdic.keys():
            di = {'Teacher':teacher.get('name'),'Subject':sub,'Day':eguna,'Hour':ordua,'Room':room,'Group':[sbg]}
            tgdic[key] = di
          else:
            if not sbg in  tgdic[key]['Group']: tgdic[key]['Group'].append(sbg)
  return tgdic

#a=load_groups_rooms_file()
#create_soluct_xml(a)

def extract_asigf_from_groups(grdic):
  #in dic:u'M\xaa \xc1ngeles Mar466A': {'Group': [u'6A'], 'Room': '6.A', 'Hour': 6, 'Teacher': u'M\xaa \xc1ngeles Mar', 'Day': 4, 'Subject': u'F\xedsica'}}
  #out: dic: { u'3KIbai Go\xf1iHiritartasuna3.JK': {'Count': 1, 'Room': '3.JK', 'Group': '3K', 'Teacher': u'Ibai Go\xf1i', 'Subject': 'Hiritartasuna'}}
  asigdic={}
  for key in grdic.keys():
    newkey = grdic[key]['Group'][0]+grdic[key]['Teacher']+grdic[key]['Subject']+grdic[key]['Room']
    if not newkey in asigdic.keys():
      ad={'Teacher':grdic[key]['Teacher'],'Group':grdic[key]['Group'][0],'Subject':grdic[key]['Subject'],
	  'Room':grdic[key]['Room'],'Count':1}
      asigdic[newkey]=ad
    else:
      asigdic[newkey]['Count']+=1
  return asigdic

def get_asigf_abrev(adic):
  #DIC bat sortu, baina eskuz esan ikasgai izen bakoitzaren laburdura
  subjects={}
  for k in adic.keys(): 
    if not adic[k]['Subject'] in subjects.keys():
      iz = input("Ikagaia: ["+adic[k]['Subject']+"]:")
      if iz != "": 
        subjects[adic[k]['Subject']] = {'ABREV':iz}
      else:
        subjects[adic[k]['Subject']] = {'ABREV':adic[k]['Subject']}
  return subjects



def extract_taldeak_from_groups(grdic):
  #in dic:u'M\xaa \xc1ngeles Mar466A': {'Group': [u'6A'], 'Room': '6.A', 'Hour': 6, 'Teacher': u'M\xaa \xc1ngeles Mar', 'Day': 4, 'Subject': u'F\xedsica'}}
  #out: {'5H': {'ABREV': '5H', 'GRUPO': '5.H', 'CURSO': '5'}}
  gdic = {}
  for key in grdic.keys():
    g = {}
    ga = grdic[key]['Group'][0]
    g['ABREV'] = ga
    g['CURSO'] = ga[0]
    g['GRUPO'] = ga[0]+"."+ga[1]
    gdic[ga] = g
    
  return gdic
  
#a=load_groups_rooms_file()
#for b in a.keys():
  #if a[b]['Teacher']=='Alfontso Muruzabal':print(a[b])

            
#Create XML for educa
def create_educa_xml():
  tree = ET.ElementTree()
  now = datetime.now()
  #root=ET.Element("xml",
		  #{'encoding':'utf-8',
		    #'version'='1.0',
		    #})
  #educa=ET.SubElement(root,"SERVICIO",
  educa=ET.Element("SERVICIO",
			      {'autor':"Asier Urio's Fet Importer",
				'fecha':now.strftime('%Y/%m/%d %H:%M:%S'),
				'modulo':"Ordutegiak",		 #Horarios?
				}) 
  tree._setroot(educa)
  return tree
  
def write_educa_xml(tree,educafile="educa.xml"):
  print(tree)
  tree.write(educafile,
           xml_declaration=True,encoding='utf-8',
           method="xml")  
  


def create_proft_xml(irakasleak):
  proft=ET.Element("PROFT")
  ID=0
  for irakasle in irakasleak.keys():
    ID+=1
    ET.SubElement(proft, 'PROFF',
			      {'ABREV':irakasleak[irakasle]['ABREV'],
				'DEPART':irakasleak[irakasle]['DEPART'],
				'ID':str(ID),
				'NOMBRE':irakasle,#irakasleak[irakasle]['NOMBRE'],			
				}) 
  indent(proft)
  return proft

def create_aulat_xml(gelak):
  aulat=ET.Element("AULAT")
  ID=0
  for gela in gelak.keys():
    ID+=1
    ET.SubElement(aulat, 'AULAF',
			      {'ABREV':gelak[gela]['ABREV'],
				'EDIFICIO':gelak[gela]['EDIFICIO'],
				'ID':str(ID),
				'MAXALUM':'0',
				'NOMBRE':gelak[gela]['NOMBRE'],			
				})   
  indent(aulat)			      
  return aulat
			     
def create_grupt_xml(taldeak):
  #in: {'5H': {'ABREV': '5H', 'GRUPO': '5.H', 'CURSO': '5'}}
  grupt=ET.Element("GRUPT")
  ID = 0
  for key in taldeak.keys():
    ID += 1
    if taldeak[key]['CURSO'] <= '4':
      nivel = 'ESO'
    elif taldeak[key]['CURSO'] > '4':
      nivel = 'BACH'
    else: 
      nivel = ''
    if taldeak[key]['GRUPO'][-1] in ['P','Q']:
      nivel = 'DIV'  
    if key[0] != 'b': ET.SubElement(grupt, 'GRUPF',
			      {'ABREV':taldeak[key]['ABREV'],
				'CURSO':taldeak[key]['CURSO'],
				'DESCRIP':'',
				'GRUPO':taldeak[key]['GRUPO'][-1],
				'ID':str(ID),
				'MAXALUM':'0',
				'NIVEL':nivel,
				'TURNO':'D',
				})
  indent(grupt)
  return grupt		


def create_asigt_xml(idic,buildings,teachers,ikasgaiak):
  #ind: dic: { u'3KIbai Go\xf1iHiritartasuna3.JK': {'Count': 1, 'Room': '3.JK', 'Group': '3K', 'Teacher': u'Ibai Go\xf1i', 'Subject': 'Hiritartasuna'}}
  #out: educa's ASIGT element
  asigt=ET.Element("ASIGT")
  ID=0
  for key in idic.keys():
    ID+=1
    if idic[key]['Room'] not in buildings.keys(): 
      print(idic[key]['Room'])
      #buildings[idic[key]['Room']]='1'
    if idic[key]['Group'][0]=='b':
      grup = ""
    else:
      grup = idic[key]['Group']
    if idic[key]['Room'] == "":
      aula = ""
      edificio = ""
    else:
      aula = buildings[idic[key]['Room']]['ABREV']
      edificio = buildings[idic[key]['Room']]['EDIFICIO']
    if idic[key]['Subject'] not in ikasgaiak.keys(): #teachers.keys()
        print(ikasgaiak[idic[key]['Subject']])
        ikasgaiak[idic[key]['Subject']]['ABREV'] = input("ABREV: ")
        ikasgaiak[idic[key]['Subject']]['NOMBRE'] = input("NOMBRE: ")
    ET.SubElement(asigt, 'ASIGF',
			      {'ASIG':ikasgaiak[idic[key]['Subject']]['ABREV'],
				'AULA':aula,
				'AULA1':'',
				'AULA2':'',
				'AULA3':'',
				'AULA4':'',
				'EDIFICIO': edificio,
				'GRUP':grup,
				'HORASEM':str(idic[key]['Count']),
				'ID':str(ID),
				'NALUM':'',
				'PROF':teachers[idic[key]['Teacher']]['ABREV'],
				'TIPO':'',
				})
  indent(asigt)
  return asigt

def create_soluct_xml(saioak,teachers,ikasgaiak,buildings): 
  #print(saioak[saioak.keys()[0]])#FIXME ezabatu
  #print(saioak)
  soluct=ET.Element("SOLUCT")
  for key in saioak.keys():
    if saioak[key]['Room'] not in buildings.keys():
        aula=""
    else:
        aula = buildings[saioak[key]['Room']]['ABREV']
    #print(key)
#    if not adic[k]['Subject'] in subjects.keys():
#      iz=input("Ikagaia: ["+adic[k]['Subject']+"]:")
    print(key,": ",saioak[key]['Group'])
    if saioak[key]['Group'] != ['']: 
        cur = saioak[key]['Group'][0][0]
    else:
        cur = ""
    if saioak[key]['Group'] != ['']: 
        grup = saioak[key]['Group'][0][1]
    else:
        grup = ""    
    if saioak[key]['Group'] != ['']: 
        cgrup = saioak[key]['Group'][0]
    else:
        cgrup = ""  
    if cur <= '4':
      nivel = 'ESO'
    elif cur > '4':
      nivel = 'BACH'
    else: 
      nivel = ''
    if grup in ['P','Q']:
      nivel = 'DIV' 
    ET.SubElement(soluct, 'SOLUCF',
			      {'ASIG':ikasgaiak[saioak[key]['Subject']]['ABREV'],
				'AULA': aula,
				'CODGRUPO': cgrup,
				'CURSO':cur,
				'DIA':str(saioak[key]['Day']),
				'GRUPO':grup,
				'HORA':str(saioak[key]['Hour']),
				'NIVEL':nivel,
				'PROF':teachers[saioak[key]['Teacher']]['ABREV'],
				'SESIONES':'1',
				'TAREA':'',
				'TURNO':'D',
				})
  indent(soluct)
  return soluct


def create_nomasigt_xml(asigc,ikasgaiak):   
  nomasigt = ET.Element("NOMASIGT")
  ID = 0
  for key in asigc.keys():
    ID += 1
    ET.SubElement(nomasigt, 'NOMASIGF',
			      {'ABREV':ikasgaiak[asigc[key]['Subject']]['ABREV'],
				'ACTIV':'1',
				'ID':str(ID),
				'NOMBRE':asigc[key]['Subject'],				
				})
  indent(nomasigt)
  return nomasigt


def create_without_students_dict(teachers, ikasgaiak,egunak,orduak,teachersfile="teachers.xml"):
  tree=ET.parse(teachersfile)
  root=tree.getroot()
  #Ikaslerik gabeko jarduerak lortzeko.
  #FIXME:Zaintzak ez ditu hartzen!!
      #<Hour name="08:30-9:25">
     #<Subject name="1.ZaintzaAintzira"></Subject><Room name="1.ReflexionAintzira"></Room>
    #</Hour>
  t={}
  d={}
  for irak in root.findall('.//Teacher'):
    irakizena=irak.get('name')
    print(irakizena)
    if irakizena not in teachers.keys():
        print(irakizena)
        teachers[irakizena]['ABREV'] = input("ABREV: ")
        teachers[irakizena]['DEPART'] = input("Depart: ")
    
    for eg in irak.findall('.//Day'):
      eguna=egunak[eg.get('name')]
      for ordu in eg.findall('.//Hour'):
        ordua=orduak[ordu.get('name')]
        subjects=ordu.findall('.//Subject')
        stud=ordu.findall(".//Students")
        rooma=ordu.findall(".//Room")
        if rooma != []:
            room = rooma[0].get('name')
        else:
            room = ""
        if stud == [] and subjects != []:
          #print(subjects[0].get('name'),ordua,eguna,irakizena)
          if subjects[0].get('name') not in ikasgaiak.keys():
            iz=input("Ikagaia: ["+subjects[0].get('name')+"]:")
            if iz != "": 
              ikasgaiak[subjects[0].get('name')]={'ABREV':iz}
            else:
              ikasgaiak[subjects[0].get('name')]={'ABREV':subjects[0].get('name')}	    
          t[irakizena+subjects[0].get('name')+str(ordua)+str(eguna)]={'Count':1,'Room':"",'Group':"b",'Teacher':irakizena,'Subject':subjects[0].get('name')}
          d[irakizena+subjects[0].get('name')+str(ordua)+str(eguna)]={'Teacher':irakizena,'Subject':subjects[0].get('name'),'Day':eguna,'Hour':ordua,'Room':room,'Group':[""]}
  return t,d

def create_teacher_groups_dict2(root):
  t={}
  for irak in root.findall('.//Teacher'):
    irakizena=irak.get('name')
    for eg in irak.findall('.//Day'):
      eguna=egunak[eg.get('name')]
      for ordu in eg.findall('.//Hour'):
        ordua=orduak[ordu.get('name')]
        subjects=ordu.findall('.//Subject')
        if subjects!=[]:
          sub=subjects[0].get('name')
          ikasgaia=sub
          for a in ordu.findall(".//Students"):
            if a !=[]:
              group=str(a.get('name')[0])+str(a.get('name')[2])
              key=irakizena+str(eguna)+str(ordua)+group
              if key in t.keys():
                t[key]['count']=t[key]['count']+1
              else:
                d={'teacher':irakizena,'group':group,'subject':sub,'day':eguna,'hour':ordua,'count':1}#FIXME count beti da bat, eguna eta ordua ezberdinuak direlako
                t[key]=d
  return t

def t_txikia(a):
  if a.get('name')[-1]=='P':
    return 'P'
  else:
    return ''



def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def prettify(elem):
  """Return a pretty-printed XML string for the Element.
  """
  rough_string = ET.tostring(elem, 'utf-8')
  reparsed = xml.dom.minidom.parseString(rough_string)
  return reparsed.toprettyxml(indent="\t")


#for k in tdic.keys():
  #print(tdic[k]['teacher'],tdic[k]['groups'],tdic[k]['subject'],tdic[k]['count'])

	  #if (gps in t.keys(): t[gps]=t[gps]+1
	#for ikas in ordu.findall('.//Students'):
	  #if ikas !=[] and (ikas.get('name'))[0]!='b':
	    
	    
	    
	    
	    #ikasleak=ikas.get('name')[0]+ikas.get('name')[2]
	    #if ikas.get('name')[-1]=='P':ikasleak=ikasleak+'P'
	    #print(irakizena,eguna,ordua,ikasleak,ikasgaia)
    #print(t)
    


#for a in root.findall(".//ASIGT/ASIGF[@ASIG='2FRA']"): print(a.attrib)
#Lortu ikasgaien izenak for a in root.findall(".//Students"): print(a.get('name')[0:3])
#list(set([a.get('name')[0:3] for a in root.findall(".//Students")]))
#taldeak=sorted(list(set([a.get('name')[0:3] for a in root.findall(".//Students")])))

	      

#Parseatu feten irteera *teachers.xml
#Irakurri, ikasgai, gela eta irakasleen ALIASAK BG01...
#Egin HASH,DIctionary bat horiekin
#Taldeen izenak moldatu <Students name="1 -H -Frantsesa -HA"> -> 1H (Ikusi errepikatzen diren, talde gehiago diren.. (egin behar da ASIGT bat talde bakoitzarako)
#Zenbatu ikasgai bera ikasle talde berekin zenbat ordu dituen
#ASIG,AULA,GRUP eta PROF dictionary hori erabiliz ezarri
#ASIG=ikasgaiak["IKT"], AULA=gelak["InformatikaGela1"], GRUP=taldeak["1H"], PROF=Irakasleak["Asier Urio"]... 
def load_ikasgaiak_from_fet(root):
  ikasgaiak=sorted(list(set([a.get('name')[0:3] for a in root.findall(".//Subject")])))
  for a in root.findall(".//Subject"):
      if a.get('name')[-2]=="_": a.set('name',a.get('name')[0:-2])
      if "aintza" in a.get('name'): a.set('name','Zaintza')    
      if "uardia" in a.get('name'): a.set('name','Zaintza')    
      if "Tutore Bilera" in a.get('name'): a.set('name','Tutore Bilera')    
  asigfall=[]                             
  asigf=[]   
  for a in t[1].findall('.//Hour'):
      b =  a.findall('.//Students')
      c =  a.findall('.//Subject')
  #    for d in c:
  #      print(d.get('name'))
      for x in b:
  #      print(x.get('name')[0:3])
        year=x.get('name')[0]
        group=x.get('name')[0]+x.get('name')[2]
        if x.get('name')[-1] == "P": 
          subject=d.get('name')[0:3]+"P"
        else:
          subject=d.get('name')[0:3]
        print('ASIG='+year+d.get('name')[0:3]+' GRUP='+group)
        asigfall.append('ASIG='+year+subject+' GRUP='+group)
  #Talde txikiak, talde normaltzat hartzen ditu, bihurtzen dudalako 2-k-p eta 2-k-h 2-k
  count={}
  for asig in asigfall:
    if asig in asigf: count[asig]=int(count[asig])+1
    else:
      asigf.append(asig)
      count[asig]=1
                            
                            
              
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
generate_all()
