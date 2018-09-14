import pandas as pd
import numpy as np
from numpy import genfromtxt
import math
import sys
import csv
import os.path

RED = '\033[1;38;2;225;20;20m'
WHITE = '\033[1;38;2;255;251;214m'
YELLO = '\033[1;38;2;255;200;0m'
ORANGE = '\033[1;38;2;255;120;10m'
GREEN = '\033[1;38;2;0;175;117m'

def g(b, row):
	output = b['0']
	for att in attr:
		output += b[att] * row[att]
	return 1 / (1 + 2.71828**(-output))

def min(arr):
	m = float('inf')
	for i in range(len(arr)):
		if arr[i] < m:
			m = arr[i]
	return m

def max(arr):
	m = float('-inf')
	for i in range(len(arr)):
		if arr[i] > m:
			m = arr[i]
	return m

def normalize(arr):
	mul = (arr.max() - arr.min()) / 2
	arr /= mul
	shift = arr.min() + 1
	arr -= shift
	return (arr, mul, shift)

def check_house(house, row):
	if (row.name == house):
		return 1
	else:
		return 0

if len(sys.argv) != 2:
	print(ORANGE + "Usage: " + sys.argv[0] + " file.csv")
	exit(1)

sys.stdout.write(WHITE)
print "...Importing Data..."

if os.path.isfile(sys.argv[1]) == 0:
	print(RED + "404 File not found >.< Can't help you there...")
	sys.exit(1)
data = pd.read_csv(sys.argv[1])

f = open("result", "w")

print "...Cleaning Data..."

data = data.drop(['First Name','Last Name','Birthday','Best Hand',
	'Arithmancy', 'Defense Against the Dark Arts', 'Care of Magical Creatures'], axis=1)
data = data.set_index('Hogwarts House')

houses = ['Ravenclaw', 'Gryffindor', 'Slytherin', 'Hufflepuff']
attr = ['Astronomy','Herbology','Divination','Muggle Studies',
'Ancient Runes','History of Magic','Transfiguration','Potions','Charms','Flying']

b = dict()
for h in houses:
	data.loc[h] = data.loc[h].fillna(data.loc[h].mean())
	b[h] = dict()
	b[h]['0'] = 0.0
	for att in attr:
		b[h][att] = 0.0

m = dict()
c = dict()
for att in attr:
	data[att], m[att], c[att] = normalize(data[att])
	print >> f, m[att]
	print >> f, c[att]

lr = 0.5
numIter = 10

sys.stdout.write(YELLO)
print "Iterations: {0} | Learning Rate: {1} | Data Size: {2}".format(numIter, lr, len(data))
sys.stdout.write(WHITE)
print "...Traning..."
sys.stdout.write(YELLO)

partial = dict()
for h in houses:
	partial[h] = dict()


for n in range(numIter):
	cost = dict()
	for h in houses:
		cost[h] = 0
		for (i, row) in data.iterrows():
			y = check_house(h, row)
			p = g(b[h], row)
			partial[h]['0'] = (y - p)
			for att in attr:
				partial[h][att] = row[att] * (y - p)
			b[h]['0'] += lr * partial[h]['0'] / len(data)
			for att in attr:
				b[h][att] += lr * partial[h][att] / len(data)
			cost[h] += y * math.log(p) + (1 - y) * math.log(1 - p)
		cost[h] /= -len(data)
		print "{0}: current cost value {1}".format(h, cost[h])
	sys.stdout.write(WHITE)
	print "Iteration {0} complete".format(n)
	print YELLO

count = 0
tmp = dict()
for (i, row) in data.iterrows():
	t = houses[0]
	max = g(b[t], row)
	for h in houses:
		tmp[h] = g(b[h], row)
		if tmp[h] > max:
			max = tmp[h]
			t = h
	if row.name == t:
		count += 1
conf = float(count * 100 / len(data))

sys.stdout.write(GREEN)
print "Training Complete! Confidence: {0}%".format(conf)
print "Exporting Results"

for h in houses:
	print >> f, b[h]['0']
	for att in attr:
		print >> f, b[h][att]

f.close()
print "Done!"
