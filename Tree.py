from random import randint
import random

class Tree:
	def __init__(self, parent=None, name=''):
		self.name = name
		self.parent = parent
		self.value = 0
		self.children =[]
		self.probability = round(random.random(), 2)
		self.probabilityGivenOne = round(random.random(), 2) # based on the parent value
		self.probabilityGivenZero = round(random.random(), 2) # based on the parent value

	def setProbabilityGivenOne(self, probability):
		self.probabilityGivenOne = probability

	def setProbabilityGivenZero(self, probability):
		self.probabilityGivenZero = probability

	def getJSONFormat(self):
		result = {"name": self.name, "children": []}
		for child in self.children:
			result["children"].append(child.getJSONFormat())
		return result

	def getChildren(self):
		return self.children

	def setParent(self, parent):
		self.parent = parent

	def isRoot(self):
		return self.parent == None

	def getName(self):
		return self.name

	def addChild(self, child):
		self.children.append(child)

	def getProbability(self):
		if self.parent is None:
			return self.probability
		
		if self.parent.value == 0:
			return self.probabilityGivenZero
		else:
			return self.probabilityGivenOne

	def setValue(self, value):
		self.value = value

	def getValue(self):
		return self.value