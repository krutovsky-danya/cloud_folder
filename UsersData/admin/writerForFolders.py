import csv

FoldersDataFromServer = [["admin", 0, None],
                         ["Girls", 1, 0],
                         ["JustAwesomeArts", 2, 0],
                         ["ABitOfGifs", 3, 0],
                         ["RocketThings", 4, 0]]

with open('FoldersDataFromServer.csv', 'w', newline='') as csvfile:
     spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|',
                             quoting=csv.QUOTE_MINIMAL)
     for i in FoldersDataFromServer:
         spamwriter.writerow(i)
