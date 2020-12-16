# TCP Flow Performance
## MahiMahi Simulation Environment
This repository also contains a [MahiMahi](http://mahimahi.mit.edu/) simulation environment so that users can see the impact of TCP congestion control parameters.
### Dependencies
First, you must install MahiMahi:
```bash
sudo add-apt-repository ppa:keithw/mahimahi
sudo apt-get update
sudo apt-get install mahimahi
```
Before you can run MahiMahi, you must set ip_forward=1
```bash
sudo sysctl -w net.ipv4.ip_forward=1
```
## Iperf
### Installation
```bash
sudo apt-get install iperf
```
## Run
Go to folder mahimahi:
```bash
cd mahimahi
```
Run server 1 on port 5050:
```bash
iperf -s -p 5050 -i 1 > ./log5050.txt
```
Run server 2 on port 5052:
```bash
iperf -s -p 5052 -i 1 > ./log5052.txt
```
Start simulation shell:
```bash
./start_shell
```
In this shell:
```bash
./start_client
```
Wait until figure show up, then stop all processes.
```bash
python3 throughput.py
```
