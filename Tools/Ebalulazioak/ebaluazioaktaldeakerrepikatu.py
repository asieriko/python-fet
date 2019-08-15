import xml.etree.ElementTree as ET
import sys, getopt
import csv
import random
from collections import defaultdict

def extractinfoXML(inputfile,forbiden):
    tree = ET.parse(inputfile)
    root = tree.getroot()
    teachers = root.findall(".//Teacher")
    tdic={}
    gdic= defaultdict(list)
    allgroups=[]
    for teacher in teachers:
        groups=[]
        name=teacher.attrib.get('name')
        #print(name)
        students = teacher.findall(".//Students")
        for group in students:
            #print(group.attrib.get('name')[:3])
            if group.attrib.get('name')[0] in forbiden:
                #print("FFFF:",group.attrib.get('name')[:3])
                continue
            if group.attrib.get('name')[:3] not in groups:
                groups.append(group.attrib.get('name')[:3])
            if group.attrib.get('name')[:3] not in allgroups:
                allgroups.append(group.attrib.get('name')[:3])
            if name not in gdic[group.attrib.get('name')[:3]]:
                gdic[group.attrib.get('name')[:3]].append(name)
        tdic[name] = groups
    return allgroups,gdic,tdic


def evaluate(g1,g2):
    t=[]
    conf = 0
    for teacher in g1:
            if teacher in g2:
                conf += 1
    return conf


f = "/home/asier/Hezkuntza/SGCC-Erregistroak-18-19/PR01 Matriculacion y planificacion docente y servicios complementarios/PR0102 Planificacion/Horarios/Horario-18-19-Version7_teachers_LOmXmpv.xml"
fb = ['M','b','B','6','U']
a,g,t = extractinfoXML(f,fb)



for k1 in sorted(g.keys()):
    for k2 in sorted(g.keys()):
        print(k1,";",k2,";",evaluate(g[k1],g[k2]))
