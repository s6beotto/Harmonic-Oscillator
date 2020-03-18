#!/usr/bin/env python3

# import modules
from matplotlib import pyplot as plt
from tools import getRootDirectory, getOutputFilename, countTransitions, running_mean
import csv
import numpy as np

import argparse
import pathlib

# parse CLI arguments
parser = argparse.ArgumentParser(description='Plot an interesting part of the path of a particle at different metropolis states.')
parser.add_argument('filename', type=pathlib.Path, help='Input filename')
parser.add_argument('-i', '--iterations', nargs='+', help='Metropolis iterations to use')
parser.add_argument('-ic', '--iteration_count', default=None, help='Metropolis iteration to use to measure the number of transitions')
parser.add_argument('-n', '--number', type=int, default=100, help='Number of time positions to show')
parser.add_argument('-o', '--output', type=pathlib.Path, help='Output filename')
args = parser.parse_args()

iterations_used = [int(i) for i in args.iterations]

# use the max iteration as a default to measure the number of transitions
if args.iteration_count == None:
	iteration_count  = max(iterations_used)
else:
	iteration_count = int(args.iteration_count)

# filesystem stuff
root_path = getRootDirectory()

full_path = (root_path / args.filename)
if not full_path.exists() or full_path.is_dir():
	exit(-1)

relative_path = full_path.relative_to(root_path / 'data')

print('\033[1m[Track Pretty]\033[0m Computing file %s ... ' %relative_path, end='')

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

# find the most interesting area, i.e. the section with the most transitions
num_time_lattice_positions = len(data[list(data.keys())[0]])

time_lattice_positions_to_use = args.number

if time_lattice_positions_to_use > num_time_lattice_positions:
	print('\nError: Maximum number of time lattice positions is %d' %num_time_lattice_positions)
	exit(-1)

min_time_position = max_time_position = 0

number_of_transitions = {}

while max_time_position < num_time_lattice_positions:
	max_time_position += time_lattice_positions_to_use
	# count the transitions of the running mean of the track data
	number_of_transitions[(min_time_position, max_time_position)] = countTransitions(running_mean(data[iteration_count - 1][min_time_position:max_time_position], 10))
	min_time_position = max_time_position
print(number_of_transitions)
min_time_position, max_time_position = max(number_of_transitions, key=number_of_transitions.get)
print(min_time_position, max_time_position)

plt.figure()
for iteration in iterations_used:
	iteration = int(iteration)
	# plot
	plt.errorbar(data[iteration - 1][min_time_position:max_time_position], numbers[min_time_position:max_time_position], label='path after %d iteration%s' %(iteration, 's' if iteration > 1 else ''))
	plt.xlabel('Position')
	plt.ylabel('Number')
	plt.title('time slice %d:%d' %(min_time_position, max_time_position))
plt.legend()


# filesystem stuff
out_filename = getOutputFilename(relative_path, 'track_pretty_%s' %('-'.join([str(i) for i in iterations_used])), args.output)

# write to disk
plt.savefig(out_filename)
print('done')