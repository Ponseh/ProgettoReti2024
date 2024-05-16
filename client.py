import socket

def send_get_request(server_address='127.0.0.1', server_port=8000, 
                    resource_path='/index.html'):
    # Creazione socket + connessione server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_address, server_port))

    # Richiesta HTTP GET
    request = f"GET {resource_path} HTTP/1.1\r\nHost: {server_address}\r\n\r\n"
    
    # Invio richiesta
    client_socket.sendall(request.encode())

    # Ricezione risposta
    response = b''
    while True:
        part = client_socket.recv(1024)
        if not part:
            break
        response += part

    # Chiusura socket
    client_socket.close()

    # Decodifica e stampa risposta
    print(response.decode('utf-8'))

if __name__ == '__main__':
    send_get_request()
