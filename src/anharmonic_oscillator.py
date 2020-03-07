from tools import Potential, Energy, deltaEnergy, Kinetic, Metropolis, getRootDirectory, distanceToParameter
import numpy as np
import csv
from configparser import ConfigParser
import argparse
import pathlib

parser = argparse.ArgumentParser(description='Create samples for the harmonic oscillator')
parser.add_argument("-i", "--iterations", type=int, default=100,
                    help="Number of Metropolis iterations")
parser.add_argument("-N", "--number", type=int, default=100,
                    help="Number of lattice sites")
parser.add_argument("-m", "--mass", type=float, default=0.01,
                    help="Mass of the particle")
parser.add_argument("-u", "--mu", type=float, default=10,
                    help="Depth of the potential")
parser.add_argument("-t", "--tau", type=float, default=0.1,
                    help="Time step size")
parser.add_argument("-hb", "--hbar", type=float, default=1,
                    help="Value of the reduces Plancks constant")
parser.add_argument("-init", "--initial", type=float, default=0,
                    help="Initial values for the path")
parser.add_argument("-ir", "--initial-random", type=float, default=0,
                    help="Use random distribution around initial value")
parser.add_argument("-d", "--distance", type=float, default=10,
                    help="Distance of the minima")
parser.add_argument('-o', '--output', type=pathlib.Path,
					help="Output filename")
args = parser.parse_args()


# parameters
iterations = args.iterations
N = args.number
mass = args.mass
mu = args.mu
tau = args.tau
hbar = args.hbar
initial = args.initial
initial_random = args.initial_random
distance = args.distance
lambda_ = distanceToParameter(distance)
output = args.output

parameters = [
			'iterations', 'N', 'mass', 'mu', 'tau', 'hbar', 'initial', 'initial_random',
            'distance', 'lambda_',
			]

p = Potential(-mu, lambda_)

de = deltaEnergy(p, mass, tau)

m = Metropolis(de, init=initial, valWidth=1, initValWidth=initial_random, hbar=hbar, tau=tau, N=N)

root_path = getRootDirectory()
dir_ = root_path / 'data' / 'anharmonic_oscillator_track'
dir_.mkdir(parents=True, exist_ok=True)

file_ = dir_ / ('N%di%dinit%sm%0.4fl%0.4fd%0.4f.csv' % (N, iterations, 'rand' if initial == None else str(initial), mass, lambda_, distance))

if output != None:
	file_ = output

config_filename = file_.with_suffix('.cfg')
config = ConfigParser()
config['DEFAULT'] = {p: eval(p) for p in parameters}
config['DEFAULT']['type'] = 'anharmonic_oscillator'

accept_ratios = []
with file_.open('w', newline='') as file:
	writer = csv.writer(file)
	writer.writerow(['num'] + [str(i) for i in range(N)])
	for iteration in range(iterations):
		data, accept_ratio = next(m)
		accept_ratios.append(accept_ratio)
		writer.writerow([iteration] + list(data))
accept_ratio = np.mean(accept_ratios)

config['DEFAULT']['accept_ratio'] = str(accept_ratio)

with open(config_filename, 'w') as configfile:
	config.write(configfile)