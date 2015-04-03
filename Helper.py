#!/usr/bin/env python
import json

def ouputToCSV(filename, data):
	f = open(filename, 'w')
	for item in data:
		f.write(','.join([str(x) for x in item]) + '\n')
	f.close


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


def convertDataToDecisionTreeFormat(data, classNumber):
    dimensions = len(data[0]) - 1
    # format {"class":"className", "X1":1, "X2"}
    result = []
    for d in data:
        c = {"name":str(d[classNumber])}
        for x in range(dimensions):
            c["X" + str(x + 1)] = str(d[x])
        result.append(c)

    return result
