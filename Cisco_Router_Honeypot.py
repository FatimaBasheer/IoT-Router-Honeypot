#Cisco Router Honeypot

import socket
import sys
import signal
import os
import getpass
import datetime
import thread

TCP_IP = '127.0.0.1'
TCP_PORT = 6005 #hard-coded tcp port
BUFFER_SIZE = 20  #for faster responses
def signal_handler(sig, frame):
    global s
    s.shutdown(socket.SHUT_RDWR)
    print('You pressed Ctrl+C!\n')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

#reading the telnet password - granting access to the router
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

#reading the commands from the user terminal to the honeypot frontend(client)
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

#simulate router functionalities by providing command line on login , hacks in the system present here
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
            fp.write("IP Addr: "+str(addr[0])+" Port: "+str(addr[1])+" Timestamp: {:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())+" > "+str(icmd)+"\n")
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

#handling multiple clients to the front-end honeypot
def on_new_client(conn,addr):
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

#router admin login is "admin" & "123" while telnet client login is "admin"
#main function
password = "123"
username = "admin"

user_in = raw_input('Username : ')
user_input = getpass.getpass('Password : ')


if  user_input != password or user_in != username  :
    sys.exit('Incorrect Password : Terminating ... \n')

print('Administrater is logged in!\n')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(5)
print('Starting Server on '+str(TCP_PORT))
while True:
    conn, addr = s.accept()
    thread.start_new_thread(on_new_client,(conn ,addr))
s.close()
