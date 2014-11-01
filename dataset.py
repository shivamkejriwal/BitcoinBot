import csv
import pymongo
from pymongo import MongoClient

mongo_client = MongoClient()
db = mongo_client["test"]
trades = db["BitCoins"] # trades

#sudo service mongod start
#sudo service mongod stop

#mongoimport --db test --collection BitCoins --type csv --fields timestamp,price,volume --file bitstampUSD.csv
#db.BitCoins.ensureIndex({"timestamp":1})

def importData():
	dataFileName='bitstampUSD.csv'
	with open(dataFileName) as f:
		fieldnames =("timestamp","price","volume")
		reader = csv.DictReader(f,fieldnames)
		for row in reader:
			print row
	trades.ensure_index("timestamp")#ensureIndex
		#BitCoins.insert(records)


def test():
	count = trades.count()
	print count
	for trade in trades.find().sort("timestamp",1).limit(5):
		print trade
test()
#importData()