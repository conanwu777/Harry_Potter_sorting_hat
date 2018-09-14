import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from numpy import genfromtxt
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

def normalize(arr, m, c):
	arr /= m
	arr -= c
	return arr

if len(sys.argv) != 2:
	print(ORANGE + "Usage: " + sys.argv[0] + " file.csv")
	exit(1)

sys.stdout.write(WHITE)
print "...Importing Data..."

if os.path.isfile(sys.argv[1]) == 0:
	print(RED + "404 File not found >.< Can't help you there...")
	sys.exit(1)
data = pd.read_csv(sys.argv[1])

print "...Cleaning Data..."

data = data.drop(['Index', 'Hogwarts House','First Name','Last Name','Birthday','Best Hand',
	'Arithmancy', 'Defense Against the Dark Arts', 'Care of Magical Creatures'], axis=1)

houses = ['Ravenclaw', 'Gryffindor', 'Slytherin', 'Hufflepuff']
attr = ['Astronomy','Herbology','Divination','Muggle Studies',
'Ancient Runes','History of Magic','Transfiguration','Potions','Charms','Flying']

Hogwarts = ["gold", "steelblue", "crimson", "mediumseagreen"]

if os.path.isfile('result') == 0:
	print(RED + "Opps, it seems that the hat is not TRAINED yet...cannot help you")
	sys.exit(1)

sys.stdout.write(YELLO)
print ".....*#$@$^*&^*!@&....^$%*@&....#$@(#*$....."

with open('result') as f:
	data = data.fillna(data.mean())
	m = dict()
	c = dict()
	for att in attr:
		m[att] = float(f.readline())
		c[att] = float(f.readline())
		data[att] = normalize(data[att], m[att], c[att])

	b = dict()
	for h in houses:
		b[h] = dict()
		b[h]['0'] = float(f.readline())
		for att in attr:
			b[h][att] = float(f.readline())
	f.close

new_col = []
tmp = dict()
for (i, row) in data.iterrows():
	t = houses[0]
	max = g(b[t], row)
	for h in houses:
		tmp[h] = g(b[h], row)
		if tmp[h] > max:
			max = tmp[h]
			t = h
	new_col.append(t)
data.insert(loc=0, column='Prediction', value=new_col)

sys.stdout.write(GREEN)
print "All sorted!"
print "Exporting..."
o = open("houses.csv", "w")
print >> o, "Index,Hogwarts House"
for (i, row) in data.iterrows():
	print >> o, "{0},{1}".format(i, row['Prediction'])
o.close

print "Making graph"

sns.set(style="ticks")
g = sns.PairGrid(data, hue='Prediction', palette=Hogwarts)
g = g.map_diag(plt.hist)
g = g.map_offdiag(plt.scatter, s=7)
g = g.add_legend()
g.savefig("check.png")
plt.show()
