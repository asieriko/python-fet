import csv
import time
import xml.dom.minidom
from xml.etree import ElementTree as ET
from datetime import datetime
from itertools import chain
from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, ParagraphProperties,TableCellProperties
from odf import table, text

def get_years(root):
   years = sorted(list(set(b.get('CODGRUPO') for b in root.findall('.//SOLUCF'))))
   return years

def get_teachers(root):
   years = sorted(list(set(b.get('PROF') for b in root.findall('.//SOLUCF'))))
   return years

def get_rooms(root):
   rooms = sorted(list(set(b.get('AULA') for b in root.findall('.//SOLUCF'))))
   return rooms


def open(edfile="../educa.xml"):
   tree = ET.parse(edfile)
   root = tree.getroot()
   return tree,root

def teacher_name(root,cod):
  name = root.findall('.//PROFF[@ABREV="'+cod+'"]')[0].get('NOMBRE')
  return name

def room_name(root,cod):
  if cod == "": return "" #FIXME gela batzuk jarri gabe daude, zaintzak eta bilerak...
  name = root.findall('.//AULAF[@ABREV="'+cod+'"]')[0].get('NOMBRE')
  #r.findall('.//AULAF[@ABREV="1A5"]')[0].get('NOMBRE')
  return name  
  
t, r = open()
y = get_years(r)


textdoc = OpenDocumentText()
# Create a style for the paragraph with page-break
withbreak = Style(name="WithBreak", parentstylename="Standard", family="paragraph")
withbreak.addElement(ParagraphProperties(breakbefore="page"))
textdoc.automaticstyles.addElement(withbreak)

TAB_style = Style(name="Table", family="table-cell")
TAB_style.addElement(TableCellProperties(border="0.05pt solid #000000"))
textdoc.automaticstyles.addElement(TAB_style)

h1style = Style(name="Heading 1", family="paragraph")
h1style.addElement(TextProperties(attributes={'fontsize':"24pt",'fontweight':"bold" }))
h1style.addElement(ParagraphProperties(breakbefore="page"))
textdoc.automaticstyles.addElement(h1style)

p = text.P(text=u'Horarios por grupos')
textdoc.text.addElement(p)



for year in y:
  #p = text.P(stylename=withbreak,text=year)
  h=text.H(outlinelevel=1, stylename=h1style, text=year)
  textdoc.text.addElement(h)
  #textdoc.text.addElement(p)
  datatable = table.Table(name="local-table")
  t = table.TableColumns()
  t.addElement(table.TableColumn(numbercolumnsrepeated=6))
  datatable.addElement(t)
  t = table.TableRows()
  datatable.addElement(t)
  tr = table.TableRow()
  t.addElement(tr)
  for eguna in ('Saioa','Astelehena','Asteartea','Asteazkena','Osteguna','Ostirala'):
    tc = table.TableCell(valuetype="string", stylename="Table")
    tc.addElement(text.P(text=eguna))
    tr.addElement(tc)
  rownum = 0
  for hour in range(1,8):
    if hour == 4:
      tr = table.TableRow()
      t.addElement(tr)
    tr = table.TableRow()
    t.addElement(tr)
    tc = table.TableCell(valuetype="string", stylename="Table")
    tr.addElement(tc)
    tc.addElement(text.P(text=hour))
    for day in range(1,6):
      tc = table.TableCell(valuetype="string", stylename="Table")
      tr.addElement(tc)
      l = r.findall('.//SOLUCF[@CODGRUPO="'+year+'"][@DIA="'+str(day)+'"][@HORA="'+str(hour)+'"]')
      for a in l: 
	tc.addElement(text.P(text=a.get("ASIG") + ' (' + teacher_name(r,a.get("PROF")) +' - '+ room_name(r,a.get("AULA"))+')'))
    rownum += 1
  textdoc.text.addElement(datatable)
  

textdoc.save("ordutegia_ikasle.odt")
print "ikasle"


textdoc = OpenDocumentText()
# Create a style for the paragraph with page-break
withbreak = Style(name="WithBreak", parentstylename="Standard", family="paragraph")
withbreak.addElement(ParagraphProperties(breakbefore="page"))
textdoc.automaticstyles.addElement(withbreak)
p = text.P(text=u'Horarios por profesores')
textdoc.text.addElement(p)

TAB_style = Style(name="Table", family="table-cell")
TAB_style.addElement(TableCellProperties(border="0.05pt solid #000000"))
textdoc.automaticstyles.addElement(TAB_style)

h1style = Style(name="Heading 1", family="paragraph")
h1style.addElement(TextProperties(attributes={'fontsize':"24pt",'fontweight':"bold" }))
h1style.addElement(ParagraphProperties(breakbefore="page"))
textdoc.automaticstyles.addElement(h1style)

teachers = get_teachers(r)

for teacher in teachers:
  h=text.H(outlinelevel=1, stylename=h1style,text=teacher_name(r,teacher))
  textdoc.text.addElement(h)
  datatable = table.Table(name="local-table")
  t = table.TableColumns()
  t.addElement(table.TableColumn(numbercolumnsrepeated=6))
  datatable.addElement(t)
  t = table.TableRows()
  datatable.addElement(t)
  tr = table.TableRow()
  t.addElement(tr)
  for eguna in ('Saioa','Astelehena','Asteartea','Asteazkena','Osteguna','Ostirala'):
    tc = table.TableCell(valuetype="string", stylename="Table")
    tr.addElement(tc)
    tc.addElement(text.P(text=eguna))
  rownum = 0
  for hour in range(1,8):
    if hour == 4:
      tr = table.TableRow()
      t.addElement(tr)
    tr = table.TableRow()
    t.addElement(tr)
    tc = table.TableCell(valuetype="string", stylename="Table")
    tr.addElement(tc)
    tc.addElement(text.P(text=hour))
    for day in range(1,6):
      tc = table.TableCell(valuetype="string", stylename="Table")
      tr.addElement(tc)
      l = r.findall('.//SOLUCF[@PROF="'+teacher+'"][@DIA="'+str(day)+'"][@HORA="'+str(hour)+'"]')
      if l != []: tc.addElement(text.P(text=l[0].get("ASIG") + ' (' + room_name(r,l[0].get("AULA"))+')'))
      groups = sorted(list(set(a.get("CODGRUPO") for a in  l)))
      tc.addElement(text.P(text=", ".join(groups)))
    rownum += 1
  textdoc.text.addElement(datatable)
  
textdoc.save("ordutegia_irakasle.odt")
print "irakasle"

#ROOMS
textdoc = OpenDocumentText()
# Create a style for the paragraph with page-break
withbreak = Style(name="WithBreak", parentstylename="Standard", family="paragraph")
withbreak.addElement(ParagraphProperties(breakbefore="page"))
textdoc.automaticstyles.addElement(withbreak)
p = text.P(text=u'Horarios por aulas')
textdoc.text.addElement(p)

TAB_style = Style(name="Table", family="table-cell")
TAB_style.addElement(TableCellProperties(border="0.05pt solid #000000"))
textdoc.automaticstyles.addElement(TAB_style)

h1style = Style(name="Heading 1", family="paragraph")
h1style.addElement(TextProperties(attributes={'fontsize':"24pt",'fontweight':"bold" }))
h1style.addElement(ParagraphProperties(breakbefore="page"))
textdoc.automaticstyles.addElement(h1style)

rooms = get_rooms(r)

for room in rooms:
  h=text.H(outlinelevel=1, stylename=h1style, text=room_name(r,room))
  textdoc.text.addElement(h)
  datatable = table.Table(name="local-table")
  t = table.TableColumns()
  t.addElement(table.TableColumn(numbercolumnsrepeated=6))
  datatable.addElement(t)
  t = table.TableRows()
  datatable.addElement(t)
  tr = table.TableRow()
  t.addElement(tr)
  for eguna in ('Saioa','Astelehena','Asteartea','Asteazkena','Osteguna','Ostirala'):
    tc = table.TableCell(valuetype="string", stylename="Table")
    tr.addElement(tc)
    tc.addElement(text.P(text=eguna))
  rownum = 0
  for hour in range(1,8):
    if hour == 4:
      tr = table.TableRow()
      t.addElement(tr)
    tr = table.TableRow()
    t.addElement(tr)
    tc = table.TableCell(valuetype="string", stylename="Table")
    tr.addElement(tc)
    tc.addElement(text.P(text=hour))
    for day in range(1,6):
      tc = table.TableCell(valuetype="string", stylename="Table")
      tr.addElement(tc)
      l = r.findall('.//SOLUCF[@AULA="'+room+'"][@DIA="'+str(day)+'"][@HORA="'+str(hour)+'"]')
      if l != []:
	teachers = sorted(list(set(teacher_name(r,a.get("PROF")) for a in  l)))
	tc.addElement(text.P(text=l[0].get("ASIG") + ' (' + ", ".join(teachers) +')'))
      groups = sorted(list(set(a.get("CODGRUPO") for a in  l)))
      tc.addElement(text.P(text=", ".join(groups)))
    rownum += 1
  textdoc.text.addElement(datatable)
  
textdoc.save("ordutegia_gela.odt")