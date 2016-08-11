import csv
import time
import xml.dom.minidom
from xml.etree import ElementTree as ET
from datetime import datetime
from itertools import chain

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


def get_years(root):
   years = sorted(list(set(b.get('CODGRUPO') for b in root.findall('.//SOLUCF'))))
   return years

def get_teachers(root):
   years = sorted(list(set(b.get('PROF') for b in root.findall('.//SOLUCF'))))
   return years

def open(edfile="educa.xml"):
   tree = ET.parse(edfile)
   root = tree.getroot()
   return tree,root

def create_table_years(root,year):
  table = ET.Element("table")
  headertr = ET.SubElement(table,"thead")
  headertd = ET.SubElement(headertr,"tr")
  headerth = ET.SubElement(headertd,"th")
  headerth.text = year
  for hour in range(1,9):
    hourtd =  ET.SubElement(table,"tr")
    for day in range(1,6):
      daytr =  ET.SubElement(hourtd,"td")
      l = root.findall('.//SOLUCF[@CODGRUPO="'+year+'"][@DIA="'+str(day)+'"][@HORA="'+str(hour)+'"]')
      for a in l: 
	subjectp = ET.SubElement(hourtd,"p")
	subjectp.text = a.get("ASIG") 
  return table


def create_table_teachers(root,teacher):
  table = ET.Element("table")
  headertr = ET.SubElement(table,"thead")
  headertd = ET.SubElement(headertr,"tr")
  headerth = ET.SubElement(headertd,"th")
  headerth.text = teacher_name(root,teacher)
  for hour in range(1,9):
    hourtd =  ET.SubElement(table,"tr")
    for day in range(1,6):
      daytr =  ET.SubElement(hourtd,"td")
      l = root.findall('.//SOLUCF[@PROF="'+teacher+'"][@DIA="'+str(day)+'"][@HORA="'+str(hour)+'"]')
      for a in l: 
	subjectp = ET.SubElement(hourtd,"p")
	subjectp.text = a.get("ASIG") + '(' + a.get("CODGRUPO") +')'
  return table

def teacher_name(root,cod):
  name = root.findall('.//PROFF[@ABREV="'+cod+'"]')[0].get('NOMBRE')
  return name

def start_html():
  html = ET.Element("html")
  head = ET.SubElement(html,"head")
  style = ET.SubElement(head,"style")
  style.text = """
table td 
{
  table-layout:fixed;
  width:20px;
  border-collapse: collapse;
  overflow:hidden;
  word-wrap:break-word;
  empty-cells: show;
}
td,th {
  min-width: 7em; /* the normal 'fixed' width */
  width: 7em; /* the normal 'fixed' width */
  max-width: 7em; /* the normal 'fixed' width, to stop the cells expanding */
}
tr,td { 
  border: solid;
  border-width: 1px 1px 1px 1px;
}"""
  body = ET.SubElement(html,"body")
  return html
  
  
t, r = open()
y = get_years(r)
html = start_html()
for year in y:
  html.append(create_table_years(r, year))
tree=ET.ElementTree()
indent(html)
tree._setroot(html)
tree.write("ordutegia_ikasle.html")
#ET.dump(html)
y = get_teachers(r)
html = start_html()
for year in y:
  html.append(create_table_teachers(r, year))
tree=ET.ElementTree()
indent(html)
tree._setroot(html)
tree.write("ordutegia_irakasle.html")