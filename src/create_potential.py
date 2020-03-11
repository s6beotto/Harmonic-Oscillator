from matplotlib import pyplot as plt
from tools import Potential, distanceToParameter, getRootDirectory
import numpy as np
import argparse
import pathlib

# parse CLI arguments
parser = argparse.ArgumentParser(description='Calculate the autorelation function between the metropolis samples.')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-H', '--harmonic', action='store_true', help='Use the harmonic potential')
group.add_argument('-a', '--anharmonic', action='store_true', help='Use the anharmonic potential')
parser.add_argument('-d', '--distance', type=float, default=1)
parser.add_argument('-o', '--output', type=pathlib.Path, help='Output filename')
args = parser.parse_args()

root_path = getRootDirectory()

mu = 10 if args.harmonic else -1
d = 0 if args.harmonic else args.distance


xvalues = np.arange(-5-d / 2, 5+d / 2, 0.01)
if args.anharmonic:
	lambda_ = distanceToParameter(d)
else:
	lambda_ = 0
p = Potential(mu, lambda_)
yvalues = p(xvalues)
plt.figure()
plt.errorbar(xvalues, yvalues)
plt.xlabel('Distance')
plt.ylabel('Potential energy')

out_filename = root_path / ('imgs/potential/%s_%f.pdf' %('harm' if args.harmonic else 'anharm', d))
out_filename.parent.mkdir(parents=True, exist_ok=True)

if args.output:
	out_filename = args.output
out_filename.parent.mkdir(parents=True, exist_ok=True)

plt.savefig(out_filename)