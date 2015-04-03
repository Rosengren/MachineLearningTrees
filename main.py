#!/usr/bin/env python
from Tree import Tree
from Helper import *
from Buckets import *
from BayesianClassifier import *
from DataGenerator import DataGenerator
from DecisionTree import DecisionTree
from Dependence import Dependence


# Customize output
####################################
CLASSNAMES = ['A','B','C','D']
NUMBER_OF_CLASSES = len(CLASSNAMES)
NUMBER_OF_DIMENSIONS = 10
NUMBER_OF_SAMPLES_PER_CLASS = 2000
####################################


if __name__ == '__main__':

	# GENERATE DEPENDENT DATA
		
	# generate = DataGenerator()
	# samples = []
	# trees = {}
	# for c in CLASSNAMES:
	# 	tree = generate.generateTree(['X'+`i` for i in range(NUMBER_OF_DIMENSIONS)])
	# 	data = generate.generateDependentData(NUMBER_OF_SAMPLES_PER_CLASS, c, tree)
	# 	sample = data['samples']
	# 	for s in sample:
	# 		s.append(data['name'])
	# 		samples.append(s)

	# 	trees[c] = tree

	# saveJSONtoFile("flare.json", trees['A'].getJSONFormat())

	# gen = DataGenerator()
	# samples = []
	# trees = {}
	# for c in classNames:
	#     tree = gen.generateTree(['X'+`i` for i in range(1, numberOfDimensions + 1)])
	#     data = gen.generateDependentData(numberOfSamplesPerClass, c, tree)
	#     sample = data['samples']
	#     for s in sample:
	#         s.append(data['name'])
	#         s.reverse
	#         samples.append(s)
	#     trees[c] = tree

	


	# TESTING DEPENDENCE TREE

	# ouputToCSV('datasets/testData.csv', samples)
	# dep = Dependence()
	# jointProbs, indiviProb = dep.train(samples, NUMBER_OF_DIMENSIONS)
	# cA = dep.calculateWeights(jointProbs['A'], indiviProb['A'])
	# cB = dep.calculateWeights(jointProbs['B'], indiviProb['B'])
	# cC = dep.calculateWeights(jointProbs['C'], indiviProb['C'])
	# cD = dep.calculateWeights(jointProbs['D'], indiviProb['D'])

	# saveJSONtoFile('flare.json', trees['A'].getJSONFormat())

	# dep.printEdges()


	# TESTING BAYESIAN CLASSIFIER

	# buckets('datasets/iris.csv', 'datasets/iris', ',', 4)
	# tenfold("datasets/iris", "num,num,num,num,class")

	# buckets('datasets/heartDisease.csv', 'datasets/heartDisease', ',', 13)
	# tenfold("datasets/heartDisease", "num,num,num,num,num,num,num,num,num,num,num,num,num,class")


	# buckets('datasets/wine.csv', 'datasets/wine', ',', 0)
	# tenfold("datasets/wine", "class,num,num,num,num,num,num,num,num,num,num,num,num,num")

	# TESTING DECISION TREE

	# testingSet = []
	# trainingSet = []
	# i = 0

	# total = len(samples)

	# # 8 = 8-fold cross validation
	# nth = total / (total / 8 / NUMBER_OF_CLASSES)

	# # puts every nth element into the testing data set
	# for t in samples:
	#     if i % nth == 0:
	#         testingSet.append(t)
	#     else:
	#         trainingSet.append(t)
	#     i += 1

	# trainingSet = convertDataToDecisionTreeFormat(trainingSet, NUMBER_OF_DIMENSIONS)
	# convertedTesting = convertDataToDecisionTreeFormat(testingSet, NUMBER_OF_DIMENSIONS)

	# dataAttributes = ["name", "X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8", "X9", "X10"]

	# dt = DecisionTree()
	# tree = dt.create_decision_tree(trainingSet, dataAttributes, dataAttributes[0])

	# print tree
	# print "---------------------------------------------------------------------------"
	# print dt.print_tree(tree, "")