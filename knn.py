import csv, random,math, operator, sys
from math import *
from decimal import Decimal

#loading in the training set, the split 2/3
#TO DO: add in different kinds of splits

class KNN():
	def __init__(self, trainingSet = [] ,testSet = [],split =.67):
		self.trainingSet = trainingSet
		self.testSet = testSet
		self.split = split
		random.seed(1)

	def loadDataset(self, filename):
		with open('iris.data', 'rb') as csvfile:
		    lines = csv.reader(csvfile)
		    dataset = list(lines)
		    for x in range(len(dataset)-1):
		        for y in range(4):
		            dataset[x][y] = float(dataset[x][y])
		       
		        if random.random() < self.split:
		            self.trainingSet.append(dataset[x])
		        else:
		            self.testSet.append(dataset[x])

	def euclideanDistance( x, y):
	    return sqrt(sum(pow(a-b,2) for a, b in zip(x, y)))

	def manhattan_distance( x,y):
		return sum(abs(a-b) for a,b in zip(x,y))

	def square_rooted(self, x):
	 	return round(sqrt(sum([a*a for a in x])),3)
	 
	def cosine_similarity(self,x,y):
	   numerator = sum(a*b for a,b in zip(x,y))
	   denominator = self.square_rooted(x)*self.square_rooted(y)
	   return round(numerator/float(denominator),3)

	#getting the k-closest neightbors by whatever distance formula you set 
	def getNeighbors(self, x, k):
		trainingSet = self.trainingSet 
		testInstance = self.testSet[x]

		distances = []
		length    = len(testInstance)-1
		for x in range(len(trainingSet)):
			#print testInstance, trainingSet[x]
			dist = self.cosine_similarity(testInstance[:-1], trainingSet[x][:-1])
			print dist
			distances.append((trainingSet[x], dist))
		
		#if euclidian or manhatten then different
		#distances.sort(key=operator.itemgetter(0))
		distances.sort(key=operator.itemgetter(1), reverse = True)
		neighbors = []
		for x in range(k):
			neighbors.append(distances[x][0])
		return neighbors

	#getting the response
	#TO-DO different types of classvoting methods
	def getResponse(self, neighbors):
		classVotes = {}
		for x in range(len(neighbors)):
			response = neighbors[x][-1]
			if response in classVotes:
				classVotes[response] += 1
			else:
				classVotes[response] = 1
		sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
		return sortedVotes[0][0]

	#getting the overall accuaracy
	def getAccuracy(self, predictions):
		correct = 0
		for x in range(len(self.testSet)):
			if self.testSet[x][-1] == predictions[x]:
				correct += 1
		return (correct/float(len(self.testSet))) * 100.0
	
def main(strk):
	# prepare data
	knnmodel = KNN([],[],.67)
	knnmodel.loadDataset('iris.data')
	print 'Train set: ' + repr(len(knnmodel.trainingSet))
	print 'Test set: ' + repr(len(knnmodel.testSet))
	# generate predictions
	predictions=[]
	k = int(strk)
	for x in range(len(knnmodel.testSet)):
		neighbors = knnmodel.getNeighbors(x, k)
		result = knnmodel.getResponse(neighbors)
		predictions.append(result)
		print('> predicted=' + repr(result) + ', actual=' + repr(knnmodel.testSet[x][-1]))
	accuracy = knnmodel.getAccuracy( predictions)
	print('Accuracy: ' + repr(accuracy) + '%')
	
main(sys.argv[1])