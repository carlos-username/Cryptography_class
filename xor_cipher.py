#!/usr/bin/python2
import sys # for arguments
from random import randint #for python random generator
from os import system #for using gnu/linux tools

def encrypt(plain_text,arch): #subroutine for encrypting and decrypting
    categoria={"friend0":"friend1.txt","friend1":"friend2.txt"} #dictionary containing friend's name as well as its matching file's name
    archivo = open(categoria[arch], "r") # to open file matching the user's name within the dictionary, it's more suitable for reading
    key=str(archivo.readline()) #getting the first line of the key
    cipher="" #string to store cipher
    for letter in xrange(len(plain_text)): #read string letter by letter
        cipher+=chr(ord(plain_text[letter])^ord(key[letter%len(key)])) # getting to xor letter by letter
    system("sed -i '1d' %s" % categoria[arch]) # using gnu/linux tool called sed for deleting lines from file
    archivo.close() # close file
    return cipher

def keys_gen(number_keys,length_pad): 
    archivo1 = open("friend1.txt", "w") #to open files by using read mode
    archivo2 = open("friend2.txt", "w")
    for _ in xrange(0,number_keys): 
        ch="" #string storing key
        for _ in xrange(0,length_pad):
            while True:
                var=randint(32,126) # choosing one ascii number at a time by using random 
                if var!=92: #getting rid of character "/"
                    break #cease loop in case no character "/" is found
            ch+=chr(var) #concatenate string, adding ascii number up and mapping it to its ascii value
        archivo1.write(ch+"\n") #writing key to file making sure a break line is added at the end of each one
        archivo2.write(ch+"\n")
    archivo1.close() # closing files
    archivo2.close()

def main():
    try: #to make sure that parameters are given correctly and as expected
        number_of_keys=int(sys.argv[1])  # number of keys about to be added to both of the files
        keys_gen(number_of_keys,int(sys.argv[2])) #calling subroutine to generate both files containing keys inside
        for i in xrange(number_of_keys): 
            if i%2==0: #if i is pair, then assign 0 to x in order that friend 1 and friend 0 can be switchen when required
                x=0
            else:
                x=1
            message = str(raw_input('I am Friend '+str(x)+', Enter message to your friend '+str((x+1)%2)+": "))
            cifrado=encrypt(message,"friend"+str(x)) #to encrypt message by providing the key within the file and its corresponding message
            print "cipher-> ",cifrado
            print "plain text to friend",str((x+1)%2),": ",encrypt(cifrado,"friend"+str((x+1)%2)) # decrypt message by providing the cipher and the matching key
    except:
       print 'pad length or number of keys was not defined' # in case something goes wrong, raise exception
       return
main() # call what is inside main's subroutine
    
