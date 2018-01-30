from iminuit import Minuit
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from lmfit import Parameters, minimize, Parameter, Minimizer

def funct(x, s, z, m, p1, e1, f1, g1, p2, e2, f2, g2,
			p3, e3, f3, g3, p4, e4, f4, g4, p5, e5, f5, g5):
	try:
		res = s + z/x**m + \
			 p1*(1+e1*(x-f1))/((x-f1)*(x-f1)+g1*g1/4) + \
			 p2*(1+e2*(x-f2))/((x-f2)*(x-f2)+g2*g2/4) + \
			 p3*(1+e3*(x-f3))/((x-f3)*(x-f3)+g3*g3/4) + \
			 p4*(1+e4*(x-f4))/((x-f4)*(x-f4)+g4*g4/4) + \
			 p5*(1+e5*(x-f5))/((x-f5)*(x-f5)+g5*g5/4)
	except ZeroDivisionError:
		return 0
	return res

def func(params, x, y):
	s = params['s'].value
	z = params['z'].value
	m = params['m'].value
	p1 = params['p1'].value
	p2 = params['p2'].value
	p3 = params['p3'].value
	p4 = params['p4'].value
	p5 = params['p5'].value
	e1 = params['e1'].value
	e2 = params['e2'].value
	e3 = params['e3'].value
	e4 = params['e4'].value
	e5 = params['e5'].value
	f1 = params['f1'].value
	f2 = params['f2'].value
	f3 = params['f3'].value
	f4 = params['f4'].value
	f5 = params['f5'].value
	g1 = params['g1'].value
	g2 = params['g2'].value
	g3 = params['g3'].value
	g4 = params['g4'].value
	g5 = params['g5'].value
	try:
		res = s + z/x**m + \
			 p1*(1+e1*(x-f1))/((x-f1)*(x-f1)+g1*g1/4) + \
			 p2*(1+e2*(x-f2))/((x-f2)*(x-f2)+g2*g2/4) + \
			 p3*(1+e3*(x-f3))/((x-f3)*(x-f3)+g3*g3/4) + \
			 p4*(1+e4*(x-f4))/((x-f4)*(x-f4)+g4*g4/4) + \
			 p5*(1+e5*(x-f5))/((x-f5)*(x-f5)+g5*g5/4)
	except ZeroDivisionError:
		return 0
	return res

data = pd.read_table('/root/Downloads/201109062220.dat',
					 names=['f','X','Y','Z'], sep=' ')
x = np.array(data.f)
y = np.array(data.X)

# step of smoothing = 5;10
step = 10
ys = []
xs = []
for i in range(int(len(y)/step)):
	suma=0
	for j in range(i*step,(i+1)*step):
		suma += y[j]
	xs.append(x[int((i+1/2)*step)])
	ys.append(suma/step)

plt.plot(x,y,label='data')
plt.plot(xs,ys,label='smoothed')
plt.legend()
plt.grid()
plt.title('Smoothing data step='+str(step))
plt.show()

############################################################################
# scipy.optimize.curve_fit
'''
kwargs = (8e-4,1.,0.8,
		8e-3, -0.25, 7.01, 1.,
		7e-3, -0.15, 14.0, 1.9,
		6e-3, -0.2,  20.0, 2.2,
		5e-3, -0.2,  25.0, 3.5,
		4e-3, -0.2,  32.0, 4.2)

# sigma - optional: None or y
sigma = None
# bounds - limits for parameters
bounds = ((0,-np.inf,-np.inf,
		   0,-np.inf,7,0.8,
		   0,-np.inf,11,1.3,
		   0,-np.inf,17,1.7,
		   0,-np.inf,23,2.1,
		   0,-np.inf,29,2.4),
		  (100,np.inf,np.inf,
		  100,np.inf,9,20,
		  100,np.inf,17,20,
		  100,np.inf,22,20,
		  100,np.inf,29,20,
		  100,np.inf,35,20))
# method : {‘lm’, ‘trf’, ‘dogbox’}, optional
method = 'dogbox'

popt, pcov = curve_fit(funct, xs, ys, p0=kwargs, sigma=sigma, bounds=bounds, method=method)
print('par ',popt)

plt.plot(xs,ys,label='data')
plt.plot(xs,[funct(xi,*popt) for xi in xs],label='fit')
plt.legend()
plt.grid()
plt.title('scipy.optimize method='+method+' p0=kwargs sigma=None')
plt.show()
'''
############################################################################
############################################################################
# lmfit.minimize

fit_params = Parameters()
fit_params['s'] = Parameter(value=8e-4)
fit_params['m'] = Parameter(value=1.0)
fit_params['z'] = Parameter(value=0.8)
fit_params['p1'] = Parameter(value=8e-3, min=0, max=100)
fit_params['e1'] = Parameter(value=-0.25)
fit_params['f1'] = Parameter(value=7.01, min=7, max=9)
fit_params['g1'] = Parameter(value=1.0, min=0.8, max=9)
fit_params['p2'] = Parameter(value=7e-3, min=0, max=100)
fit_params['e2'] = Parameter(value=-0.15)
fit_params['f2'] = Parameter(value=14.0, min=11, max=17)
fit_params['g2'] = Parameter(value=1.9, min=1.3, max=9)
fit_params['p3'] = Parameter(value=6e-3, min=0, max=100)
fit_params['e3'] = Parameter(value=-0.2)
fit_params['f3'] = Parameter(value=20.0, min=17, max=22)
fit_params['g3'] = Parameter(value=2.2, min=1.7, max=20)
fit_params['p4'] = Parameter(value=5e-3, min=0, max=100)
fit_params['e4'] = Parameter(value=-0.2)
fit_params['f4'] = Parameter(value=25.0, min=23, max=29)
fit_params['g4'] = Parameter(value=3.5, min=2.1, max=20)
fit_params['p5'] = Parameter(value=4e-3, min=0, max=100)
fit_params['e5'] = Parameter(value=-0.2)
fit_params['f5'] = Parameter(value=32.0, min=29, max=35)
fit_params['g5'] = Parameter(value=4.2, min=2.4, max=20)

minner = Minimizer(func, fit_params, fcn_args=(xs,ys))
result = minner.minimize()
final = ys + result.residual


plt.plot(xs,ys,label='data')
plt.plot(xs,result.residual,label='fit')
plt.legend()
plt.grid()
# plt.title('lmfit.minimize method='+method+' p0=None sigma=y')
plt.show()

############################################################################
