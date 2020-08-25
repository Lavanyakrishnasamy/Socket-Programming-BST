import ConfigParser
import os
from subprocess import call
import sys 
import threading

class startClients(threading.Thread):

    def __init__ (self, rate):
        threading.Thread.__init__(self)
        self.rate = rate

    def run(self):
        call(["python","client.py",self.rate])

def read_config(cfg_fn):
	config = ConfigParser.RawConfigParser()
	config.read(config_filename)
	n = config.get('attributes', 'no_of_clients')
	print n
	r = config.get('attributes', 'no_of_numbers')
	print  r
	return n,r

if __name__ == '__main__':
	# config_filename = str(input('Enter the config file name: '))
	config_filename = 'ipc_config.cfg'
	noc,non = read_config(config_filename)
	n = int(noc)
	threads = []
	for num in range(0, n):
		# Calling Clients 
	    thread = startClients(non)
	    thread.start()
	    threads.append(thread)
	for thread in threads:
	    thread.join()