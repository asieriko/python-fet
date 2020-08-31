#!/usr/bin/python
import sys, getopt
import json

from datetime import datetime
from itertools import chain
from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, ParagraphProperties,TableCellProperties, GraphicProperties
from odf.text import P, H, List, ListItem
from odf.table import Table, TableColumn, TableRow, TableCell
from odf import table, text

fileu = "/home/asier/Hezkuntza/python-hezkuntza/python-fet/teachergroups.json"
files = "/home/asier/Hezkuntza/python-hezkuntza/python-fet/teachergroups-es.json"


h1style = Style(name="Heading 1",  family="paragraph",parentstylename="Heading 1")
h1style.addElement(GraphicProperties(fill="solid",fillcolor="#e6e6ff"))
h1style.addElement(TextProperties(attributes={'fontsize':"14pt",'fontweight':"bold",'color':"#000099" }))
h1style.addElement(ParagraphProperties(breakbefore="page",margintop="0.4cm",marginbottom="0.2cm",backgroundcolor="#e6e6ff",padding="0.05cm",borderleft="none",borderright="none",bordertop="none",borderbottom="2.01pt solid #000099",shadow="none"))

h2style = Style(name="Heading 2",  family="paragraph",parentstylename="Heading 2")
h2style.addElement(TextProperties(attributes={'fontsize':"12pt",'color':"#000099" }))
h2style.addElement(ParagraphProperties(margintop="0.2cm",marginbottom="0.2cm",padding="0.05cm",borderleft="none",borderright="none",bordertop="none",shadow="none"))

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
    textdoc.automaticstyles.addElement(h2style)
    return textdoc


def print_odf(groups,filejson,odtfile):    
    textdoc = createdoc()            
    p = text.P(text=u'Listado profesores por grupos')
    textdoc.text.addElement(p)
    
    with open(filejson) as data_file:    
        data = json.load(data_file)
    
    for group in groups:
        h=text.H(outlinelevel=1, stylename=h1style, text=group)
        textdoc.text.addElement(h)
        for teacher in data[group]:
            h=text.H(outlinelevel=2, stylename=h2style, text=teacher)
            textdoc.text.addElement(h)
    textdoc.save(odtfile)




groups = ['1-A','1-B','1-C','1-D','1-E','1-H','1-I','1-J','1-K','1-L','2-A','2-B','2-C','2-D','2-P','2-H','2-I','2-J','3-A','3-B','3-C','3-P','3-H','3-I','3-J','3-K','3-Q','4-A','4-B','4-C','4-D','4-H','4-I','4-J','4-K','4-L','5-A','5-B','5-H','5-I','5-J','6-A','6-B','6-H','6-I','6-J']
#textdoc_init()
print_odf(groups,files,"teacherlist.odt")
