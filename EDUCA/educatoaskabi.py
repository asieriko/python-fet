#!/usr/bin/python
import sys, getopt, os
import csv
import xml.dom.minidom
from lxml import etree as ET

path = "/home/asier/Hezkuntza/python-hezkuntza/python-fet/EDUCA/"

fileg = os.path.join(path,"educa.xml")
tree = ET.parse(fileg)     
root = tree.getroot()

solucfcvs = []
solucf = root.findall(".//SOLUCF")
for sol in solucf:
    solucfcvs.append([sol.attrib['PROF'],sol.attrib['ASIG'],sol.attrib['CURSO']+"_"+sol.attrib['ASIG'],sol.attrib['AULA'],sol.attrib['CODGRUPO'],sol.attrib['CURSO'],sol.attrib['DIA'],sol.attrib['HORA']])

headers = ['POSTU','IKASGAI','MAILA_IKASGAI','GELA','TALDEA','MAILA','EGUNA','ORDUA']

with open('ordutegia.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')
    spamwriter.writerow(headers)
    for s in solucfcvs:
        spamwriter.writerow(s)