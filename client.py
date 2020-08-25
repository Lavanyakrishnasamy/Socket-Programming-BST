import socket     
import sys
from random import randint
import time

print 'No of numbers to be send to the server :', str(sys.argv[1])  
npm =  str(sys.argv[1])
r = int(npm)        
  
ClientSocket = socket.socket()          
  
host = socket.gethostname()
port = 1234           
  
ClientSocket.connect((host, port)) 
while True:
	for _ in range(0,r):
		data = randint(1,1000)
		# print data
		ClientSocket.send(str(data))
		time.sleep(1)
	break
print ClientSocket.recv(1024) 
ClientSocket.close()   