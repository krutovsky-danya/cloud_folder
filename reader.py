# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 20:43:12 2019

@author: Даня
"""
import csv

FilesDataFromServer = {}
with open('FilesDataFromServer.csv', newline='') as csvfile:
    fresh = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in fresh:
        data = row[1][1:-1]
        a = data.split('), (')
        for i in range(len(a)):
            if len(a[i]) > 0:
                if a[i][0] == '(':
                    a[i] = a[i][1:]
                if a[i][-1] == ')':
                    a[i] = a[i][:-1]
                n = a[i].rfind(' ')
                x = a[i][:n - 1]
                y = a[i][n + 1:]
                a[i] = (x[1:-1] , int(y))
            else:
                a = []
        
        FilesDataFromServer[row[0]] = a

for i in FilesDataFromServer:
    print(i, FilesDataFromServer[i])
        