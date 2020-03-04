import numpy as np
from pathlib import Path
import os
from cycler import cycler

def getRootDirectory():
	return Path(os.path.dirname(os.path.realpath(__file__))).parent

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
	return [np.mean((data - mean) * (d[i:i + l] - mean)) for i in list(xdata)]

def autoCorrelationNormalized(data, xdata):
	correlation = autoCorrelation(data, xdata)
	return correlation / correlation[0]

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

STATE_INIT, STATE_LEFT, STATE_RIGHT = None, 1, 2

class TransitionCounter:
	def __init__(self):
		self.transitions = -1
		self.lastState = STATE_INIT

	def registerValue(self, value):
		state = STATE_LEFT
		if value > 0:
			state = STATE_RIGHT
		if state != self.lastState:
			self.lastState = state
			self.transitions += 1

	def getTransitions(self):
		return self.transitions

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

def deltaEnergy(kinetic, potential):
	def wrapper(x, x_old, x_new, index, kinetic=kinetic, potential=potential):
		return potential(x_new) - potential(x_old) + kinetic(x[index - 1], x_new) + kinetic(x_new, x[(index + 1) % len(x)]) - (kinetic(x[index - 1], x_old) + kinetic(x_old, x[(index + 1) % len(x)]))
	return wrapper

class Metropolis:
	# Metropolis algorithm
	def __init__(self, deltaEnergy, init=0, initValWidth=1, valWidth=1, periodic=True, N=100, hbar=1, tau=0.1):
		if type(init) in [float, int]:
			self.values = np.random.normal(size=N, loc=init, scale=initValWidth)
		else:
			self.values = np.array(init)
			N = len(self.values)
		if periodic:
			self.values[-1] = self.values[0]

		self.deltaEnergy = deltaEnergy
		self.valWidth = valWidth
		self.periodic = periodic
		self.N = N
		self.hbar = hbar
		self.tau = tau

	def __next__(self):
		start = 1 if self.periodic else 0
		stop = self.N
		accepted = 0
		for i in range(start, stop):
			newvalue = np.random.normal(loc=self.values[i], scale=self.valWidth)
			deltaEnergy = self.deltaEnergy(self.values, self.values[i], newvalue, i)
			if deltaEnergy < 0:
				self.values[i] = newvalue
				accepted += 1
				# accept it

			else:
				if np.exp(- self.tau * deltaEnergy / self.hbar) > np.random.rand():
					self.values[i] = newvalue
					accepted += 1
					# accept it

				# reject
		if self.periodic:
			self.values[0] = self.values[-1]
		return self.values, accepted / (stop / start)

	def __iter__(self):
		return self

if __name__ == '__main__':
	# Test Case TransitionCounter
	tC = TransitionCounter()
	values = np.random.uniform(-1, 1, 10)
	for v in values:
		tC.registerValue(v)
	print(tC.getTransitions(), values)

	# Test Case getMinima, distanceToParameter
	for d in range(1, 17):
		print(distanceToParameter(d), 2 * getMinima(distanceToParameter(d)))

	# Test Case bootstrap:
	#values = np.random.normal(loc=0, scale=1, size=100)
	#bootstrap_values = bootstrap(10000, values)
	#print(bootstrap_values)