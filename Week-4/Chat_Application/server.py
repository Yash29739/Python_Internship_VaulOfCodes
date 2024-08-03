import socket
import threading
from chat import format_message, is_valid_name

PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
EXIT_MESSAGE = "!EXIT"

clients, names = [], []
clients_lock = threading.Lock()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

def startChat():
    print(f"Server is working on {SERVER}")

    server.listen()

    while True:
        try:
            conn, addr = server.accept()
            conn.send("NAME".encode(FORMAT))
            name = conn.recv(1024).decode(FORMAT)
            
            if not is_valid_name(name, names):
                conn.send("Name already taken or invalid. Please choose a different name.".encode(FORMAT))
                conn.close()
                continue

            with clients_lock:
                names.append(name)
                clients.append(conn)
            
            print(f"Name is: {name}")
            
            broadcastMessage(format_message("Server", f"{name} has joined the chat!").encode(FORMAT))
            conn.send('Connection successful!'.encode(FORMAT))

            thread = threading.Thread(target=handle, args=(conn, addr, name))
            thread.start()

            print(f"Active connections: {threading.activeCount() - 1}")

        except Exception as e:
            print(f"Error: {e}")

def handle(conn, addr, name):
    print(f"New connection: {addr}")
    connected = True

    while connected:
        try:
            message = conn.recv(1024).decode(FORMAT)
            if message == EXIT_MESSAGE:
                connected = False
                broadcastMessage(format_message("Server", f"{name} has left the chat.").encode(FORMAT))
                removeClient(conn, name)
                break
            if message:
                broadcastMessage(message.encode(FORMAT))
        except Exception as e:
            print(f"Error handling message: {e}")
            break

    conn.close()

def broadcastMessage(message):
    with clients_lock:
        for client in clients:
            try:
                client.send(message)
            except:
                continue

def removeClient(conn, name):
    with clients_lock:
        if conn in clients:
            clients.remove(conn)
            names.remove(name)

if __name__ == "__main__":
    startChat()
