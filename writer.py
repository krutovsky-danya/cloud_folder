# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 20:10:04 2019

@author: Даня
"""

import csv

FoldersDataFromServer = [["Danya", 0, None],
                         ["Downloads", 1, 0],
                         ["Desktop", 2, 0],
                         ["Homeworks", 3, 0],
                         ["Downloads", 4, 1],
                         ["Drivers", 5, 1],
                         ["Python", 6, 2],
                         ["Trash", 7, 2],
                         ["Economics", 8, 3],
                         ["Under13", 9, 3]]

with open('FoldersDataFromServer.csv', 'w', newline='') as csvfile:
     spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|',
                             quoting=csv.QUOTE_MINIMAL)
     for i in FoldersDataFromServer:
         spamwriter.writerow(i)
