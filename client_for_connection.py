import socket

server_address = ('', 60000)

client_socket = socket.socket()
client_socket.connect(server_address)
print("We are connected")
print("Sending information...")
client_socket.send("grisha - pes sutuliy".encode())

data = client_socket.recv(1024).decode()

print(data)

client_socket.close()

print("Mission complete")


