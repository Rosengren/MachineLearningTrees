#!/usr/bin/env python
from Tree import Tree
from Helper import *
from Buckets import *
from BayesianClassifier import *
from OptimalBayesClassifier import *
from Dependence import Dependence
from DecisionTree import DecisionTree
from DataGenerator import DataGenerator


# Customize output
####################################
CLASSNAMES = ['A','B','C','D']
NUMBER_OF_CLASSES = len(CLASSNAMES)
NUMBER_OF_DIMENSIONS = 10
NUMBER_OF_SAMPLES_PER_CLASS = 2000
####################################


if __name__ == '__main__':

	# GENERATE DEPENDENT DATA
		
	generate = DataGenerator()
	samples = []
	trees = {}
	for c in CLASSNAMES:
		tree = generate.generateTree(['X'+`i` for i in range(NUMBER_OF_DIMENSIONS)])
		data = generate.generateDependentData(NUMBER_OF_SAMPLES_PER_CLASS, c, tree)
		sample = data['samples']
		for s in sample:
			s.append(data['name'])
			samples.append(s)

		trees[c] = tree

	saveJSONtoFile("flare.json", trees['A'].getJSONFormat())

	testingSet = []
	trainingSet = []
	i = 0

	total = len(samples)

	# 8 = 8-fold cross validation
	nth = total / (total / 8 / NUMBER_OF_CLASSES)

	# puts every nth element into the testing data set
	for t in samples:
	    if i % nth == 0:
	        testingSet.append(t)
	    else:
	        trainingSet.append(t)
	    i += 1


	# TESTING DEPENDENCE TREE

	# ouputToCSV('datasets/testData.csv', samples)
	# dependence = Dependence()
	# jointProbs, indiviProb = dependence.train(samples, NUMBER_OF_DIMENSIONS)
	# cA = dependence.calculateWeights(jointProbs['A'], indiviProb['A'])
	# cB = dependence.calculateWeights(jointProbs['B'], indiviProb['B'])
	# cC = dependence.calculateWeights(jointProbs['C'], indiviProb['C'])
	# cD = dependence.calculateWeights(jointProbs['D'], indiviProb['D'])

	# saveJSONtoFile('flare.json', trees['A'].getJSONFormat())

	# dependence.printEdges()


	# TESTING OPTIMAL BAYESIAN CLASSIFIER (WITH BINARY PROBABILITIES)

	classifier = OptimalBayesClassifier()
	classifier.train(trainingSet, 10)
	classifier.test(testingSet, 10)


	# TESTING BAYESIAN CLASSIFIER

	# buckets('datasets/iris.csv', 'datasets/iris', ',', 4)
	# tenfold("datasets/iris", "num,num,num,num,class")

	# buckets('datasets/heartDisease.csv', 'datasets/heartDisease', ',', 13)
	# tenfold("datasets/heartDisease", "num,num,num,num,num,num,num,num,num,num,num,num,num,class")


	# buckets('datasets/wine.csv', 'datasets/wine', ',', 0)
	# tenfold("datasets/wine", "class,num,num,num,num,num,num,num,num,num,num,num,num,num")

	# TESTING DECISION TREE


	# trainingSet = convertDataToDecisionTreeFormat(trainingSet, NUMBER_OF_DIMENSIONS)
	# convertedTesting = convertDataToDecisionTreeFormat(testingSet, NUMBER_OF_DIMENSIONS)

	# dataAttributes = ["name", "X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8", "X9", "X10"]

	# dt = DecisionTree()
	# tree = dt.create_decision_tree(trainingSet, dataAttributes, dataAttributes[0])

	# print tree
	# print "---------------------------------------------------------------------------"
	# print dt.print_tree(tree, "")