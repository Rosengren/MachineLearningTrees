import random
from random import randint

class DataGenerator:
	def __init__(self, dimensions):

		self.root = {}
		self.weights = []
		self.featureList = []

		if dimensions:
			for x in range(0, len(dimensions)):
				self.featureList.append(self.generateFeature(dimensions[x]))


	def generateFeature(self, featureName):
		return {'name': featureName, 'children': []}



	def generateTree(self, featureList={}):
		if not featureList:
			featureList = self.featureList

		numberOfConnections = len(featureList)
		unconnectedFeatures = featureList[:]
		parentFeatures = []

		for i in range(0, numberOfConnections):
			index = randint(0, len(unconnectedFeatures) - 1)

			if parentFeatures:
				parent = random.choice(parentFeatures)
				parent['children'].append(unconnectedFeatures[index])
				self.weights.append({"vertices": [parent["name"], unconnectedFeatures[index]["name"]], "weight": round(random.random(), 2)})
			else:
				self.root = unconnectedFeatures[index]

			parentFeatures.append(unconnectedFeatures[index])
			del unconnectedFeatures[index]

		print(self.weights)
		return self.root

	def generateClass(self, className):
		if not self.root:
			self.root = generateTree()


	def calculateProbability(root, child):
		weight = 1
		for w in weights:
			if root['name'] in w['vertices'] and child['name'] in w['vertices']:
				weight = w["weight"]

		return weight * child['weight'] / root['weight']


	# def calculateNewProbability(self, parent, child):
	# 	parent[]
	# 	return
		





features = [
						{'name': 'A', 'probability':round(random.random(), 2), 'children': []},
						{'name': 'B', 'probability':round(random.random(), 2), 'children': []},
						{'name': 'C', 'probability':round(random.random(), 2), 'children': []},
						{'name': 'D', 'probability':round(random.random(), 2), 'children': []},
						{'name': 'E', 'probability':round(random.random(), 2), 'children': []}
					]

d = DataGenerator(features)
root = d.generateTree(features)

	# TODO:
	#  d-dimensions
	#  c classes
	# write method to generate probabilities
	# write method to assign probabilities to each node
	# write method that returns the vector and class name
	# write method that returns all of the classes
	# write method that writes to file all of the generated data in csv format