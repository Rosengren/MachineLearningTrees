#!/usr/bin/env python
from random import randint
import random
from Tree import Tree

class DataGenerator:
	def __init__(self):
		return

	def generateTree(self, listOfDimensions):
		connections = len(listOfDimensions)
		dimensions = [(Tree(None, dim)) for dim in listOfDimensions]
		parents = []

		root = None
		for i in range(connections):
			index = randint(0, len(dimensions) - 1)

			if root is None:
				root = dimensions[index]
				parents.append(root)
			else:
				parent = random.choice(parents)
				child = dimensions[index]
				child.setParent(parent)
				parent.addChild(child)
				parents.append(child)

			del dimensions[index]

		return root


	# This method does a breadth first search to get the probabilities of each dimension
	# The probability is determined by requesting the result of their parent.
	# That is, if the parent gets a 1, the child will use the appropriate probability
	def generateDependentData(self, numberOfSamples, className, dependenceTree):
		samples = []
		for x in range(numberOfSamples):
			sample = []
			queue = [dependenceTree]
			while queue:
				current = queue[0]
				ran = round(random.random(), 2)
				current.setValue(0 if (ran > current.getProbability()) else 1)
				sample.append(current.getValue())
				queue = queue[1:] + current.getChildren()

			samples.append(sample)

		return {'name': className, 'samples': samples}
