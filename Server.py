from socket import *
from threading import Thread, current_thread

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 15000

class ChatUsingThread(Thread):
    def __init__(self, connection):
        Thread.__init__(self)
        self.connection = connection

    def run(self):
        name = current_thread().getName()
        while True:
            if name == "Sender":
                data = input("Server: ")
                self.connection.send(bytes(data, "utf-8"))
            elif name == "Receiver":
                recData = self.connection.recv(1024).decode()
                if recData.lower() == "quit":
                    print("Client has closed the connection.")
                    self.connection.close()
                    break
                print("Client: ", recData)


server = socket(AF_INET, SOCK_STREAM)
server.bind((SERVER_HOST, SERVER_PORT))
server.listen(4)

print("Server is listening...")

connection, address = server.accept()

sender = ChatUsingThread(connection)
sender.setName("Sender")
receiver = ChatUsingThread(connection)
receiver.setName("Receiver")

sender.start()
receiver.start()
