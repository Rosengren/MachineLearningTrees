from Tree import Tree
import math
import operator
import random
import json
from DataGenerator import DataGenerator
# from Classifier import Classifier

# format: {'class': [[min, max], [min, max]], }
irisThesholds = {'Iris-setosa': [[4.4,5.1], [3.0,4.0], [1.3, 1.7], [0.2,0.4]],
								 'Iris-versicolor': [[5.5,6.8],[2.3,3.0],[3.2,4.8],[1.1,1.5]],
								 'Iris-virginica': [[6.0,7.7],[2.6,3.2],[4.9, 6.7],[1.8,2.5]]}

wineThresholds = {''}
# classNames = ['A']
classNames = ['A','B','C','D']
numberOfDimensions = 10
numberOfSamplesPerClass = 2000


gen = DataGenerator()
samples = []
trees = {}
for c in classNames:
	tree = gen.generateTree(['X'+`i` for i in range(numberOfDimensions)])
	data = gen.generateDependentData(numberOfSamplesPerClass, c, tree)
	sample = data['samples']
	for s in sample:
		s.append(data['name'])
		samples.append(s)

	trees[c] = tree


def trainWithThresholds(trainingSet, classLocation, thresholds):

	totalDimensionsForClass = {}


	dLength = len(trainingSet[0]) - 1
	indiviProb = {} # probability of getting a 1 for each 
	total = {}
	for train in trainingSet:
		indiviProb.setdefault(train[classLocation], [(0.0) for x in range(dLength)])
		total.setdefault(train[classLocation], [(0.0) for x in range(dLength)])

		# count total occurence of each class in training set
		if not train[classLocation] in totalDimensionsForClass:
		    totalDimensionsForClass[train[classLocation]] = 1
		else:
		    totalDimensionsForClass[train[classLocation]] += 1

		for x in range(dLength):
			if train[x] >= thresholds[train[classLocation]][x][0] and train[x] <= thresholds[train[classLocation]][x][1]:
				indiviProb[train[classLocation]][x] += 1.0
			total[train[classLocation]][x] += 1.0


	# replace frequency with probability of individual values
	for result in indiviProb:
		indiviProb[result] = map(lambda x, y: x / y, indiviProb[result], total[result])

	# Create sets for each attribute
	setOfOnes = {} # contains an array of sets for all locations where the given attribute is a 1
	location = 0 # this assumes the data is in order
	for train in trainingSet:
		setOfOnes.setdefault(train[classLocation], [set() for x in range(dLength)])
		for x in range(dLength):

			if train[x] >= thresholds[train[classLocation]][x][0] and train[x] <= thresholds[train[classLocation]][x][1]:
				setOfOnes[train[classLocation]][x].add(location)
		if location < totalDimensionsForClass[train[classLocation]]: 
			location += 1
		else:
			location = 0

	jointProbsForAllClasses = {}
	jointProbs = {}

	for c in setOfOnes:
		wholeSet = set([(x) for x in range(totalDimensionsForClass[c])])
		jointClassProbs = {}
		for X1 in setOfOnes[c]:
			for X2 in setOfOnes[c][setOfOnes[c].index(X1):]:
				if X1 != X2:
					X1i = setOfOnes[c].index(X1)
					X2i = setOfOnes[c].index(X2)

					newSet = frozenset([X1i,X2i])

					jointClassProbs.setdefault(newSet, [[0,0],[0,0]])
					jointClassProbs[newSet][0][0] = len(wholeSet.difference(setOfOnes[c][X1i]).intersection(wholeSet.difference(setOfOnes[c][X2i])))
					jointClassProbs[newSet][0][1] = len((wholeSet.difference(setOfOnes[c][X1i])).intersection(setOfOnes[c][X2i]))
					jointClassProbs[newSet][1][0] = len(setOfOnes[c][X1i].intersection(wholeSet.difference(setOfOnes[c][X2i])))
					jointClassProbs[newSet][1][1] = len(setOfOnes[c][X2i].intersection(setOfOnes[c][X1i]))

		# convert frequency into probability
		for key in jointClassProbs:
			for X1 in range(len(jointClassProbs[key])):
				for X2 in range(len(jointClassProbs[key][X1])):
					jointClassProbs[key][X1][X2] /= (1.0 * totalDimensionsForClass[c])

		# append to joint probabilities
		jointProbs[c] = jointClassProbs

			
	return (jointProbs, indiviProb)

def train(trainingSet, classLocation):

	totalDimensionsForClass = {}


	dLength = len(trainingSet[0]) - 1
	indiviProb = {} # probability of getting a 1 for each 
	total = {}
	for train in trainingSet:
		indiviProb.setdefault(train[classLocation], [(0.0) for x in range(dLength)])
		total.setdefault(train[classLocation], [(0.0) for x in range(dLength)])

		# count total occurence of each class in training set
		if not train[classLocation] in totalDimensionsForClass:
		    totalDimensionsForClass[train[classLocation]] = 1
		else:
		    totalDimensionsForClass[train[classLocation]] += 1

		for x in range(dLength):
			indiviProb[train[classLocation]][x] += train[x]
			total[train[classLocation]][x] += 1.0


	# replace frequency with probability of individual values
	for result in indiviProb:
		indiviProb[result] = map(lambda x, y: x / y, indiviProb[result], total[result])

	# Create sets for each attribute
	setOfOnes = {} # contains an array of sets for all locations where the given attribute is a 1
	location = 0 # this assumes the data is in order
	for train in trainingSet:
		setOfOnes.setdefault(train[classLocation], [set() for x in range(dLength)])
		for x in range(dLength):
			if train[x] == 1:
				setOfOnes[train[classLocation]][x].add(location)
		if location < totalDimensionsForClass[train[classLocation]]: 
			location += 1
		else:
			location = 0

	# wholeSet = set([(x) for x in range(2000)])
	jointProbsForAllClasses = {}
	jointProbs = {}

	for c in setOfOnes:
		wholeSet = set([(x) for x in range(totalDimensionsForClass[c])])
		jointClassProbs = {}
		for X1 in setOfOnes[c]:
			for X2 in setOfOnes[c][setOfOnes[c].index(X1):]:
				if X1 != X2:
					X1i = setOfOnes[c].index(X1)
					X2i = setOfOnes[c].index(X2)

					newSet = frozenset([X1i,X2i])

					jointClassProbs.setdefault(newSet, [[0,0],[0,0]])
					jointClassProbs[newSet][0][0] = len(wholeSet.difference(setOfOnes[c][X1i]).intersection(wholeSet.difference(setOfOnes[c][X2i])))
					jointClassProbs[newSet][0][1] = len((wholeSet.difference(setOfOnes[c][X1i])).intersection(setOfOnes[c][X2i]))
					jointClassProbs[newSet][1][0] = len(setOfOnes[c][X1i].intersection(wholeSet.difference(setOfOnes[c][X2i])))
					jointClassProbs[newSet][1][1] = len(setOfOnes[c][X2i].intersection(setOfOnes[c][X1i]))

		# convert frequency into probability
		for key in jointClassProbs:
			for X1 in range(len(jointClassProbs[key])):
				for X2 in range(len(jointClassProbs[key][X1])):
					jointClassProbs[key][X1][X2] /= (1.0 * totalDimensionsForClass[c])

		# append to joint probabilities
		jointProbs[c] = jointClassProbs

			
	return (jointProbs, indiviProb)
	

def calculateWeights(jointProbs, indiviProbs):
	weights = {}

	for attr in jointProbs:
		p = []
		for t in attr:
			p.append(indiviProbs[int(t)])
		

		firstWeight = 0
		for x in range(len(jointProbs[attr])):
			for y in range(len(jointProbs[attr][x])): 
				xProb = p[0]
				yProb = p[1]
				if x == 0:
					xProb = 1 - p[0]
				if y == 0:
					yProb = 1 - p[1]
				print ("Testing: x=%d, y=%d, xProb=%f, yProb=%f, jointProbs[attr][x][y]=%f" % (x, y, xProb, yProb, jointProbs[attr][x][y]))
				print attr
				print calculateWeight(jointProbs[attr][x][y], xProb, yProb)
				firstWeight += calculateWeight(jointProbs[attr][x][y], xProb, yProb)

		weights[attr] = firstWeight
		print firstWeight
	# print indiviProbs
	attributes = set() # need to get all the highest values until all are connected
	connections = []
	print len(weights)
	for weight in weights:
		print weight
		print weights[weight]
	# while len(attributes) < len(indiviProbs):

	for x in range(len(indiviProbs) - 1):
		maxKey = max(weights.iteritems(), key=operator.itemgetter(1))[0]
		del weights[maxKey]

		for h in maxKey:
			attributes.add(h)

		connections.append(maxKey)
		
	# print connections
	# print len(connections)

	return connections


def calculateWeight(xyProb, xProb, yProb):
	if xProb == 0 or yProb == 0 or xyProb == 0:
		return 0
	print "xyProb = %f, xProb = %f, yProb = %f" % (xyProb, xProb, yProb)
	return xyProb * math.log(xyProb / (xProb * yProb))


def ouputToCSV(filename, data):
	f = open(filename, 'w')
	for item in data:
		f.write(','.join([str(x) for x in item]) + '\n')
	f.close

def saveJSONtoFile(filename, data):
 with open(filename, 'w') as fp:
     json.dump(data, fp)

def calculatedTreeToJSON(data, listOfDimensions):
	nodes = [(Tree(None, dim)) for dim in listOfDimensions]

	root = None
	for d in data:
		(a, b) = d
		nodes[b].setParent(nodes[a])
		nodes[a].addChild(nodes[b])

		# for a in d:
			# p.append[]
		print d

	for n in nodes:
		# if n.isRoot():
		print n.getJSONFormat()

			# root = n
		# 	break;

	# print root.getJSONFormat()
	# dimensions = [(Tree(None, dim)) for dim in listOfDimensions]
	# parents = []

	# root = None
	# for d in range(dimensions):



	# for i in range(connections):
	# 	index = randint(0, len(dimensions) - 1)

	# 	if root is None:
	# 		root = dimensions[index]
	# 		parents.append(root)
	# 	else:
	# 		parent = random.choice(parents)
	# 		child = dimensions[index]
	# 		child.setParent(parent)
	# 		parent.addChild(child)
	# 		parents.append(child)

	# 	del dimensions[index]

	# return root
	# for d in data:
	# 	for 

ouputToCSV('testData.csv', samples)
jointProbs, indiviProb = train(samples, numberOfDimensions)
cA = calculateWeights(jointProbs['A'], indiviProb['A'])
# cB = calculateWeights(jointProbs['B'], indiviProb['B'])
# cC = calculateWeights(jointProbs['C'], indiviProb['C'])
# cD = calculateWeights(jointProbs['D'], indiviProb['D'])

saveJSONtoFile('flare.json', trees['A'].getJSONFormat())
# saveJSONtoFile('generated.json', cA)

# calculatedTreeToJSON(cA, [0,1,2,3,4,5,6,7,8,9])


# TEST IRIS:


def readCSVInput(filename, classNumber):
	result = []
	with open(filename) as f:
		lines = f.readlines()

	for line in lines:
		elements = line.rstrip().split(',')
		for x in range(len(elements)):
			if x != classNumber:
				elements[x] = float(elements[x])
		result.append(elements)

	return result

# numberOfDimensions = 4
# samples = readCSVInput("iris.csv", 4)
# jointProbs, indiviProb = trainWithThresholds(samples, numberOfDimensions, irisThesholds)
# cI = calculateWeights(jointProbs['Iris-virginica'], indiviProb['Iris-virginica'])
# cI2 = calculateWeights(jointProbs['Iris-versicolor'], indiviProb['Iris-versicolor'])
# cI3 = calculateWeights(jointProbs['Iris-setosa'], indiviProb['Iris-setosa'])
# print cI
# print cI2
# print cI3
# cN = calculateWeights()