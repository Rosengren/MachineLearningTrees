import random

def buckets(filename, bucketName, separator, classColumn):
	"""the original data is in the file named filename
	buckeName: the prefix for all the bucket names
	separator: the character that divides the columns
						(for example, tab or comma)
	classColumn: the column that indicates the calss"""

	# put the data in 10 buckets
	numberOfBuckets = 10

	data = {}
	# read in the data and divide by category
	with open(filename) as f:
		lines = f.readlines()
	for line in lines:

		# get the category
		category = line.split(',')[classColumn]
		data.setdefault(category, [])
		data[category].append(line)

	# initialize the buckets
	buckets = []
	for i in range(numberOfBuckets):
		buckets.append([])

	# for each category put the data into the buckets
	for k in data.keys():
		# randomize order of instances for each class
		random.shuffle(data[k])
		bNum = 0
		# divide into buckets
		for item in data[k]:
			buckets[bNum].append(item)
			bNum = (bNum + 1) % numberOfBuckets

	# write to file
	for bNum in range(numberOfBuckets):
		f = open("%s-%02i.csv" % (bucketName, bNum + 1), 'w')
		for item in buckets[bNum]:
			f.write(item)
		f.close()


# Run buckets function
# buckets("iris.csv", 'iris', ',', 4)
# buckets("heartDisease.csv", 'heartDisease', ',', 13)
# buckets("testData.csv", 'testData', ',', 10)
