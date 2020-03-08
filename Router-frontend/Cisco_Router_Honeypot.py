#Cisco Router Honeypot

import socket
import sys
import signal
import os
import getpass

TCP_IP = '127.0.0.1'
TCP_PORT = 6005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response
def signal_handler(sig, frame):
    global s
    s.shutdown(socket.SHUT_RDWR)
    print('You pressed Ctrl+C!\n')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def read_input_password(c):
    lastord=-1
    startpassword=0
    passwordchars=[]
    while 1:
        data = None
        try:
            data = c.recv(1)
        except socket.error, ex:
            print(ex)
        if not data:
            break
        cord = ord(data)

        if startpassword == 1:
            if cord != 13:
                passwordchars.append(data)
                c.send("*")
            else:
                c.send(data)
                return ''.join(passwordchars)
        if (cord == 1) and (lastord == 253): startpassword=1
        lastord=cord

def read_input(c):
    lastord=-1
    startinput=1
    inputchars=[]
    data = None
    while 1:
        try:
            data = c.recv(1)
        except socket.error, ex:
            print(ex)
        if not data:
            break
        cord = ord(data)

        if startinput == 1:
            c.send(data)
            if (cord != 13) and (cord != 0): inputchars.append(data)
            else: return "".join(inputchars)
        if (cord == 1) and (lastord == 253): startinput=1
        lastord=cord
        # result = c.recv(1024)

def requestPassword(c):
    c.send('Password: ')
    return read_input_password(c)

def simulate_router(c):
    icmd = None
    file = None
    fp = open("log.txt","a+")
    c.send("Copyright (c) 2001 - 2011 Huawei")
    temp = c.recv(1)
    while icmd != "exit":
        c.send('\n Router> ')
        icmd = read_input(c)
        temp = c.recv(1)
        if icmd!=None:
            fp.write("IP Addr: "+str(addr[0])+" Port: "+str(addr[1])+" > "+str(icmd)+"\n")
        if icmd == "ls":
            print("ls")
            path = os.listdir('./chroot_dir/')
            try:
                for file in path:
                    c.send(file)
                    c.send("  ")
                c.send("\n")
            except Exception ,ex:
                print(ex)
        print("Command Recieved: "+str(icmd))
        c.send('\n')
    fp.close()
password = "123"
username = "admin"

user_in = raw_input('Username : ')
user_input = getpass.getpass('Password : ')


if  user_input != password or user_in != username  :
    sys.exit('Incorrect Password : Terminating ... \n')

print('Administrater is logged in!\n')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print('Starting Server on '+str(TCP_PORT))
conn, addr = s.accept()
print('Connection address:'+str(addr))
conn.send("\377\375\042\377\373\001")
passstr = requestPassword(conn)
print("Password is : "+passstr)
try:
    if passstr == "admin":
        simulate_router(conn)
    else: conn.send("Incorrect Password, Terminating...\n")
except socket.error ,ex:
    print(ex)
conn.close()
