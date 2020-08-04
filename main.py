#!/usr/bin/env python3
import sys
import union
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import *
from PySide2.QtGui import *

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Right
        width = 300
        height = 30
        self.DATbtn = QPushButton('Select *.DAT-File')
        self.DATbtn.setFixedSize(width, height)
        self.INFbtn = QPushButton('Select *.INF-File')
        self.INFbtn.setFixedSize(width, height)
        self.SETbtn = QPushButton('Select *.SET-File')
        self.SETbtn.setFixedSize(width, height)
        self.DATline = QLineEdit()
        self.DATline.setReadOnly(True)
        self.DATline.setFixedSize(width, height)
        self.INFline = QLineEdit()
        self.INFline.setReadOnly(True)
        self.INFline.setFixedSize(width, height)
        self.SETline = QLineEdit()
        self.SETline.setReadOnly(True)
        self.SETline.setFixedSize(width, height)
        self.analysis = QPushButton("Analyze")
        self.analysis.setEnabled(True) 

        self.right = QVBoxLayout()
        self.right.setMargin(5)
        self.right.setSizeConstraint(QLayout.SetFixedSize)
        self.right.addWidget(self.DATbtn)
        self.right.addWidget(self.DATline)
        self.right.addWidget(self.INFbtn)
        self.right.addWidget(self.INFline)
        self.right.addWidget(self.SETbtn)
        self.right.addWidget(self.SETline)
        self.right.addWidget(self.analysis)


        # Left 
        self.left = QVBoxLayout()
        self.left.setMargin(5)
        
        self.layout = QHBoxLayout()
        self.layout.addLayout(self.left)
        self.layout.addLayout(self.right)
        self.setLayout(self.layout)
        
        # Signals & Slots
        self.DATbtn.clicked.connect(self.getfileDAT)
        self.INFbtn.clicked.connect(self.getfileINF)
        self.SETbtn.clicked.connect(self.getfileSET)
        '''self.DATline.textChanged[str].connect(self.check_disable)
        self.INFline.textChanged[str].connect(self.check_disable)
        self.SETline.textChanged[str].connect(self.check_disable)'''
        self.analysis.clicked.connect(self.fill_all_tables)
        

    @Slot()
    def fill_all_tables(self):
        data = union.main(self.DATline.text(), self.INFline.text(), self.SETline.text())
        self.tables = []
        self.titles = []
        for i in range(len(data)):
            self.table = QTableWidget()
            self.title = QTextEdit()
            self.title.setReadOnly(True)
            self.text = "WINDOW NUMBER: {}\nnumber of extents: {}\nselected extents: {}".format(i + 1, data[i].number_of_extents, data[i].selected_extents)
            print(self.text)
            self.title.setText(self.text)
            self.left.addWidget(self.title)
            self.left.addWidget(self.table)
            self.tables.append(self.table)
            self.titles.append(self.title)
        for i in range(0, len(data)):
            self.fill_table(i, data[i])

    @Slot()
    def fill_table(self, number, datum):
        self.tables[number].setColumnCount(len(datum.plain_table[0]))
        self.tables[number].setHorizontalHeaderLabels(datum.plain_table[0])
        self.tables[number].horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        items = 0
        for j in range(1, len(datum.plain_table)):
            rows = datum.plain_table[j]
            self.tables[number].insertRow(items)
            for i in range(len(rows)):
                self.tables[number].setItem(items, i, QTableWidgetItem(rows[i]))
            items += 1
        self.tables[number].setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tables[number].setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  
        self.tables[number].setMaximumSize(self.getQTableWidgetSize(number))
        self.tables[number].setMinimumSize(self.getQTableWidgetSize(number))
        self.titles[number].setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.titles[number].setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  
        self.titles[number].setMaximumSize(self.getQTitleWidgetSize(number))
        self.titles[number].setMinimumSize(self.getQTitleWidgetSize(number))
        print(self.getQTableWidgetSize(number))

    @Slot()
    def getQTitleWidgetSize(self, number):
        w = self.getQTableWidgetSize(number).width()
        h = 75
        return QSize(w, h)

    @Slot()
    def getQTableWidgetSize(self, number):
        w = self.tables[number].verticalHeader().width() + 4 
        for i in range(self.tables[number].columnCount()):
            w += self.tables[number].columnWidth(i) + 10
        h = self.tables[number].horizontalHeader().height() + 4
        for i in range(self.tables[number].rowCount()):
            h += self.tables[number].rowHeight(i)
        return QSize(w, h)

    @Slot()
    def check_disable(self):
        if (not self.DATline.text() or not self.INFline.text() or not self.SETline.text()):
            self.analysis.setEnabled(False)
            self.analysis.setStyleSheet("background-color: none")
        else:
            self.analysis.setEnabled(True)
            self.analysis.setStyleSheet("background-color: red")

    @Slot() 
    def getfileDAT(self):
      fname = QFileDialog.getOpenFileName(self, filter="*.DAT *.dat")
      print(fname)
      self.DATline.setText(fname[0])
    
    @Slot()
    def getfileINF(self):
      fname = QFileDialog.getOpenFileName(self, filter="*.INF *.inf")
      self.INFline.setText(fname[0])
    
    @Slot()
    def getfileSET(self):
      fname = QFileDialog.getOpenFileName(self, filter="*.SET *.set")
      self.SETline.setText(fname[0])



class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("PRC-INT")
        
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("")

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)
        self.file_menu.addAction(exit_action)

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(widget)
        self.setCentralWidget(self.scroll)
    
        
    @Slot()
    def exit_app(self, checked):
        QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    widget = Widget()
    window = MainWindow(widget)
    window.resize(2000, 1600)
    window.show()

    sys.exit(app.exec_())
