# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 19:27:10 2019

@author: Даня
"""

from PyQt5.QtCore import QRect
#from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication,
                             QDialog,
                             QGridLayout,
                             QLabel,
                             QHBoxLayout,
                             QVBoxLayout,
                             QPushButton,
                             QTabWidget,
                             QTreeWidget,
                             QTreeWidgetItem,
                             QWidget,
                             QMainWindow)

class Cloud_Folder(QWidget):
    def __init__(self, parent=None):
        super(Cloud_Folder, self).__init__(parent)
        
        self.home = "Danya"
        self.folders = {"Danya" : ["HomeWork_OfCourse.", "Pictures.",
                                   "Documents."],
                        "Server" : ["ReadMe.txt"],
                        "Nickita" : ["Do Not Touch.f"],
                        "Vald" : ["Do Not Touch Me!.f"],
                        "Homework 4Tb" : ["Hmmmmm.f"]}
        
        self.createTree()
        self.createInventory()
        self.createServer()
        
        layout = QHBoxLayout()
        #layout.addWidget(QLabel("Path[S:Dnaya//"), 0, 0, 1, 3)
        layout.addWidget(self.Tree)
        layout.addLayout(self.Inventory)
        layout.addWidget(self.Server)
        
        self.setLayout(layout)
        
        self.setWindowTitle("Cloud Folder")
        #self.setWindowIcon()
        self.setGeometry(100, 100, 900, 250)
    
    def createTree(self):
        self.Tree = QTreeWidget()
        self.Tree.header().setVisible(False)
        self.createLay(self.Tree, self.home)
        
        
    def createInventory(self):
        self.Inventory = QVBoxLayout()
        self.Boxes = QHBoxLayout()
        self.UserBox = QWidget()
        self.ServerBox = QWidget()
        self.Boxes.addWidget(self.UserBox)
        self.Boxes.addWidget(self.ServerBox)
        self.Inventory.addLayout(self.Boxes)
        self.createInfo()
        self.Inventory.addLayout(self.Info)
        
    
    def createInfo(self):
        self.Info = QHBoxLayout()
        self.Info.addWidget(QLabel("Info:"))
        lay = QVBoxLayout()
        A = QPushButton("Apply")
        lay.addWidget(A)
        B = QPushButton("Find someone")
        lay.addWidget(B)
        self.Info.addLayout(lay)
    
    def createServer(self):
        self.Server = QTabWidget()
        
        tab_1 = QTreeWidget()
        tab_1.header().setVisible(False)
        tab_1_layout = QVBoxLayout()
        connections = ["Server", "Nickita", "Vald", "Homework 4Tb"]
        for i in connections:
            self.createLay(tab_1, i)
    
        tab_1.setLayout(tab_1_layout)
        
        tab_2 = QLabel()
        #tab_2.setPixmap(QPixmap("bebop.jpg"))
        
        
        self.Server.addTab(tab_1, "&Connected")
        self.Server.addTab(tab_2, "&Preview")
    
    def changeInventory(self, _name=None):
        self.Inventory = QVBoxLayout()
        if _name == None:
            _name = self.home
        for i in self.folders[_name]:
            btn = QPushButton(i)
            print(i)
            self.Inventory.addWidget(btn)
            
    def createLay(self, home, lay):
        a = QTreeWidgetItem(home, [lay])
        if lay.count('.') == 0:
            for i in self.folders[lay]:
                self.createLay(a, i)

        

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setCentralWidget(Cloud_Folder())
    win.show()
    sys.exit(app.exec_()) 