#!/usr/bin/python2
from random import randint
import math

def inverse(a, b): #extended gcd or generating x within 1=e(x)+y(phi(n))
  value=b
  X,Y,Xant,Yant= 0,1,1,0

  while b != 0:
      int_division = a//b
      (a,b)=(b,a%b)
      temp = X
      X = Xant - int_division * X
      Xant = temp
      temp = Y
      Y = Yant - int_division * Y
      Yant = temp
  if Xant < 0:
    return value+Xant
  else:
    return Xant

def gcd(num1,num2): #for greatest common denominator 
  if num2==0:
    return num1
  else:
    return gcd(num2,num1%num2)
    
def primo(num): #validating prime numbers
    if num%2==0:
        return False
    tope=math.ceil(math.sqrt(num))
    div=3
    while div<tope:
        if num%div==0:
            return False
        div+=2
    return True

def Generador_primo(): #generating prime numbers
    while True:
      n=randint(100000,999999)
      if primo(n) and primo((n-1)/2):
        break
    return n

def get_e(phi_n): #seeking a public key e that is relatively prime to phi(n)
  while True:
    e=Generador_primo()
    if gcd(e,phi_n)==1:
      break
  return e

def main():
  p=Generador_primo()
  q=Generador_primo()
  n=p*q
  phiN=(p-1)*(q-1)
  e=get_e(phiN)
  d=inverse(e,phiN)
  data={"n":n,"e":e,"d":d}
  return data
  #print(json.JSONEncoder().encode(data))


