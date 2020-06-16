import serial
import time
import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Process, Value, Array

# XBee setting
serdev = '/dev/ttyUSB0'
s = serial.Serial(serdev, 9600)

s.write("+++".encode())
char = s.read(2)
print("Enter AT mode.")
print(char.decode())

s.write("ATMY 0x140\r\n".encode())
char = s.read(3)
print("Set MY 0x140.")
print(char.decode())

s.write("ATDL 0x440\r\n".encode())
char = s.read(3)
print("Set DL 0x440.")
print(char.decode())
s.write("ATID 0x1\r\n".encode())
char = s.read(3)
print("Set PAN ID 0x1.")
print(char.decode())

s.write("ATWR\r\n".encode())
char = s.read(3)
print("Write config.")
print(char.decode())

s.write("ATMY\r\n".encode())
char = s.read(4)
print("MY :")
print(char.decode())

s.write("ATDL\r\n".encode())
char = s.read(4)
print("DL : ")
print(char.decode())

s.write("ATCN\r\n".encode())
char = s.read(3)
print("Exit AT mode.")
print(char.decode())

print("start sending RPC")
a=bytes("\r", 'UTF-8')


tilt = []

s.write("/getAcc/run\r".encode())
time.sleep(0.5)
line=s.read(1)


def readstring(n, a):
    while True:
        n.value = int(s.readline()) 
        time.sleep(1.0)

line = Value('d', 0.0)
arr = Array('i', range(10))
while True:
    # send RPC to remote
    s.write("/getAcc/run\r".encode())
    action_process = Process(target=readstring, args=(line, arr))
    action_process.start()
    action_process.join(timeout=1.0)
    print(line.value)
    tilt.append(line.value)
    if len(tilt) >= 21:
        fig, ax = plt.subplots(1, 1)
        l1=ax.plot([i for i in range(21)], tilt)
        ax.set_xlabel('time')
        ax.set_ylabel('# of data')
        ax.legend((l1),('# of data'))
        plt.show()
    else:
        action_process.terminate()
s.close()