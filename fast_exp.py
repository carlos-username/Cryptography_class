#!/usr/bin/python2
def fast_expo(base,exp,mod): #fast exponentiation
    pot=base%mod
    res=1
    while exp != 0:
        if exp%2==1:
            res=(res*pot)%mod
        exp>>=1
        pot=(pot*pot)%mod
    return res

def f(x):
    return int(x)*2+9
