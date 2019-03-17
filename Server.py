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
            commands[address[0]] = []
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
        commands[address[0]].append(["NewFolder", name, id, parent_id])

    elif command == "ChangeName":
        client.send("Ready".encode())
        type = client.recv(1024).decode()
        client.send("Ready".encode())
        id = client.recv(1024).decode()
        client.send("Ready".encode())
        name = client.recv(1024).decode()
        if type == "File":
            client.send("Ready".encode())
            parent_id = client.recv(1024).decode()
        client.send("Ready".encode())
        client.close()
        if type == "Folder":
            commands[address[0]].append(["ChangeName", type, id, name])
        else:
            commands[address[0]].append(["ChangeName", type, id, name, parent_id])

    elif command == "Uploading":
        client.send("Ready".encode())
        name = client.recv(1024).decode()
        client.send("Ready".encode())
        id = client.recv(1024).decode()
        client.send("Ready".encode())
        parent_id = client.recv(1024).decode()
        client.send("Ready".encode())
        file = open("UsersData//" + activeUsers[address[0]] + "//Files//" + id, 'wb')
        l = client.recv(1024)
        while (l):
            if len(l) < 1024:
                break
            file.write(l)
            l = client.recv(1024)
        file.write(l)
        file.close()
        client.send("Ready".encode())
        client.close()
        commands[address[0]].append(["Uploading", name, id, parent_id])

    elif command == "Exit":
        client.send("Ready".encode())
        client.close()
        #Открываем данные пользователя
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
            #Переписываем в соответствии с командами
            for data in commands[address[0]]:
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
            with open("UsersData//" + activeUsers[address[0]] +"//FoldersDataFromServer.csv", 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=' ', quotechar='|',
                             quoting=csv.QUOTE_MINIMAL)
                for i in FoldersDataFromServer:
                    writer.writerow(i)

            with open("UsersData//" + activeUsers[address[0]] + "//FilesDataFromServer.csv", 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=' ', quotechar='|',
                         quoting=csv.QUOTE_MINIMAL)
                for i in FilesDataFromServer:
                    writer.writerow([i, FilesDataFromServer[i]])

            del activeUsers[address[0]]
            del commands[address[0]]

host = 'localhost'
port = 60000

server = socket.socket()

server.bind((host, port))
server.listen(10)
print("Server is running")

users = {}
activeUsers = {}
commands = {}

with open('Users.csv', newline='') as csvfile:
    fresh = csv.reader(csvfile, delimiter=' ')
    for row in fresh:
        users[row[0]] = row[1]

while True:
    client, address = server.accept()
    threading.Thread(target = mainThread(client, address)).start()
