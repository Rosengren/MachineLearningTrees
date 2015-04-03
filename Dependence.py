import math
import operator
from Tree import Tree

class Dependence:
	def __init__(self):
		self.classes = []
		self.models = []
		self.jointProbabilities = {}
		self.individualProbabilities = {}
		self.undirectedEdges = []
		return



	def printEdges(self, connections=None):
		if connections is None:
			connections = self.undirectedEdges
			if self.undirectedEdges is None:
				return

		print "Edges:"
		print "------"
		for edge in connections:
			(node1, node2) = edge
			print "(%d, %d)" % (node1, node2)
		print "------"


	def train(self, trainingSet, classLocation):

		totalDimensionsForClass = {}


		dLength = len(trainingSet[0]) - 1

		totalNumberOfTestPoints = {}
		for train in trainingSet:
			self.individualProbabilities.setdefault(train[classLocation], [(0.0) for x in range(dLength)])
			totalNumberOfTestPoints.setdefault(train[classLocation], [(0.0) for x in range(dLength)])

			# count total occurence of each class in training set
			if not train[classLocation] in totalDimensionsForClass:
			    totalDimensionsForClass[train[classLocation]] = 1
			else:
			    totalDimensionsForClass[train[classLocation]] += 1

			for x in range(dLength):
				self.individualProbabilities[train[classLocation]][x] += train[x]
				totalNumberOfTestPoints[train[classLocation]][x] += 1.0


		# replace frequency with probability of individual values
		for result in self.individualProbabilities:
			self.individualProbabilities[result] = map(lambda x, y: x / y, self.individualProbabilities[result], totalNumberOfTestPoints[result])

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
			self.jointProbabilities[c] = jointClassProbs

				
		return (self.jointProbabilities, self.individualProbabilities)


	def calculateWeight(self, xyProb, xProb, yProb):
		if xProb == 0 or yProb == 0 or xyProb == 0:
			return 0
		return xyProb * math.log(xyProb / (xProb * yProb))


	def calculateWeights(self, jointProbs, indiviProbs):
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
					firstWeight += self.calculateWeight(jointProbs[attr][x][y], xProb, yProb)

			weights[attr] = firstWeight

		connections = []

		for x in range(len(indiviProbs) - 1):
			maxKey = max(weights.iteritems(), key=operator.itemgetter(1))[0]
			del weights[maxKey]

			connections.append(maxKey)

		self.undirectedEdges = connections
		return connections
