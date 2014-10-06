#!/usr/bin/python2
import math
from random import randint
#from sys import argv
class Diffie_hellman:
    def __init__(self,p,g,x,y):
        self.mod = p
        self.base = g
        self.x = x
        self.y = y
    
    def gcd(self,g,exp):
        pot=g%self.mod
        res=1
        while exp != 0:
            if exp%2==1:
                res=(res*pot)%self.mod
            exp>>=1
            pot=(pot*pot)%self.mod
        return res

    def hack(self):
        for i in xrange(2,self.mod-1):
            num=self.gcd(self.base,i)
            if num==self.gcd(self.base,self.x):
                return self.gcd(self.gcd(self.base,i),self.y)
                break
            if num==self.gcd(self.base,self.y):
                return self.gcd(self.gcd(self.base,i),self.x)
                break
        return

def primo(num):
    if num%2==0:
        return False
    tope=math.ceil(math.sqrt(num))
    div=3
    while div<tope:
        if num%div==0:
            return False
        div+=2
    return True

def test_generator(g,fac,mod):
    DH=Diffie_hellman(mod,g,None,None)
    for numero in fac:
        if DH.gcd(g,numero) == 1:
            return False
    return True

def factors(number):
    lista=[]
    for n in xrange(1,number-1):
        if number%n==0:
            lista.append(n)
    return lista

def main():
    while True:
        p=randint(3,99999)
        g=randint(3,99999)
        if primo(p) and primo(g) and test_generator(g,factors(p),p) and g<p:
            break
    print "p-> ",p
    print "g-> ",g
    x,y=(randint(1,p-1),randint(1,p-1))
    print "x-> ",x
    print "y-> ",y
    Diffie=Diffie_hellman(p,g,x,y)
    fX=Diffie.gcd(g,x)
    fY=Diffie.gcd(g,y)
    print "f(x)-> ",fX
    print "f(y)-> ",fY
    print "f(x)^y-> ",Diffie.gcd(fX,y)
    print "f(y)^x-> ",Diffie.gcd(fY,x)
    print "hack-> ",Diffie.hack() 
    
main()
