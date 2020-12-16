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
import ctypes
from multiprocessing import Process, Queue, Lock, Value, Manager

def log_cwnd (s, starttime,color,q):
	print('process id:', os.getpid())
	x=[]
	y=[]
	while True:
		# Read CWND
		# NOTE: We are parsing the first 92 bytes into a tuple where the first 7 elements are 1 byte long
		# and the next 21 are 4 bytes long. Then getting index 25 (the snd_cwnd)

		cwnd = struct.unpack("B"*7+"I"*21, s.getsockopt(socket.SOL_TCP, socket.TCP_INFO, 92))[25]
		advmss = struct.unpack("B"*7+"I"*21, s.getsockopt(socket.SOL_TCP, socket.TCP_INFO, 92))[26]
		cwnd_size = cwnd * advmss
		t = time.time() - starttime
		x.append(t)
		y.append(cwnd)		
		q.put((x,y,color))
		#f.write(str(cwnd_size) + '\n')
		#print((time.time() - starttime))
		#time.sleep(0.2 - ((time.time() - starttime) % 0.2))
		time.sleep(0.1)
		
def start_1(TUNER,starttime,q):
	SAVE_CWND = 1
	TCP_CONGESTION = 13
	ADDRESS = os.environ.get("MAHIMAHI_BASE") or "127.0.0.1"

	PORT = 5050
	SIZE = 1024

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	if TUNER:
		s.setsockopt(socket.IPPROTO_TCP, TCP_CONGESTION, b'reno')
		color = 'r'
	else:
		s.setsockopt(socket.IPPROTO_TCP, TCP_CONGESTION, b'cubic')
		color='b'

	print (ADDRESS)
	try:
		s.connect((ADDRESS, PORT))
		print ("connection established")
	except socket.error as msg:
		print ("cannot connect: ", msg)
		sys.exit(-1)

	msg = ''.join(random.choice(string.ascii_letters) for _ in range(SIZE))

	# Open a log file to print TCP info
	if SAVE_CWND:
		#f=open("cwnd_data.csv", 'w')
		#p = Process(target=log_cwnd,args=(f,s,fig,ax))
		#p.start()
		thread.start_new_thread(log_cwnd, (s, starttime,color,q))
		
	try:
		while True:
			s.send(str.encode(msg))
	except KeyboardInterrupt:
		print("Finished")
		#f.close()

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_ylabel("cwnd (packets)")
ax.set_xlabel("time (s)")
fig.show()
q= Queue()
starttime = time.time()
p1 = Process(target=start_1, args = (1,starttime,q))
p2 = Process(target=start_1, args = (0,starttime,q))
p1.start()
#time.sleep(5)
p2.start()
while (True):
	r = None
	for i in range(100):
		try:
			res = q.get_nowait()
			if res:
				r=res
		except:
			continue

	if r:
		x= r[0]
		y = r[1]
		color = r[2]
		ax.plot(x,y,color=color)
		
		



		
