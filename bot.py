'''
Created on Mar 22, 2015

@author: Shivam
'''
#from __future__ import division

if __name__ == '__main__':
    pass

import datetime
from datetime import datetime,date, timedelta
import urllib,urllib2,json
import numpy as np

#import pandas as pd



def getData(start,end,count):
    print "Fetching Data ...",start
    # RESPONSE ITEMS
    # ==============
    # Each bucket is an array of the following information:
    # 
    # time bucket start time
    # low lowest price during the bucket interval
    # high highest price during the bucket interval
    # open opening price (first trade) in the bucket interval
    # close closing price (last trade) in the bucket interval
    # volume volume of trading activity during the bucket interval
    gran = (end-start).total_seconds()/count#86400 #sec/hr
    url = 'https://api.exchange.coinbase.com/products/BTC-USD/candles'
    values = {'start' : start,'end' : end,'granularity' : gran }
    data = urllib.urlencode(values)
    reqUrl = url+"?"+data
    res = urllib2.urlopen(reqUrl).read()
    #print "Loading Data ..."
    candles = json.loads(res)
    return candles


# count = 200
# end = date.today()
# start = end - timedelta(days=30)
# #end = datetime(today.year, 2, 1)
# #start = datetime(today.year, 1, 1)

# candles = getData(start,end,count)
# data = []
# for candle in candles:
#     #print candle
#     data.append(candle[4]) # get only closing price



#d1 = datetime.date(2008, 3, 12)

def getLargeData(delay=0):
    data = []

    end = date.today() - timedelta(days=delay*30)
    #print "Last Day: ",end
    for i in range(5):
        start = end - timedelta(days=10)
        candles = getData(start,end,200)
        #print "----------:"len(candles)
        for candle in candles:
            data.append(candle[4]) # get only closing price
        end = start
    return data



class neuralNet:
    weigth = []
    sequence = []
    size = 0
    count = 0
    def __init__(self, sequence, size):

        if len(sequence)==0:
            print "No Data"
            return

        self.weight = np.zeros(size)
        #self.weight = np.ones(size)
        self. sequence = sequence
        self. size = size
        self.count = len(sequence)
        self.printState()

    def printState(self):
        print "==============="
        print "Size of X:",self.size
        print "Count of X:",self.count
        print "Weight:",self.weight
        #print "Sequence:",self.sequence
        print "==============="

    # can be considered activation function
    # maps output values to  set {-1,0,1}
    def getReal(self,old,new):
        margin = 10
        diff = new-old
        if diff>margin: return 1
        elif diff<margin*-1: return -1
        else: return 0

    # maps predicted values to set {-1,0,1}
    def getPrediction(self,x):
        pred = np.dot(x,self.weight)
        #print "pred:",pred
        margin = 10
        if pred>margin: return 1
        elif pred<margin*-1: return -1
        else : return 0

    def trainOne(self,inputs,y):
        #print "--------",inputs,y
        x = np.array(inputs)
        alpha = .001#1/float(self.count)
        pred = self.getPrediction(x)
        real = self.getReal(x[-1],y)
        error = real-pred
        #print x[-1],y,"(",pred,real,"):",error
        #update
        for j in range(len(self.weight)):
            self.weight[j]+=alpha*error*x[j]

    def train(self):
        print "Training..."
        for i in range(self.count-self.size):
            subSequence = self.sequence[i:i+self.size]
            self.trainOne(subSequence,self.sequence[i+self.size])
            #print self.weight

    def testOne(self,x,y):
        x = np.array(   x)
        #print "--------",x,y
        pred = self.getPrediction(x)
        real = self.getReal(x[-1],y)
        if pred!=real : return 1
        return 0
        #error = real-pred
        #return abs(error)

    def test(self):
        print "Testing..."
        totalError = 0
        for i in range(self.count-self.size):
            subSequence = self.sequence[i:i+self.size]
            totalError += self.testOne(subSequence,self.sequence[i+self.size])
        totalError/=self.count
        print "total error:",totalError

    def testData(self,dataSeq):
        print "Testing...dataSeq..."
        if len(dataSeq)==0:
            print "No Data"
            return

        print "Count of X:",len(dataSeq) 
        totalError = 0
        for i in range(self.count-self.size):
            subSequence = dataSeq[i:i+self.size]
            totalError += self.testOne(subSequence,dataSeq[i+self.size])
        totalError/=self.count
        print "Total Error:",totalError

    def getState(self):
        print self.weigth



# Main
# ===========

#data = getLargeData()
#print len(data)

# sequence = []
# for i in range(len(outputs)):
#     sequence.append(int(data[i][0],0))

# print sequence

nn = neuralNet(getLargeData(2),7)
nn.train()


nn.printState()
#nn.test()
nn.testData(getLargeData())



# Misc Fucntions
# ==============

def reshapeData(sequence,size):
    count = len(sequence)
    x =[]
    y =[]
    for i in range(count-size):
        subSequence = sequence[i:i+size]
        output = sequence[i+size]
        #print subSequence,output
        x.append(subSequence)
        y.append(output)
    return x,y




###############################################################################
#from sklearn import svm

#X,y= reshapeData(data,3)
#for ele in X:print ele
#print x,y
#clf = svm.SVR()
#clf.fit(X, y)
#print clf.predict([228.39, 212.44, 219.5])
#print clf.score(X,y)


# import matplotlib.pyplot as plt
# # look at the results
# plt.scatter(X, y, c='k', label='data')
# plt.hold('on')
# plt.plot(X, y_rbf, c='g', label='RBF model')
# plt.plot(X, y_lin, c='r', label='Linear model')
# plt.plot(X, y_poly, c='b', label='Polynomial model')
# plt.xlabel('data')
# plt.ylabel('target')
# plt.title('Support Vector Regression')
# plt.legend()
# plt.show()


