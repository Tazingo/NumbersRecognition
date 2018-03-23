"""
Hand writing recognition
"""

from __future__ import print_function
from future.builtins import input
import sys
import knn
from dataset import *
from imgprocess import *
import util

def recog(vec,ts):
    return knn.classify(vec, ts.mat, ts.labels, 3)

# test case
def testCase():
    testset = testSet()
    trainingset = trainingSet()
    errors = 0
    print(trainingset.n)
    for i in range(len(testset.mat)):
        n = testset.labels[i]
        r = recog(testset.mat[i],trainingset)
        print("the recognition came back with: %d, the real answer is: %d" % (r,n))
        if r != n:
            errors +=1
            trainingset.selfLearn(testset.mat[i],n)
    print("Errors: %d in total %d" % (errors,testset.n))

# recognise from img
def recogImg(fn):
    img = IMGProcess(fn,(32,32))
    vec = img.getVec()
    ts = trainingSet()
    util.printVec(vec,32)
    return recog(vec, ts), vec

if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("Invalid command")
        print("Usage: hwr.py test|<filename>")
        print("Command test, test with test case")
        print("Command <filename>, recognise from image")
        exit(0)
    if sys.argv[1] == "test":
        print("=========")
        print("Self test")
        print("=========")
        testCase()
    else:
        fn = sys.argv[1]
        r, vec = recogImg(fn)
        print("\nrecognition result is %d\n" % r)
        c = input("Is the result correct? (Y or N): ")
        if c.lower() == "n":
            try:
                cr = int(input("What is the correct answer? "))
            except:
                pass
            else:
                ts = trainingSet()
                ts.selfLearn(vec,cr)