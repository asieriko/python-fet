#!/usr/bin/env python3
from PyQt5 import uic, QtWidgets, QtCore, QtGui
import xml.etree.ElementTree as ET
from lxml import etree
import sys, os
#import ../TimetableEval/teachereval


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.ui = uic.loadUi("/".join(os.path.realpath(__file__).split('/')[:-1])+'/'+'mainwindow.ui', self)
        self.ui.zaintzakButton.clicked.connect(self.getZaintzaTeachers)
        self.ui.denakButton.clicked.connect(self.getTeachers)
        self.ui.libreButton.clicked.connect(self.getFreeTeachers)
        self.ui.ateraButton.clicked.connect(self.close)
        self.ui.openB.clicked.connect(self.openxml)
        self.teacherCB.activated[str].connect(self.fillTimetable)
        self.ui.listWidget.currentItemChanged.connect(self.fillTimetable2)
        self.ui.tableWidget.setHorizontalHeaderLabels(["Astelehena","Asteartea","Asteazkena","Osteguna","Ostirala"]);
        self.ui.tableWidget.setVerticalHeaderLabels(["08:30\n-\n9:25","09:25\n-\n10:20","10:20\n-\n11:15","11:15\n-\n11:45","11:45\n-\n12:40","12:40\n-\n13:35","13:35\n-\n14:30","14:30\n-\n15:20"]);
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(1)
        self.ui.tableWidget.verticalHeader().setSectionResizeMode(1)
        self.ui.tableWidget_2.setVerticalHeaderLabels(["Extremos mañana","Extremos mediodia","Huecos","Entrar 1, Salir 6","Entrar 1, Salir 7","Dias completos"]);
        self.ui.tableWidget_2.setHorizontalHeaderLabels(["Kopurua"]);
        self.ui.tableWidget_2.verticalHeader().setSectionResizeMode(1)
        self.ui.denakRB.toggled.connect(self.tog)
        self.ui.zaintzakRB.toggled.connect(self.tog)
        self.ui.deusRB.toggled.connect(self.tog)
        self.inputxmlf = ""
        #self.center()
        self.show()
        self.colors = [QtGui.QColor("red"),QtGui.QColor("green"),QtGui.QColor("blue"),QtGui.QColor("magenta"), QtGui.QColor("yellow"),
        QtGui.QColor("cyan"),QtGui.QColor("gray"),QtGui.QColor("darkRed"),QtGui.QColor("darkGreen"),
        QtGui.QColor("darkBlue"),QtGui.QColor("darkMagenta"),QtGui.QColor("darkYellow"),QtGui.QColor("darkCyan"),QtGui.QColor("darkGray"),QtGui.QColor("lightGray")]

    @QtCore.pyqtSlot()
    def openxml(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home/asier',"teachers.xml files (*teachers.xml)")
        self.inputxmlf = fname[0]
        self.setWindowTitle = "Ordutegia - " + self.inputxmlf
        self.getTeachers()
        self.evaluateAll()

    @QtCore.pyqtSlot()
    def tog(self):
        self.fillTimetable(self.ui.listWidget.currentItem().text())


    def getFreeTeachers(self):
        et = etree.parse(self.inputxmlf)
        sel = self.ui.tableWidget.selectedRanges()
        hour = self.ui.tableWidget.verticalHeaderItem(sel[0].topRow()).text().replace('\n','')
        day = self.ui.tableWidget.horizontalHeaderItem(sel[0].leftColumn()).text()
        allteachers = [at.attrib.get('name') for at in et.xpath(".//Teacher")]
        bussyteachers = [at.getparent().getparent().getparent().attrib.get('name') for at in et.xpath(".//Teacher/Day[@name='"+day+"']/Hour[@name='"+hour+"']/Subject")]
        freeteachers = sorted(list(set(allteachers)-set(bussyteachers)))
        current = self.ui.teacherCB.currentText()
        self.tlist = []
        if current not in freeteachers:
            self.tlist.append(current)
        for t in freeteachers:
            self.tlist.append(t) #if the selected teacher has Zaintza it gets duplicated
        self.ui.teacherCB.clear()
        self.ui.teacherCB.addItems(self.tlist)
        self.ui.listWidget.clear()
        self.ui.listWidget.addItems(self.tlist)


    def getZaintzaTeachers(self):
        et = etree.parse(self.inputxmlf)
        #print(et.xpath(".//Teacher[Day[@name='Astelehena']/Hour[@name='08:30-9:25']/Subject[@name='Zaintza']]"))
        #print(et.xpath(".//Teacher/Day[@name='Astelehena']/Hour[@name='08:30-9:25']/not(Subject)"))
        sel = self.ui.tableWidget.selectedRanges()
        hour = self.ui.tableWidget.verticalHeaderItem(sel[0].topRow()).text().replace('\n','')
        day = self.ui.tableWidget.horizontalHeaderItem(sel[0].leftColumn()).text()
        teachers = et.xpath(".//Teacher/Day[@name='"+day+"']/Hour[@name='"+hour+"']/Subject[@name='Zaintza']")
        self.tlist = [self.ui.teacherCB.currentText()]
        for t in teachers:
            self.tlist.append(t.getparent().getparent().getparent().attrib.get('name')) #if the selected teacher has Zaintza it gets duplicated
        self.ui.teacherCB.clear()
        self.ui.teacherCB.addItems(self.tlist)
        self.ui.listWidget.clear()
        self.ui.listWidget.addItems(self.tlist)


    def getTeachers(self):
      self.tree = ET.parse(self.inputxmlf)
      self.root = self.tree.getroot()
      teachers = self.root.findall(".//Teacher")
      self.tlist = list(teacher.attrib.get('name') for teacher in teachers)
      self.ui.teacherCB.clear()
      self.ui.teacherCB.addItems(self.tlist)
      self.ui.listWidget.clear()
      self.ui.listWidget.addItems(self.tlist)
      self.fillTimetable(self.root.findall(".//Teacher")[0].attrib.get('name')) #fixme: get from the list

    def fillTimetable2(self,curr,prev):
        self.ui.teacherCB.setCurrentIndex(self.tlist.index(curr.text()))
        self.fillTimetable(str(curr.text()))

    def fillTimetable(self,text):
        self.ui.listWidget.item(self.tlist.index(text)).setSelected(True)
        self.ui.listWidget.setCurrentRow(self.tlist.index(text))
        sel = self.ui.tableWidget.selectedRanges()
        self.ui.tableWidget.clearContents()
        for s in sel:
            self.ui.tableWidget.setRangeSelected(s, True)
        dayt = 0
        sl = []
        teacher = self.root.findall(".//Teacher[@name='"+text+"']")[0]
        days = teacher.findall(".//Day")
        for day in days:
            hourt = 0
            hours = day.findall(".//Hour")
            for hour in hours:
                subject = hour.findall(".//Subject")
                if subject != []:
                    subject = subject[0].attrib.get('name')
                    room = hour.findall(".//Room")
                    if room != []:
                        room = room[0].attrib.get('name')
                    else:
                        room = ""
                    students = hour.findall(".//Students")
                    s = ""
                    for student in students:
                        s = s + student.attrib.get('name')
                    scolor = str(subject)+s
                    if students != [] and  not scolor in sl:
                        sl.append(scolor)
                    self.ui.tableWidget.setItem(int(hourt), int(dayt), QtWidgets.QTableWidgetItem(str(subject)+" \n "+str(s)+" \n "+str(room)))
                    if not self.ui.deusRB.isChecked():
                        if subject == "Zaintza":
                            self.ui.tableWidget.item(int(hourt), int(dayt)).setBackground(QtGui.QColor(QtGui.QColor(100,100,150)));
                            if room[-1] == "2" :
                                self.ui.tableWidget.item(int(hourt), int(dayt)).setTextAlignment(2);
                                if self.ui.denakRB.isChecked():
                                    self.ui.tableWidget.item(int(hourt), int(dayt)).setForeground(QtGui.QColor(QtGui.QColor("white")))
                    if self.ui.denakRB.isChecked() and scolor in sl:
                            self.ui.tableWidget.item(int(hourt), int(dayt)).setBackground(self.colors[sl.index(scolor)])
                            if s != "" and s[0] < "3" :
                                self.ui.tableWidget.item(int(hourt), int(dayt)).setTextAlignment(2);
                                self.ui.tableWidget.item(int(hourt), int(dayt)).setForeground(QtGui.QColor(QtGui.QColor("white")))
                    self.ui.tableWidget.resizeRowToContents(int(hourt))
                hourt += 1
            dayt += 1
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(1)
        self.ui.tableWidget.verticalHeader().setSectionResizeMode(1)
        self.evaluate(text)



    def evaluateAll(self):
        #FIXME: This function is a duplicate of the one in ../TimetableEval/teachereval.py
        teachers = self.root.findall(".//Teacher")
        tdic={}
        sumdic={}
        for teacher in teachers:
            totalpre=0
            totalpost=0
            total1and6=0
            total1and7=0
            totalgaps=0
            name=teacher.attrib.get('name')
            days = teacher.findall(".//Day")
            for day in days:
                hours=day.findall(".//Hour")
                prefirst=-1#1. hutsunea?
                activities=0
                lastactivity=6
                first=False
                last6=False
                last7=False
                atsedenaldi=0
                gaps=0
                for i in range(len(hours)):
                    subject=hours[i].findall(".//Subject")
                    if subject == [] and i-1 == prefirst: prefirst=i
                    if subject == [] and i==3 and prefirst == 2: atsedenaldi = -1
                    if subject == [] and i-1 != prefirst: gaps += 1
                    if subject != []: activities += 1
                    if subject != []: lastactivity = i
                    if subject != [] and i==0: first=True
                    if subject != [] and i==6: last6=True
                    if subject != [] and i==7:
                        last7=True
                        last6=False
                if prefirst<6:
                    totalpre += prefirst+1+atsedenaldi #+1 hasten delako 0n, eta <6, bestela esan nahi duelako egun osoa 7 orduak libre dituela, bestela atsedenaldia hutsune bezala hartzen du
                    if lastactivity>3 and prefirst<3:
                        totalgaps += lastactivity - activities - prefirst - 1
                    else:
                        totalgaps += lastactivity - activities - prefirst
                #if prefirst<6: totalgaps = gaps - (6-lastactivity)
                if lastactivity<6: totalpost += 6-lastactivity
                if lastactivity<=3:totalpost -= 1 #atsedenaldia hutsune bezlaa ez hartzeko
                if first and last6: total1and6 += 1
                if first and last7: total1and7 += 1
            tdic[name.encode('utf-8')]=(name.encode('utf-8'),totalpre,totalpost,totalgaps,total1and6,total1and7,total1and6+total1and7)
            if total1and6+total1and7 in sumdic.keys():
                sumdic[total1and6+total1and7] += 1
            else:
                sumdic[total1and6+total1and7] = 1

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)

        msg.setText("Global Timetable Results")
        header=sumdic.keys()
        text = ""
        for key in sumdic.keys():
            text += "\n"+ str(key) + ":\t " + str(sumdic[key]) 
        print(text)
        
        msg.setInformativeText(text)
        msg.setWindowTitle("Timbetable results")
        
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msg.exec_()
        
        return tdic, sumdic

    def evaluate(self,teachername):
        teacher = self.root.findall(".//Teacher[@name='"+teachername+"']")[0]
        totalpre=0
        totalpost=0
        total1and6=0
        total1and7=0
        totalgaps=0
        days = teacher.findall(".//Day")
        for day in days:
          hours=day.findall(".//Hour")
          prefirst=-1#1. hutsunea?
          activities=0
          lastactivity=6
          first=False
          last6=False
          last7=False
          atsedenaldi=0
          gaps=0
          for i in range(len(hours)):
            subject=hours[i].findall(".//Subject")
            if subject == [] and i-1 == prefirst: prefirst=i
            if subject == [] and i==3 and prefirst == 2: atsedenaldi = -1
            if subject == [] and i-1 != prefirst: gaps += 1
            if subject != []: activities += 1
            if subject != []: lastactivity = i
            if subject != [] and i==0: first=True
            if subject != [] and i==6: last6=True
            if subject != [] and i==7:
              last7=True
              last6=False
          if prefirst<6:
            totalpre += prefirst+1+atsedenaldi #+1 hasten delako 0n, eta <6, bestela esan nahi duelako egun osoa 7 orduak libre dituela, bestela atsedenaldia hutsune bezala hartzen du
            if lastactivity>3 and prefirst<3:
              totalgaps += lastactivity - activities - prefirst - 1
            else:
              totalgaps += lastactivity - activities - prefirst
          #if prefirst<6: totalgaps = gaps - (6-lastactivity)
          if lastactivity<6: totalpost += 6-lastactivity
          if lastactivity<=3:totalpost -= 1 #atsedenaldia hutsune bezlaa ez hartzeko
          if first and last6: total1and6 += 1
          if first and last7: total1and7 += 1
        items = [totalpre,totalpost,totalgaps,total1and6,total1and7,total1and6+total1and7]
        for i in range(6):
            self.ui.tableWidget_2.setItem(i, 0, QtWidgets.QTableWidgetItem(str(items[i])))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())