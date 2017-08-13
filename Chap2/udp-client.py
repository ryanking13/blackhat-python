import socket
import sys

if len(sys.argv) != 3:
    print "[*] Usage: python %s HOST PORT" % sys.argv[0]
    exit(0)

target_host = sys.argv[1]       # www.google.com
target_port = int(sys.argv[2])  # 80

# AF_INET : using IPv4
# SOCK_DGRAM : using UDP
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.sendto("DATAYOUWANTTOSEND", (target_host, target_port))

data, addr = client.recvfrom(4096)

print data, addr

print response
