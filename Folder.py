# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 19:13:26 2019

@author: Даня
"""

class Folder():
    def __init__(self, name = None, id = None, parent_id = None):
        self.name = name
        self.id = id
        self.parent_id = parent_id
        self.folders = []
        self.files = []
        self.path = None 

    def changeName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def addFile(self, file):
        self.files.append(file)

    def addFolder(self, folder):
        self.folders.append(folder)

    def setPath(self, item):
        self.path = item
