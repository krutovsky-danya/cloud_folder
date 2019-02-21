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
                             QVBoxLayout,
                             QPushButton,
                             QTabWidget,
                             QWidget)

class Cloud_Folder(QDialog):
    def __init__(self, parent=None):
        super(Cloud_Folder, self).__init__(parent)
        
        self.home = "Danya"
        self.folders = {"Danya" : ["HomeWork_OfCourse", "Pictures",
                                   "Documents"],
                        "Server" : ["ReadMe.txt"],
                        "Nickita" : ["Do Not Touch"],
                        "Vlad" : ["Do Not Touch Me!"],
                        "Homework 4Tb" : ["Hmmmmm"]}
        
        self.createTree()
        self.createInventory()
        self.createTab()
        
        layout = QGridLayout()
        layout.addWidget(QLabel("Path[S:Dnaya//"), 0, 0, 1, 3)
        layout.addLayout(self.Tree, 1, 0, 2, 1)
        layout.addLayout(self.Inventory, 1, 1)
        layout.addWidget(QLabel("Info"), 2, 1)
        layout.addWidget(self.Tab, 1, 2, 2, 1)
        
        self.setLayout(layout)
        
        self.setWindowTitle("Cloud Folder")
        #self.setWindowIcon()
        self.setGeometry(100, 100, 900, 450)
    
    def createTree(self):
        self.Tree = QVBoxLayout()
        
        self.root = QPushButton(self.home)
        self.root.setFlat(True)
        
        self.Tree.addWidget(self.root)
    
    def createInventory(self):
        self.Inventory = QVBoxLayout()
        self.Inventory.setGeometry(QRect(0, 0, 300, 300))
        self.changeInventory()
    
    def createTab(self):
        self.Tab = QTabWidget()
        
        tab_1 = QWidget()
        tab_1_layout = QVBoxLayout()
        connections = ["Server", "Nickita", "Vald", "Homework 4Tb"]
        btns = []
        for i in range(len(connections)):
            btns.append(QPushButton(connections[i]))
            btns[i].setFlat(True)
            btns[i].clicked.connect(lambda:self.changeInventory(_name=connections[i]))
            tab_1_layout.addWidget(btns[i])
    
        tab_1.setLayout(tab_1_layout)
        
        tab_2 = QLabel()
        #tab_2.setPixmap(QPixmap("bebop.jpg"))
        
        
        self.Tab.addTab(tab_1, "&Connected")
        self.Tab.addTab(tab_2, "&Preview")
    
    def changeInventory(self, _name=None):
        self.Inventory = QVBoxLayout()
        if _name == None:
            _name = self.home
        for i in self.folders[_name]:
            btn = QPushButton(i)
            print(i)
            self.Inventory.addWidget(btn)
            
        

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = Cloud_Folder()
    gallery.show()
    sys.exit(app.exec_()) 