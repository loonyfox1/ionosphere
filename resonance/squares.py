from scipy.optimize import leastsq
import numpy as np
import pandas as pd


def Murnaghan(parameters, x):
	print(parameters)
	s, z, m, p1, e1, f1, g1, p2, e2, f2, g2, p3, e3, f3, g3, p4, e4, f4, g4, p5, e5, f5, g5 = parameters
	res = s + \
		  p1*(1+e1*(x-f1))/((x-f1)*(x-f1)+g1*g1/4) + \
		  p2*(1+e2*(x-f2))/((x-f2)*(x-f2)+g2*g2/4) + \
		  p3*(1+e3*(x-f3))/((x-f3)*(x-f3)+g3*g3/4) + \
		  p4*(1+e4*(x-f4))/((x-f4)*(x-f4)+g4*g4/4) + \
		  p5*(1+e5*(x-f5))/((x-f5)*(x-f5)+g5*g5/4)
	return res

def normalize(y):
	maxy = max(y)
	y = [i/maxy for i in y]
	return y

def objective(pars, y, x):
	#we will minimize this function
	err =  (y - Murnaghan(pars, x))**2
	return err

p = [8e-4, 1., 0.8,
	8e-3, -0.25, 7.01, 1.,
	7e-3, -0.15, 14.0, 1.9,
	6e-3, -0.2, 20.0, 2.2,
	5e-3, -0.2, 25.0, 3.0,
	4e-3, -0.2, 32.0, 4.2]

data = pd.read_table('/root/Downloads/201109062220.dat', names=['f','X','Y','Z'], sep=' ')
x = data.f
y = normalize(data.X)

plsq = leastsq(objective, p, args=(y, x))

print('Fitted parameters = {0}'.format(plsq[0]))

import matplotlib.pyplot as plt
plt.plot(x,y, 'ro')

#plot the fitted curve on top
x = np.linspace(min(data.f), max(data.f), 50)
y = Murnaghan(plsq[0], x)
plt.plot(x, y, 'k-')
plt.xlabel('Volume')
plt.ylabel('Energy')
plt.savefig('nonlineenergiesar-curve-fitting.png')
