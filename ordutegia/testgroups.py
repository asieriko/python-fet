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
from odf.style import Style, TextProperties, ParagraphProperties,TableCellProperties, GraphicProperties
from odf.text import P, H, List, ListItem
from odf.table import Table, TableColumn, TableRow, TableCell
from odf import table, text

fileg = "/home/asier/Hezkuntza/python-hezkuntza/python-fet/ordutegia/subgroups.xml"
filet = "/home/asier/Hezkuntza/python-hezkuntza/python-fet/ordutegia/teachers.xml"

tree = ET.parse(fileg)     
root = tree.getroot()

tree2 = ET.parse(filet)     
root2 = tree2.getroot()

orduak = ['08:30-9:25','09:25-10:20','10:20-11:15', '11:15-11:45','11:45-12:40','12:40-13:35', '13:35-14:30','14:30-15:20']


h1style = Style(name="Heading 1",  family="paragraph",parentstylename="Heading 1")
h1style.addElement(GraphicProperties(fill="solid",fillcolor="#e6e6ff"))
h1style.addElement(TextProperties(attributes={'fontsize':"14pt",'fontweight':"bold",'color':"#000099" }))
h1style.addElement(ParagraphProperties(breakbefore="page",margintop="0.4cm",marginbottom="0.2cm",backgroundcolor="#e6e6ff",padding="0.05cm",borderleft="none",borderright="none",bordertop="none",borderbottom="2.01pt solid #000099",shadow="none"))

# Create a style for the paragraph with page-break
withbreak = Style(name="WithBreak", parentstylename="Standard", family="paragraph")
withbreak.addElement(ParagraphProperties(breakbefore="page"))

TAB_style = Style(name="Table", family="table-cell")
TAB_style.addElement(TableCellProperties(border="0.05pt solid #000000"))

tableheaders = Style(name="Table Headers", family="paragraph", parentstylename="Standard")
tableheaders.addElement(ParagraphProperties(numberlines="false", linenumber="0",textalign="center",margintop="0.2cm",marginbottom="0.2cm"))
tableheaders.addElement(TextProperties(attributes={'fontsize':"12pt",'fontweight':"bold"}))

def createdoc():
    
    textdoc = OpenDocumentText()
    #def textdoc_init():
    textdoc.automaticstyles.addElement(withbreak)
    textdoc.automaticstyles.addElement(TAB_style)
    textdoc.styles.addElement(tableheaders)
    textdoc.automaticstyles.addElement(h1style)
    return textdoc


def print_odf(Matrix,name,textdoc,odtfile):    
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
        tc = TableCell(stylename="Table")
        tr.addElement(tc)
        p = P(stylename=tableheaders,text=eguna)
        tc.addElement(p)
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
    

    textdoc.save(odtfile)


def findsg(groups,verbose=False):
    textdoc = createdoc()            
    p = text.P(text=u'Horarios por grupos')
    textdoc.text.addElement(p)
    
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
        print_odf(Matrix,group,textdoc,"ordutegia_ikasle.odt")


def findt():
    teachers = root2.xpath(".//Teacher")
    textdoc = createdoc()       
    #p = text.P(text=u'Horarios por profesores')
    #textdoc.text.addElement(p)
    
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
                room = h.findall(".//Room")
                stu = []
                for st in stud:
                    stu.append(st.attrib.get('name'))
                if sub != [] and Matrix[j][i].count(sub[0].attrib['name'])==0:
                    #print(d.attrib['name'],h.attrib['name'],sub[0].attrib['name'])
                    #print(i,j)
                    if stu != '' and sub[0].attrib['name'] != 'Zaintza' and sub[0].attrib['name'][:2] != 'MB':
                        text = sub[0].attrib['name'] + ' (' + '-'.join(stu) + ')'
                    elif sub[0].attrib['name'] == 'Zaintza':
                        text = sub[0].attrib['name'] + ' (' + room[0].attrib['name'] + ')'
                    elif  sub[0].attrib['name'][:2] == 'MB':
                        text = sub[0].attrib['name'] + ' (' + room[0].attrib['name'][0] + ')'
                    else:
                        text = sub[0].attrib['name']
                    Matrix[j][i].append(text)
                j += 1
            i += 1
        print(group)
        print_odf(Matrix,group,textdoc,"ordutegia_irakasle.odt")


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
findt()
