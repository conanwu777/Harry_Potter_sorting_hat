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
sns.set()
Hogwarts = ["steelblue", "mediumseagreen", "crimson", "gold"]

sys.stdout.write(YELLO)
print "...Computing Graphs..."

fig, ax = plt.subplots(figsize=(12, 12))
ax = sns.scatterplot(x="Astronomy", y="Defense Against the Dark Arts",
	hue="Hogwarts House", palette=Hogwarts, data=data)

plt.tight_layout()
plt.legend()

sys.stdout.write(WHITE)
print "...Outputting..."

fig.savefig("scatter.png")

sys.stdout.write(GREEN)
print "DONE!!!"

plt.show()
