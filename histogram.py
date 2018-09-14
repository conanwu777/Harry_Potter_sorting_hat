import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from numpy import genfromtxt
import sys
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

f = open("result", "w")
data = pd.read_csv(sys.argv[1])

print "...Cleaning Data..."

data = data.drop(['Index','First Name','Last Name','Birthday','Best Hand'], axis=1)
data = data.set_index('Hogwarts House')

houses = ('Ravenclaw', 'Gryffindor', 'Slytherin', 'Hufflepuff')
Hogwarts = ('steelblue', 'mediumseagreen', 'crimson', 'gold')
attr = ('Arithmancy','Astronomy','Herbology','Defense Against the Dark Arts',
'Divination','Muggle Studies','Ancient Runes','History of Magic',
'Transfiguration','Potions','Care of Magical Creatures','Charms','Flying')

for h in houses:
	data.loc[h] = data.loc[h].fillna(data.loc[h].mean())

def hist_attr(att, x, y):
	sns.distplot(data.loc['Ravenclaw'][att], color='steelblue', kde=False,
		label='Ravenclaw', ax=axes[x][y])
	sns.distplot(data.loc['Hufflepuff'][att],
		color='gold', kde=False, label='Hufflepuff', ax=axes[x][y])
	sns.distplot(data.loc['Gryffindor'][att],
		color='crimson', kde=False, label='Gryffindor', ax=axes[x][y])
	sns.distplot(data.loc['Slytherin'][att],
		color='mediumseagreen', kde=False, label='Slytherin', ax=axes[x][y])

sys.stdout.write(YELLO)
print "...Computing Graphs..."

f, axes = plt.subplots(3, 5, figsize=(20, 12))
i = 0
for att in attr:
	hist_attr(att, i / 5, i % 5)
	i += 1

sys.stdout.write(WHITE)
print "...Outputting..."

plt.tight_layout()
plt.legend()
f.savefig("histogram.png")

sys.stdout.write(GREEN)
print "DONE!!!"

plt.show()
