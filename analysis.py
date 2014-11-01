import numpy as np
import matplotlib.pyplot as plt

#dataset = [1,5,7,2,6,7,8,2,2,7,8,3,7,3,7,3,15,6]
#dataset = np.random.random_integers(333,350,27)
#dataset = np.random.random(60)*400


def MovingAverage(values, window):
	weights=np.repeat(1.0,window)/window
	smas = np.convolve(values,weights,'valid')
	return smas


def ExpMovingAverage(values, window):
	weights = np.exp(np.linspace(-1., 0., window))
	weights /= weights.sum()

	# Here, we will just allow the default since it is an EMA
	a =  np.convolve(values, weights)[:len(values)]
	a[:window] = a[window]
	return a #again, as a numpy array.

#Will return a 3EMA of the dataset
#print ExpMovingAverage(dataset, 3)


def MACD(values):

# requires 26 values of data
# macd line acc uptil last 12 values
# histogram acc uptil last 9 values

#MACD Line: (12-day EMA - 26-day EMA)
#Signal Line: 9-day EMA of MACD Line
#MACD Histogram: MACD Line - Signal Line

	if len(values)<27:return None

	ema26 = ExpMovingAverage(values,26)
	ema12 = ExpMovingAverage(values,12)
	macd = ema12-ema26
	macd_ema9 = ExpMovingAverage(macd,9) #signal line
	macd_histogram = macd-macd_ema9

	#print "min", np.min(dataset)
	#print "max", np.max(dataset)
	#x = np.linspace(0, 20, 1000)  # 100 evenly-spaced values from 0 to 50

	result =  ExpMovingAverage(dataset,5)
	return macd,macd_ema9,macd_histogram
	

# Bollinger Bands are a volatility indicator
def BoilerBands(values):

	if len(values)<22:return None

	upperBB = []
	lowerBB = []
	middleBB = []

	
	ema = ExpMovingAverage(values,21)

	for i in range(21,len(values)):
		currentEMA = ema[i-21:len(values)]
		std = np.std(currentEMA)
		ave = np.mean(currentEMA)
		uBB = ave + (2*std)
		lBB = ave - (2*std)
		mBB = currentEMA[len(currentEMA)-1]
		upperBB.append(uBB)
		lowerBB.append(lBB)
		middleBB.append(mBB)

	if len(values)==22:
		upperBB = upperBB[0]
		lowerBB = lowerBB[0]
		middleBB = middleBB[0]

	else:
		upperBB = np.append(np.full(21,upperBB[0]),upperBB)
		lowerBB = np.append(np.full(21,lowerBB[0]),lowerBB)
		middleBB = np.append(np.full(21,middleBB[0]),middleBB)

	#result = np.empty(21).fill()
	#lastValue = values[len(values)-1]
	#percentB = (last - lowerBB) / (upperBB - lowerBB)
	#Bandwidth = (upperBB - lowerBB) / middleBB 
	# bandwidth is equal to four times the 20-period coefficient of variation.
	return upperBB,lowerBB,middleBB #,percentB,Bandwidth


def plotHistogram(histogram_values):
	plt.hist(histogram_values)
	plt.title("Macd Histogram")
	plt.xlabel("Value")
	plt.ylabel("Frequency")
	plt.show()

def plotLineGraph(values,macd,macd_ema9):
	x = range(len(values))
	plt.plot(x,values-values.mean(),'-b', label='value')
	plt.plot(x,macd,'-r', label='macd')
	plt.plot(x,macd_ema9,'-g', label='signal line')

	plt.xlabel('Timestamp')
	plt.ylabel('Price')
	plt.title('Trades')
	plt.legend(loc='upper left')
	#plt.legend(['trades', 'ema'], loc='upper left')
	plt.show()


dataset = np.random.random_integers(333,350,23)
print dataset
upperBB,lowerBB,middleBB = BoilerBands(dataset)
print upperBB,lowerBB,middleBB
#macd,macd_ema9,macd_histogram = MACD(dataset)
print macd,macd_ema9,macd_histogram
#plotHistogram(macd_histogram)
#plotLineGraph(dataset[],macd,macd_ema9)









# Online 
# ============

# required var: SignalLine,

#Calculate ema Online
def ema_online(values,sPrev,window):

	sFirst=yFirst=values[len(values)-1-window]
	yCurr = values[len(values)-1]

	alpha = 2/(window+1)
	sCurr=alpha*yCurr+(1-alpha)*sPrev
	return sCurr

def macd_online(values,sPrev,window):
	ema26 = ExpMovingAverage(values,sPrev,26)
	ema12 = ExpMovingAverage(values,sPrev,12)
	macd = ema12-ema26
	macd_ema9 = ExpMovingAverage(macd,9) #signal line
	macd_histogram = macd-macd_ema9

	#print "min", np.min(dataset)
	#print "max", np.max(dataset)
	#x = np.linspace(0, 20, 1000)  # 100 evenly-spaced values from 0 to 50

	result =  ExpMovingAverage(dataset,5)
	return macd,macd_ema9,macd_histogram