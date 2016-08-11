from PyQt5 import uic, QtWidgets, QtCore, QtGui
import sys
import teachereval

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.ui = uic.loadUi('mainwindow.ui', self)
        self.ui.openteachers.clicked.connect(self.openxml)
        self.ui.outputcsv.clicked.connect(self.opencsvdir)
        self.ui.process.clicked.connect(self.processdata)
        self.ui.exit.clicked.connect(self.close)
        self.inputxmlf = ""
        self.outcsvdir = ""
        self.name = ""
        self.show()

    @QtCore.pyqtSlot()
    def openxml(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home/asier')
        self.inputxmlf = fname[0]
        self.ui.inputxml.setText(self.inputxmlf)
        d =fname[0].rfind("/")
        self.name = fname[0][d+1:]
        self.outcsvdir = fname[0][:d]
        self.ui.outputcsvdir.setText(self.outcsvdir)

    @QtCore.pyqtSlot()
    def opencsvdir(self):
        dname = QtWidgets.QFileDialog.getExistingDirectory(self, 'Open file', '/home/asier')
        self.outcsvdir = dname
        self.ui.outputcsvdir.setText(dname)

    @QtCore.pyqtSlot()
    def processdata(self):
        print("Process to: " + self.outcsvdir+self.name+".csv")
        tdic, sumdic = teachereval.evaluate(self.inputxmlf)
        for key in sumdic.keys():
            self.ui.tableWidget.setItem(int(key), 0, QtWidgets.QTableWidgetItem(str(sumdic[key])))

        try:
            file = self.outcsvdir+self.name+".csv"
            teachereval.write(tdic,sumdic,file)
            QtWidgets.QMessageBox.information(self, 'File writed', ''' Results writed in: ''' + file,QtWidgets.QMessageBox.Ok)
        except Exception as e:
            print("Error writing file: ", e)
            QtWidgets.QMessageBox.critical(self, 'Error', ''' Error writing csv file''',QtWidgets.QMessageBox.Ok)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())
