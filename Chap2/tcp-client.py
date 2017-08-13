import socket
import sys

if len(sys.argv) != 3:
    print "[*] Usage: python %s HOST PORT" % sys.argv[0]
    exit(0)

target_host = sys.argv[1]       # www.google.com
target_port = int(sys.argv[2])  # 80

# AF_INET : using IPv4
# SOCK_STREAM : using TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host, target_port))
client.send("GET / HTTP/1.1\r\n"
            "HOST: google.com\r\n\r\n")

response = client.recv(4096)

print response
