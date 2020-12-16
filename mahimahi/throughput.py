import re
import matplotlib.pyplot as plt
import time

INTERVAL = 50
SCNDFLOWSTART = 10
fig, throughput = plt.subplots()
throughput.set_xlabel("time (s)")
throughput.set_ylabel("throughput (Mbps)")
time.sleep(10)

time_list1 = []
rate_list1 = []

with open('./log5050.txt','r') as f:# iperf-log.txt is the iperf log file name
    row_data = f.readlines() # Read each line of the iperf log file into a list
    for line in row_data:    # Use regular expressions for matching, and the matching content can be changed according to the actual situation
        time = re.findall(r"-(.*) sec", line)
        rate = re.findall(r"Bytes (.*) Mbits/sec", line)
        if(len(time)>0):     # Store the data when there is throughput and time data in the current row
            if (float(time[0])>INTERVAL):
                break
            
            time_list1.append(float(time[0]))
            rate_list1.append(float(rate[0]))
            

time_list2 = []
rate_list2 = []

with open('./log5052.txt','r') as f:# iperf-log.txt is the iperf log file name
    row_data = f.readlines() # Read each line of the iperf log file into a list
    for line in row_data:    # Use regular expressions for matching, and the matching content can be changed according to the actual situation
        time = re.findall(r"-(.*) sec", line)
        rate = re.findall(r"Bytes (.*) Mbits/sec", line)
        if(len(time)>0):     # Store the data when there is throughput and time data in the current row
            if (float(time[0])>INTERVAL-SCNDFLOWSTART):
                break
            time_list2.append(float(time[0])+SCNDFLOWSTART)
            try:
            	rate_list2.append(float(rate[0]))
            except:
            	print(line)
throughput.plot(time_list1,rate_list1,color='r', label='TCP Reno')
throughput.plot(time_list2,rate_list2, color = 'b', label = 'TCP Cubic')
throughput.legend()
plt.show()
