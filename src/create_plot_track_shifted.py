#!/usr/bin/env python3

# import modules
from matplotlib import pyplot as plt
from tools import getRootDirectory, getOutputFilename
import csv
import numpy as np

import argparse
import pathlib

# parse CLI arguments
parser = argparse.ArgumentParser(description='Plot the path of a particle at different metropolis states shifted.')
parser.add_argument('filename', type=pathlib.Path, help='Input filename')
parser.add_argument('-i', '--iterations', nargs='+')
parser.add_argument('-o', '--output', type=pathlib.Path, help='Output filename')
args = parser.parse_args()

iterations_used = [int(i) for i in args.iterations]

# filesystem stuff
root_path = getRootDirectory()

full_path = (root_path / args.filename)
if not full_path.exists() or full_path.is_dir():
	exit(-1)

relative_path = full_path.relative_to(root_path / 'data')

print('\033[1m[Track shifted]\033[0m Computing file %s ... ' %relative_path, end='')

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
for num, iteration in enumerate(iterations_used):
	iteration = int(iteration)
	# plot
	plt.errorbar(numbers, data[iteration - 1] - num, label='after %d iteration%s' %(iteration, 's' if iteration > 1 else ''))
	plt.xlabel('Number')
	plt.ylabel('Position $- n$')
plt.legend()


# filesystem stuff
out_filename = getOutputFilename(relative_path, 'track_shifted_%s' %('-'.join([str(i) for i in iterations_used])), args.output)

# write to disk
plt.savefig(out_filename)
print('done')