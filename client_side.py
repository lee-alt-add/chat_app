import socket, threading



def receive_messages(client_socket):
    """Receive messages from the server."""
    
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except:
            print("Disconnected from the server.")
            client_socket.close()
            break

def start_client():
    """Start the chat client."""
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5555))  # Replace with server IP

    # Receive the prompt for the name
    name_prompt = client.recv(1024).decode('utf-8')
    name = input(name_prompt)
    client.send(name.encode('utf-8'))

    # Start a thread to receive messages
    threading.Thread(target=receive_messages, args=(client,)).start()

    # Send messages to the server
    while True:
        message = input()
        client.send(message.encode('utf-8'))
        
if __name__ == "__main__":
    start_client()