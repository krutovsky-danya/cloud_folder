import socket, threading, time

class ThreadForClient(threading.Thread):
    def __init__(self, client_sock, client_address):
        threading.Thread.__init__(self)
        self.client_sock = client_sock
        self.client_address = client_address
        print("New thread started for", client_address)

    def run(self):
        self.client_sock.send("Are you ready to start sending? (y/n)".encode())
        data = self.client_sock.recv(1024).decode()
        while data != "y" and data != "n":
            print("client", self.client_address, "sent", data)
            self.client_sock.send("I don't understand you".encode())
            data = self.client_sock.recv(1024).decode()

        if data == "n":
            print("client", self.client_address, "closed connection")
            self.client_sock.close()

        else:
            print("client", self.client_address, "started sending")
            filename = self.client_sock.recv(1024).decode()
            file = open('Files//' + filename, 'wb')
            l = self.client_sock.recv(1024)
            while (l):
                file.write(l)
                l = self.client_sock.recv(1024)
            file.close()

            print("client with ip:", self.client_address, "has completed sending")
            self.client_sock.close()


host = '0.0.0.0'
port = 60000

server = socket.socket()

server.bind((host, port))
server.listen(10)
print('server is running')

threads = []

def thread_status():
    while True:
        print(len(threads))
        for i in range(len(threads)):
            print("Status of thread ", i, threads[i].is_alive())
        time.sleep(5)

thread_status = threading.Thread(target = thread_status)
thread_status.start()

while True:
    client, address = server.accept()
    thread = ThreadForClient(client, address)
    thread.start()
    threads.append(thread)
