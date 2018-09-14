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

if len(sys.argv) != 2:
	print(ORANGE + "Usage: " + sys.argv[0] + " file.csv")
	exit(1)

sys.stdout.write(WHITE)
print "...Importing Data..."

if os.path.isfile(sys.argv[1]) == 0:
	print(RED + "404 File not found >.< Can't help you there...")
	sys.exit(1)
data = pd.read_csv(sys.argv[1])
data = data.drop(['Index'], axis=1)
f = open(sys.argv[1], 'rb')

print "...Cleaning Data..."

reader = csv.reader(f)
header = next(reader)
header = header[6:]
for i in range(0, len(header)):
	data = data[pd.notnull(data[header[i]])]

sys.stdout.write(YELLO)
print "...Computing Graphs..."

Hogwarts = ["steelblue", "mediumseagreen", "crimson", "gold"]
sns.set(style="ticks")
g = sns.PairGrid(data, hue="Hogwarts House", palette=Hogwarts)
g = g.map_diag(plt.hist)
g = g.map_offdiag(plt.scatter, s=3)
g = g.add_legend()

sys.stdout.write(WHITE)
print "...Outputting..."

g.savefig("pairplot.png")

sys.stdout.write(GREEN)
print "DONE!!!Output saved as pairplot.png"
