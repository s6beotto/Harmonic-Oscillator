#!/usr/bin/env python3

# import modules
from matplotlib import pyplot as plt
from tools import getRootDirectory
import csv
import numpy as np

import argparse
import pathlib

# parse CLI arguments
parser = argparse.ArgumentParser(description='Plot the path of a particle at different metropolis states.')
parser.add_argument('filename', type=pathlib.Path, help="Input filename")
parser.add_argument('-i', "--iterations", nargs='+')
parser.add_argument('-o', '--output', type=pathlib.Path, help="Output filename")
args = parser.parse_args()

iterations_used = [int(i) for i in args.iterations]

# filesystem stuff
root_path = getRootDirectory()

full_path = (root_path / args.filename)
if not full_path.exists() or full_path.is_dir():
	exit(-1)

relative_path = full_path.relative_to(root_path / 'data')

print("[Track] Computing file %s ... " %relative_path, end='')

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
for iteration in iterations_used:
	iteration = int(iteration)
	# plot
	print(len(data[iteration - 1]), len(numbers))
	plt.errorbar(data[iteration - 1], numbers, label='path after %d iteration%s' %(iteration, 's' if iteration > 1 else ''))
	plt.xlabel('Position')
	plt.ylabel('Number')
plt.legend()

out_filename = root_path / 'imgs' / relative_path

out_filename = out_filename.with_suffix('')
out_filename = pathlib.Path('%s_track_%s.pdf' %(out_filename, '-'.join([str(i) for i in iterations_used])))
if args.output:
	out_filename = args.output
out_filename.parent.mkdir(parents=True, exist_ok=True)

# write to disk
plt.savefig(out_filename)
print('done')