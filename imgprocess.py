from __future__ import print_function
from PIL import Image
from os.path import isfile
import numpy as np
import sys

class IMGProcess(object):

    def __init__(self,fn,size):
        self.fn = fn
        if not isfile(fn):
            print("File not exist",file=sys.stderr)
            exit(1)
        self.img = Image.open(fn)
        self.size = size

    def getVec(self):
        # convert to grayscale
        gs = self.img.convert('L')
        # convert img to array
        gs = np.array(gs)
        # find char
        pixels = []
        sx, sy = self.img.size
        for x in range(sx):
            for y in range(sy):
                if gs[y][x] != 255:
                    pixels.append([x,y])
        pixels = np.array(pixels)
        xmin, ymin = pixels.min(axis=0)
        xmax, ymax = pixels.max(axis=0)
        # crop
        c = self.img.crop((xmin,ymin,xmax,ymax))
        c.thumbnail(self.size,Image.ANTIALIAS)
        # resize
        r = Image.new("L",self.size,"white")
        offset = (
            int((self.size[0]-c.size[0])/2),
            int((self.size[1]-c.size[1])/2)
            )
        r.paste(c,offset)
        r = np.array(r.convert("L"))
        # convert to vector
        v = np.zeros((1,self.size[0]*self.size[1]))
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if r[i][j] < 128:
                    v[0,self.size[0]*i+j] = 1
                else:
                    v[0,self.size[0]*i+j] = 0
        return v[0]