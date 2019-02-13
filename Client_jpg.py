import socket

server_address = ('', 60000)

client = socket.socket()
client.connect(server_address)

file = open("test.jpg", "rb")

l = file.read(1024)

print("Start sending")

while(l):
    client.send(l)
    l = file.read(1024)

client.close()
print("Mission complete")
