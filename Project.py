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
                             QWidget)

class Cloud_Folder(QDialog):
    def __init__(self, parent=None):
        super(Cloud_Folder, self).__init__(parent)
        
        self.home = "Danya"
        self.folders = {"Danya" : ["HomeWork_OfCourse", "Pictures",
                                   "Documents"],
                        "Server" : ["ReadMe.txt"],
                        "Nickita" : ["Do Not Touch.f"],
                        "Vald" : ["Do Not Touch Me!.f"],
                        "Homework 4Tb" : ["Hmmmmm.f"]}
        
        self.createTree()
        self.createInventory()
        self.createInfo()
        self.createTab()
        
        layout = QGridLayout()
        layout.addWidget(QLabel("Path[S:Dnaya//"), 0, 0, 1, 3)
        layout.addLayout(self.Tree, 1, 0, 2, 1)
        layout.addLayout(self.Inventory, 1, 1)
        layout.addLayout(self.Info, 2, 1)
        layout.addWidget(self.Tab, 1, 2, 2, 1)
        
        self.setLayout(layout)
        
        self.setWindowTitle("Cloud Folder")
        #self.setWindowIcon()
        self.setGeometry(100, 100, 900, 250)
    
    def createTree(self):
        self.Tree = QVBoxLayout()
        
        self.root = QPushButton(self.home)
        self.root.setFlat(True)
        
        self.Tree.addWidget(self.root)
    
    def createInventory(self):
        self.Inventory = QVBoxLayout()
        self.Inventory.setGeometry(QRect(0, 0, 300, 300))
        self.changeInventory()
    
    def createInfo(self):
        self.Info = QHBoxLayout()
        self.Info.addWidget(QLabel("Info:"))
        lay = QVBoxLayout()
        A = QPushButton("Apply")
        lay.addWidget(A)
        B = QPushButton("Find someone")
        lay.addWidget(B)
        self.Info.addLayout(lay)
    
    def createTab(self):
        self.Tab = QTabWidget()
        
        tab_1 = QTreeWidget()
        tab_1_layout = QVBoxLayout()
        connections = ["Server", "Nickita", "Vald", "Homework 4Tb"]
        for i in connections:
            self.createLayer(tab_1, i)
    
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
            
    def createLayer(self, home, lay):
        a = QTreeWidgetItem(home, lay)
        if lay.count('.') == 0:
            for i in self.folders[lay]:
                self.createLayer(a, i)
            
        

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = Cloud_Folder()
    gallery.show()
    sys.exit(app.exec_()) 