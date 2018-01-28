from iminuit import Minuit, describe, Struct
from iminuit.frontends import ConsoleFrontend
import numpy as np
import pandas as pd

def funct(x,s, z, m, p1, e1, f1, g1, p2, e2, f2, g2, p3, e3, f3, g3, p4, e4, f4, g4, p5, e5, f5, g5):
	# print(*p)
	# s, z, m, p1, e1, f1, g1, p2, e2, f2, g2, p3, e3, f3, g3, p4, e4, f4, g4, p5, e5, f5, g5 = p
	res = s + z/x**m + \
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

def minimizeMe(s, z, m, p1, e1, f1, g1, p2, e2, f2, g2, p3, e3, f3, g3, p4, e4, f4, g4, p5, e5, f5, g5):
	# print(p)
	# s, z, m,
	# p1, e1, f1, g1,
	# p2, e2, f2, g2,
	# p3, e3, f3, g3,
	# p4, e4, f4, g4,
	# p5, e5, f5, g5 = p
	return sum((funct(x, s, z, m, p1, e1, f1, g1, p2, e2, f2, g2, p3, e3, f3, g3, p4, e4, f4, g4, p5, e5, f5, g5) - y)**2
			for x, y in zip(x, y))

data = pd.read_table('/root/Downloads/201109062220.dat', names=['f','X','Y','Z'], sep=' ')

x = data.f
y = normalize(data.X)

p = [8e-4, 1., 0.8,
	5e-4, 8e-3, -0.25, 7.01, 1.,
	3e-4, 7e-3, -0.15, 14.0, 1.9,
	2e-4,  6e-3, -0.2, 20.0, 2.2,
	1e-4,  5e-3, -0.2, 25.0, 3.0,
	0.5e-4,  4e-3, -0.2, 32.0, 4.2]

m = Minuit(minimizeMe, s=p[0], z=p[1], m=p[2],
					   p1=p[3], e1=p[4], f1=p[5], g1=p[6],
					   p2=p[7], e2=p[8], f2=p[9], g2=p[10],
					   p3=p[11], e3=p[12], f3=p[13], g3=p[14],
					   p4=p[15], e4=p[16], f4=p[17], g4=p[18],
					   p5=p[19], e5=p[20], f5=p[21], g5=p[22],
					   limit_f1=(7,9), limit_f2=(12,16),
					   limit_f3=(19,23), limit_f4=(24,28),
					   limit_f4=(29,35))																																							))
m.print_param()
m.migrad()
