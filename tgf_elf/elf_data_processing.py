from __future__ import division
from __future__ import print_function
from read_elf_file import Read_ELF_Class
from numpy import pi,sqrt,fft,nanstd,nan,arctan2,abs
from scipy import signal
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class ELF_Data_Processing_Class(object):
	CONST_P = np.pi/180

	def __init__(self,filename,delta_day,delta_night,time,atgf,args):
		self.args = args
		self.atgf = atgf
		self.filename = filename
		self.dd = delta_day #+ 1/self.CONST_DELTAF
		self.dn = delta_night #+ 1/self.CONST_DELTAF
		self.time = time + 1/self.args['CONST_DELTAF']
		if self.args['ela']==10:
			if int(self.filename[5:13])>=20130401 and \
			   int(self.filename[5:13])<=20131130:
				self.args['CONST_SCALE'] = self.args['CONST_SCALE'][1]
			else:
				self.args['CONST_SCALE'] = self.args['CONST_SCALE'][0]

	def plot_peak(self):
		CONST_SCALE = self.args['CONST_SCALE']
		font = {'size'   : 3}
		mpl.rc('font', **font)
		mpl.rcParams['axes.linewidth'] = 0.3
		mpl.rcParams['lines.linewidth'] = 0.3
		mpl.rcParams['xtick.direction'] = 'in'
		mpl.rcParams['ytick.direction'] = 'in'
		mpl.rcParams['xtick.top'] = True
		mpl.rcParams['ytick.right'] = True
		mpl.rcParams['xtick.major.size'] = 2
		mpl.rcParams['ytick.major.size'] = 2
		mpl.rcParams['xtick.major.width'] = 0.3
		mpl.rcParams['ytick.major.width'] = 0.3

		if self.args['ela']==7:
			time_array = [ti for ti in self.t if ti>=self.time-200e-3 and ti<self.time+600e-3]
		else:
			time_array = [ti for ti in self.t if ti>=self.time-40e-3 and ti<self.time+120e-3]
		start = self.t.index(time_array[0])
		end = self.t.index(time_array[-1])+1
		timex = [(t-self.time)*1e3 for t in time_array]

		fig = plt.figure(figsize=(3,4))

		ax1 = fig.add_subplot(4,1,1)
		ax1.plot(timex,np.array(self.detrended_x[start:end])/CONST_SCALE/1e-12,color='red')
		ax1.axhline(3*self.std_x/CONST_SCALE/1e-12,color='gray',linestyle='dotted')
		ax1.axhline(-3*self.std_x/CONST_SCALE/1e-12,color='gray',linestyle='dotted')
		ax1.scatter(timex[self.index-start],np.array(self.detrended_x[self.index])/CONST_SCALE/1e-12,
					facecolors='none',edgecolors='orange',marker='o',s=2,linewidths=0.6,zorder=3)
		ax1.scatter(timex[self.index-start],np.array(self.detrended_x[self.index])/CONST_SCALE/1e-12,
					facecolors='none',edgecolors='black',marker='o',s=0.2,linewidths=0.3,zorder=3)
		ax1.set_ylabel('Bx [pT]')

		ax2 = fig.add_subplot(4,1,2,sharey=ax1)
		ax2.plot(timex,np.array(self.detrended_y[start:end])/CONST_SCALE/1e-12,color='blue')
		ax2.axhline(3*self.std_y/CONST_SCALE/1e-12,color='gray',linestyle='dotted')
		ax2.axhline(-3*self.std_y/CONST_SCALE/1e-12,color='gray',linestyle='dotted')
		ax2.scatter(timex[self.index-start],np.array(self.detrended_y[self.index])/CONST_SCALE/1e-12,
					facecolors='none',edgecolors='orange',marker='o',s=2,linewidths=0.6,zorder=3)
		ax2.scatter(timex[self.index-start],np.array(self.detrended_y[self.index])/CONST_SCALE/1e-12,
					facecolors='none',edgecolors='black',marker='o',s=0.2,linewidths=0.3,zorder=3)
		ax2.set_ylabel('By [pT]')

		ax3 = fig.add_subplot(4,1,3)
		ax3.plot(timex,np.array(self.total_data[start:end])/CONST_SCALE/1e-12,color='black')
		ax3.axhline(3*self.std_total/CONST_SCALE/1e-12,color='gray',linestyle='dotted')
		# ax3.axhline(-3*self.std_total/CONST_SCALE/1e-12,color='gray',linestyle='dotted')
		ax3.scatter(timex[self.index-start],np.array(self.total_data[self.index])/CONST_SCALE/1e-12,
					facecolors='none',edgecolors='orange',marker='o',s=2,linewidths=0.6,zorder=3)
		ax3.scatter(timex[self.index-start],np.array(self.total_data[self.index])/CONST_SCALE/1e-12,
					facecolors='none',edgecolors='black',marker='o',s=0.2,linewidths=0.3,zorder=3)
		ax3.set_ylabel('B [pT]')

		ax4 = fig.add_subplot(4,1,4)
		ax4.plot(timex,self.azimuth_positive[start:end],color='violet',label='CG+')
		ax4.plot(timex,self.azimuth_negative[start:end],color='green',label='CG-')
		ax4.scatter(timex[self.index-start],np.array(self.azimuth_positive[self.index]),
					facecolors='none',edgecolors='orange',marker='o',s=2,linewidths=0.6,zorder=3)
		ax4.scatter(timex[self.index-start],np.array(self.azimuth_positive[self.index]),
					facecolors='none',edgecolors='black',marker='o',s=0.2,linewidths=0.3,zorder=3)
		ax4.scatter(timex[self.index-start],np.array(self.azimuth_negative[self.index]),
					facecolors='none',edgecolors='orange',marker='o',s=2,linewidths=0.6,zorder=3)
		ax4.scatter(timex[self.index-start],np.array(self.azimuth_negative[self.index]),
					facecolors='none',edgecolors='black',marker='o',s=0.2,linewidths=0.3,zorder=3)
		ax4.axhline(self.atgf,color='gray',label='TGF')
		# ax4.text(0,self.atgf,'TGF',color='gray',fontsize=3)
		ax4.set_ylabel('Azimuth [degree]')
		ax4.legend(loc=4,framealpha=1)

		axarr = [ax1,ax2,ax3,ax4]

		ax3.set_xlabel('ATGF='+str(round(self.atgf,1))+', A(CG+/CG-)='+str(round(self.azimuth_positive[self.index],1))+'/'+ \
															  str(round(self.azimuth_negative[self.index],1)))
		ax4.set_xlabel('Time after '+self.sec_to_str(self.time-1/self.args['CONST_DELTAF'])+' UT [ms]')
		ax1.set_title('TGF'+str(self.args['id'])+', '+str(self.args['timestamp']))

		if self.args['ela']==7:
			[a.set_xticks(np.arange(-200,601,50)) for a in axarr]
		else:
			[a.set_xticks(np.arange(-40,121,10)) for a in axarr]

		[a.margins(0,0.1) for a in axarr[:-1]]
		ax4.margins(0,0.05)

		[a.axvline(0,c='gray',zorder=1,linestyle='dashed') for a in axarr]
		[a.axhline(0,c='gray',zorder=1,linestyle='dashed') for a in axarr[:2]]

		[a.axvline((self.dd)*1e3,c='gray',linestyle='dashed',zorder=1) for a in axarr]
		[a.axvline((self.dn)*1e3,c='gray',linestyle='dashed',zorder=1) for a in axarr]

		ax1.text((self.dd)*1e3,ax1.get_ylim()[1]*0.6,'day',rotation='vertical',color='grey',
				fontsize=2,ha='left',va='bottom')
		ax1.text((self.dn)*1e3,ax1.get_ylim()[1]*0.6,'night',rotation='vertical',color='grey',
				fontsize=2,ha='right',va='bottom')

		fig.subplots_adjust(top=0.91, bottom=0.08, left=0.12, right=0.95, hspace=0.4,
						wspace=None)
		if len(str(self.args['id']))<4:
			sid = ''
			for i in range(4-len(str(self.args['id']))):
				sid += '0'
			sid += str(self.args['id'])
		else:
			sid = str(self.args['id'])

		plt.savefig(self.args['dest_img']+'TGF'+sid,dpi=700)

	def sec_to_str(self,sec):
		res = self.filename[-8:-6]+':'+str(int(self.filename[-6:-4])+int(sec//60.))+':'+ \
			  str(round(sec%60.,3))
		return res

	def check_stantion(self):
		with open(self.args['dest_txt']+self.filename,'r') as f:
			s = str(f.read(46))
		s = s[s.find('ELA')+3:s.find('ELA')+5]
		if str(self.args['ela'])==s or str(self.args['ela'])==s[0]:
			return True
		else:
			print('ID '+str(self.args['id'])+': error of header '+self.filename)
			return False

	def read_data(self):
		channel_x,channel_y = None,None
		if os.path.exists(self.args['dest_txt']+self.filename):
			channels = pd.read_table(self.args['dest_txt']+self.filename,sep='\t',
								     names=['x','y'],skiprows=[0])
			channel_x = np.array(channels.x)
			channel_y = np.array(channels.y)
		else:
			try:
				read_class = Read_ELF_Class(filename=self.filename,
											destination_in=self.args['dest_bin'],
											destination_out=self.args['dest_txt'])
				channel_x,channel_y = read_class.read()
			except:
				# print('ID '+str(self.args['id'])+': file '+self.filename+' did not find')
				return None,None,None
		if not self.check_stantion():
			return None,None,None

		N = len(channel_x)
		# NS antenna placement for Ela 7
		return channel_x*self.args['NS_COEFF'],channel_y,N

	def filtering(self,data):
		CONST_FN = self.args['CONST_FN']

		b, a = signal.butter(N=3,Wn=[(50-0.5)/CONST_FN,(50+0.5)/CONST_FN],
							 btype='bandstop',analog=False)

		filtered1 = signal.lfilter(b, a, data)
		try:
			b, a = signal.butter(N=3,Wn=[(150-0.5)/CONST_FN,(150+0.5)/CONST_FN],
								 btype='bandstop',analog=False)
			filtered2 = signal.lfilter(b, a, filtered1)

			b, a = signal.butter(N=3,Wn=[(250-0.5)/CONST_FN,(250+0.5)/CONST_FN],
								 btype='bandstop',analog=False)
			filtered = signal.lfilter(b, a, filtered2)
		except ValueError:
			filtered = filtered1

		return list(filtered)

	def detrending(self,filtered,degree):
		mov_avg = filtered[:degree]
		detrended=[0]*degree

		for i in range(degree,self.N-degree):
			chunk = filtered[i-degree:i+degree+1]
			chunk = sum(chunk)/len(chunk)
			mov_avg.append(chunk)
			detrended.append(filtered[i]-chunk)

		detrended = np.array(detrended+[0]*degree)
		mov_avg = mov_avg+filtered[-degree:]
		detrended[detrended==0] = 1e-9
		return detrended,mov_avg

	def sigma_clipping(self,detrended,sigma):
		peaked = np.array(detrended[:])

		for j in range(self.args['sigma_iter']):
			std = nanstd(peaked)
			for i in range(self.N):
				if abs(peaked[i])>sigma*std:
					peaked[i] = nan
		return std

	def channels_to_data(self):
		data = np.array([sqrt(self.detrended_x[i]*self.detrended_x[i]+ \
							  self.detrended_y[i]*self.detrended_y[i])
						 for i in range(self.N)])
		data[data==0] = 1e-9
		std_total = [np.sqrt((self.detrended_x[i]/data[i]*self.std_x)**2 + \
							 (self.detrended_y[i]/data[i]*self.std_y)**2)
							  for i in range(len(data))]
		std_total = (np.nanmax(std_total)-np.nanmin(std_total))/2+np.nanmin(std_total)
		return data,std_total

	def find_peak(self):
		CONST_INDENT = self.args['CONST_INDENT']
		CONST_FS = self.args['CONST_FS']
		res = []
		for i in range(self.N):
			if self.t[i]<=self.time+self.dd+CONST_INDENT/CONST_FS and \
			   self.t[i]>=self.time+self.dn-CONST_INDENT/CONST_FS:
				res.append(abs(self.total_data[i]))
		for i in range(self.N):
			if self.t[i]<=self.time+self.dd+CONST_INDENT/CONST_FS and \
			   self.t[i]>=self.time+self.dn-CONST_INDENT/CONST_FS:
				start = i
				break
		if res!=[]:
			peak = max(res)
			index = res.index(peak)+start
			time_peak = self.t[index]
		else:
			peak = -1
			index = 5000
			time_peak = 5000/CONST_FS
		return peak,time_peak,index

	def azimuth(self):
		az_pos_array = []
		az_neg_array = []

		for i in range(self.N):
			xx = self.detrended_x[i]
			yy = self.detrended_y[i]

		# positive discharge ==========================================
			if   xx>=0 and yy<=0:
				az_pos = np.rad2deg(np.arctan(np.abs(xx)/np.abs(yy)))
			elif xx<=0 and yy<=0:
				az_pos = 360 - np.rad2deg(np.arctan(np.abs(xx)/np.abs(yy)))
			elif xx<=0 and yy>=0:
				az_pos = 180 + np.rad2deg(np.arctan(np.abs(xx)/np.abs(yy)))
			elif xx>=0 and yy>=0:
				az_pos = 180 - np.rad2deg(np.arctan(np.abs(xx)/np.abs(yy)))
			else:
				print("Quadrant is not defined")

		# negative discharge ==========================================
			xx = -xx
			yy = -yy

			if   xx>=0 and yy<=0:
				az_neg = np.rad2deg(np.arctan(np.abs(xx)/np.abs(yy)))
			elif xx<=0 and yy<=0:
				az_neg = 360 - np.rad2deg(np.arctan(np.abs(xx)/np.abs(yy)))
			elif xx<=0 and yy>=0:
				az_neg = 180 + np.rad2deg(np.arctan(np.abs(xx)/np.abs(yy)))
			elif xx>=0 and yy>=0:
				az_neg = 180 - np.rad2deg(np.arctan(np.abs(xx)/np.abs(yy)))
			else:
				print("Quadrant is not defined")

			az_pos_array.append(az_pos)
			az_neg_array.append(az_neg)

		return az_pos_array, az_neg_array


	def data_processing(self):
		self.channel_x,self.channel_y,self.N = self.read_data()

		if self.channel_x is None:
			return None

		# t - time array
		self.t = [i*300./self.N for i in range(self.N)]

		# processing for channel_x
		self.filtered_x = self.filtering(self.channel_x)
		self.detrended_x,self.mov_avg_x = self.detrending(self.filtered_x,self.args['degree_x'])
		self.std_x = self.sigma_clipping(self.detrended_x,self.args['sigma_x'])

		# processing for channel_y
		self.filtered_y = self.filtering(self.channel_y)
		self.detrended_y,self.mov_avg_y = self.detrending(self.filtered_y,self.args['degree_y'])
		self.std_y = self.sigma_clipping(self.detrended_y,self.args['sigma_y'])

		# data = sqrt(channel_x**2 + channel_y**2)
		self.total_data,self.std_total = self.channels_to_data()

		self.azimuth_positive,self.azimuth_negative = self.azimuth()
		self.B,self.time_peak,self.index = self.find_peak()

		result = {
			'B': self.B/self.args['CONST_SCALE'],
			'std': self.std_total/self.args['CONST_SCALE'],
			'dd': self.dd,
			'dn': self.dn,
			'delta': self.time_peak-self.time,
			'Ap': self.azimuth_positive[self.index],
			'An': self.azimuth_negative[self.index],
		}

		self.plot_peak()

		return result
