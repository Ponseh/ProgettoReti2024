import socket
import os

def send_get_request(host, port, path):
    # Creazione socket + connessione server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Richiesta HTTP GET
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n"
    
    # Invio richiesta
    client_socket.sendall(request.encode())

    # Ricezione risposta
    response = b""
    while True:
        part = client_socket.recv(1024)
        if not part:
            break
        response += part

    # Chiusura socket
    client_socket.close()

    # Decodifica e stampa risposta
    print(response.decode("utf-8"))

if __name__ == "__main__":
    server_host = "127.0.0.1"
    server_port = 8000
    resource_path = "/index.html"
    send_get_request(server_host, server_port, resource_path)
