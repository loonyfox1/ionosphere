from __future__ import division
from __future__ import print_function
from numpy import pi,log,fft,zeros,sin,exp,sqrt,trapz,array,transpose,absolute,imag,real
from scipy import signal,special,integrate
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import time
import threading
import cPickle as pickle
import numpy as np
import os.path
mpl.rcParams.update(mpl.rcParamsDefault)

class Charge_Moment_Class(object):
	CONST_MU0 = 4e-7*pi
	# A - Earth's radius, m
	CONST_A = 6372795
	# C - velocity of light, m/sec
	CONST_C = 299792458
	# FS - sampling rate, Hz = 1/sec
	CONST_T = 300

	def __init__(self,B,d,args):
		self.B = B
		# d - array/tuple of distance like ((r_day,day=True),(r_night,day=False))
		self.d = d
		self.args = args
		self.f = self.frequency_array()

	def charge_moment(self):
		c = float(self.c_fun())
		return float(self.B/c),c

	def number_of_point(self):
		return int(round(self.args['CONST_FS']*self.CONST_T))

	def omega(self,fi):
		return 2*pi*fi

	def frequency_array(self):
		self.N = self.number_of_point()
		return fft.rfftfreq(n=self.N,d=1/self.args['CONST_FS'])[1:]

	def receiver_transfer_function(self):
		if self.args['ela']==7:
			file_name='filter_ela7.dump'
		else:
			file_name='filter_ela10.dump'

		if os.path.isfile(file_name):
			with open(file_name, 'rb') as pickle_file:
				res = pickle.load(pickle_file)

		else:
			z0 = zeros(self.N)
			z0[0] = 1

			b, a = signal.cheby1(N=2, rp=3, Wn=self.args['CONST_WN'][0]/self.args['CONST_FN'], analog=False)
			z1 = signal.lfilter(b, a, z0)

			res1 = absolute(fft.rfft(z1))
			res1=res1/max(res1)

			b, a = signal.cheby1(N=3, rp=3, Wn=self.args['CONST_WN'][1]/self.args['CONST_FN'], analog=False)
			z2 = signal.lfilter(b, a, z1)

			res2 = absolute(fft.rfft(z2))
			res2=res2/max(res2)

			b, a = signal.cheby1(N=3, rp=3, Wn=self.args['CONST_WN'][2]/self.args['CONST_FN'], analog=False)
			z3 = signal.lfilter(b, a, z2)

			res = absolute(fft.rfft(z3))
			res=res/max(res)

			with open(file_name, 'wb') as pickle_file:
				pickle.dump(res, pickle_file)

		return res

	def itf_worker(self,input_array,lock_input_array,output_dictionary,lock_output_dictionary,itf2):
		while len(input_array)>0:
			time_fi=0
			if len(input_array)>0:
				with lock_input_array:
					if len(input_array)>0:
						time_fi=input_array.pop(0)
			if time_fi!=0:
				itf1 = -1j*pi*self.CONST_MU0*time_fi/2/self.magnetic_altitude(time_fi)/self.phase_velocity(time_fi)
				itf3 = special.hankel2([1],[2*pi*self.r*time_fi/self.phase_velocity(time_fi)])
				itf4 = exp(-self.attenuation_factor(time_fi)*self.r)
				output_res=itf1*itf3*itf4*itf2
				with lock_output_dictionary:
					output_dictionary[time_fi]=output_res

	def ionosphere_transfer_function(self):
		res = []

		itf2 = sqrt(self.r/self.CONST_A/sin(self.r/self.CONST_A))

		input_array=list(self.f)
		lock_input_array=threading.Lock()

		output_dictionary={}
		lock_output_dictionary=threading.Lock()

		worker_array=[]
		for index_worker in range(100):
			worker_array.append(threading.Thread(target=self.itf_worker,args=(input_array,lock_input_array,output_dictionary,lock_output_dictionary,itf2)))
			worker_array[-1].start()
		[x.join() for x in worker_array]
		for fi in self.f:
			res.append(output_dictionary[fi])
			
		return res

	def total_distance(self):
		return self.d[0][0]+self.d[1][0]

	def c_fun(self):
		res_c = sqrt(pi*self.args['CONST_DELTAF']/self.args['CONST_HI']* \
						trapz(array(self.integrand()),
						x=self.f, axis=0))
		return res_c

	def ionosphere_transfer_function_fft(self):
		d_total = self.total_distance()
		dc = int(self.d[0][0]/d_total*self.N)

		res = []
		for check_day in self.d:
			self.day = check_day[1]
			self.r = check_day[0]
			if self.r==0:
				res.append([])
			else:
				self.r = d_total
				if self.r/self.CONST_A>np.pi:
					self.r = self.r - np.pi*self.CONST_A
				res.append(list(np.fft.ifft(self.ionosphere_transfer_function())))
		return np.fft.fft(res[0][:dc]+res[1][dc:])

	def integrand(self):
		res_rtf = self.receiver_transfer_function()
		res_itf = self.ionosphere_transfer_function_fft()
		return [absolute(itf*rtf*itf*rtf)
				for itf,rtf in zip(res_itf,res_rtf)]

	def magnetic_altitude(self,fi):
		return real(self.magnetic_characteristic_altitude(fi))

	def phase_velocity(self,fi):
		return self.CONST_C/real(self.propagation_parameter(fi))

	def attenuation_factor(self,fi):
		return self.omega(fi)/self.CONST_C*abs(imag(self.propagation_parameter(fi)))

	def propagation_parameter(self,fi):
		return sqrt(self.magnetic_characteristic_altitude(fi)/ \
					   self.electric_characteristic_altitude(fi))

	def magnetic_characteristic_altitude(self,fi):
		logfi77 = log(fi/7.7)
		if self.day:
			res = (101.5 - 3.1*logfi77 + \
				1j*(7.0 - 0.9*logfi77))*1e3
		else:
			res = (114.7 - 8.4*logfi77 + \
				1j*(13.2 - 2.0*logfi77))*1e3
		return res

	def electric_characteristic_altitude(self,fi):
		fi77 = 7.7/fi
		if self.day:
			fi17 = 1.7/fi
			fi17_822 = (fi17)**0.822
			res = (51.1 + 1.9*log(fi/1.7) - 2.45*fi17_822 - 2.84*(fi17)**1.645 + \
				1j*(-2.98 - 8.8*fi17_822 + 1.86*(fi77)**1.645))*1e3
		else:
			fi77_626 = (fi77)**1.626
			fi77_813 = (fi77)**0.813
			res = (67.5 + 2.0*log(fi/7.7) - 2.54*fi77_813 - 2.72*fi77_626 + \
				1j*(-3.14 - 8.7*fi77_813 + 1.92*fi77_626))*1e3
		return res

if __name__ == '__main__':
	B = 14.4e-12
	d = ((5352e3,True),(0,False))

	charge_moment_class = Charge_Moment_Class(B=B,d=d)
	res = charge_moment_class.charge_moment()
	delay1,delay2 = charge_moment_class.time_delay()
	print(delay1,delay2)
	print ('p =',res/1000,'C*km')
	print ('excpect 330 C*km')
