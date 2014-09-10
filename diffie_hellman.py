#!/usr/bin/python2
#script for diffie hellman
import math
from random import randint
from sys import argv
def primo(num):
    if num%2==0:
        return False
    tope=math.ceil(math.sqrt(num))
    div=3
    while div<=tope:
        if num%div==0:
            return False
        div+=2
    return True

def maxpot(base,exp,mod):
    pot=base%mod
    res=1
    while exp != 0:
        if exp%2==1:
            res=(res*pot)%mod
        exp>>=1
        pot=(pot*pot)%mod
    return res

def hack(base,mod,x,y):
    for i in xrange(2,mod-1):
        num=maxpot(base,i,mod)
        if num==fx(base,x,mod):
            return maxpot(maxpot(base,i,mod),y,mod)
            break
        if num==fy(base,y,mod):
            return maxpot(maxpot(base,i,mod),x,mod)
            break
    return

def factors(number):
    lista=[]
    for n in xrange(1,number-1):
        if number%n==0:
            lista.append(n)
    return lista

def fx(g,x,mod):
    return maxpot(g,x,mod)

def fy(g,y,mod):
    return maxpot(g,y,mod)

def test_generator(g,fac,mod):
    for numero in fac:
        if maxpot(g,numero,mod) == 1:
            return False
    return True
            
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
    fX=fx(g,x,p)
    fY=fy(g,y,p)
    print "f(x)-> ",fX
    print "f(y)-> ",fY
    print "f(x)^y-> ",maxpot(fX,y,p)
    print "f(y)^x-> ",maxpot(fY,x,p)
    print "hack-> ",hack(g,p,x,y) 
    
main()
