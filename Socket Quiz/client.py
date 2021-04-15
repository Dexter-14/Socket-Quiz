import socket
import sys
import select
clientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)


SERVER_IP=socket.gethostbyname(socket.gethostname())
SERVER_PORT=9999
ADDR=(SERVER_IP,SERVER_PORT)

clientSocket.connect(ADDR)
FORMAT="utf-8"
while True:

	sockets_list=[sys.stdin, clientSocket]

	read_sockets, write_socket, error_socket=select.select(sockets_list,[],[])

	for socket in read_sockets:
		if(socket==clientSocket):
			message=clientSocket.recv(2048).decode(FORMAT)
			print(message)
		else:
			message=sys.stdin.readline()
			clientSocket.send(message.encode(FORMAT))
			sys.stdout.flush()


clientSocket.close()
sys.exit()


