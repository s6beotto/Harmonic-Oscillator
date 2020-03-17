#!/usr/bin/env python3

# import modules
from matplotlib import pyplot as plt
from tools import getRootDirectory, getColorIterator, getOutputFilename
import csv
import numpy as np
import statsmodels.api as sm
import argparse
import pathlib

color_iterator = getColorIterator()

# parse CLI arguments
parser = argparse.ArgumentParser(description='Check distribution via a qq plot.')
parser.add_argument('filename', type=pathlib.Path, help="Input filename")
parser.add_argument('-i', "--iteration", type=int)
parser.add_argument('-o', '--output', type=pathlib.Path, help="Output filename")
args = parser.parse_args()

iteration = args.iteration

# filesystem stuff
root_path = getRootDirectory()

full_path = (root_path / args.filename)
if not full_path.exists() or full_path.is_dir():
	exit(-1)

relative_path = full_path.relative_to(root_path / 'data')

print('[QQ] Computing file %s ... ' %relative_path, end='')

data = {}

# read csv file
with full_path.open('r') as csvfile:
	reader = csv.reader(csvfile)
	for i, row in enumerate(reader):
		if i == 0:
			numbers = np.array([int(r) for r in row[1:]])
			pass
		else:
			num = int(row[0])
			positions = np.array([float(r) for r in row[1:]])
			data[num] = positions

plt.figure()

d = data[iteration - 1]

# create qq plot
sm.qqplot(d, dist='norm', label='qq plot after %d iteration%s' %(iteration, 's' if iteration > 1 else ''))

plt.legend()

# filesystem stuff
out_filename = getOutputFilename(relative_path, 'qq_%d' %iteration, args.output)

# write to disk
plt.savefig(out_filename)
print('done')