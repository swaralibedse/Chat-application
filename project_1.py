import socket
import threading

def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")

    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                print(f"Connection with {client_address} closed.")
                break
            print(f"Received message from {client_address}: {message}")
            broadcast_message(message, client_socket)
        except Exception as e:
            print(f"Error handling connection with {client_address}: {e}")
            break

    client_socket.close()

def broadcast_message(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode("utf-8"))
            except Exception as e:
                print(f"Error broadcasting message to a client: {e}")

def main():
    global clients
    clients = []

    server_host = "127.0.0.3"
    server_port = 9999

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(5)

    print(f"Server is listening on {server_host}:{server_port}")

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)

        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":
    main()
