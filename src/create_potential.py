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

print('\033[1m[Potential]\033[0m Computing ... ', end='')

xvalues = np.arange(-2.5 - d / 2, 2.5 + d / 2, 0.01)
if args.anharmonic:
	lambda_ = distanceToParameter(d)
else:
	lambda_ = 0
p = Potential(mu, lambda_)
yvalues = p(xvalues)
plt.figure()
plt.plot(xvalues, yvalues, label='Potential energy')
plt.xlabel('Distance')
plt.ylabel('Potential energy')
plt.plot(xvalues, np.zeros_like(xvalues), color='black', linewidth=0.5)
plt.xlim(min(xvalues), max(xvalues))

plt.legend()

out_filename = root_path / ('imgs/potential/%s_%s.pdf' %('harm' if args.harmonic else 'anharm', ("%0.1f" % d).replace('.', '_')))

if args.output:
	out_filename = args.output
out_filename.parent.mkdir(parents=True, exist_ok=True)

plt.savefig(out_filename)
print('done')