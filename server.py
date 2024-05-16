import os
import mimetypes
import http.server
import socketserver
from urllib.parse import unquote, urlparse, parse_qs
import signal

class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        # File a cui il client sta facendo richiesta
        parsed_url = urlparse(self.path)
        path = unquote(parsed_url.path)
        file_name = os.path.normpath(path)
        
        # Eventuali parametri li salvo in un array
        parameters = parse_qs(parsed_url.query)

        if file_name == os.sep:
            file_name = os.sep + 'index.html'

        absolutePath = os.getcwd() + os.sep + 'resources' + file_name

        if os.path.isfile(absolutePath):
            self.send_response(200)
            mime_type, _ = mimetypes.guess_type(absolutePath)
            self.send_header('Content-type', mime_type)
            self.end_headers()

            with open(absolutePath, 'rb') as f:
                self.wfile.write(f.read())
            
            print(f"Eseguita GET da {self.client_address} su "
                  f"file \"{file_name}\", utilizzato mime type \"{mime_type}\" "
                  f"per header e inviato codice di risposta \"200\" (OK)\nSono "
                  f"stati passati questi parametri: {parameters}\n")
        else:
            self.send_error(404)
            print(f"Eseguita GET {self.client_address} su "
                  f"file \"{file_name}\" inesistente, inviato "
                  f"codice di risposta \"404\" (Not Found)\nSono "
                  f"stati passati questi parametri: {parameters}\n")

def signal_handler(sig, frame):
    print('Chiusura del server...')
    httpd.server_close()
    print('Server chiuso correttamente')
    exit(0)

class MyThreadedTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

def run(server_class=MyThreadedTCPServer, handler_class=MyHTTPRequestHandler,
        address='127.0.0.1', port=8000):
    global httpd
    server_address = (address, port)
    
    signal.signal(signal.SIGINT, signal_handler)

    try:
        httpd = server_class(server_address, handler_class)
        print(f"Server funzionante su: http://{address}:{port} ...\n")
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()

if __name__ == '__main__':
    run()