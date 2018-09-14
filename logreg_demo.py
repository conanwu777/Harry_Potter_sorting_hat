import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from numpy import genfromtxt
import sys
import csv
import os.path

def g(x):
	return 1 / (1 + 2.71828**(-x))

def output(b0, b1, b2, xh, xa, i):
	res = float(b0 + b1 * xa[i] + b2 * xh[i])
	return res

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
	mul = max(arr) - min(arr)
	arr /= mul
	shift = min(arr)
	arr -= shift
	return (arr, mul, shift)


if len(sys.argv) != 2:
	print(ORANGE + "Usage: " + sys.argv[0] + " file.csv")
	exit(1)

if os.path.isfile(sys.argv[1]) == 0:
	print(RED + "404 File not found >.< Can't help you there...")
	sys.exit(1)

data = pd.read_csv(sys.argv[1])
data = data.drop(['Index'], axis=1)


house, xh, xa = [], [], []
for i in range(len(data)):
	if np.isnan(data.Herbology[i]) == 0 and np.isnan(data.Astronomy[i]) == 0:
		xa.append(data.Astronomy[i])
		xh.append(data.Herbology[i])
		house.append(data['Hogwarts House'][i])

xa, xa_m, xa_c = normalize(xa)
xh, xh_m, xh_c = normalize(xh)

lr = 0.1
numIter = 200

sl, gr, hu, ra = [0,0,0], [0,0,0], [0,0,0], [0,0,0]
for n in range(numIter):
	for i in range(len(xh)):
		ys = 1.0 if house[i] == 'Slytherin' else 0.0
		yg = 1.0 if house[i] == 'Gryffindor' else 0.0
		yh = 1.0 if house[i] == 'Hufflepuff' else 0.0
		yr = 1.0 if house[i] == 'Ravenclaw' else 0.0
		p = g(output(sl[0], sl[1], sl[2], xh, xa, i))
		sl[0] = sl[0] + lr * (ys - p) * p * (1 - p)
		sl[1] = sl[1] + lr * (ys - p) * p * (1 - p) * xa[i]
		sl[2] = sl[2] + lr * (ys - p) * p * (1 - p) * xh[i]
		p = g(output(gr[0], gr[1], gr[2], xh, xa, i))
		gr[0] = gr[0] + lr * (yg - p) * p * (1 - p)
		gr[1] = gr[1] + lr * (yg - p) * p * (1 - p) * xa[i]
		gr[2] = gr[2] + lr * (yg - p) * p * (1 - p) * xh[i]
		p = g(output(hu[0], hu[1], hu[2], xh, xa, i))
		hu[0] = hu[0] + lr * (yh - p) * p * (1 - p)
		hu[1] = hu[1] + lr * (yh - p) * p * (1 - p) * xa[i]
		hu[2] = hu[2] + lr * (yh - p) * p * (1 - p) * xh[i]
		p = g(output(ra[0], ra[1], ra[2], xh, xa, i))
		ra[0] = ra[0] + lr * (yr - p) * p * (1 - p)
		ra[1] = ra[1] + lr * (yr - p) * p * (1 - p) * xa[i]
		ra[2] = ra[2] + lr * (yr - p) * p * (1 - p) * xh[i]


lsl = [sl[0] - sl[1] * xa_c - sl[2] * xh_c - 0.5, sl[1] / xa_m, sl[2] / xh_m]
Slytherin_line = [-(lsl[1] * x + lsl[0]) / lsl[2] for x in data.Astronomy]
lgr = [gr[0] - gr[1] * xa_c - gr[2] * xh_c - 0.5, gr[1] / xa_m, gr[2] / xh_m]
Gryffindor_line = [-(lgr[1] * x + lgr[0]) / lgr[2] for x in data.Astronomy]
lhu = [hu[0] - hu[1] * xa_c - hu[2] * xh_c - 0.5, hu[1] / xa_m, hu[2] / xh_m]
Hufflepuff_line = [-(lhu[1] * x + lhu[0]) / lhu[2] for x in data.Astronomy]
lra = [ra[0] - ra[1] * xa_c - ra[2] * xh_c - 0.5, ra[1] / xa_m, ra[2] / xh_m]
Ravenclaw_line = [-(lra[1] * x + lra[0]) / lra[2] for x in data.Astronomy]

sns.set()
Hogwarts = ["steelblue", "mediumseagreen", "crimson", "gold"]
fig, ax = plt.subplots(figsize=(12, 12))
ax = sns.scatterplot(x="Astronomy", y="Herbology",
	hue="Hogwarts House", palette=Hogwarts, data=data, s=50, alpha=0.8)
plt.plot(data.Astronomy, Slytherin_line, color="mediumseagreen")
plt.plot(data.Astronomy, Gryffindor_line, color="crimson")
plt.plot(data.Astronomy, Hufflepuff_line, color="gold")
plt.plot(data.Astronomy, Ravenclaw_line, color="steelblue")

plt.tight_layout()
plt.legend()
plt.show()
