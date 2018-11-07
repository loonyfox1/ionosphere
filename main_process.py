from __future__ import print_function
from __future__ import division
from distance import Distance_Class
from terminator import Terminator_Class
from day_night_distance import Day_Night_Distance_Class
from charge_moment import Charge_Moment_Class
from time_delay import Time_Delay_Class
from elf_data_processing import ELF_Data_Processing_Class
import time

class Main_Class(object):
	def __init__(self, args):
		self.args = args
		self.year,self.month,self.day,self.hour, \
			 self.minute,self.second,self.utime = self.date_time()
		self.filename = self.find_filename()

	def print_info(self):
		print('-----------------------------')
		print('\nTGF ID',self.args['id'])
		print('ELF file',self.filename)
		print('Stantion ELA',self.s,'\n')

		print('Year ',self.year)
		print('Month',self.month)
		print('Day  ',self.day)
		print('UTime',self.utime,'h\n')

		print('TGF Lat',str(round(self.lat,1))+' N' if self.args['lat']>0 else str(-round(self.lat,1))+' S')
		print('TGF Lon',str(round(self.lon,1))+' E\n' if self.args['lon']>0 else str(-round(self.lon,1))+' W\n')

		print('Stantion Lat',str(round(self.lat_s,1))+' N' if self.lat_s>0 else str(-round(self.lat_s,1))+' S')
		print('Stantion Lon',str(round(self.lon_s,1))+' E\n' if self.lon_s>0 else str(-round(self.lon_s,1))+' W\n')

		print('Distance day  ',int(self.d[0][0]/1000) if self.d[0][1]==True  else int(self.d[1][0]/1000),'km')
		print('Distance night',int(self.d[0][0]/1000) if self.d[0][1]==False else int(self.d[1][0]/1000),'km\n')

		print('Day   delay',round(self.dd*1000,3),'ms')
		print('Night delay',round(self.dn*1000,3),'ms\n')

		print('B noise',round(self.std*1e12,3),'pT')
		print('B pulse',round(self.B*1e12,3),'pT\n')

		print('c(r)',round(self.c*1e17,4),'e-17')
		print('Charge moment',round(self.p/1000,3),'C*km\n')

	def find_filename(self):
		if self.month<10: smonth = '0'+str(self.month)
		else: smonth = str(self.month)

		if self.day<10: sday = '0'+str(self.day)
		else: sday = str(self.day)

		if self.hour<10: shour = '0'+str(self.hour)
		else: shour = str(self.hour)

		sminute = self.minute//5*5
		if sminute<10: sminute = '0'+str(sminute)
		else: sminute = str(sminute)

		return str(self.year)+'/'+ \
			   str(self.year)+smonth+sday+'/'+ \
			   str(self.year)+smonth+sday+shour+sminute+'.dat'

	def time_to_sec(self):
		return self.minute%5*60+self.second

	def date_time(self):
		# 'yy-mm-ddTHH:MM:SS.SSS'
		self.year = int(self.args['timestamp'][:4])
		self.month = int(self.args['timestamp'][5:7])
		self.day = int(self.args['timestamp'][8:10])
		self.hour = int(self.args['timestamp'][11:13])
		self.minute = int(self.args['timestamp'][14:16])
		self.second = float(self.args['timestamp'][17:])
		self.utime = round(float(self.args['timestamp'][11:13])+ \
						   float(self.args['timestamp'][14:16])/60+ \
						   float(self.args['timestamp'][17:])/3600,2)
		return self.year,self.month,self.day,self.hour,self.minute,self.second,self.utime

	def main(self):
		start_time = time.time()

		# define coordinates of terminator
		terminator_class = Terminator_Class(
				utime=self.utime,year=self.year,month=self.month,day=self.day)
		self.l0,self.p0,self.lx,self.px = terminator_class.terminator()

		# define distance in day/night, azimuth
		day_night_distance_class = Day_Night_Distance_Class(
				slat1=self.args['lat'],slon1=self.args['lon'],
				flat1=self.args['lat_s'],flon1=self.args['lon_s'],
				lambda0=self.l0,phi0=self.p0,lambdax=self.lx,phix=self.px)
		self.d,self.ATGF = day_night_distance_class.day_night_distance()

		# define day/night time delay
		time_delay_class = Time_Delay_Class(r=self.d[0][0]+self.d[1][0])
		self.dd,self.dn = time_delay_class.time_delay()

		# processing data and define B
		elf_data_processing_class = ELF_Data_Processing_Class(
				filename=self.filename,delta_day=self.dd,delta_night=self.dn,
				time=self.time_to_sec(),atgf=self.ATGF,args=self.args)
		res = elf_data_processing_class.data_processing()

		if res is None:
			return None

		self.delta = res['delta']
		self.dd = res['dd']
		self.dn = res['dn']
		self.B = res['B']
		self.std = res['std']
		self.Ap = res['Ap']
		self.An = res['An']

		# calculate charge moment
		charge_moment_class = Charge_Moment_Class(B=self.B,d=self.d,args=self.args)
		self.p,self.c = charge_moment_class.charge_moment()

		if self.args['verbose']:
			self.print_info()

		if self.d[0][1]==True:
			dayd = float(self.d[0][0])
		else:
			dayd = -float(self.d[1][0])
		result = {'ID': self.args['id'],
				  'LON': self.args['lon'],
				  'LAT': self.args['lat'],
				  'TIMESTAMP': self.args['timestamp'],
				  'COUNTS': self.args['counts'],
				  'GEOG': self.args['geog'],
				  'DUR': self.args['dur'][0],
				  'DIST': int((self.d[0][0]+self.d[1][0])/1000),
				  'DC': round(dayd/(float(self.d[0][0])+float(self.d[1][0])),2),
				  'DD': int(self.dd*1000),
				  'DN': int(self.dn*1000),
				  'DELTA': int(self.delta*1000),
				  'BP': round(self.B*1e12,1),
				  'BN': round(self.std*1e12,1),
				  'CR': round(self.c*1e17,4),
				  'P': round(self.p/1000,2),
				  'PMIN': round(self.std/self.c/1000,3),
				  'AP': int(self.Ap),
				  'AN': int(self.An),
				  'ATGF': int(self.ATGF),
				  }
		print('ID '+str(self.args['id'])+': done')
		# print('ID '+str(self.args['id'])+', time: ',time.time()-start_time)
		return result
