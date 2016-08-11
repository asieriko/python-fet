import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QToolTip, QDialog, QInputDialog, QStatusBar, QFileDialog
from PyQt5.QtGui import QFont 
from PyQt5 import uic, QtCore
import MendiFet as MF


def generate(csvfile,days,hours,schoolname,fetfile):
    a=MF.MendiFet()
    #a.printm()
    a.read_csv_data(csvfile)
    a.set_hours(hours)
    a.set_days(days)
    a.set_name(schoolname)
    print("Generate from raw data")
    a.generate_from_raw_data()
    #a.no_class_hours_mendillorri()
    print("Generate teachers")
    a.generate_teachers_from_activities()
    print("Generate subjects")
    a.generate_subjects_from_activities()
    print("Generate rooms")
    a.generate_rooms_from_activities()
    print("Generate buildings")
    a.generate_buildings_from_rooms()
    print("Generate XML")
    a.create_groups_XML(a.generate_groups_from_activities())
    #a.printm()
    print("Write")
    a.write(fetfile)


class ConfUi(QDialog):
    def __init__(self):
        super(ConfUi, self).__init__()
        self.ui = uic.loadUi('configuredialog.ui', self)
        
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
                        
        self.ui.dayNames.addItems(["Astelehena","Asteartea","Asteazkena","Osteguna","Ostirala"]);
        self.ui.hourNames.addItems(["8.30 - 9.25","9.25 - 10.20","10.20 - 11.15","11.15 - 11.45","11.45 - 12.40","12.40 - 13.35","13.35 - 14.40","14.30 - 15.22"]);
        self.ui.addDay.clicked.connect(self.addday)
        self.ui.addHour.clicked.connect(self.addhour)
        self.ui.removeDay.clicked.connect(self.removeday)
        self.ui.removeHour.clicked.connect(self.removehour)
        self.show()

    @QtCore.pyqtSlot()
    def addday(self):
        nday, ok = QInputDialog.getText(self, 'Add New Day', 
            'Enter new Day:')
        
        if ok:
            self.ui.dayNames.addItem(nday)
    
    @QtCore.pyqtSlot()
    def addhour(self):
        nhour, ok = QInputDialog.getText(self, 'Add New Hour', 
            'Enter new Hour:')
        
        if ok:
            self.ui.hourNames.addItem(nhour)
            
    @QtCore.pyqtSlot()
    def removehour(self):
        pass
    
    @QtCore.pyqtSlot()
    def removeday(self):
        pass
  
    @QtCore.pyqtSlot()
    def reject(self):
        self.hide()
    
    @QtCore.pyqtSlot()
    def accept(self):
        self.hide()

class MendiFetGUI(QMainWindow):
    
    def __init__(self):
        super(MendiFetGUI, self).__init__()
        self.ui = uic.loadUi('mainwindow.ui', self)
       
        cui = ConfUi()
        cui.hide()
        
        #self.ui.statusBar.showMessage("Ready")
        self.ui.selectInput.clicked.connect(self.selectInputFile)
        self.ui.selectOutput.clicked.connect(self.selectOutputFile)
        self.ui.configure.clicked.connect(cui.show)
        self.ui.generate.clicked.connect(self.generateFile)
        self.show()
 

    @QtCore.pyqtSlot()
    def generateFile(self):
        if self.ui.inputfile.text() == '' or self.ui.outputfile.text() == '':
            print("Error")
        else:
            print("generate")
        pass

 
    @QtCore.pyqtSlot()
    def selectInputFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home/asier',"csv files (*.csv)")
        self.ui.inputfile.setText(fname[0])
    
    @QtCore.pyqtSlot()
    def selectOutputFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Save file', '/home/asier',"fet files (*.fet)")
        self.ui.outputfile.setText(fname[0])
            
            
if __name__ == '__main__':
    
    csvfile = '/home/asier/Hezkuntza/fet/ordutegia/denagarbi15-16.csv'
    fetfile = '/home/asier/Hezkuntza/fet/ordutegia/denagarbi15-16.fet'
    hours =['08:30-9:25','09:25-10:20', '10:20-11:15','11:15-11:45', '11:45-12:40','12:40-13:35', '13:35-14:30', '14:30-15:20' ]
    days = ['Astelehena', 'Asteartea', 'Asteazkena', 'Osteguna', 'Ostirala']
    schoolname = 'Mendillorri BHI'
    
    
    app = QApplication(sys.argv)
    ex = MendiFetGUI()
    #ex.statusbar.showMessage("external")
    sys.exit(app.exec_())
    
    
    