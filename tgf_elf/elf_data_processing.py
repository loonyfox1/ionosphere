import numpy as np
import matplotlib.pyplot as plt

class ELF_Data_Processing_Class(object):
	# DEGREE - parameter of detrending
	DEGREE = 10
	# SIGMA - parameter of peaking
	SIGMA = 3

	def __init__(self,filename,delta_day,delta_night,time):
		self.filename = filename
		self.dd = delta_day
		self.dn = delta_night
		# time in this 5 min in second
		self.time = time

	def read_data(self):
		self.channel1,self.channel2 = [],[]
		with open(self.filename,'r') as f:
			for line in f:
				s = f.readline()
				self.channel1.append(int(s[:s.find('\t')]))
				self.channel2.append(int(s[s.find('\t')+1:]))
		return self.channel1,self.channel2,len(self.channel1)

	def channels_to_data(self):
		return [np.sqrt(self.channel1[i]**2+self.channel2[i]**2)
				for i in range(self.N)]

	def detrending(self):
		self.detrended=[0]*self.DEGREE
		for i in range(self.DEGREE,self.N-self.DEGREE):
			chunk=self.data[i-self.DEGREE:i+self.DEGREE]
			chunk=sum(chunk)/len(chunk)
			self.detrended.append(self.data[i]-chunk)
		self.detrended = self.detrended+[0]*self.DEGREE
		return self.detrended

	def peaking(self):
		mean = np.mean(self.detrended)
		self.peaked = []
		for i in range(self.N):
			self.peaked.append(self.detrended[i]-mean)
		std = np.std(self.peaked)
		for i in range(self.N):
			if abs(self.peaked[i])<self.SIGMA*std:
				self.peaked[i] = 0
		return self.peaked

	def find_peak(self):
		if self.dd>self.dn:
			delta = self.dd
		else:
			delta = self.dn
		peak = max([self.peaked[i] for i in range(self.N)
					if self.t[i]>=time-delta and self.t[i]<=time+delta])
		return peak

	def data_processing(self):
		self.channel1,self.channel2,self.N = self.read_data()
		self.t = [i*300/self.N for i in range(self.N)]
		self.data = self.channels_to_data()
		self.detrended = self.detrending()
		self.peaked = self.peaking()
		self.B = self.find_peak()
		return self.B

	def plot(self):
		fig = plt.figure()

		ax1 = fig.add_subplot(3,1,1)
		ax1.plot(self.t,self.data,label='data',color='blue')
		ax1.set_title(filename)

		ax1.axvline(time+dd,color='grey',linestyle=':',label='delta day')
		ax1.axvline(time+dn,color='grey',linestyle='--',label='delta night')
		ax1.axvline(time-dd,color='grey',linestyle=':')
		ax1.axvline(time-dn,color='grey',linestyle='--')

		major_ticks = np.arange(0, 301, 30)
		minor_ticks = np.arange(0, 301, 15)

		ax1.set_xticks(major_ticks)
		ax1.set_xticks(minor_ticks, minor=True)
		ax1.grid(which='minor', alpha=0.2)
		ax1.grid(which='major', alpha=0.5)
		ax1.legend()

		ax2 = fig.add_subplot(3,1,2,sharex=ax1)
		ax2.plot(self.t,self.detrended,label='detrended',color='green')

		ax2.axvline(time+dd,color='grey',linestyle=':')
		ax2.axvline(time+dn,color='grey',linestyle='--')
		ax2.axvline(time-dd,color='grey',linestyle=':')
		ax2.axvline(time-dn,color='grey',linestyle='--')

		ax2.set_xticks(major_ticks)
		ax2.set_xticks(minor_ticks, minor=True)
		ax2.grid(which='minor', alpha=0.2)
		ax2.grid(which='major', alpha=0.5)
		ax2.legend()

		ax = fig.add_subplot(3,1,3,sharex=ax1,sharey=ax2)
		ax.plot(self.t,self.peaked,label='peaked',color='red')

		ax.axvline(time+dd,color='grey',linestyle=':')
		ax.axvline(time+dn,color='grey',linestyle='--')
		ax.axvline(time-dd,color='grey',linestyle=':')
		ax.axvline(time-dn,color='grey',linestyle='--')

		ax.set_xticks(major_ticks)
		ax.set_xticks(minor_ticks, minor=True)
		ax.grid(which='minor', alpha=0.2)
		ax.grid(which='major', alpha=0.5)
		ax.legend()

		plt.show()

if __name__ == '__main__':
	destination = '/root/ELF_data/'
	filename = '201109062210.dat'
	time = 34.4489
	dd = 0.04
	dn = 0.035

	elf_data_processing_class = ELF_Data_Processing_Class(filename=filename,
				delta_day=dd,delta_night=dn,time=time)
	B = elf_data_processing_class.data_processing()

	print('B =',B)

	elf_data_processing_class.plot()
