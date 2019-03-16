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
