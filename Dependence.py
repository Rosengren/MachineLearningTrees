import math
from Tree import Tree

class Dependence:
	def __init__(self):
		self.classes = []
		self.models = []
		return


	# FIRST THING's FIRST:
	# 	GET ALL OF THE NUMBERS
	# 	FORMAT: {'name': 'className', 'occurences': [10,30,75,8,...],
	#            '':}
	# OR: {'className': [occurence], 'className2': [occurance]}


	# INPUT FORMAT: [{'name': 'className', 'dimensions': [1 0 1 0 0 1]}]
	# FORMAT: 
	#  {'className': [occurence], 'className2': [occurance]}
	# Need this information:
	#  	probability of x1, x2, x3, x4, ...
	# 	probability
	def train(self, trainingSet):
		total = len(trainingSet)
		results = {}
		for train in trainingSet:
			results.setdefault(train['name'], [(0) for x in range(len(train['dimensions']))])
			for x in range(len(train['dimensions'])):
				results['name'][x] += 1

		# Now calculate all probabilities
		# for c in results:
		# 	for dimension in range(len(c)):
		# 		c['dimensions'][dimension] = 1.0 * c['dimensions'][dimension] / total

		# for c in results:
		# 	for dimension in range(len(c)):
		# 		for dimension2 in range(dimension, len(c)):
					# WHERE DO I STORE xy probabilities?
					# how do I identify which property connects which two vertices?
					# G = (V, E, W)
					# Edge = ['attr1', 'attr2']
					# weight = weight

		return

	# data format: [{'xyProb': 0.10, 'xProb': 0.50, 'yProb'}]
	# returns [(weight, ['class1', 'class2']), ( ... ), ...]
	def calculateWeights(self, data):
		results = []
		for d in data:
			results.append(self.calculateWeight(d['xyProbabilities'], d['xProbability'], d['yProbability'])

		return results

	# input: array [{'xyProb': 0.2, 'xProb': 0.5, 'yProb': 0.7}, {...}]
	def calculateWeight(self, probabilities):
		result = 0
		for prob in probabilities:
			result += prob['xyProb'] * math.log(prob['xyProb'] / (prob['xProb'] * prob['yProb']))

		return result


# STEPS:
# 1. Go through the data set once to collect all of the
#		 Necessary Information for the weights



# TESTING:
# 1. Go through the tree to determine the probability of each class
# 2. Choose the highest