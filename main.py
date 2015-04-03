from Tree import Tree
from Helper import *
from DataGenerator import DataGenerator
# from DecisionTree import DecisionTree
from Classifier import Classifier
from Dependence import Dependence


# Customize output
####################################
CLASSNAMES = ['A','B','C','D']
NUMBER_OF_DIMENSIONS = 10
NUMBER_OF_SAMPLES_PER_CLASS = 2000
####################################



if __name__ == '__main__':
		
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


	ouputToCSV('testData.csv', samples)
	dep = Dependence()
	jointProbs, indiviProb = dep.train(samples, NUMBER_OF_DIMENSIONS)
	cA = dep.calculateWeights(jointProbs['A'], indiviProb['A'])
	cB = calculateWeights(jointProbs['B'], indiviProb['B'])
	cC = calculateWeights(jointProbs['C'], indiviProb['C'])
	cD = calculateWeights(jointProbs['D'], indiviProb['D'])

	saveJSONtoFile('flare.json', trees['A'].getJSONFormat())

	dep.printEdges()