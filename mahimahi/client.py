#!/usr/bin/python
import socket
import sys
import random
import string
import time
import os
import struct
import matplotlib.pyplot as plt
import _thread as thread
import re
from multiprocessing import Process, Queue, Lock, Value, Manager

def log_cwnd (s, starttime,color,v1,v2):
	#print('process id:', os.getpid())
	#x=[]
	#y=[]
	while True:
		# Read CWND
		# NOTE: We are parsing the first 92 bytes into a tuple where the first 7 elements are 1 byte long
		# and the next 21 are 4 bytes long. Then getting index 25 (the snd_cwnd)

		cwnd = struct.unpack("B"*7+"I"*21, s.getsockopt(socket.SOL_TCP, socket.TCP_INFO, 92))[25]
		advmss = struct.unpack("B"*7+"I"*21, s.getsockopt(socket.SOL_TCP, socket.TCP_INFO, 92))[26]
		cwnd_size = cwnd * advmss
		t = time.time() - starttime
		if (color == 'b'):
			v1.append([t,cwnd])		
		else:
			v2.append([t,cwnd])
		
		#f.write(str(cwnd_size) + '\n')
		#print((time.time() - starttime))
		#time.sleep(0.2 - ((time.time() - starttime) % 0.2))
		time.sleep(0.01)
		
def start_1(TUNER,starttime,v1,v2):
	SAVE_CWND = 1
	TCP_CONGESTION = 13
	ADDRESS = os.environ.get("MAHIMAHI_BASE") or "127.0.0.1"

	PORT = 5050
	SIZE = 1024
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	if TUNER:
		s.setsockopt(socket.IPPROTO_TCP, TCP_CONGESTION, b'reno')
		color = 'r'
		PORT = 5050
	else:
		s.setsockopt(socket.IPPROTO_TCP, TCP_CONGESTION, b'cubic')
		color='b'
		PORT = 5052
	try:
		s.connect((ADDRESS, PORT))
		print ("connection established")
		print (s.getpeername())
	except socket.error as msg:
		print ("cannot connect: ", msg)
		sys.exit(-1)

	msg = ''.join(random.choice(string.ascii_letters) for _ in range(SIZE))

	# Open a log file to print TCP info
	if SAVE_CWND:
		#f=open("cwnd_data.csv", 'w')
		#p = Process(target=log_cwnd,args=(f,s,fig,ax))
		#p.start()
		thread.start_new_thread(log_cwnd, (s, starttime,color,v1,v2))
		
	try:
		while True:
			s.send(str.encode(msg))
	except KeyboardInterrupt:
		print("Finished")
		#f.close()

fig, cwnd = plt.subplots()
cwnd.set_ylabel("cwnd (packets)")
cwnd.set_xlabel("time (s)")


INTERVAL = 50
SCNDFLOWSTART = 10

v1 = Manager().list()
v2 = Manager().list()
starttime = time.time()
p1 = Process(target=start_1, args = (1,starttime,v1,v2))
p2 = Process(target=start_1, args = (0,starttime,v1,v2))
p1.start()
#test = sp.Popen(["sudo","nethogs"],stdout=sp.PIPE)
#print(test.communicate()[0])
time.sleep(SCNDFLOWSTART)
p2.start()
time.sleep(INTERVAL-SCNDFLOWSTART)
l = list(v1)
la = list(v2)
l1 = []
l2 = []
l3 = []
l4 = []
for i in range(len(l)):
	l1.append(l[i][0])
	l2.append(l[i][1])
for i in range(len(la)):
	l3.append(la[i][0])
	l4.append(la[i][1])
cwnd.plot(l1, l2,color='b', label='TCP Cubic')
cwnd.plot(l3, l4,color='r', label = 'TCP Reno')
cwnd.legend()
plt.show()
while(True):
	pass
#p2.start()
