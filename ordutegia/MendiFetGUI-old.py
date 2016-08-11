from PySide.QtGui import *
from PySide.QtCore import *
import sys
#import Teacher

class lineEditDelegate(QStyledItemDelegate):

  def __init__(self, model, parent=None):
      super(lineEditDelegate, self).__init__(parent)
      self.parent= parent
      self.model= model

  def createEditor(self, parent, option, index):

      if not index.isValid():
          return False

      self.currentIndex=index  

      self.lineEdit = QLineEdit(parent)
      value = index.data(Qt.DisplayRole)
      self.lineEdit.text=value #setCurrentIndex(value)

      return self.lineEdit

  def setEditorData(self, editor, index):
      value = index.data(Qt.DisplayRole)
      editor.text = value

  def setModelData(self, editor, model, index):

      if not index.isValid():
          return False

      index.model().setData(index, editor.text, Qt.EditRole)

  def paint(self, painter, option, index):
      currentIndex= index.data(Qt.DisplayRole)

      opt= QStyleOptionComboBox()
      opt.rect= option.rect
      currentComboIndex= self.model.createIndex(1,0)#(index,0)
      opt.currentText= self.model.data(currentComboIndex, Qt.DisplayRole)
      
      QApplication.style().drawComplexControl(QStyle.CC_ComboBox, opt, painter)

      QStyledItemDelegate.paint(self, painter, option, index)

class TeacherModel(QAbstractTableModel):
    def __init__(self, datain, parent = None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
#def loadEducaXml(self,fileName)
#...
    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role == Qt.UserRole:
            return self.arraydata
        elif role != Qt.DisplayRole:
            return None
        #elif role == Qt.EditRole:
            #return str(self.arraydata[index.row()][index.column()])
        return (self.arraydata[index.row()][index.column()])

    def lerroadata(self, index, role):
        if not index.isValid():
            return None
        elif role == Qt.UserRole:
            return self.arraydata
        elif role != Qt.DisplayRole:
            return None
        return (self.arraydata[index.row()])
#def saveEducaXml(self,fileName)
#...
#def saveFetXml(self,fileName)
#...
    def saveModel(self):
        for row in range(len(self.arraydata)):
          for column in range(len(self.arraydata[0])):
            print self.arraydata[row][column]
        
    def setData(self, index, value,role):
        self.arraydata[index.row()][index.column()] = value
        return True
     
    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

      
class Window(QMainWindow):
   
   def __init__(self, parent = None):
   
      QMainWindow.__init__(self, parent)      
      
      csvfile='/home/asier/Hezkuntza/2013-2014/Kudeaketa/fet/ordutegiak/denagarbi.csv'
      separator=','
      s=[line.rstrip().split(separator) for line in open(csvfile,'r')]

      headers=s[0]
      raw_data=s[1:]

    
      self.setWindowTitle("Ordutegiak prestatzeko EIG")
      widget = QWidget()
      
      self.tablemodel = TeacherModel(raw_data)
      print headers
      #tablemodel.headerData=headers

      projectView = QTableView()
      projectView.setModel(self.tablemodel)

      #projectView.setColumnCount(len(headers))
      #projectView.setHorizontalHeaderLabels(headers)
      self.selectionModel = projectView.selectionModel()

      #led = lineEditDelegate(self.tablemodel)
      #projectView.setItemDelegateForColumn(1, led);
      projectView.show()
      vbox = QVBoxLayout(self)
      b=QPushButton("Gorde")
      d=QPushButton("hautapena")
      e=QPushButton("Atera")
      vbox.addWidget(projectView)
      vbox.addWidget(d)
      vbox.addWidget(b)
      vbox.addWidget(e)
      b.show()
      d.show()
      e.show()
      widget.setLayout(vbox)
      self.setCentralWidget(widget)
      b.clicked.connect(self.tablemodel.saveModel)
      d.clicked.connect(self.fillSelection)
      e.clicked.connect(quit)
            
      self.setLayout(vbox)  
      
   def fillSelection(self):
      indexes = self.selectionModel.selectedIndexes()
      for index in indexes:
         text = u"(%i,%i)" % (index.row(), index.column())
         print text
         print self.tablemodel.data(index,Qt.DisplayRole)
         print self.tablemodel.lerroadata(index,Qt.DisplayRole)

      
if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())      