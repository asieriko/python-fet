#!/usr/bin/python
import sys, getopt
import csv

from lxml import etree as ET



import time
import xml.dom.minidom
#from xml.etree import ElementTree as ET
from datetime import datetime
from itertools import chain
from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, ParagraphProperties,TableCellProperties
from odf import table, text

fileg = "/home/asier/Hezkuntza/python-hezkuntza/python-fet/EDUCA/subgroups.xml"
filet = "/home/asier/Hezkuntza/python-hezkuntza/python-fet/EDUCA/teachers.xml"

tree = ET.parse(fileg)     
root = tree.getroot()

tree2 = ET.parse(filet)     
root2 = tree2.getroot()

orduak = ['08:30-9:25','09:25-10:20','10:20-11:15', '11:15-11:45','11:45-12:40','12:40-13:35', '13:35-14:30','14:30-15:20']
textdoc = OpenDocumentText()
#def textdoc_init():
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


def print_odf(Matrix,name):
    hours = len(Matrix)
    h=text.H(outlinelevel=1, stylename=h1style, text=name)
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
        tc.addElement(text.P(text=eguna))
        tr.addElement(tc)
    for hour in range(hours):
        if hour == 3:
            tr = table.TableRow()
            t.addElement(tr)
            continue
        tr = table.TableRow()
        t.addElement(tr)
        tc = table.TableCell(valuetype="string", stylename="Table")
        tr.addElement(tc)
        tc.addElement(text.P(text=orduak[hour]))
        for day in range(5):
            tc = table.TableCell(valuetype="string", stylename="Table")
            tr.addElement(tc)
            tc.addElement(text.P(text=' - '.join(Matrix[hour][day])))
    textdoc.text.addElement(datatable)
    

    textdoc.save("ordutegia_ikasle.odt")


def findsg(groups,verbose=False):
    for group in groups:
        subgroups = root.xpath(".//Subgroup[starts-with(@name,'"+group+"')]")
        w, h = 5, 8 
        Matrix = [[[] for x in range(w)] for y in range(h)] 
        for s in subgroups: 
            #print(s.attrib['name'])
            ds = s.findall(".//Day")
            i = 0
            for d in ds:
                hs = d.findall(".//Hour")
                j = 0
                for h in hs:
                    sub = h.findall(".//Subject")
                    room = h.findall(".//Room")
                    if sub != [] and Matrix[j][i].count(sub[0].attrib['name']+' ('+room[0].attrib['name']+')')==0:
                        #print(d.attrib['name'],h.attrib['name'],sub[0].attrib['name'])
                        #print(i,j)
                        Matrix[j][i].append(sub[0].attrib['name']+' ('+room[0].attrib['name']+')')
                    j += 1
                i += 1
        print(group)
        if group[0]<"5" or group[-1] < 'H':
            dbh = True
        else:
            dbh = False
        printmat(Matrix,verbose)
        print_odf(Matrix,group)


def findt():
        teachers = root2.xpath(".//Teacher")
        w1, h1 = 5, 8 
        #Matrix = [[[] for x in range(w)] for y in range(h)]
        for s in teachers: 
            group = s.attrib.get('name')
            #print(s.attrib['name'])
            ds = s.findall(".//Day")
            i = 0
            Matrix = [[[] for x in range(w1)] for y in range(h1)]
            for d in ds:
                hs = d.findall(".//Hour")
                j = 0
                for h in hs:
                    sub = h.findall(".//Subject")
                    stud = h.findall(".//Students")
                    stu = []
                    for st in stud:
                        stu.append(st.attrib.get('name'))
                    if sub != [] and Matrix[j][i].count(sub[0].attrib['name'])==0:
                        #print(d.attrib['name'],h.attrib['name'],sub[0].attrib['name'])
                        #print(i,j)
                        if stu != '':
                            text = sub[0].attrib['name'] + ' (' + '-'.join(stu) + ')'
                        else:
                            text = sub[0].attrib['name']
                        Matrix[j][i].append(text)
                    j += 1
                i += 1
            print(group)
            print_odf(Matrix,group)


def printmat(mat,verbose=False):
    h = len(mat)
    for j in range(h):
        for i in range(5):
            if mat[j][i] == [] and j != 3  and not((j == 7) and (i == 4)):
                print(mat[j][i],"FALTA!!",end="\t")
            elif verbose:
                print(mat[j][i],end="\t")
        if verbose: print()


groups = ['1-A','1-B','1-C','1-D','1-E','1-H','1-I','1-J','1-K','1-L','2-A','2-B','2-C','2-D','2-P','2-H','2-I','2-J','3-A','3-B','3-C','3-P','3-H','3-I','3-J','3-K','3-Q','4-A','4-B','4-C','4-D','4-H','4-I','4-J','4-K','4-L','5-A','5-B','5-H','5-I','5-J','6-A','6-B','6-H','6-I','6-J']
#textdoc_init()
findsg(groups)
#findt()