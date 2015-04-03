from DataGenerator import DataGenerator
from random import shuffle

class OptimalBayesClassifier:

	def __init__(self):
		self.classes = {}
		self.totalForClass = {}
		self.totalForAllClasses = 0
		self.classProbability = {}

	# Training set format: [{'name': 'className', 'samples': [ [sample_1], [sample_2], [...], ...] }]
	def train(self, trainingSet, classNumber):
		dimensions = len(trainingSet[0]) - 1 # classNumber

		for train in trainingSet:
			self.classes.setdefault(train[classNumber], [(0.0) for x in range(dimensions)])

			for dimension in range(dimensions):
				if dimension == classNumber:
					continue

				self.classes[train[classNumber]][dimension] += train[dimension]

			if train[classNumber] not in self.totalForClass:
				self.totalForClass[train[classNumber]] = 1
			else:
				self.totalForClass[train[classNumber]] += 1

		# convert frequency to probability P(x|class)
		for c in self.classes:
			for x in range(len(self.classes[c])):
				self.classes[c][x] /= self.totalForClass[c]

		for c in self.totalForClass:
			self.totalForAllClasses += self.totalForClass[c]

		# class probability
		self.classProbability = {}
		for c in self.totalForClass:
			self.classProbability[c] = 1.0 * self.totalForClass[c] / self.totalForAllClasses


	def test(self, testingSet, classNumber):
		correct = 0
		total = 0
		for test in testingSet:
			total += 1
			highestProbability = -1
			highestClass = None
			for c in self.classes:
				probability = 1
				for dimension in range(len(self.classes[c])):
					if dimension == classNumber:
						continue

					if test[dimension] == 1:
						probability *= self.classes[c][dimension]
					else:
						probability *= 1 - self.classes[c][dimension]

				if probability > highestProbability:
					highestProbability = probability
					highestClass = c

			if highestClass == test[classNumber]:
				correct += 1

		print ("Accuracy is %.2f percent. (%d out of %d tests)" % (100 * correct / total, correct, total))
