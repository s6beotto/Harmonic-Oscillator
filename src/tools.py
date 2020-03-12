import numpy as np
from pathlib import Path
import os
from cycler import cycler

import ctypes
from ctypes import cdll

def getRootDirectory():
	return Path(os.path.dirname(os.path.realpath(__file__))).parent

libmetropolis = cdll.LoadLibrary(getRootDirectory() / 'src' / 'libmetropolis.so')
libmetropolis.metropolis.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)
libmetropolis.metropolis.restype = ctypes.POINTER(ctypes.c_double)

libmetropolis.get_accept_ratio.argtypes = ()
libmetropolis.get_accept_ratio.restype = ctypes.c_double

def getMinima(lambda_):
	# mimina at +/- sqrt(-a/(2b))
	return np.sqrt(-1 / (2 * lambda_))

def distanceToParameter(distance):
	# calculate lambda parameter from distance
	return -1/2 * (distance / 2)**-2

def autoCorrelation(data, xdata):
	mean = np.mean(data)
	d = np.concatenate((data, data))
	l = len(data)
	return [1 / (l - i) * np.mean((data - mean) * (d[i:i + l] - mean)) for i in list(xdata)]

def autoCorrelationNormalized(data, xdata):
	correlation = autoCorrelation(data, xdata)
	return correlation / correlation[0]

def getIntegratedCorrelationTime(data, factor = 5):
	tint = data[0]
	num = 0
	while num < factor * tint and not num >= len(data):
		num += 1
		tint += data[num]

	return tint / 2

colors_raw = ['1f77b4', 'ff7f0e', '2ca02c', 'd62728', '9467bd', '8c564b', 'e377c2', '7f7f7f', 'bcbd22', '17becf']

def getColorIterator():
	def make_lighter(color):
		r, g, b = (int(color[i:i+2], base=16) for i in [0, 2, 4])
		r, g, b = (r + 255) // 2, (g + 255) // 2, (b + 255) // 2
		return '#%02X%02X%02X' %(r, g, b)

	colors = [('#'+color, make_lighter(color)) for color in colors_raw]
	return iter(cycler('color', colors))

def bootstrap(num, values, func=np.mean):
	# bootstrap function
	return [func(np.random.choice(values, size = len(values))) for n in range(num)]

def meanSquare(values):
	return np.mean(values * values)

def countTransitions(values):
	return sum(values[1:] / values[:-1] < 0)

def Potential(mu, lambda_):
	# Potential Energy with parameters
	def wrapper(x, mu=mu, lambda_=lambda_):
		return mu * (x ** 2 + lambda_ * x ** 4)
	return wrapper

def Kinetic(m, tau):
	# Kinetic Energy with parameters
	def wrapper(x_i, x_j, m=m, tau=tau):
		return m / 2 * (x_i - x_j) ** 2 / tau ** 2
	return wrapper

def Energy(kinetic, potential):
	# Energy function with parameters
	def wrapper(x, kinetic=kinetic, potential=potential):
		return sum([kinetic(x[i], x[i+1]) for i in range(len(x)-1)]) + sum([potential(xx) for xx in x])
	return wrapper

def deltaEnergy(potential, m, tau):
	def wrapper(x, x_old, x_new, index, m=m, tau=tau, potential=potential):
		return potential(x_new) - potential(x_old) + m / tau ** 2 * (x_new ** 2 - x_old ** 2 - (x[index - 1] + x[(index + 1) % len(x)]) * (x_new - x_old))
	return wrapper

class MetropolisPython:
	# Metropolis algorithm
	def __init__(self, init=0, initValWidth=1, valWidth=1, periodic=True, N=100, hbar=1, tau=0.1, m=1.0, lambda_=0, mu = 1.0):
		if type(init) in [float, int, np.float64]:
			self.values = np.random.normal(size=N, loc=init, scale=initValWidth)
		else:
			self.values = np.array(init)
			N = len(self.values)
		if periodic:
			self.values[-1] = self.values[0]

		self.potential = Potential(mu, lambda_)

		self.deltaEnergy = deltaEnergy(self.potential, m, tau)
		self.valWidth = valWidth
		self.periodic = periodic
		self.N = N
		self.hbar = hbar
		self.tau = tau
		self.mass = m
		self.mu = mu
		self.lambda_ = lambda_

	def __next__(self):
		start = 1 if self.periodic else 0
		stop = self.N
		accepted = 0

		# precalculate random variables
		rand_vals = np.random.rand(self.N)
		newvalues = np.random.normal(size=self.N, loc=0, scale=self.valWidth)
		for i in range(start, stop):
			newvalue = newvalues[i] + self.values[i]
			deltaEnergy = self.deltaEnergy(self.values, self.values[i], newvalue, i)
			if deltaEnergy < 0:
				self.values[i] = newvalue
				accepted += 1
				# accept it

			elif np.exp(- self.tau * deltaEnergy / self.hbar) > rand_vals[i]:
				self.values[i] = newvalue
				accepted += 1
				# accept it

				# reject
		if self.periodic:
			self.values[0] = self.values[-1]
		return self.values, accepted / (stop - start)

	def __iter__(self):
		return self

class MetropolisC:
	# Metropolis algorithm
	def __init__(self, init=0, initValWidth=1, valWidth=1, periodic=True, N=100, hbar=1, tau=0.1, m=1.0, lambda_=0, mu = 1.0):
		if type(init) in [float, int, np.float64]:
			self.values = np.random.normal(size=N, loc=init, scale=initValWidth)
		else:
			self.values = np.array(init)
			N = len(self.values)
		if periodic:
			self.values[0] = self.values[-1]

		self.valWidth = valWidth
		self.periodic = periodic
		self.N = N
		self.hbar = hbar
		self.tau = tau
		self.mass = m
		self.mu = mu
		self.lambda_ = lambda_

	def __next__(self):
		num_numbers = len(self.values)
		array_type = ctypes.c_double * num_numbers
		result = libmetropolis.metropolis(ctypes.c_int(num_numbers - 1), array_type(*self.values[1:]), ctypes.c_double(self.valWidth), ctypes.c_double(self.mass), ctypes.c_double(self.tau), ctypes.c_double(self.mu), ctypes.c_double(self.lambda_), ctypes.c_double(self.hbar))
		accept_ratio = libmetropolis.get_accept_ratio()
		libmetropolis.reset_ratio()
		self.values = np.ctypeslib.as_array(result, shape=(num_numbers - 1, ))
		if self.periodic:
			self.values = np.insert(self.values, 0, self.values[-1])
		return self.values, accept_ratio

	def __iter__(self):
		return self

Metropolis = MetropolisC
#Metropolis = MetropolisPython

if __name__ == '__main__':
	# Test Case getMinima, distanceToParameter
	for d in range(1, 17):
		print(distanceToParameter(d), 2 * getMinima(distanceToParameter(d)))

	# Test Case bootstrap:
	#values = np.random.normal(loc=0, scale=1, size=100)
	#bootstrap_values = bootstrap(10000, values)
	#print(bootstrap_values)