import socket
import select
import sys
import random
from _thread import *
import threading
FORMAT="utf-8"

# AF_NET is the address of the socket
# SOL_SOCKET means the type of the socket
#SOCK_STREAM means that the data or characters are read in a flow

serverSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

SERVER_IP=socket.gethostbyname(socket.gethostname())
SERVER_PORT=9999

ADDR=(SERVER_IP,SERVER_PORT)
serverSocket.bind(ADDR)

serverSocket.listen(20)

Ques= [" Who is the first person to reach Mount Everest? \n a.Sherpa Tensing, Edmund Hillary b.Rajesh Sharma c.Charles Hillary d.Johan don\n",
     " Which is the first country to issue paper currency? \n a.China b.India c.USA d.UK\n",
     " Who is the first Prime Minister of Britain? \n a.George Washington b.Robert Walpole c.Henry Waterloo d.George Bush\n",
     " Which is the first country to prepare a constitution? \n a.China b.India c.USA d.UK\n",
     " Which is the first spacecraft to reach on Mars? \n a.Viking - 1 b.Vikrant -1 c.Shelter d.Magway\n",
     " How many wonders are there in the world? \n a.7 b.8 c.10 d.4\n",
     " The South Pole of the Earth is located in \n a.Pacific Ocean b.Arctic Ocean c.Antarctica d.Norway\n",
     " How many states are there in India? \n a.24 b.29 c.30 d.31\n",
     " Who invented the telephone? \n a.A.G Bell b.John Wick c.Thomas Edison d.G Marconi\n",
     " Who is Shiva? \n a.The Destroyer b.God of Heaven c.The Creator d.God of Gods\n",
     " Who was the first Indian female astronaut ? \n a.Sunita Williams b.Kalpana Chawla c.None of them d.Both of them\n ",
     " What is the smallest continent? \n a.Asia b.Antarctic c.Africa d.Australia\n",
     " What is the smallest country in the world? \n a.San Marino b.Monaco c.Lebanon d.Vatican City\n",
     " How many players are on the field in cricket? \n a.6 b.7 c.11 d.8\n",
     " UN stands for? \n a.United Nations b.Union Nation c.United Nato d.United Northern\n",
     " World's tallest statue is \n a.Statue of Unity b.Statue of Liberty c.Christ the Redeemer d.Others\n",
     " Where is the official home of Santa Claus? \n a.Canada b.Sweden c.Italy d.Finland\n",
     " What is 7*7?\n a.69 b.49 c.57 d.77",
     " Which is the Largest country?\n a.China b.India c.Russia d.Canada\n",
     " 9+9= \n a.18 b.81 c.2 d.G 32\n",
     " 7+7= \n a.11 b.12 c.14 d.13\n",
     " 2+2= \n a.2 b.4 c.1 d.3\n",
     " 1+9= \n a.2 b.44 c.32 d.10\n",
     " 4*4= \n a.22 b.32 c.11 d.16\n",
     " 2+7= \n a.6 b.7 c.9 d.8\n",
     " 1+1= \n a.1 b.3 c.4 d.2\n",
     " 1*2*3= \n a.6 b.8 c.3 d.7\n",
     " 3+1*4= \n a.2 b.7 c.3 d.10\n",
     " 9*9= \n a.81 b.18 c.4 d.12\n",
     " 1*0= \n a.0 b.10 c.01 d.1\n",
     " 3^2= \n a.9 b.8 c.10 d.4\n",
     " 9*10= \n a.90 b.32 c.12 d.33\n"]


Ans = ['a', 'a', 'b', 'c', 'a', 'a', 'c', 'b', 'a', 'a', 'b', 'd', 'd', 'c', 'a', 'a', 'd','b','c','a','c','b','d','d','c','d','a','b','a','a','a','a']
Player_clients=[]
scores=[]
bzr=[0,0]
client=["",-1]
send_msg=""

def Finish():
	send_to_all("Quiz has ended!!\n\n")
	if(max(scores)<5):
		send_to_all("The Quiz has come to a Tie.")

		for x in range(len(Player_clients)):
			send_msg="You have scored " + str(scores[x]) + " points.\n\n"
			Player_clients[x].send(send_msg.encode(FORMAT))

	serverSocket.close()

def Start():
	bzr[1]=random.randint(0,10000)%len(Ques)
	if(len(Ques)!=0):
		for connection in Player_clients:
			connection.send(Ques[bzr[1]].encode(FORMAT))

def send_to_all(message):
	for clients in Player_clients:
		try:
			clients.send(message.encode(FORMAT))
		except:
			clients.close()
			remove(clients)

def clientthread(conn,addr):
    #Intro MSG
	conn.send("Connection established...\nGet ready for Quiz\nPress any key as a Buzzer.\n".encode(FORMAT))
	while True:
		if(len(Player_clients)==3):
			message=conn.recv(2048).decode(FORMAT)
			if message:
				if bzr[0]==0:
					client[0]=conn
					bzr[0]=1
					i=0

					while i<len(Player_clients):
						if(Player_clients[i]==conn):
							break
						i += 1
					client[1] = i

				elif bzr[0]==1 and client[0]==conn:

					if(message[0]==Ans[bzr[1]][0]):
						send_to_all("Player " + str(client[1]+1) + " has been awarded + 1\n\n")
						scores[i]=scores[i]+1

						if(scores[i]>=5):
							send_to_all("Player " + str(client[1]+1) + " Congrats! Won the quiz.\n\n")
							Finish()
							sys.exit()

					else: 
						send_to_all("Player " + str(client[1]+1) + "is deducted by -0.5\n\n")
						scores[i]= scores[i]-(1/2)

					bzr[0]=0

					if(len(Ques)!=0):
						Ques.pop(bzr[1])
						Ans.pop(bzr[1])

					if(len(Ques)==0):
						Finish()
					else:
						Start()

				else:
					send_msg="OOps! Player "+str(client[1]+1)+" has pressed the buzzer first.\n\n"
					conn.send(send_msg.encode(FORMAT))


			else:
				#Remove the connection
				if conn in Player_clients:
					Player_clients.remove(conn)


while True:
	conn, addr=serverSocket.accept()
	Player_clients.append(conn)
	print(addr[0] + ' connected\n')
	scores.append(0)
	start_new_thread(clientthread,(conn, addr))
	if(len(Player_clients)==3):
		Start()

conn.close()
serverSocket.close()