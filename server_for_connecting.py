import socket

address = ('0.0.0.0', 60000)

server_socket = socket.socket()

server_socket.bind(address)
server_socket.listen(2)
print('server is running')

while True:
    connection, address = server_socket.accept()
    print("New connection from", address)

    data = connection.recv(1024).decode()

    print(data)

    connection.send('Sounds good!'.encode())

    connection.close()
    print("Mission complete")

