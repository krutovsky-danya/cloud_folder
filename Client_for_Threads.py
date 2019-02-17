import socket, time
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from datetime import datetime

host = ''
port = 60000

client = socket.socket()
client.connect((host, port))
print("We are connected")

data = client.recv(1024).decode()
print(data)

mydata = input()

while mydata != "n" and mydata != "y":
    client.send(mydata.encode())
    data = client.recv(1024).decode()
    print(data)
    mydata = input()

if mydata == "n":
    client.send(mydata.encode())
    client.close()

else:
    client.send(mydata.encode())
    print("Please, choose your file")
    time.sleep(0.5)
    Tk().withdraw()
    filepath = askopenfilename()
    
    client.send(filepath[filepath.rfind("/") + 1:].encode())
    file = open(filepath, 'rb')

    l = file.read(1024)

    startTime = datetime.now()
    
    while (l):
        client.send(l)
        l = file.read(1024)
    file.close()
    endTime = datetime.now()
    
    client.close()

    print("Mission complete")
    print("Transmission time:", endTime - startTime)
    


