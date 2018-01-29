from iminuit import Minuit, describe, Struct
from iminuit.frontends import ConsoleFrontend
import numpy as np
import pandas as pd

def funct(x,s, z, m, p1, e1, f1, g1, p2, e2, f2, g2, p3, e3, f3, g3, p4, e4, f4, g4, p5, e5, f5, g5):
	# print(*p)

	# s, z, m, p1, e1, f1, g1, p2, e2, f2, g2, p3, e3, f3, g3, p4, e4, f4, g4, p5, e5, f5, g5 = p
	try:
		res = s + \
			 p1*(1+e1*(x-f1))/((x-f1)*(x-f1)+g1*g1/4) + \
			 p2*(1+e2*(x-f2))/((x-f2)*(x-f2)+g2*g2/4) + \
			 p3*(1+e3*(x-f3))/((x-f3)*(x-f3)+g3*g3/4) + \
			 p4*(1+e4*(x-f4))/((x-f4)*(x-f4)+g4*g4/4) + \
			 p5*(1+e5*(x-f5))/((x-f5)*(x-f5)+g5*g5/4)
	except ZeroDivisionError:
		return 0
	return res

def color_noise(W,f):
	y = [np.log(i) for i in W]
	x = [-np.log(i) for i in f]
	c = np.polyfit(x,y,1)
	# print c[0], np.exp(c[1])
	return W - np.exp(c[1])*np.power(f,-c[0])

def normalize(y):
	maxy = max(y)
	y = [i/maxy for i in y]
	return y

def minimizeMe(s, z, m, p1, e1, f1, g1, p2, e2, f2, g2, p3, e3, f3, g3, p4, e4, f4, g4, p5, e5, f5, g5):
	# print(p)
	# s, z, m,
	# p1, e1, f1, g1,
	# p2, e2, f2, g2,
	# p3, e3, f3, g3,
	# p4, e4, f4, g4,
	# p5, e5, f5, g5 = p
	return sum((funct(x, s, z, m, p1, e1, f1, g1, p2, e2, f2, g2, p3, e3, f3, g3, p4, e4, f4, g4, p5, e5, f5, g5) - y)**2/y/	y
			for x, y in zip(x, y))

data = pd.read_table('/root/Downloads/201109062220.dat', names=['f','X','Y','Z'], sep=' ')

x = data.f
y = normalize(data.Z)
y = color_noise(x,y)

p = [8e-4, 1., 0.8,
	8e-3, -0.25, 7.01, 1.,
	7e-3, -0.15, 14.0, 1.9,
	6e-3, -0.2, 20.0, 2.2,
	5e-3, -0.2, 25.0, 3.5,
	4e-3, -0.2, 32.0, 4.2]

m = Minuit(minimizeMe, s=p[0], z=p[1], m=p[2],
					   p1=p[3], e1=p[4], f1=p[5], g1=p[6],
					   p2=p[7], e2=p[8], f2=p[9], g2=p[10],
					   p3=p[11], e3=p[12], f3=p[13], g3=p[14],
					   p4=p[15], e4=p[16], f4=p[17], g4=p[18],
					   p5=p[19], e5=p[20], f5=p[21], g5=p[22],
					   limit_f1=(7,9), limit_f2=(12,16),
					   limit_f3=(19,23), limit_f4=(24,28),
					   limit_f5=(29,36), limit_g1=(1.,2.),
					   limit_g2=(1.2,2.5), limit_g3=(1.5,3.),
					   limit_g4=(2.,3.5), limit_g5=(2.5,4.))
m.print_param()
m.migrad()
