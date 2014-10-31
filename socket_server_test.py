#!/usr/bin/python2
import socket
import sys
import os
import json
import threading
from rsa import *
from fast_exp import *
import re

class myThread (threading.Thread):
    def __init__(self, conn,addr):
        threading.Thread.__init__(self)
        self.conn=conn
        self.addr=addr
    def run(self):
        clientthread(self.conn,self.addr)

def file_is_empty(path):
    return os.stat(path).st_size==0

def check_ip(ip):
    for hosts in open(".keys/authorized_keys","r"):
        if ip in hosts:
            return hosts

def key_files(paths):
    for i in paths:
        if not os.path.exists(i) or file_is_empty(i):
            return False
    return True

def read_files(key_name):
    key_pair = {}
    with open(key_name) as f:
        for line in f:
            (key, val) = line.split()
            key_pair[key] = int(val)
    return key_pair

paths=[".keys",".keys/id_rsa",".keys/id_rsa.pub"]
if not key_files(paths):
    print "You have not created your key pairs, they are going to be created ..."
    os.mkdir( paths[0] )
    try:
        with open(paths[1], 'w') as a, open(paths[2], 'w') as b:
            data=main()
            a.write("d "+str(data['d']) + "\n" + "n " + str(data["n"]) + "\n")
            print "your private key was stored within .keys/id_rsa"
            b.write("e "+str(data['e']) + "\n" + "n " + str(data["n"]) + "\n")
            print "your public key was stored within .keys/id_rsa.pub"
    except IOError as e:
        print 'Operation failed: %s' % e.strerror

if not os.path.exists(".keys/authorized_keys") and file_is_empty(".keys/authorized_keys"):
    hosts_file=open(".keys/authorized_keys","a")
else:
    hosts_file=open(".keys/authorized_keys","r")


HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(5)
print 'Socket now listening'
#Function for handling connections. This will be used to create threads                                                                                                                       
def respond():
    while True:
        #Receiving from client
        data = conn.recv(1024)
        print data
        reply = 'OK...' + data
        if not data:
            break
        if data=="exit":
            conn.close()
            break
        if data=="get public key":
            try: 
                conn.send("write ip and e-mail separated by blank space")
                data = conn.recv(1024)
                info=data.split()
                datos=check_ip(info[0]).split()
                print info
                print datos
                os.system("echo 'Host: %s \n e: %s \n n: %s \n' | mail -s 'requested public keys' -a 'From: company@associates.com' %s" % (datos[0],datos[1],datos[2],info[1]) ) 
            except:
                conn.send("Host does not exist")
        conn.send(reply)
        

def authenticate(dos_var,pub_key):
    dos_var=dos_var.split()
    pub_key=pub_key.split()
    print "dos_var: ",dos_var
    fx=f(dos_var[0]) # for x                                                                                                                                                            
    print "fx ",fx
    fx_unencrypt=fast_expo(int(dos_var[1]),int(pub_key[1]),int(pub_key[2]))
    print "fx_unencrypt ", fx_unencrypt
    if fx == fx_unencrypt:
        return True
    else:
        return False

def challenge():
    private_key=json.JSONEncoder().encode(read_files(".keys/id_rsa"))
    private_key=json.loads(private_key)
    x=randint(1000,10000)
    fx=f(x)
    fx_encrypt=fast_expo(int(fx),int(private_key['d']),int(private_key['n']))
    conn.send(str(x) + " " + str(fx_encrypt))


def clientthread(conn,addr):
    print "inside thread: ",addr
    public_key=json.JSONEncoder().encode(read_files(".keys/id_rsa.pub"))
    conn.send(public_key)
    public_key_client=json.loads(conn.recv(1024))
    if not check_ip(addr):
        hosts_file.write(str(addr) + " " + str(public_key_client["e"]) + " " + str(public_key_client["n"]))
        hosts_file.close()
        respond()
    else:
        pub_client=check_ip(addr)
        challenge()
        print "challenge sent!"
        client_challenge=conn.recv(1024)
        print "client challenge: ",client_challenge
        print "authenticating client...."
        print "pub_client: ",pub_client
        if authenticate(client_challenge,pub_client):
            print "Client authenticated :D"
            hosts_file.close()
            respond()
        else:
            print "You are not the client you are telling you are... Goodbye"
            hosts_file.close()
            conn.close()
    conn.close()

#keep talking with the client
while 1:
    #waiting to accept a connection 
    conn, addr = s.accept()
    print 'Connected with ', addr[0]
    thread=myThread(conn,addr[0])
    thread.start()
    
s.shutdown(socket.SHUT_RDWR)
s.close()
