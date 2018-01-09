import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, least_squares

data = pd.read_table('/root/Downloads/201109062220.dat', names=['f','X','Y','Z'], sep=' ')

def color_noise(W,f):
	y = [np.log(i) for i in W]
	x = [-np.log(i) for i in f]
	c = np.polyfit(x,y,1)
	print c[0], np.exp(c[1])
	return W - np.exp(c[1])*np.power(f,-c[0])

def funct(x,*p):
	s, p1, e1, f1, g1 = p
	res = s + \
		  p1*(1+e1*(x-f1))/((x-f1)*(x-f1)+g1*g1/4) #+ \
		  # p2*(1+e2*(x-f2))/((x-f2)*(x-f2)+g2*g2/4) + \
		  # p3*(1+e3*(x-f3))/((x-f3)*(x-f3)+g3*g3/4) + \
		  # p4*(1+e4*(x-f4))/((x-f4)*(x-f4)+g4*g4/4) + \
		  # p5*(1+e5*(x-f5))/((x-f5)*(x-f5)+g5*g5/4)
	return res

def normalize(y,maxy):
	# maxy = max(y)
	y = [i/maxy for i in y]
	return y

def main(data,lims,N):
	res = []
	maxw = max(data.X)
	res = []
	p = [[5e-4, 8e-3, -0.25, 7.01, 1.],
		[3e-4, 7e-3, -0.15, 14.0, 1.9],
		[2e-4,  6e-3, -0.2, 20.0, 2.2],
		[1e-4,  5e-3, -0.2, 25.0, 3.0],
		[0.5e-4,  4e-3, -0.2, 32.0, 4.2]]
	for i in range(N):
		W = np.array(data.X[data.f>lims[i]][data.f<lims[i+1]])
		W = [x-8e-3 for x in normalize(W,maxw)]
		for x in range(len(W)):
			if W[x]<0:
				W[x]=1e-8
		F = data.f[data.f>lims[i]][data.f<lims[i+1]]
		# W = color_noise(W,F)
		popt, pcov = curve_fit(funct, F, W, method='lm',p0=p[i]	)
		print popt, pcov
		# plt.plot(F,W)
		# plt.plot(F,funct(F, *popt))
		# plt.title('k='+str(i+1))
		# plt.show()
		res.append(popt)
	return res

lims = [4.9,11.1,17.9,25.1,29.9,36.1]   # limits between resonances
N = 5                                   # number of resonances

res = main(data,lims,N)

# s, p1, e1, f1, g1 = res              # parameters

maxw = max(data.X)
W = [x-8e-3 for x in normalize(data.X,maxw)]
for x in range(len(W)):
	if W[x]<0:
		W[x]=1e-8
result = []
for j in range(len(W)):
	suma = 0
	x = data.f[j]
	for k in range(N):
		  suma += res[k][1]*(1+res[k][2]*(x-res[k][3]))/((x-res[k][3])*(x-res[k][3])+res[k][4]*res[k][4]/4)
	result.append(suma)
plt.clf()
plt.plot(data.f, W, color='blue', label='data')
plt.plot(data.f,result, color='red', label='fitting')
plt.grid()
plt.xlabel('freq')
plt.ylabel('W / W_max')
plt.legend()
plt.show()
