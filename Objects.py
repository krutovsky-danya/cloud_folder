# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 15:37:55 2019

@author: Даня
"""

class Obj():
    def __init__(self, name=None, kind=None):
        self.name = name
        self.kind = kind
    
    def changeName(self, name):
        self.name = name
    
    def info(self):
        return self.name
    
    def getKind(self):
        return self.kind

class File(Obj):
    def _init__(self, name=None, path=None):
        super().__init__(name=name, kind='File')
        self.path = path

class Folder(Obj):
    def __init__(self, name=None, f_id=None, parent=None):
        super().__init__(name=name, kind='Folder')
        self.id = f_id
        self.parent = parent
        self.folders = []
        self.files = []
    
    def addFile(self, file):
        self.files.append(file)
        
    def addFolder(self, folder):
        self.folders.append(folder)