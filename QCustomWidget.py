# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 19:24:25 2019

@author: Даня
"""

from PyQt5.QtWidgets import (QLabel,
                             QHBoxLayout,
                             QWidget)

class QCustomQWidget (QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.textLabel = QLabel()
        self.layout.addWidget(self.textLabel)
        self.setLayout(self.layout)
        self.obj = None
        self.id = None

    def setText(self, text):
        self.text = text
        self.textLabel.setText(text)

    def setObject(self, obj):
        self.obj = obj

    def getText(self):
        return self.text

    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type

    def getObject(self):
        return self.obj

    def setID(self, id):
        self.id = id

    def getID(self):
        return self.id