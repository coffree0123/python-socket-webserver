import os
import sys
import ssl
import socket

from request import Request
from toolbox import log, template

def handle_socket(conn):
    request = Request()
    receive_message = conn.recv(4096)
    # Transform receive_message from bytes to str.
    receive_message = receive_message.decode('utf-8')
    log("receive:", receive_message)
    # HTTP message processing.
    try:
        # Get path and query.
        path = receive_message.split()[1]
        request.parse_path(path)
        # Get cookie content.
        request.get_cookie(receive_message)
        # Get method and body.
        request.method = receive_message.split()[0]
        request.body = receive_message.split('\r\n\r\n')[1]
        # Check if body is empty. If body is empty, treats it as a GET package.
        request.method = "POST" if request.body != "" else "GET"
        # Respond corresponding to receive route.
        response_message = request.response()
        conn.sendall(response_message)
    except Exception as e:
        log("error", e)

    # Close connection.
    log("conn end", request.method)
    conn.close()


def run_socket(host, port):
    # HTTPs
    # Use below to create cert and key.
    # openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
    # openssl rsa -in key.pem -out key.pem (去除輸入密碼環節)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('./cert.pem', './key.pem')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Reuse port.
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)
    s = context.wrap_socket(s, server_side=True)
    # Use double fork to implement multithread.
    while True:
        try:
            (conn, addr) = s.accept()
            if (os.fork() == 0):
                if (os.fork() == 0):
                    handle_socket(conn)
                quit()
            else:
                conn.close()
                os.wait()
        except KeyboardInterrupt:
            # Press Ctrl-c exit.
            quit()
        except Exception as e:
            log("error", e)
                

def main():
    # Usage: python server.py $PORT
    # Get host ip and port number
    port = int(sys.argv[1])
    hostname = socket.gethostname()
    host = socket.gethostbyname(hostname)

    run_socket(host, port)

if __name__ == '__main__':
    main()