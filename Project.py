# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 19:27:10 2019

@author: Даня
"""

from PyQt5.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel,
                             QVBoxLayout, QPushButton, QTabWidget, QWidget)

class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)
        
        self.createTree()
        self.createInventory()
        self.createTab()
        
        layout = QGridLayout()
        layout.addLayout(self.Tree, 0, 0, 2, 1)
        layout.addWidget(QLabel("Inventory"), 0, 1)
        layout.addWidget(QLabel("Info"), 1, 1)
        layout.addWidget(self.Tab, 0, 2, 2, 1)
        
        self.setLayout(layout)
        
        self.setWindowTitle("Cloud Folder")
        #self.setWindowIcon()
    
    def createTree(self):
        self.Tree = QVBoxLayout()
        
        Danya = QPushButton("Danya")
        Danya.setFlat(True)
        
        self.Tree.addWidget(Danya)
    
    def createTab(self):
        self.Tab = QTabWidget()
        
        tab_1 = QWidget()
        tab_1_layout = QVBoxLayout()
        connection = ["Server", "Nickita", "Vald", "Homework 4Tb"]
        
        for i in connection:
            btn = QPushButton(i)
            btn.setFlat(True)
            tab_1_layout.addWidget(btn)
    
        tab_1.setLayout(tab_1_layout)
        
        tab_2 = QWidget()
        
        self.Tab.addTab(tab_1, "&Connected")
        self.Tab.addTab(tab_2, "&Preview")

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec_()) 