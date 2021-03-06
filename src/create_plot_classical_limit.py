#!/usr/bin/env python3

# import modules
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
from tools import getRootDirectory, getOutputFilename
import csv

import argparse
import pathlib

# parse CLI arguments
parser = argparse.ArgumentParser(description='Create a plot showing the classical limit.')
parser.add_argument('filename', type=pathlib.Path, help='Input filename')
parser.add_argument('-o', '--output', type=pathlib.Path, help='Output filename')
args = parser.parse_args()

# filesystem stuff
root_path = getRootDirectory()

full_path = (root_path / args.filename)
if not full_path.exists() or full_path.is_dir():
	exit(-1)

relative_path = full_path.relative_to(root_path / 'data')

print('\033[1m[Classical limit]\033[0m Computing file %s ... ' %relative_path, end='')

# read csv file
with full_path.open('r') as csvfile:
	reader = csv.reader(csvfile)
	hbars = []
	datas = []
	for i, row in enumerate(reader):
		if i == 0:
			header_min = [float(v) for v in row[1:]]
		elif i == 1:
			header_max = [float(v) for v in row[1:]]
		else:
			hbar = float(row[0])
			data = [int(v) for v in row[1:]]
			hbars.append(hbar)
			datas.append(data)

# plot
fig, ax = plt.subplots(figsize=(6,6))
cs = ax.imshow(datas, extent=[min(header_min), max(header_max), 2.0, 0.0], norm=LogNorm())

cbar = fig.colorbar(cs)
cbar.ax.minorticks_off()

x0, x1 = ax.get_xlim()
y0, y1 = ax.get_ylim()
ax.set_aspect(abs(x1-x0)/abs(y1-y0))

plt.xlabel('position')
plt.ylabel('$\\hbar$')


# filesystem stuff
out_filename = getOutputFilename(relative_path, 'classical', args.output)

# write to disk
plt.savefig(out_filename)
print('done')