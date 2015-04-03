from DataGenerator import DataGenerator
from random import shuffle

class BayesClassifier:

	def __init__(self):
		self.classes = {}
		self.totalForClass = {}
		self.totalForAllClasses = 0
		self.classProbability = {}
		self.thresholds = {}
		return

	# Training set format: [{'name': 'className', 'samples': [ [sample_1], [sample_2], [...], ...] }]
	def train(self, trainingSet, classNumber):
		dimensions = len(trainingSet[0]) - 1 # classNumber

		for train in trainingSet:
			# print train[classNumber]
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


		# print self.classes
		# print self.totalForClass
		# print self.totalForAllClasses
		# print self.classProbability

	def trainWithThresholds(self, trainingSet, classNumber):
		dimensions = len(trainingSet[0]) - 1 # classNumber
		for train in trainingSet:
			# print train[classNumber]
			self.classes.setdefault(train[classNumber], [(0.0) for x in range(dimensions)])
			self.thresholds.setdefault(train[classNumber], [([0.0,0.0]) for x in range(dimensions)])

			for dimension in range(dimensions):
				if dimension == classNumber:
					continue

				# set thresholds
				if self.thresholds[train[classNumber]][dimension][1] == 0 or train[dimension] > self.thresholds[train[classNumber]][dimension][1]: # MAX
					self.thresholds[train[classNumber]][dimension][1] = train[dimension]
				if self.thresholds[train[classNumber]][dimension][0] == 0 or train[dimension] < self.thresholds[train[classNumber]][dimension][0]: # MIN
					self.thresholds[train[classNumber]][dimension][0] = train[dimension]

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

		print self.thresholds
		print len(self.classes)


	def testWithThresholds(self, testingSet, classNumber):
		correct = 0
		total = 0
		for test in testingSet:
			total += 1
			highestProbability = -1
			highestClass = None
			for c in self.classes:
				probability = 1
				# for dimension in range(len(self.thresholds[c])):
				for dimension in range(5):
					if dimension == classNumber:
						continue

					# print self.thresholds[c][dimension][1]
					# print len(self.thresholds[c])
					# print len(test)
					# print len(self.classes[c])
					# print test[dimension]
					if test[dimension] >= self.thresholds[c][dimension][0] or test[dimension] <= self.thresholds[c][dimension][1]:
						# probability *= self.classes[c][dimension]
						probability *= 0.6
					else:
						probability *= 0.4 # 1 - self.classes[c][dimension]
						# probability *= 1 - self.classes[c][dimension]

				if probability > highestProbability:
					highestProbability = probability
					highestClass = c

			print "Prediction: %s, Actual: %s with %f probability" % (highestClass, test[classNumber], highestProbability)
			if highestClass == test[classNumber]:
				correct += 1

		print ("Accuracy is %.2f percent. Total test cases = %d." % (100 * correct / total, total))


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

			print "Prediction: %s, Actual: %s with %f probability" % (highestClass, test[classNumber], highestProbability)
			if highestClass == test[classNumber]:
				correct += 1
			# determine if it's right

		print ("Accuracy is %.2f percent. Total test cases = %d." % (100 * correct / total, total))

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

def ouputToCSV(filename, data):
	f = open(filename, 'w')
	for item in data:
		f.write(','.join([str(x) for x in item]) + '\n')
	f.close


ouputToCSV('testData.csv', samples)

classifier = BayesClassifier()

testingSet = []
trainingSet = []
i = 0

# we want 1000 test data or 250 from each
total = len(samples)
numOfClasses = len(classNames)

every = total / (total / 8 / numOfClasses)
for t in samples:
	if i % every == 0:
		testingSet.append(t)
	else:
		trainingSet.append(t)
	i += 1


# TEST RANDOM DATA

classifier.train(trainingSet, 10)
classifier.test(testingSet, 10)
