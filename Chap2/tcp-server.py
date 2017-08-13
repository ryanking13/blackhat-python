import socket
import threading
import sys

def handle_client(client_socket):

    request = client_socket.recv(1024)

    print "[*] Received: %s" % request

    client_socket.send("ACK!")
    client_socket.close()


if len(sys.argv) != 2:
    print "[*] Usage: python %s PORT" % sys.argv[0]
    exit(0)

bind_ip = "0.0.0.0"
bind_port = int(sys.argv[1])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)

print "[*] Listening on %s:%d" % (bind_ip, bind_port)

while True:

    client, addr = server.accept()

    print "[*] Accepted connection from: %s:%d" % (addr[0], addr[1])

    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
