from tools import getRootDirectory, Potential, deltaEnergy, MetropolisPythonRandom
import ctypes
from ctypes import cdll
import numpy as np

libmetropolis = cdll.LoadLibrary(getRootDirectory() / 'bin' / 'libmetropolis.so')
libmetropolis.metropolis.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)
libmetropolis.metropolis.restype = ctypes.POINTER(ctypes.c_double)

libmetropolis.metropolis_Random.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_bool)
libmetropolis.metropolis_Random.restype = ctypes.POINTER(ctypes.c_double)

libmetropolis.get_accept_ratio.argtypes = ()
libmetropolis.get_accept_ratio.restype = ctypes.c_double

libmetropolis.potential_check.argtypes = (ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)
libmetropolis.potential_check.restype = ctypes.POINTER(ctypes.c_double)

libmetropolis.delta_energy.argtypes = (ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)
libmetropolis.delta_energy.restype = ctypes.c_double

start = -5
stop = 5
num = 100
mu = 10.0
lambda_ = 0.0

result = libmetropolis.potential_check(ctypes.c_int(num), ctypes.c_double(start), ctypes.c_double(stop), ctypes.c_double(mu), ctypes.c_double(lambda_))
values_C = np.ctypeslib.as_array(result, shape=(num + 1, ))

pot = Potential(mu, lambda_)
values_P = pot(np.linspace(start, stop, num + 1))

print('Calculate the ratio between the data obtained with Python and C++\n if they are equal (within discretisation error) the minimum and maximum values should be near 1.0:')

print('min: %0.8f, max: %0.8f' %(min((values_C + 0.00001) / (values_P + 0.00001)), max((values_C + 0.00001) / (values_P + 0.00001))))


mu = 1.0
lambda_ = 0.0
mass = 1.0
tau = 0.1
pot = Potential(mu, lambda_)
dEnergy = deltaEnergy(pot, mass, tau)
hbar = 1.0

values_P = []
values_C = []

for i in range(100):
	values = np.random.normal(loc=0.0, scale=10.0, size=1000)
	index = np.random.randint(10, 990)
	x_old = values[index]
	x_new = x_old + np.random.normal(loc=0.0, scale=1.0)
	left = values[index-1]
	right = values[index+1]
	values_P.append(dEnergy(values, x_old, x_new, index))
	values_C.append(libmetropolis.delta_energy(ctypes.c_double(left), ctypes.c_double(right), ctypes.c_double(x_new), ctypes.c_double(x_old), ctypes.c_double(mass), ctypes.c_double(tau), ctypes.c_double(mu), ctypes.c_double(lambda_)))

values_P = np.array(values_P)
values_C = np.array(values_C)


print('min: %0.8f, max: %0.8f' %(min((values_C + 0.00001) / (values_P + 0.00001)), max((values_C + 0.00001) / (values_P + 0.00001))))

values = np.random.normal(loc=0.0, scale=10.0, size=1000)


N = 10
values = np.random.normal(loc=0.0, scale=10.0, size=N)
random_gauss = np.random.normal(loc=0.0, scale=1.0, size=N)
random_uniform = np.random.uniform(0, 1, size=N)

m = MetropolisPythonRandom(random_gauss, random_uniform, init=values, valWidth=1, initValWidth=0, hbar=hbar, tau=tau, N=N, m=mass, lambda_=0, mu=mu)
newvalues_P = np.array(next(m)[0])
#print(newvalues_P[0])

array_type = ctypes.c_double * N
result = libmetropolis.metropolis_Random(ctypes.c_int(N), array_type(*values), array_type(*random_gauss), array_type(*random_uniform), ctypes.c_double(1), ctypes.c_double(mass), ctypes.c_double(tau), ctypes.c_double(mu), ctypes.c_double(lambda_), ctypes.c_double(hbar), ctypes.c_bool(True))
newvalues_C = np.ctypeslib.as_array(result, shape=(N, ))
#print(newvalues_C)


print('min: %0.8f, max: %0.8f' %(min((newvalues_C + 0.00001) / (newvalues_P + 0.00001)), max((newvalues_C + 0.00001) / (newvalues_P + 0.00001))))