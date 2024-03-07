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
                data = input("Client: ")
                self.connection.send(bytes(data, "utf-8"))
                if data.lower() == "quit":
                    print("Closing the connection...")
                    self.connection.close()
                    break
            elif name == "Receiver":
                recData = self.connection.recv(1024).decode()
                if recData.lower() == "quit":
                    print("Server has closed the connection.")
                    self.connection.close()
                    break
                print("Server: ", recData)

client = socket()
client.connect((SERVER_HOST, SERVER_PORT))

sender = ChatUsingThread(client)
sender.setName("Sender")
receiver = ChatUsingThread(client)
receiver.setName("Receiver")

sender.start()
receiver.start()
