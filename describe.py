import csv
import sys
import os.path
import numpy
from numpy import genfromtxt
import matplotlib.pyplot as plt

RED = '\033[1;38;2;225;20;20m'
WHITE = '\033[1;38;2;255;251;214m'
YELLO = '\033[1;38;2;255;200;0m'
ORANGE = '\033[1;38;2;255;120;10m'
GREEN = '\033[1;38;2;0;175;117m'

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def count(data, res):
	count = []
	for col in range(0, len(data[1])):
		c = 0
		for i in range(1, len(data)):
			if numpy.isnan(data[i][col]) == 0:
				c += 1
		count.append(c);
	res["Count"] = count

def mean(data, res):
	mean = []
	for col in range(0, len(data[1])):
		if res["Count"][col] == 0:
			mean.append(float('nan'));
		else:
			sum = 0
			for i in range(1, len(data)):
				if numpy.isnan(data[i][col]) == 0:
					sum += data[i][col]
			mean.append(sum / res["Count"][col]);
	res["Mean"] = mean

def std(data, res):
	std = []
	for col in range(0, len(data[1])):
		if res["Count"][col] == 0:
			std.append(float('nan'));
		else:
			sum = 0
			for i in range(1, len(data)):
				if numpy.isnan(data[i][col]) == 0:
					sum += (data[i][col] - res["Mean"][col])**2
			std.append((sum / res["Count"][col])**0.5)
	res["Std"] = std

def min(data, res):
	min = []
	for col in range(0, len(data[1])):
		if res["Count"][col] == 0:
			min.append(float('nan'));
		else:
			m = float('inf')
			for i in range(1, len(data)):
				if numpy.isnan(data[i][col]) == 0 and data[i][col] < m:
					m = data[i][col]
			min.append(m)
	res["Min"] = min

def max(data, res):
	max = []
	for col in range(0, len(data[1])):
		if res["Count"][col] == 0:
			max.append(float('nan'));
		else:
			m = float('-inf')
			for i in range(1, len(data)):
				if numpy.isnan(data[i][col]) == 0 and data[i][col] > m:
					m = data[i][col]
			max.append(m)
	res["Max"] = max

def median(arr):
	sort = sorted(arr)
	if len(sort) % 2:
		return sort[len(sort) / 2]
	else:
		return (sort[len(sort) / 2 - 1] + sort[len(sort) / 2]) / 2

def get_num_arr(col, data):
	arr = []
	for i in range(0, len(data)):
		if numpy.isnan(data[i][col]) == 0:
			arr.append(data[i][col])
	return arr

def p50(data, res):
	med = []
	for col in range(0, len(data[1])):
		if res["Count"][col] == 0:
			med.append(float('nan'));
		else:
			med.append(median(get_num_arr(col, data)))
	res["50%"] = med

def p25(data, res):
	q1 = []
	for col in range(0, len(data[1])):
		if res["Count"][col] == 0:
			q1.append(float('nan'));
		else:
			arr = get_num_arr(col, data)
			arr = sorted(arr)
			arr = arr[0 : len(arr) / 2]
			q1.append(median(arr))
	res["25%"] = q1

def p75(data, res):
	q3 = []
	for col in range(0, len(data[1])):
		if res["Count"][col] == 0:
			q3.append(float('nan'));
		else:
			arr = get_num_arr(col, data)
			arr = sorted(arr)
			if len(arr) % 2:
				arr = arr[len(arr) / 2 + 1 : len(arr)]
			else:
				arr = arr[len(arr) / 2 : len(arr)]
			q3.append(median(arr))
	res["75%"] = q3

def print_line(res, x):
	print("%s%-5s%s" % (WHITE, x, YELLO)),
	for i in range(0, len(res[x])):
		if res["Count"][i] > len(data) / 10:
			print("%16.3f" % res[x][i]),
	print("")


if len(sys.argv) != 2:
	print(ORANGE + "Usage: " + sys.argv[0] + " file.csv")
	exit(1)

if os.path.isfile(sys.argv[1]) == 0:
	print(RED + "404 File not found >.< Can't help you there...")
	sys.exit(1)

f = open(sys.argv[1], 'rb')
reader = csv.reader(f)
header = next(reader)
res = dict()
data = genfromtxt(sys.argv[1], delimiter=',')
count(data, res)
mean(data, res)
std(data, res)
min(data, res)
p25(data, res)
p50(data, res)
p75(data, res)
max(data, res)

print("%s%-5s" % (WHITE, "")),
for i in range(0, len(data[0])):
	if res["Count"][i] > len(data) / 10:
		print("%16.14s" % header[i]),
print("")
print_line(res, "Count")
print_line(res, "Mean")
print_line(res, "Std")
print_line(res, "Min")
print_line(res, "25%")
print_line(res, "50%")
print_line(res, "75%")
print_line(res, "Max")
