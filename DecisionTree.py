#!/usr/bin/env python
import math, copy
from Tree import Tree
from DataGenerator import DataGenerator

class DecisionTree():
    def __init__(self):
        return

    def majority_value(self, data, target_attr):
        dic = {}
        max_item = ""
        for record in data:
            dic[record[target_attr]] = dic.get(record[target_attr], 0) + 1
        counts = [(j,i) for i,j in dic.items()]
        count, max_item = max(counts)
        del dic
        return max_item

    def entropy(self, data_input, target_attr):
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

    def information_gain(self, data_input, attr, target_attr):
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
            subset_entropy += val_prob * self.entropy(data_subset, target_attr)

        return(self.entropy(data, target_attr) - subset_entropy )

    def gain_ratio(self, data_input, attr, target_attr):
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

    def gini(self, data_input, attr, target_attr):
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

    def choose_attribute(self, data_input, attributes, target_attr, fitness_func):
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

        return best_attr

    def get_subset(self, data_input, best, val):
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

    def create_decision_tree(self, data_input, attributes, target_attr):
        """ Returns a new decision tree """

        fitness_func = self.information_gain # alternatively, use gain_ratio

        data    = data_input[:]
        vals    = [record[target_attr] for record in data]
        default = self.majority_value(data, target_attr)

        # If the dataset or attributes is empty, return the default value. Subtract
        # 1 to account for target attributes
        if not data or (len(attributes) - 1) <= 0:
            return default
        # If all the records in dataset have the same values, return it
        elif vals.count(vals[0]) == len(vals):
            return vals[0]
        else:
            # Choose the next best attribute
            best_attr = self.choose_attribute(data, attributes, target_attr, fitness_func)
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
                subtree = self.create_decision_tree(
                        self.get_subset(data, best_attr, val),
                        [attr for attr in attributes if attr != best_attr],
                        target_attr)

                # Add the new subtree to the empty dictionary
                tree[best_attr][val] = subtree

        return tree

    def print_tree(self, tree, string):
        """ This function recursively crawls through the d-tree and print out """


        if type(tree) == dict:
            print "%s%s" % (string, tree.keys()[0])
            for item in tree.values()[0].keys():
                print "%s\t%s" % (string, item)
                self.print_tree(tree.values()[0][item], string + "\t")
        else:
            print "%s\t->\t%s" % (string, tree)


    def train(self, testingSet):

        total = 0
        correct = 0

        for test in testingSet:
            total += 1
            t = tree.copy()
            prediction = ''
            while type(t) == dict:
                if len(t.keys()) > 1:
                    break
                key = t.keys()[0]
                if key == None:
                    break
                lookAt = attributes_array.index(key)

                if str(test[lookAt]) not in t[key]:
                    prediction = str(test[lookAt])
                    break
                t = t[key][str(test[lookAt])]

            if test[10] == prediction:
                correct += 1


        print "Total: %d, Correct: %d, Accuracy: %f%" % (total, correct, 100.0 * current / total)
