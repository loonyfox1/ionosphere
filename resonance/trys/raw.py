from iminuit import Minuit
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

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

data = pd.read_table('/root/Downloads/201109062220.dat',
					 names=['f','X','Y','Z'], sep=' ')
x = data.f
y = data.X

############################################################################
# iminuit.Minuit.migrad
'''
def minimize(s, z, m, p1, e1, f1, g1, p2, e2, f2, g2,
			 p3, e3, f3, g3, p4, e4, f4, g4, p5, e5, f5, g5):
	return sum((funct(x, s, z, m, p1, e1, f1, g1, p2, e2, f2,
					  g2, p3, e3, f3, g3, p4, e4, f4, g4, p5,
					  e5, f5, g5) - y)**2 for x, y in zip(x, y))

kwargs = dict(s=8e-4, z=1., m=0.8,
	p1=8e-3, e1=-0.25, f1=7.01, g1=1.,
	p2=7e-3, e2=-0.15, f2=14.0, g2=1.9,
	p3=6e-3, e3=-0.2,  f3=20.0, g3=2.2,
	p4=5e-3, e4=-0.2,  f4=25.0, g4=3.5,
	p5=4e-3, e5=-0.2,  f5=32.0, g5=4.2,
	pedantic = False, print_level = 0,
    limit_p1 = (0., 100), limit_p2 = (0., 100), limit_p3 = (0., 100),
    limit_p4 = (0., 100), limit_p5 = (0., 100),
    limit_f1 = (7,9), limit_f2 = (11,17), limit_f3 = (17,22),
    limit_f4 = (23,29), limit_f5 = (29,35),
    limit_g1 = (0.8,20), limit_g2 = (1.3,20), limit_g3 = (1.7,20),
    limit_g4 = (2.1,20), limit_g5 = (2.4,20),
    limit_s = (0, 100),
  	errordef = 1)

m = Minuit(minimize, **kwargs)
param = m.migrad()
print('----Minuit\n')
print(param.name(),param.value(),param.error())
'''
############################################################################
############################################################################
# scipy.optimize.curve_fit

kwargs = (8e-4,1.,0.8,
	   	8e-3, -0.25, 7.01, 1.,
		7e-3, -0.15, 14.0, 1.9,
		6e-3, -0.2,  20.0, 2.2,
		5e-3, -0.2,  25.0, 3.5,
		4e-3, -0.2,  32.0, 4.2)

# sigma - optional: None or y
sigma = y
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
method = 'trf'

popt, pcov = curve_fit(funct, x, y, p0=None, sigma=sigma, bounds=bounds, method=method)
print('par ',popt)

popt = s, z, m, p1, e1, f1, g1, p2, e2, f2, g2, p3, e3, f3, g3, p4, e4, f4, g4, p5, e5, f5, g5

plt.plot(x,y,label='data')
plt.plot(x,[funct(xi,s, z, m, p1, e1, f1, g1, p2, e2, f2, g2, p3, e3, f3, g3, p4, e4, f4, g4, p5, e5, f5, g5) for xi in x],label='fit')
plt.legend()
plt.grid()
plt.title('scipy.optimize method='+method+' p0=None sigma=y')
plt.show()
############################################################################
# lmfit.minimize
'''
fit_params = Parameters()
fit_params['s'] = Parameter(value=1.2, min=0.1, max=1000)
fit_params['m'] = Parameter(value=40.0, vary=False)
fit_params['z'] = Parameter(value=4, min=0)

result = minimize(myfunc, fit_params, args=(x, data), kws={'someflag':True}, ....)


plt.plot(x,y,label='data')
plt.plot(x,[funct(xi,popt) for xi in x],label='fit')
plt.legend()
plt.grid()
plt.title('lmfit.minimize method='+method+' p0=None sigma=y')
plt.show()
'''
############################################################################
