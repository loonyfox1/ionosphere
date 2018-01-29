import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def normalize(y):
	maxy = max(y)
	y = [i/maxy for i in y]
	return y

def Murnaghan(parameters, x):
	# print(parameters)
	s, z, m, p1, e1, f1, g1, p2, e2, f2, g2, p3, e3, f3, g3, p4, e4, f4, g4, p5, e5, f5, g5 = parameters
	res = s + \
		  p1*(1+e1*(x-f1))/((x-f1)*(x-f1)+g1*g1/4) + \
		  p2*(1+e2*(x-f2))/((x-f2)*(x-f2)+g2*g2/4) + \
		  p3*(1+e3*(x-f3))/((x-f3)*(x-f3)+g3*g3/4) + \
		  p4*(1+e4*(x-f4))/((x-f4)*(x-f4)+g4*g4/4) + \
		  p5*(1+e5*(x-f5))/((x-f5)*(x-f5)+g5*g5/4)
	return res

data = pd.read_table('/root/Downloads/201109062220.dat', names=['f','X','Y','Z'], sep=' ')
x = data.f
y = normalize(data.X)
p=[1.947E-05,
1,
0.8,
0.0005807,
-0.8618,
8.885,
9.671,
-4.178E-05,
-0.3296,
14.29,
4.546,
0.0002202,
-0.5604,
19.89,
5.824,
6.258E-05,
-0.1746,
26.25,
4.507,
0.001448,
-0.04974,
32.31,
24.29]
fity = [Murnaghan(p,xi) for xi in x]


plt.clf()
plt.plot(x,y,label='data')
plt.plot(x,fity,label='fit')
plt.legend()
plt.grid()
plt.ylabel('W / W_max')
plt.xlabel('Freq')
plt.title('Resonance fitting')
plt.show()
