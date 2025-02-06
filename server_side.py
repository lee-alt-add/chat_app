import socket, threading

HOST = "0.0.0.0"
PORT = 5555
clients = {}
client_names = {}

def broadcast(message, sender_socket):
    """Send a message to all clients except the sender."""
    
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode('utf-8'))
            except:
                # Removes client if sending fails
                del clients[client_socket]
                client_socket.close()

def handle_client(client_socket):
    """Handle communication with a connected client."""
    
    # Ask the client for their name
    client_socket.send("Enter your name: ".encode('utf-8'))
    name = client_socket.recv(1024).decode('utf-8').strip()
    clients[client_socket] = name
    client_names[client_socket] = name
    
    # Notify all users of the new user
    broadcast(f"{name} has joined the chat", client_socket)
    
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            broadcast(f"{name}: {message}", client_socket)
        except:
            #remove the client if error occurs
            del client_names[client_socket]
            del clients[client_socket]
            client_socket.close()
            broadcast(f"{name} has left the chat", client_socket)
            break

def start_server():
    """ Starts the server """
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server started, waiting on connection...")
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()