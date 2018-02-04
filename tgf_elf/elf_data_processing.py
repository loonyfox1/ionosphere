import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

class ELF_Data_Processing_Class(object):
	# P = pi/180
	CONST_P = np.pi/180

	def __init__(self,filename,delta_day,delta_night,time,A,stantion,
				 degree,sigma,plot):
		self.filename = filename
		self.dd = delta_day
		self.dn = delta_night
		self.DEGREE = degree
		self.plot = plot
		self.SIGMA = sigma
		# time in this 5 min in second
		self.time = time
		# A - azimuth, degree
		self.A = A
		self.CONST_FS, self.CONST_FN, self.CONST_SCALE, _, _, _, _, _ = stantion()

	def read_data(self):
		self.channel1,self.channel2 = [],[]
		with open(self.filename,'r') as f:
			lines = f.readlines()[1:]
			for s in lines:
				self.channel1.append(int(s[:s.find('\t')]))
				self.channel2.append(int(s[s.find('\t')+1:]))
		return self.channel1,self.channel2,len(self.channel1)

	def channels_to_data(self):
		self.data = [np.sqrt(self.channel1[i]**2+self.channel2[i]**2)
				for i in range(self.N)]
		return self.data

	def filtering(self):
		b, a = signal.butter(N=3,Wn=[(50-0.25)/self.CONST_FN,(50+0.25)/self.CONST_FN],
							 btype='bandstop',analog=False)
		filtered1 = signal.lfilter(b, a, self.data)
		try:
			b, a = signal.butter(N=3,Wn=[(150-0.25)/self.CONST_FN,(150+0.25)/self.CONST_FN],
								 btype='bandpass',analog=False)
			filtered2 = signal.lfilter(b, a, filtered1)

			b, a = signal.butter(N=3,Wn=[(250-0.25)/self.CONST_FN,(250+0.25)/self.CONST_FN],
								 btype='bandpass',analog=False)
			self.filtered = signal.lfilter(b, a, filtered2)
		except ValueError:
			self.filtered = filtered1

		return list(self.filtered)

	def plot_filtering(self):
		fig = plt.figure()
		ax1 = fig.add_subplot(1,1,1)
		ax1.plot(np.fft.rfftfreq(n=self.N,d=1/self.CONST_FS),
				np.abs(np.fft.rfft(self.data))**2,label='data',color='blue')
		ax1.plot(np.fft.rfftfreq(n=self.N,d=1/self.CONST_FS),
				np.abs(np.fft.rfft(self.filtered))**2,label='filtered',color='red')
		ax1.set_title(self.filename)
		ax1.legend()
		plt.show()

	def detrending(self):
		self.mov_avg = self.filtered[:self.DEGREE]
		self.detrended=[0]*self.DEGREE
		for i in range(self.DEGREE,self.N-self.DEGREE):
			chunk = self.filtered[i-self.DEGREE:i+self.DEGREE]
			chunk = sum(chunk)/len(chunk)
			self.mov_avg.append(chunk)
			self.detrended.append(self.filtered[i]-chunk)
		self.detrended = self.detrended+[0]*self.DEGREE
		self.mov_avg = self.mov_avg+self.filtered[-self.DEGREE:]
		return self.detrended,self.mov_avg

	def peaking(self):
		peaked = self.detrended[:]
		plt.plot(self.t,peaked,label='step 0')

		std0 = np.std(peaked)
		for i in range(self.N):
			if abs(peaked[i])>self.SIGMA*std0:
				peaked[i] = self.SIGMA*std0*np.sign(peaked[i])
		plt.plot(self.t,peaked,label='step 1')

		std1 = np.std(peaked)
		for i in range(self.N):
			if abs(peaked[i])>self.SIGMA*std1:
				peaked[i] = self.SIGMA*std1*np.sign(peaked[i])
		plt.plot(self.t,peaked,label='step 2')

		std2 = np.std(peaked)
		for i in range(self.N):
			if abs(peaked[i])>self.SIGMA*std2:
				peaked[i] = self.SIGMA*std2*np.sign(peaked[i])
		plt.plot(self.t,peaked,label='step 3')

		plt.legend()
		plt.grid()
		plt.xlabel('Time, sec')
		plt.ylabel('Amplitude')
		plt.title('Peaking '+self.filename)
		if self.plot:
			plt.show()

		mean = np.mean(peaked)
		self.peaked = [pi-mean for pi in self.detrended]
		for i in range(self.N):
			if abs(self.peaked[i])<=self.SIGMA*std2:
				self.peaked[i] = 0

		return self.peaked

	def azimuth(self):
		return [np.arctan(self.channel1[i]/self.channel2[i])/self.CONST_P
				for i in range(self.N)], \
			   [np.arctan(self.channel1[i]/self.channel2[i]-np.pi)/self.CONST_P
				for i in range(self.N)]

	def plot_azimuth(self):
		plt.axhline(self.A,label='TGF')
		plt.axvline(self.time)
		plt.axvline(self.time+self.dd,color='grey',linestyle=':')
		plt.axvline(self.time+self.dn,color='grey',linestyle='--')
		plt.plot(self.t,self.azimuth_positive,label='CG+')
		plt.plot(self.t,self.azimuth_negative,label='CG+')
		plt.xlabel('Time, sec')
		plt.ylabel('Azimuth, degree')
		plt.title('Azimuth'+self.filename)
		plt.grid()
		plt.show()

	def find_peak(self):
		self.azimuth_positive,self.azimuth_negative = self.azimuth()
		if self.plot:
			self.plot_azimuth()
		if self.dd>self.dn:
			delta = self.dd
		else:
			delta = self.dn
		peak = max([abs(self.peaked[i]) for i in range(self.N)
					if self.t[i]>=self.time-delta and
					self.t[i]<=self.time+delta])
		return peak

	def data_processing(self):
		self.channel1,self.channel2,self.N = self.read_data()
		# data = sqrt(channel1**2 + channel2**2)
		self.data = self.channels_to_data()

		# t - time array
		self.t = [i*300/self.N for i in range(self.N)]

		self.filtered = self.filtering()
		self.detrended,self.mov_avg = self.detrending()
		self.peaked = self.peaking()
		self.B = self.find_peak()
		if self.plot:
			self.plot()
		return self.B/self.CONST_SCALE

	def plot(self):
		fig = plt.figure()

		ax1 = fig.add_subplot(2,1,1)
		ax1.plot(self.t,self.data,label='data',color='blue')
		ax1.plot(self.t,self.filtered,label='filtered',color='yellow')
		ax1.plot(self.t,self.mov_avg,label='moving average',color='black')
		ax1.set_title(self.filename)

		ax1.axvline(self.time+self.dd,color='grey',linestyle=':',label='delta day')
		ax1.axvline(self.time+self.dn,color='grey',linestyle='--',label='delta night')
		ax1.axvline(self.time,color='grey',label='TGF time')

		major_ticks = np.arange(0, 301, 30)
		minor_ticks = np.arange(0, 301, 15)

		ax1.set_xticks(major_ticks)
		ax1.set_xticks(minor_ticks, minor=True)
		ax1.grid(which='minor', alpha=0.2)
		ax1.grid(which='major', alpha=0.5)
		ax1.legend()

		ax2 = fig.add_subplot(2,1,2,sharex=ax1)
		ax2.plot(self.t,self.detrended,label='detrended',color='green')
		ax2.plot(self.t,self.peaked,label='peaked',color='red')

		ax2.axvline(self.time+self.dd,color='grey',linestyle=':')
		ax2.axvline(self.time+self.dn,color='grey',linestyle='--')
		ax2.axvline(self.time,color='grey')

		ax2.set_xticks(major_ticks)
		ax2.set_xticks(minor_ticks, minor=True)
		ax2.grid(which='minor', alpha=0.2)
		ax2.grid(which='major', alpha=0.5)
		ax2.legend()

		# ax3 = fig.add_subplot(3,1,3,sharex=ax1,sharey=ax2)
		# ax3.plot(self.t,self.peaked,label='peaked',color='red')
        #
		# ax3.axvline(self.time+self.dd,color='grey',linestyle=':')
		# ax3.axvline(self.time+self.dn,color='grey',linestyle='--')
		# ax3.axvline(self.time,color='grey')
        #
		# ax3.set_xticks(major_ticks)
		# ax3.set_xticks(minor_ticks, minor=True)
		# ax3.grid(which='minor', alpha=0.2)
		# ax3.grid(which='major', alpha=0.5)
		# ax3.legend()

		plt.show()

if __name__ == '__main__':
	destination = '/root/ELF_data/'
	filename = '200905101155.dat'
	time = 2*60+15.985

	filename = '200811130740.dat'
	time = 4*60+4.279

	dd = 0.050
	dn = 0.042

	A = 98

	elf_data_processing_class = ELF_Data_Processing_Class(filename=filename,
				delta_day=dd,delta_night=dn,time=time,A=A)
	B = elf_data_processing_class.data_processing()

	print('B =',B)

	elf_data_processing_class.plot()
