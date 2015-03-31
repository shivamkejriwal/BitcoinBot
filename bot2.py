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

# Converts a time series sequence into the X,Y format
def reshapeData(sequence,size):
    print "Reshaping Data ..."
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


class neuralNet:
    weigth = []
    size = 0
    count = 0
    def __init__(self,size):

        if len(sequence)==0:
            print "No Data"
            return

        self.weight = np.zeros(size)
        #self.weight = np.ones(size)
        self. size = size
        self.count = 0
        self.printState()

    def printState(self):
        print "==============="
        print "Size of X:",self.size
        print "Count of X:",self.count
        print "Weight:",self.weight
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
        alpha = .001 #1/float(self.size)
        pred = self.getPrediction(x)
        real = self.getReal(x[-1],y)
        error = real-pred
        #print x[-1],y,"(",pred,real,"):",error
        #update
        for j in range(len(self.weight)):
            self.weight[j]+=alpha*error*x[j]
        self.count+=1

    def train(self,x,y):
        print "Training..."
        count = len(y)
        for i in range(count):
            self.trainOne(x[i],y[i])
            #print self.weight

    def testOne(self,x,y):
        x = np.array(x)
        #print "--------",x,y
        pred = self.getPrediction(x)
        real = self.getReal(x[-1],y)
        if pred!=real : return 1
        return 0
        #error = (real-pred)
        #print "error rate:",error
        #return abs(error)

    def test(self,x,y):
        print "Testing...dataSeq..."
        if len(x)<=0 or len(y)<=0:
            print "No Data"
            return
        
        count = len(y) 
        totalError = 0
        print "Count of Y:",count
        for i in range(count):
            totalError += self.testOne(x[i],y[i])
        totalError/=count
        print "Total Error:",totalError

    def getState(self):
        print self.weigth






# Main
# ===========
size = 7
sequence = getLargeData(2)
dataX,dataY  = reshapeData(sequence,size)

nn = neuralNet(size)
nn.train(dataX,dataY)
nn.printState()
sequence = getLargeData()
dataX,dataY  = reshapeData(sequence,size)
nn.test(dataX,dataY)

