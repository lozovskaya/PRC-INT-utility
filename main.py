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
        
        # Left
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Right
        self.DATbtn = QPushButton('Select *.DAT-File')
        self.INFbtn = QPushButton('Select *.INF-File')
        self.SETbtn = QPushButton('Select *.SET-File')
        self.DATline = QLineEdit()
        self.DATline.setReadOnly(True)
        self.INFline = QLineEdit()
        self.INFline.setReadOnly(True)
        self.SETline = QLineEdit()
        self.SETline.setReadOnly(True)
        self.analysis = QPushButton("Analyse")
        self.analysis.setEnabled(False)

        self.right = QVBoxLayout()
        self.right.setMargin(5)
        self.right.addWidget(self.DATbtn)
        self.right.addWidget(self.DATline)
        self.right.addWidget(self.INFbtn)
        self.right.addWidget(self.INFline)
        self.right.addWidget(self.SETbtn)
        self.right.addWidget(self.SETline)
        self.right.addWidget(self.analysis)
        
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.table)
        self.layout.addLayout(self.right)
        self.setLayout(self.layout)
        
        # Signals & Slots
        self.DATbtn.clicked.connect(self.getfileDAT)
        self.INFbtn.clicked.connect(self.getfileINF)
        self.SETbtn.clicked.connect(self.getfileSET)
        self.DATline.textChanged[str].connect(self.check_disable)
        self.INFline.textChanged[str].connect(self.check_disable)
        self.SETline.textChanged[str].connect(self.check_disable)
        self.analysis.clicked.connect(self.fill_table)
        
        '''terminal = QSplitter(Qt.Vertical)
        # self.output = QPlainTextEdit()
        terminal.addWidget(self.table)
        terminal.addWidget(self.SETbtn)'''
    @Slot()
    def fill_table(self):
        data = union.main(self.DATline.text(), self.INFline.text(), self.SETline.text())
        self.table.setColumnCount(len(data[0].plain_table[0]))
        self.table.setHorizontalHeaderLabels(data[0].plain_table[0])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        items = 0
        for rows in data[0].plain_table:
            print(rows)
            self.table.insertRow(items)
            for i in range(len(rows)):
                self.table.setItem(items, i, QTableWidgetItem(rows[i]))
            items += 1

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
        self.setCentralWidget(widget)
    
        
    @Slot()
    def exit_app(self, checked):
        QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    widget = Widget()
    window = MainWindow(widget)
    window.resize(1000, 800)
    window.show()

    sys.exit(app.exec_())
