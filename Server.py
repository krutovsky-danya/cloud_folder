import socket, csv, threading, os, time

class mainThread(threading.Thread):
    def __init__(self, client, address, server):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.server = server
        print("New thread for", str(self.address))

    def run(self):
        command = self.client.recv(1024).decode()
        if command == "Login":
            self.client.send("Ready".encode())
            data = self.client.recv(1024).decode()
            login, password = data[0:data.find('~')], data[data.find('~') + 1:]

            if login in self.server.users and self.server.users[login] == password:
                self.client.send("Passed".encode())
                self.client.recv(1024).decode()
                print("Start1")

                file = open(("UsersData//" + login + "//FoldersDataFromServer.csv"), 'rb')
                l = file.read(1024)
                while (l):
                    self.client.send(l)
                    l = file.read(1024)
                file.close()
                print("Done1")

                self.client.recv(1024).decode()
                print("Start2")

                file = open(("UsersData//" + login + "//FilesDataFromServer.csv"), 'rb')
                l = file.read(1024)
                while (l):
                    self.client.send(l)
                    l = file.read(1024)
                file.close()
                print("Done2")

                self.client.recv(1024).decode()
                print("Done3")

                self.server.activeUsers[self.address[0]] = login
                self.server.commands[self.address[0]] = []
                self.client.close()

            elif login in self.server.users:
                self.client.send("LogIn".encode())
                self.client.close()

            else:
                self.client.send("Password".encode())
                self.client.close()

        elif command == "NewFolder":
            self.client.send("Ready".encode())
            name = self.client.recv(1024).decode()

            self.client.send("Ready".encode())
            id = self.client.recv(1024).decode()

            self.client.send("Ready".encode())
            parent_id = self.client.recv(1024).decode()
            self.client.send("Ready".encode())
            self.client.close()
            print(name, id, parent_id)
            self.server.commands[self.address[0]].append(["NewFolder", name, id, parent_id])

        elif command == "ChangeName":
            self.client.send("Ready".encode())
            type = self.client.recv(1024).decode()
            self.client.send("Ready".encode())
            id = self.client.recv(1024).decode()
            self.client.send("Ready".encode())
            name = self.client.recv(1024).decode()
            if type == "File":
                self.client.send("Ready".encode())
                parent_id = self.client.recv(1024).decode()
            self.client.send("Ready".encode())
            self.client.close()
            if type == "Folder":
                self.server.commands[self.address[0]].append(["ChangeName", type, id, name])
            else:
                self.server.commands[self.address[0]].append(["ChangeName", type, id, name, parent_id])

        elif command == "Uploading":
            self.client.send("Ready".encode())
            name = self.client.recv(1024).decode()
            self.client.send("Ready".encode())
            id = self.client.recv(1024).decode()
            self.client.send("Ready".encode())
            parent_id = self.client.recv(1024).decode()
            self.client.send("Ready".encode())
            file = open("UsersData//" + self.server.activeUsers[self.address[0]] + "//Files//" + id, 'wb')
            print(name, id, parent_id)
            size = self.client.recv(1024).decode()
            print(size)
            localsize = 0
            self.client.send("Ready".encode())
            l = self.client.recv(1024)
            localsize += len(l)
            while (localsize < int(size)):
                file.write(l)
                l = self.client.recv(1024)
                localsize += len(l)
            file.write(l)
            file.close()
            print("Done")
            self.client.send("Ready".encode())
            self.client.close()
            self.server.commands[self.address[0]].append(["Uploading", name, id, parent_id])

        elif command == "Download":
            self.client.send("Ready".encode())
            print("Done1")
            ID = self.client.recv(1024).decode()
            print(ID)
            self.client.send(str(os.path.getsize("UsersData//" + self.server.activeUsers[self.address[0]] + '//Files//' + ID)).encode())
            print("Done3")
            self.client.recv(1024).decode()
            file = open("UsersData//" + self.server.activeUsers[self.address[0]] + '//Files//' + ID, 'rb')
            l = file.read(1024)
            while(l):
                self.client.send(l)
                l = file.read(1024)
            file.close()
            self.client.recv(1024).decode()
            self.client.close()

        elif command == "Exit":
            self.client.send("Ready".encode())
            self.client.close()
            #Открываем данные пользователя
            FoldersDataFromServer = []
            with open("UsersData//" + self.server.activeUsers[self.address[0]] +"//FoldersDataFromServer.csv", newline='') as csvfile:
                fresh = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for row in fresh:
                    adname, adself_id, adparent_id = row
                    if adparent_id == '':
                        adparent_id = None
                    else:
                        adparent_id = int(adparent_id)
                    FoldersDataFromServer.append([adname, int(adself_id), adparent_id])

            FilesDataFromServer = {}
            with open("UsersData//" + self.server.activeUsers[self.address[0]] + "//FilesDataFromServer.csv", newline='') as csvfile:
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
                #Переписываем в соответствии с командами
                for data in self.server.commands[self.address[0]]:
                    if data[0] == "NewFolder":
                        FoldersDataFromServer.append([data[1], data[2], data[3]])
                        FilesDataFromServer[data[2]] = []

                    elif data[0] == "ChangeName":
                        if data[1] == "Folder":
                            for i in range(len(FoldersDataFromServer)):
                                if FoldersDataFromServer[i][1] == int(data[2]):
                                    FoldersDataFromServer[i][0] = data[3]
                                    break
                        else:
                            for i in range(len(FilesDataFromServer[data[4]])):
                                if FilesDataFromServer[data[4]][i][1] == int(data[2]):
                                    FilesDataFromServer[data[4]][i] = (data[3], int(data[2]))
                                    break
                    elif data[0] == "Uploading":
                        FilesDataFromServer[data[3]].append((data[1], int(data[2])))

                #Сохраняем
                with open("UsersData//" + self.server.activeUsers[self.address[0]] +"//FoldersDataFromServer.csv", 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=' ', quotechar='|',
                                 quoting=csv.QUOTE_MINIMAL)
                    for i in FoldersDataFromServer:
                        writer.writerow(i)

                with open("UsersData//" + self.server.activeUsers[self.address[0]] + "//FilesDataFromServer.csv", 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=' ', quotechar='|',
                             quoting=csv.QUOTE_MINIMAL)
                    for i in FilesDataFromServer:
                        writer.writerow([i, FilesDataFromServer[i]])

                del self.server.activeUsers[self.address[0]]
                del self.server.commands[self.address[0]]

class server():
    def __init__(self):
        self.host = '0.0.0.0'
        self.port = 60000

        self.server = socket.socket()

        self.server.bind((self.host, self.port))
        self.server.listen(10)
        print("Server is running")

        self.users = {}
        self.activeUsers = {}
        self.commands = {}

        self.threads = []

        with open('Users.csv', newline='') as csvfile:
            fresh = csv.reader(csvfile, delimiter=' ')
            for row in fresh:
                self.users[row[0]] = row[1]

        self.run()

    def run(self):
        while True:
            client, address = self.server.accept()
            newthread = mainThread(client = client, address = address, server = self)
            newthread.start()
            self.threads.append(newthread)
            print("Start")

server = server()