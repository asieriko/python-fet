#!/usr/bin/python
import sys, getopt
import csv

from lxml import etree as ET

file = "/home/asier/fet-results/timetables/Horario-16-17-multi/1/Horario-16-17_subgroups.xml"

tree = ET.parse(file)     
root = tree.getroot()

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
                    if sub != [] and Matrix[j][i].count(sub[0].attrib['name'])==0:
                        #print(d.attrib['name'],h.attrib['name'],sub[0].attrib['name'])
                        #print(i,j)
                        Matrix[j][i].append(sub[0].attrib['name'])
                    j += 1
                i += 1
        print(group)
        if group[0]<"5" or group[-1] < 'H':
            dbh = True
        else:
            dbh = False
        printmat(Matrix,dbh,verbose)

def printmat(mat,dbh=True,verbose=False):
    if dbh: 
        h = 7
    else:
        h = 8
    for j in range(h):
        for i in range(5):
            if mat[j][i] == [] and j != 3  and not((j == 7) and (i == 4)):
                print(mat[j][i],"FALTA!!",end="\t")
            elif verbose:
                print(mat[j][i],end="\t")
        if verbose: print()


groups = ['1-A','1-B','1-C','1-D','1-E','1-H','1-I','1-J','1-K','1-L','2-A','2-B','2-C','2-D','2-H','2-I','2-J','3-A','3-B','3-C','3-P','3-H','3-I','3-J','3-K','3-Q','4-A','4-B','4-C','4-D','4-H','4-I','4-J','4-K','4-L','5-A','5-B','5-H','5-I','5-J','6-A','6-B','6-H','6-I','6-J']
findsg(groups)