import socket, csv, threading

def mainThread(client, address):
    print("New thread for", str(address))
    command = client.recv(1024).decode()
    if command == "Login":
        client.send("Ready".encode())
        data = client.recv(1024).decode()
        login, password = data[0:data.find('~')], data[data.find('~') + 1:]

        if login in users and users[login] == password:
            client.send("Passed".encode())
            client.recv(1024).decode()
            print("Start1")

            file = open(("UsersData//" + login + "//FoldersDataFromServer.csv"), 'rb')
            l = file.read(1024)
            while (l):
                client.send(l)
                l = file.read(1024)
            file.close()
            print("Done1")

            client.recv(1024).decode()
            print("Start2")

            file = open(("UsersData//" + login + "//FilesDataFromServer.csv"), 'rb')
            l = file.read(1024)
            while (l):
                client.send(l)
                l = file.read(1024)
            file.close()
            print("Done2")

            client.recv(1024).decode()
            print("Done3")

            activeUsers[address[0]] = login
            client.close()

        elif login in users:
            client.send("LogIn".encode())
            client.close()

        else:
            client.send("Password".encode())
            client.close()

    elif command == "NewFolder":
            client.send("Ready".encode())
            name = client.recv(1024).decode()

            client.send("Ready".encode())
            id = client.recv(1024).decode()

            client.send("Ready".encode())
            parent_id = client.recv(1024).decode()
            client.send("Ready".encode())
            client.close()
            print(name, id, parent_id)
            FoldersDataFromServer = []
            with open("UsersData//" + activeUsers[address[0]] +"//FoldersDataFromServer.csv", newline='') as csvfile:
                fresh = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for row in fresh:
                    adname, adself_id, adparent_id = row
                    if adparent_id == '':
                        adparent_id = None
                    else:
                        adparent_id = int(adparent_id)
                    FoldersDataFromServer.append([adname, int(adself_id), adparent_id])
            FoldersDataFromServer.append([name, id, parent_id])
            with open("UsersData//" + activeUsers[address[0]] +"//FoldersDataFromServer.csv", 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=' ', quotechar='|',
                             quoting=csv.QUOTE_MINIMAL)
                for i in FoldersDataFromServer:
                    writer.writerow(i)

            FilesDataFromServer = {}
            with open("UsersData//" + activeUsers[address[0]] + "//FilesDataFromServer.csv", newline='') as csvfile:
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
                FilesDataFromServer[id] = []
                with open("UsersData//" + activeUsers[address[0]] + "//FilesDataFromServer.csv", 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=' ', quotechar='|',
                             quoting=csv.QUOTE_MINIMAL)
                    for i in FilesDataFromServer:
                        writer.writerow([i, FilesDataFromServer[i]])

host = 'localhost'
port = 60000

server = socket.socket()

server.bind((host, port))
server.listen(10)
print("Server is running")

users = {}
activeUsers = {}

with open('Users.csv', newline='') as csvfile:
    fresh = csv.reader(csvfile, delimiter=' ')
    for row in fresh:
        users[row[0]] = row[1]

while True:
    client, address = server.accept()
    threading.Thread(target = mainThread(client, address)).start()
