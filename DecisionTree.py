#!/usr/bin/env python
import math
import copy
import json
from Tree import Tree
from DataGenerator import DataGenerator

def saveJSONtoFile(filename, data):
 with open(filename, 'w') as fp:
     json.dump(data, fp)


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



def convertData(data, classNumber):
    dimensions = len(data[0]) - 1
    # format {"class":"className", "X1":1, "X2"}
    result = []
    for d in data:
        c = {"name":str(d[classNumber])}
        for x in range(dimensions):
            c["X" + str(x + 1)] = str(d[x])
        result.append(c)

    return result

finalData = {}

newHope = Tree()

def NEWPRINT(tree, string):
    """ This function recursively crawls through the d-tree and print out """
    if type(tree) == dict:
        # print "%s%s" % (string, tree.keys()[0])
        print '{"name": "%s%s"' % (string, tree.keys()[0])
        # string = string + "}"
        for item in tree.values()[0].keys():
            # print '%s\t, "children": [{"name": "%s", "children" : [' % (string, item)
            print ', "children": [{"name": "%s", "children" : [' % (item)
            NEWPRINT(tree.values()[0][item], string + '')
            print "]}"
    else:
        print ',{"name": "%s", "children": []}]},%s' % (tree, string)

# def NEWTREE(tree):

#     result = ""
#     if type(tree) == dict:
#         # print "%s%s" % (string, tree.keys()[0])
#         newTree
#         result += '{"name": "%s%s"' % (string, tree.keys()[0])
#         # string = string + "}"
#         for item in tree.values()[0].keys():
#             # print '%s\t, "children": [{"name": "%s", "children" : [' % (string, item)
#             result += ', "children": [{"name": "%s", "children" : [' % (item)
#             result += NEWTREE(tree.values()[0][item], string + ']}')
#     else:
#         result += ',{"name": "%s", "children": []}]%s' % (tree, string)

#     return result

classNames = ['A','B','C','D']
numberOfDimensions = 10
numberOfSamplesPerClass = 2000


gen = DataGenerator()
samples = []
trees = {}
for c in classNames:
    tree = gen.generateTree(['X'+`i` for i in range(1, numberOfDimensions + 1)])
    data = gen.generateDependentData(numberOfSamplesPerClass, c, tree)
    sample = data['samples']
    for s in sample:
        s.append(data['name'])
        s.reverse
        samples.append(s)
    trees[c] = tree

saveJSONtoFile("flare.json", trees['A'].getJSONFormat())

# samples = readCSVInput("iris.csv", 4)

numberOfDimensions = 10

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

convertedTraining = convertData(trainingSet, numberOfDimensions)
convertedTesting = convertData(testingSet, numberOfDimensions)



# data_input_array = convertData(samples, numberOfDimensions)
data_input_array = convertData(trainingSet, numberOfDimensions)


attributes_array = ["name", "X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8", "X9", "X10"]
# attributes_array = ["name", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
# attributes_array = ["X1", "X2", "X3"]
# attributes_array = ["Iris-setosa", "Iris-versicolor", "Iris-virginica"]

# Split-point of age is 36, of salary is 51K, for information gain and gain
# ratio
# data_input_array = [
#         {"department":"sales", "status":"senior", "age":"31-35",
#           "salary":"46k-50k"},
#         {"department":"sales", "status":"junior", "age":"26-30",
#           "salary":"26k-30k"},
#         {"department":"sales", "status":"junior", "age":"31-35",
#           "salary":"31k-35k"},
#         {"department":"systems", "status":"junior", "age":"21-25",
#           "salary":"46k-50k"},
#         {"department":"systems", "status":"senior", "age":"31-35",
#           "salary":"66k-70k"},
#         {"department":"systems", "status":"junior", "age":"26-30",
#           "salary":"46k-50k"},
#         {"department":"systems", "status":"senior", "age":"41-45",
#           "salary":"66k-70k"},
#         {"department":"marketing", "status":"senior", "age":"36-40",
#           "salary":"46k-50k"},
#         {"department":"marketing", "status":"junior", "age":"31-35",
#           "salary":"41k-45k"},
#         {"department":"secretary", "status":"senior", "age":"46-50",
#           "salary":"36k-40k"},
#         {"department":"secretary", "status":"junior", "age":"26-30",
#           "salary":"26k-30k"}
#         ]

# attributes_array = ["department", "status", "salary", "age"]

def majority_value(data, target_attr):
    dic = {}
    max_item = ""
    for record in data:
        dic[record[target_attr]] = dic.get(record[target_attr], 0) + 1
    counts = [(j,i) for i,j in dic.items()]
    count, max_item = max(counts)
    del dic
    return max_item

def entropy(data_input, target_attr):
    val_freq        = {}
    data_entropy    = 0.0
    data            = data_input[:]
    length          = len(data)
    for record in data:
        if(val_freq.has_key(record[target_attr])):
            val_freq[record[target_attr]] += 1.0
        else:
            val_freq[record[target_attr]] = 1.0

    # Calculate the entropy
    for freq in val_freq.values():
        data_entropy += (-freq/length) * math.log(freq/length, 2)

    return data_entropy

def information_gain(data_input, attr, target_attr):
    """ Calculate the information gain, to determine next target attribute """
    val_freq        = {}
    subset_entropy  = 0.0
    data            = data_input[:]
    length          = len(data)

    for record in data:
        if(val_freq.has_key(record[attr])):
            val_freq[record[attr]] += 1.0
        else:
            val_freq[record[attr]] = 1.0

    # Calculate the sum of the entropy for each subset of records weighted by
    # their probability of occurring in the training set
    for val in val_freq.keys():
        val_prob        = val_freq[val] / sum(val_freq.values())
        data_subset     = [record for record in data if record[attr] == val]
        subset_entropy += val_prob * entropy(data_subset, target_attr)

    return( entropy(data, target_attr) - subset_entropy )

def gain_ratio(data_input, attr, target_attr):
    """ Calculate the gain ratio, to determine next target attribute """
    val_freq        = {}
    splitinfo       = 0.0
    data            = data_input[:]
    length          = len(data)

    for record in data:
        if(val_freq.has_key(record[attr])):
            val_freq[record[attr]] += 1.0
        else:
            val_freq[record[attr]] = 1.0

    # Calculate the sum of the entropy for each subset of records weighted by
    # their probability of occurring in the training set
    for val in val_freq.keys():
        val_prob        = val_freq[val] / sum(val_freq.values())
        data_subset     = [record for record in data if record[attr] == val]
        splitinfo      += (-val_prob) * math.log(val_prob, 2)

    # IMPORTANT
    if splitinfo == 0.0:
        splitinfo = 1
    return(information_gain(data, attr, target_attr) / splitinfo)

def gini(data_input, attr, target_attr):
    """ Calculate the gini index """
    val_freq        = {}
    data            = data_input[:]
    length          = len(data)

    for record in data:
        if(val_freq.has_key(record[attr])):
            val_freq[record[attr]] += 1.0
        else:
            val_freq[record[attr]] = 1.0

    for val in val_freq.keys():
        pass

def choose_attribute(data_input, attributes, target_attr, fitness_func):
    """ Cycles through all the attributes and returns the attribute with the
    highest information gain """

    data = data_input[:]
    best_gain = 0.0
    best_attr = None

    for attr in attributes:
        if attr != target_attr:
            gain = fitness_func(data, attr, target_attr)
            if gain > best_gain:
                best_gain = gain
                best_attr = attr

    # print best_attr
    return best_attr

def get_subset( data_input, best, val):
    """ Returns a list of all the records in data with the value of attribute
    matching the given value """

    data = data_input[:]
    list = []

    if not data:
        return list
    else:
        for record in data:
            if record[best] == val:
                list.append(record)
        return list

def create_decision_tree(data_input, attributes, target_attr, fitness_func):
    """ Returns a new decision tree """
    data    = data_input[:]
    vals    = [record[target_attr] for record in data]
    default = majority_value(data, target_attr)

    # If the dataset or attributes is empty, return the default value. Subtract
    # 1 to account for target attributes
    if not data or (len(attributes) - 1) <= 0:
        return default
    # If all the records in dataset have the same values, return it
    elif vals.count(vals[0]) == len(vals):
        return vals[0]
    else:
        # Choose the next best attribute
        best_attr = choose_attribute(data, attributes, target_attr, fitness_func)
        # Create a new tree/node with the best attribute
        tree = {best_attr:{}}

        # Preprocess data, to generate a list containing the same data as data list
        # but without duplicate

        unique_data = []
        for record in data:
            if unique_data != None and best_attr != None: # and unique_data.count(record[best_attr]) != None:
                if unique_data.count(record[best_attr]) <= 0:
                    unique_data.append(record[best_attr])

        # Create a new decision tree for each of the values in the best
        # attribute field
        for val in unique_data:
            # Create a subtree for the current value under the best field
            subtree = create_decision_tree(
                    get_subset(data, best_attr, val),
                    [attr for attr in attributes if attr != best_attr],
                    target_attr,
                    fitness_func)

            # Add the new subtree to the empty dictionary
            tree[best_attr][val] = subtree

    return tree

def print_tree(tree, string):
    """ This function recursively crawls through the d-tree and print out """


    if type(tree) == dict:
        print "%s%s" % (string, tree.keys()[0])
        for item in tree.values()[0].keys():
            print "%s\t%s" % (string, item)
            print_tree(tree.values()[0][item], string + "\t")
    else:
        print "%s\t->\t%s" % (string, tree)

def getVal(tree, string):

    if type(tree) == dict:
        # print "%s%s" % (string, tree.keys()[0])
        for item in tree.values()[0].keys():
            # print "%s\t%s" % (string, item)
            cl = print_tree(tree.values()[0][item], string + "\t")
    else:
        return tree
        # print "%s\t->\t%s" % (string, tree)

    return cl


if __name__ == "__main__":
    #tree = create_decision_tree( data_input_array, attributes_array, attributes_array[1], information_gain )
    # tree = create_decision_tree(data_input_array, attributes_array, attributes_array[1], gain_ratio )
    # tree = create_decision_tree(data_input_array, attributes_array, attributes_array[0], gain_ratio )
    tree = create_decision_tree(data_input_array, attributes_array, attributes_array[0], information_gain )

    print "---------------------------------------------------------------------------"

    # print tree
    # finalData = convertToProperJSON(tree, {})
    # print finalData
    # saveJSONtoFile('flare.json', tree)

    print print_tree(tree, "")

    # attributes_array = ["X1", "X2", "X3", "X4", "X5"]
    # prediction = 0
    # prev = 0

    # get key
    # get 

    total = 0
    correct = 0
    for test in testingSet:
        total += 1
        print test
        t = tree.copy()
        prediction = ''
        while type(t) == dict:
            if len(t.keys()) > 1:
                # print t.keys()
                break
            key = t.keys()[0]
            print t.keys()[0]
            if key == None:
                break
            lookAt = attributes_array.index(key)

            if str(test[lookAt]) not in t[key]:
                prediction = str(test[lookAt])
                break
            t = t[key][str(test[lookAt])]

        if test[10] == prediction:
            correct += 1


    print "total %d" % total
    print "correct %d" % correct

    # for test in testingSet:
    #     # t = test.copy()
    #     while type(test) == dict:
    #         test = test.values()[0].keys()
    #         print test
    #     print test
    #     # print test[str(tree[1])]
    #     break
