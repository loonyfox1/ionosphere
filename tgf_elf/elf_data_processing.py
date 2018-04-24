from __future__ import division
from __future__ import print_function
from numpy import pi,sqrt,fft,nanstd,nan,arctan2,abs
from scipy import signal
import matplotlib.pyplot as plt
import time
import matplotlib
from read_elf_file import Read_ELF_Class

font = {'size'   : 8}

matplotlib.rc('font', **font)

class ELF_Data_Processing_Class(object):
	# P = pi/180
	CONST_P = pi/180

	def __init__(self,filename,delta_day,delta_night,time,A,stantion,
				 degree,sigma,plot,datetime,idd,dest_img,dest_in):
		self.CONST_FS, self.CONST_FN, self.CONST_SCALE, self.CONST_DELTAF, \
		 _, _, _, _ = stantion()
		self.filename = filename
		self.dd = delta_day + 1/self.CONST_DELTAF
		self.dn = delta_night + 1/self.CONST_DELTAF
		self.DEGREE = degree
		self.plot = plot
		self.SIGMA = sigma
		self.time = time-1.6e-3
		self.A = A
		self.id = idd
		self.datetime = datetime
		self.dest_img = dest_img
		self.dest_in = dest_in
		if self.CONST_DELTAF==51.8:
			self.CONST_INDENT = 5
		else:
			self.CONST_INDENT = 3

	def read_data(self):
		# print(self.filename,self.dest_in)
		read_class = Read_ELF_Class(filename=self.filename,destination_in=self.dest_in)
		self.channel1,self.channel2 = read_class.read_and_save()

		# self.channel1,self.channel2 = [],[]
		# with open(self.filename,'r') as f:
		# 	lines = f.readlines()[1:]
		# for s in lines:
		# 	self.channel1.append(int(s[:s.find('\t')]))
		# 	self.channel2.append(int(s[s.find('\t')+1:]))

		return self.channel1,self.channel2,len(self.channel1)

	def channels_to_data(self):
		self.data = [sqrt(self.detrended1[i]*self.detrended1[i]+self.detrended2[i]*self.detrended2[i])
					 for i in range(self.N)]
		return self.data

	def filtering(self,data):
		b, a = signal.butter(N=3,Wn=[(50-0.5)/self.CONST_FN,(50+0.5)/self.CONST_FN],
							 btype='bandstop',analog=False)

		filtered1 = signal.lfilter(b, a, data)
		try:
			b, a = signal.butter(N=3,Wn=[(150-0.5)/self.CONST_FN,(150+0.5)/self.CONST_FN],
								 btype='bandstop',analog=False)
			filtered2 = signal.lfilter(b, a, filtered1)

			b, a = signal.butter(N=3,Wn=[(250-0.5)/self.CONST_FN,(250+0.5)/self.CONST_FN],
								 btype='bandstop',analog=False)
			filtered = signal.lfilter(b, a, filtered2)
		except ValueError:
			filtered = filtered1

		# if self.plot:
		# 	self.plot_filtering()

		return list(filtered)

	def plot_filtering(self):
		fig = plt.figure()

		ax1 = fig.add_subplot(2,1,1)
		ax1.semilogy(fft.rfftfreq(n=self.N,d=1/self.CONST_FS),
				abs(fft.rfft(self.data))**2,label='data',color='red')
		ax1.semilogy(fft.rfftfreq(n=self.N,d=1/self.CONST_FS),
				abs(fft.rfft(self.filtered))**2,label='filtered',color='blue')
		ax1.set_title('Spectum '+self.filename)
		ax1.set_xlabel('Freq, Hz')
		ax1.set_ylabel('log(W**2)')
		ax1.grid()
		ax1.legend()

		ax2 = fig.add_subplot(2,1,2)
		ax2.plot(self.t,
				self.data,label='data',color='red')
		ax2.plot(self.t,
				self.filtered,label='filtered',color='blue')
		ax2.set_title('Data '+self.filename)
		ax2.set_xlabel('Time, sec')
		ax2.set_ylabel('Amplitude')
		ax2.grid()
		ax2.legend()

		plt.subplots_adjust(hspace=0.4)
		plt.show()

	def detrending(self,filtered):
		# start_time = time.time()
		mov_avg = filtered[:self.DEGREE]
		detrended=[0]*self.DEGREE
		for i in range(self.DEGREE,self.N-self.DEGREE):
			chunk = filtered[i-self.DEGREE:i+self.DEGREE+1]
			chunk = sum(chunk)/len(chunk)
			mov_avg.append(chunk)
			detrended.append(filtered[i]-chunk)
		detrended = detrended+[0]*self.DEGREE
		mov_avg = mov_avg+filtered[-self.DEGREE:]
		# print('Time_Detrending: ',time.time()-start_time)
		return detrended,mov_avg

	def peaking(self,detrended):
		# start_time = time.time()
		peaked = detrended[:]
		# check = 10000
		# while check>10:
		# 	check = 0
		# 	std = nanstd(peaked)
		# 	for i in range(self.N):
		# 		if abs(peaked[i])>self.SIGMA*std:
		# 			peaked[i] = nan
		# 			check += 1
		# plt.plot(self.t,peaked,label='step 0')

		std0 = nanstd(peaked)
		# plt.axhline(std0,c='orange')
		# plt.axhline(-std0,c='orange')

		for i in range(self.N):
			if abs(peaked[i])>self.SIGMA*std0:
				peaked[i] = nan #self.SIGMA*std0*sign(peaked[i])
		# plt.plot(self.t,eaked,label='step 1')

		std1 = nanstd(peaked)
		# plt.axhline(std1,c='red')
		# plt.axhline(-std1,c='red')

		for i in range(self.N):
			if abs(peaked[i])>self.SIGMA*std1:
				peaked[i] = nan #self.SIGMA*std1*sign(peaked[i])
		# plt.plot(self.t,peaked,label='step 2')

		std2 = nanstd(peaked)
		# plt.axhline(std2,c='green')
		# plt.axhline(-std2,c='green')

		for i in range(self.N):
			if abs(peaked[i])>self.SIGMA*std2:
				peaked[i] = nan #self.SIGMA*std2*sign(peaked[i])
		# plt.plot(self.t,peaked,label='step 3')

		std3 = nanstd(peaked)
		# plt.axhline(std3,c='black')
		# plt.axhline(-std3,c='black')

		for i in range(self.N):
			if abs(peaked[i])>self.SIGMA*std3:
				peaked[i] = nan #self.SIGMA*std3*sign(peaked[i])
		# plt.plot(self.t,peaked,label='step 4')

		# plt.legend()
		# plt.grid()
		# plt.xlabel('Time, sec')
		# plt.ylabel('Amplitude')
		# plt.title('Peaking '+self.filename)
		# if self.plot:
		# 	plt.show()
		# print('Time_Peaking: ',time.time()-start_time)
		return std3

	def azimuth(self):
		if self.CONST_DELTAF==51.8:
			return [(arctan2(-self.detrended1[i],self.detrended2[i])/self.CONST_P+360)%360
					for i in range(self.N)], \
				   [((arctan2(-self.detrended1[i],self.detrended2[i])/self.CONST_P+360)%360+180)%360
					for i in range(self.N)]
		else:
			return [(arctan2(self.detrended1[i],self.detrended2[i])/self.CONST_P+360)%360
					for i in range(self.N)], \
				   [((arctan2(self.detrended1[i],self.detrended2[i])/self.CONST_P+360)%360+180)%360
					for i in range(self.N)]

	def plot_antennas(self):
		fig = plt.figure()
		time_array = [ti for ti in self.t if ti>self.time-10e-3 and ti<self.time+210e-3]
		start = self.t.index(time_array[0])
		end = self.t.index(time_array[-1])+1

		ax1 = fig.add_subplot(3,1,1)
		ax1.plot(time_array,[self.channel1[i]-self.mov_avg1[i] for i in range(start,end)],color='yellow',label='data')
		ax1.plot(time_array,self.detrended1[start:end],label='filter',color='red',marker='o',markersize=1.5)
		ax1.axhline(0,color='black')
		ax1.axvline(self.time,color='grey')
		ax1.axvline(self.time+self.dd,color='grey',linestyle=':')
		ax1.axvline(self.time+self.dn,color='grey',linestyle='--')
		ax1.axhline(self.std1,color='lightgreen',linestyle=':')
		ax1.axhline(-self.std1,color='lightgreen',linestyle=':')
		ax1.axhline(2*self.std1,color='lightsalmon',linestyle=':')
		ax1.axhline(-2*self.std1,color='lightsalmon',linestyle=':')
		ax1.axhline(3*self.std1,color='lightskyblue',linestyle=':')
		ax1.axhline(-3*self.std1,color='lightskyblue',linestyle=':')
		ax1.scatter(self.time_peak,self.detrended1[self.index],color='black',s=5,zorder=5)
		ax1.set_ylabel('Antenna NS')
		ax1.set_title(str('TGF'+str(self.id)+', '+str(self.datetime)+', '+'deg='+str(self.DEGREE)))
		ax1.legend(loc=1)
		ax1.set_xlim([time_array[0],time_array[-1]])

		ax2 = fig.add_subplot(3,1,2,sharex=ax1)
		ax2.plot(time_array,[self.channel2[i]-self.mov_avg2[i] for i in range(start,end)],color='yellow',label='data')
		ax2.plot(time_array,self.detrended2[start:end],label='filter',color='blue',marker='o',markersize=1.5)
		ax2.axhline(0,color='black')
		ax2.axvline(self.time,color='grey')
		ax2.axvline(self.time+self.dd,color='grey',linestyle=':')
		ax2.axvline(self.time+self.dn,color='grey',linestyle='--')
		ax2.axhline(self.std2,color='lightgreen',linestyle=':')
		ax2.axhline(-self.std2,color='lightgreen',linestyle=':')
		ax2.axhline(2*self.std2,color='lightsalmon',linestyle=':')
		ax2.axhline(-2*self.std2,color='lightsalmon',linestyle=':')
		ax2.axhline(3*self.std2,color='lightskyblue',linestyle=':')
		ax2.axhline(-3*self.std2,color='lightskyblue',linestyle=':')
		ax2.scatter(self.time_peak,self.detrended2[self.index],color='black',s=5,zorder=5)
		ax2.set_ylabel('Antenna EW')
		ax2.legend(loc=1)
		ax2.set_xlim([time_array[0],time_array[-1]])

		ax3 = fig.add_subplot(3,1,3,sharex=ax1)
		ax3.plot(time_array,self.total_data[start:end],color='green',label='total data',marker='o',markersize=1.5)
		ax3.axhline(0,color='black')
		ax3.axvline(self.time,color='grey')
		ax3.axvline(self.time+self.dd,color='grey',linestyle=':')
		ax3.axvline(self.time+self.dn,color='grey',linestyle='--')
		ax3.axhline(self.std_total,color='lightgreen',linestyle=':')
		ax3.axhline(2*self.std_total,color='lightsalmon',linestyle=':')
		ax3.axhline(3*self.std_total,color='lightskyblue',linestyle=':')
		ax3.scatter(self.time_peak,self.B,color='red',s=5,zorder=5)
		ax3.legend(loc=1)
		ax3.set_xlabel('Time, sec')
		ax3.set_ylabel('Total')
		ax3.set_xlim([time_array[0],time_array[-1]])

		plt.savefig(self.dest_img+'TGF'+str(self.id)+'_'+str(self.datetime)+'data.png',dpi=360)

	def find_peak(self):
		# start_time = time.time()
		res = []
		for i in range(self.N):
			if self.t[i]<=self.time+self.dd+self.CONST_INDENT/self.CONST_FS and \
			   self.t[i]>=self.time+self.dn-self.CONST_INDENT/self.CONST_FS:
				res.append(abs(self.total_data[i]))
		for i in range(self.N):
			if self.t[i]<=self.time+self.dd+self.CONST_INDENT/self.CONST_FS and \
			   self.t[i]>=self.time+self.dn-self.CONST_INDENT/self.CONST_FS:
				start = i
				break
		if res!=[]:
			peak = max(res)
			index = res.index(peak)+start
			time_peak = self.t[index]
		else:
			peak = -1
			index = 5000
			time_peak = 5000/self.CONST_FS
		# print('Time_Find_peak: ',time.time()-start_time)
		return peak,time_peak,index

	def data_processing(self):
		self.channel1,self.channel2,self.N = self.read_data()
		# self.channel1 = [chi/self.CONST_SCALE for chi in self. channel1]
		# self.channel2 = [chi/self.CONST_SCALE for chi in self. channel2]

		# t - time array
		self.t = [i*300./self.N for i in range(self.N)]

		# plt.clf()
		# plt.plot(self.t,self.channel1,color='blue',label='NS')
		# plt.plot(self.t,self.channel2,color='red',label='EW')
		# plt.legend()
		# plt.title('2008-11-13 07:40 ELA 7')
		# plt.ylabel('Amplitude')
		# plt.xlabel('Time, sec')
		# plt.show()

		# processing for channel1
		self.filtered1 = self.filtering(self.channel1)
		self.detrended1,self.mov_avg1 = self.detrending(self.filtered1)
		self.std1 = self.peaking(self.detrended1)

		# processing for channel2
		self.filtered2 = self.filtering(self.channel2)
		self.detrended2,self.mov_avg2 = self.detrending(self.filtered2)
		self.std2 = self.peaking(self.detrended2)

		# if self.plot:
		# 	self.plot_processing()

		# data = sqrt(channel1**2 + channel2**2)
		self.total_data = self.channels_to_data()
		self.std_total = self.peaking(self.total_data)
		# self.std_total = std(self.total_data)

		self.azimuth_positive,self.azimuth_negative = self.azimuth()
		self.B,self.time_peak,self.index = self.find_peak()

		if self.plot:
			self.plot_antennas()
			self.plot_processing()

		res = {
			'B': self.B/self.CONST_SCALE,
			'std': self.std_total/self.CONST_SCALE,
			'dd': self.dd,
			'dn': self.dn,
			'delta': self.time_peak-self.time
		}
		return res

	def plot_processing(self):
		fig = plt.figure()
		time_array = [ti for ti in self.t if ti>self.time-10e-3 and ti<self.time+210e-3]
		start = self.t.index(time_array[0])
		end = self.t.index(time_array[-1])+1

		ax1 = fig.add_subplot(3,1,1)
		ax1.plot(time_array,self.channel1[start:end],label='data',color='yellow')
		ax1.plot(time_array,self.filtered1[start:end],label='filtered',color='red')
		ax1.plot(time_array,self.mov_avg1[start:end],label='mov avg',color='black')
		ax1.set_title(str('TGF'+str(self.id)+', '+str(self.datetime)+', '+'deg='+str(self.DEGREE)+', A='+str(round(self.A))))

		ax1.axvline(self.time+self.dd,color='grey',linestyle=':')
		ax1.axvline(self.time+self.dn,color='grey',linestyle='--')
		ax1.axvline(self.time,color='grey')
		ax1.legend(loc=1)
		ax1.set_ylabel('Antenna NS')

		ax2 = fig.add_subplot(3,1,2,sharex=ax1)
		ax2.plot(time_array,self.channel2[start:end],label='data',color='yellow')
		ax2.plot(time_array,self.filtered2[start:end],label='filtered',color='blue')
		ax2.plot(time_array,self.mov_avg2[start:end],label='mov avg',color='black')
		ax2.axvline(self.time+self.dd,color='grey',linestyle=':')
		ax2.axvline(self.time+self.dn,color='grey',linestyle='--')
		ax2.axvline(self.time,color='grey')
		ax2.legend(loc=1)
		ax2.set_ylabel('Antenna EW')

		ax3 = fig.add_subplot(3,1,3,sharex=ax1)
		ax3.plot(time_array,self.azimuth_positive[start:end],color='black',label='CG+',marker='o',markersize=1.5)
		ax3.plot(time_array,self.azimuth_negative[start:end],color='violet',label='CG-',marker='o',markersize=1.5)
		ax3.axhline(self.A,label='TGF',color='lime',linewidth=2)
		ax3.axvline(self.time,color='grey')
		ax3.axvline(self.time+self.dd,color='grey',linestyle=':')
		ax3.axvline(self.time+self.dn,color='grey',linestyle='--')
		ax3.legend(loc=1)
		ax3.set_xlabel('Time, sec')
		ax3.set_ylabel('Azimuth, degree')
		ax3.set_xlim([time_array[0],time_array[-1]])

		plt.savefig(self.dest_img+'TGF'+str(self.id)+'_'+str(self.datetime)+'proc.png',dpi=360,textsize=10)

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
