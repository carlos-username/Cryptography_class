#!/usr/bin/python2
from socket import *
from rsa import *
import os
import json
from random import randint
import sys
import re
from fast_exp import * 

def file_is_empty(path):
        return os.stat(path).st_size==0

def key_files(paths):
    for i in paths:
        if not os.path.exists(i) or file_is_empty(i):
            return False
    return True
    
def check_ip(ip):
    for hosts in open(".keys/known_hosts","r"):
        if ip in hosts:
            return hosts

def read_files(key_name):
    key_pair = {}
    with open(key_name,"r") as f:
        for line in f:
            (key, val) = line.split()
            key_pair[key] = int(val)
    return key_pair
                                        
PORT = 8888
ip="104.131.111.65"
s = socket(AF_INET, SOCK_STREAM)
s.connect((ip, PORT))
paths=[".keys",".keys/id_rsa",".keys/id_rsa.pub"]
if not key_files(paths):
    print "You have not created your key pairs, they are going to be created ..."
    if not os.path.exists(".keys"):
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

if not os.path.exists(".keys/known_hosts") or file_is_empty(".keys/known_hosts"):
    hosts_file=open(".keys/known_hosts","a")
else:
    hosts_file=open(".keys/known_hosts","r")

def client():
    while True:
        msg = raw_input('>> ')
        while msg == "":
                print "type: help"
                msg = raw_input('>> ')
                
        s.send(msg)
        if msg=="exit":
                sys.exit()
        if msg=="get public key":
                print s.recv(1024)
                while not re.match("((([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])[ (\[]?(\.)[ )\]]?){3}([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]))",msg) and not re.match("[^@]+@[^@]+\.[^@]+",msg):
                        msg = raw_input('enter the required format >> ')
                s.send(msg)
        if msg=="help":
                print "Getting public key to e-mail: type get public key \n to exit: type exit \n"
                        
                        
        reply = s.recv(1024)
        if reply:
            print '<< ' + str(reply)

        
def authenticate(dos_var,pub_key):
    dos_var=dos_var.split()
    pub_key=pub_key.split()
    print pub_key
    fx=f(dos_var[0]) # for x
    print "fx ", fx
    fx_unencrypt=fast_expo(int(dos_var[1]),int(pub_key[1]),int(pub_key[2]))
    print "fx_unenencrypt ", fx_unencrypt
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
    
    s.send(str(x) + " " + str(fx_encrypt))
                        
if not check_ip(ip):
    request=""
    while request != "yes" or request != "no":
        request = raw_input("The host cannot be authenticated because of first connection, do you want to send your keys? (yes/no): ")
        if request=="yes":
            reply=s.recv(1024)
            if reply:
                pub_key=json.loads(reply)
                hosts_file=open(".keys/known_hosts","a")
                hosts_file.write(str(ip)+" "+str(pub_key["e"])+" "+str(pub_key["n"]) + '\n')
                print pub_key
                public_key=json.JSONEncoder().encode(read_files(".keys/id_rsa.pub"))
                s.send(public_key)
                #s.recv(1024)
                #hosts_file.close()
                #client()
                print "key added to the server as well as server's key, connect again, goodbye..."
                sys.exit()
                
        elif request=="no":
            hosts_file.close()
            s.close()
            sys.exit()
else:
    host = check_ip(ip)
    reply=s.recv(1024)
    if reply:
        pub_key=json.loads(reply)
        #print pub_key
        public_key=json.JSONEncoder().encode(read_files(".keys/id_rsa.pub"))
        s.send(public_key)
        fx_and_x=s.recv(1024)
        if fx_and_x:
                challenge()
                if authenticate(fx_and_x,host):
                        print "Server has been authenticated..."
                        hosts_file.close()
                        client()
                else:
                        print "Warning, the server you are about to connect to does not seem to be legit, goodbye..."
                        sys.exit()
        else:
                print "your public keys are being sent to server..."
         
s.close()
