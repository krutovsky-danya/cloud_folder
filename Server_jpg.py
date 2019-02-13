import socket

server_address = ('0.0.0.0', 60000)

server = socket.socket()
server.bind(server_address)
server.listen(3)

print("Server is running")

while True:
    client, address = server.accept()
    print("New connection from", address)

    file = open('test_1.jpg', 'wb')

    l = client.recv(1024)
    while(l):
        file.write(l)
        l = client.recv(1024)
    file.close()

    client.close()
    print("Mission complete")

