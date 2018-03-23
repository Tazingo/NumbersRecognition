from __future__ import print_function
from numpy import *

def img2vector(filename):
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j] = int(lineStr[j])
    return returnVect

def splitNumber (num):
    lst = []
    while num > 0:
        lst.append(num & 0xFF)
        num >>= 8
    return lst[::-1]

def printVec(vec,n):
	for i in range(len(vec)/n):
		p = []
		for j in range(n):
			p.append(str(int(vec[i*n+j])))
		print("".join(p))
