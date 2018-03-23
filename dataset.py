from numpy import *
from os import listdir
from os.path import isfile
import os
from util import *
import struct
import io

class dataSet(object):
    n = 0
    mat = []
    labels = []
    datafile = ""
    charCode = "L" if os.name == "nt" else "I"

    def load(self):
        f = io.open(self.datafile,"rb")
        # L for windows; I for linux/unix

        self.n = struct.unpack(self.charCode,f.read(4))[0]
        veclen = struct.unpack(self.charCode,f.read(4))[0]
        self.mat = zeros((self.n,veclen))
        for i in range(self.n):
            n = struct.unpack("H",f.read(2))[0]
            self.labels.append(n)
            for j in range(veclen):
                x = struct.unpack("B",f.read(1))[0]
                self.mat[i][j] = x
        f.close()

    def save(self):
        f = open(self.datafile,"wb")
        f.write(struct.pack(self.charCode,self.n))
        f.write(struct.pack(self.charCode,len(self.mat[0])))
        for i in range(self.n):
            f.write(struct.pack("H",self.labels[i]))
            for j in self.mat[i]:
                f.write(struct.pack("B",j))
        f.close()

class trainingSet(dataSet):

    datafile = "trainingSet.dat"

    def __init__(self):
        self.labels=[]
        if isfile(self.datafile):
            self.load()
        else:
            self.loadRaw()
            self.save()

    def loadRaw(self):
        trainingFileList = listdir('trainingDigits')
        m = len(trainingFileList)
        self.mat = zeros((m,1024))
        self.n = m
        for i in range(m):
            fileNameStr = trainingFileList[i]
            fileStr = fileNameStr.split('.')[0]
            classNumStr = int(fileStr.split('_')[0])
            self.labels.append(classNumStr)
            self.mat[i,:] = img2vector('trainingDigits/%s' % fileNameStr)

    def selfLearn(self,vec,label):
        self.mat = vstack((self.mat,vec))
        self.labels.append(label)
        self.n += 1
        self.save()

class testSet(dataSet):
    datafile = "testSet.dat"

    def __init__(self):
        self.labels=[]
        if isfile(self.datafile):
            self.load()
        else:
            self.loadRaw()
            self.save()

    def loadRaw(self):
        trainingFileList = listdir('testDigits')
        m = len(trainingFileList)
        self.mat = zeros((m,1024))
        self.n = m
        for i in range(m):
            fileNameStr = trainingFileList[i]
            fileStr = fileNameStr.split('.')[0]
            classNumStr = int(fileStr.split('_')[0])
            self.labels.append(classNumStr)
            self.mat[i,:] = img2vector('testDigits/%s' % fileNameStr)
