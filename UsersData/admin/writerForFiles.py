import csv
FilesDataFromServer = {'0': [],
                       '1': [("Girl1.jpg", 1), ("Girl2.jpg", 2), ("Girl3.jpg", 3)],
                       '2': [("Art1.jpg", 4), ("Art2.jpg", 5), ("Art3.jpg", 6)],
                       '3': [("Gif1.gif", 7), ("Gif2.gif", 8), ("Gif3.gif", 9)],
                       '4': [("Saturn V.jpg", 10), ("Oppy.jpg", 11), ("F-1.jpg", 12)]}

print(FilesDataFromServer)

with open('FilesDataFromServer.csv', 'w', newline='') as csvfile:
     spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|',
                             quoting=csv.QUOTE_MINIMAL)
     for i in FilesDataFromServer:
         spamwriter.writerow([i, FilesDataFromServer[i]])
