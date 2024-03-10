from socket import *
from threading import Thread, current_thread

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 15000

class ChatUsingThread(Thread):
    should_continue = True 

    def __init__(self, connection):
        super().__init__()
        self.connection = connection

    def run(self):
        name = current_thread().getName()
        while ChatUsingThread.should_continue:  
            try:
                if name == "Sender":
                    data = input("You: ")
                    self.connection.sendall(bytes(data, "utf-8"))
                    if data.lower() == "quit":
                        print("Closing the connection...")
                        self.connection.close()
                        ChatUsingThread.should_continue = False  
                        break
                elif name == "Receiver":
                    recData = self.connection.recv(1024).decode()
                    if recData.lower() == "quit":
                        print("Client has closed the connection.")
                        self.connection.close()
                        ChatUsingThread.should_continue = False  
                        break
                    print("Client: ", recData)
            except Exception as e:
                print("An error occurred:", e)
                break

try:
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)
    print("Server is listening...")

    connection, address = server_socket.accept()
    print("Connected to:", address)

    sender = ChatUsingThread(connection)
    sender.setName("Sender")
    receiver = ChatUsingThread(connection)
    receiver.setName("Receiver")

    sender.start()
    receiver.start()

    
    sender.join()
    receiver.join()

    print("Connection closed.")
except Exception as e:
    print("An error occurred:", e)
finally:
    print("Server is shutting down...")
