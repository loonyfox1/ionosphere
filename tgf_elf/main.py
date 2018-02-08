from distance import Distance_Class
from terminator import Terminator_Class
from day_night_distance import Day_Night_Distance_Class
from charge_moment import Charge_Moment_Class
from time_delay import Time_Delay_Class
from elf_data_processing import ELF_Data_Processing_Class
import numpy as np
from argparse import ArgumentParser, ArgumentTypeError, RawDescriptionHelpFormatter
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from datetime import datetime as dt

EXTRA_HELP = """
Example usage:
python main.py -v -p -id 081113 -t 2008-11-13T07:44:04.238 -lat 2.89 -lon 7.33 -d /root/git/ionosphere/tgf_elf/ --degree 10 --sigma 3

"""


class Main_Class(object):
	def __init__(self,args):
		self.id = args.id
		self.datetime = args.datetime
		self.lat = args.lat
		self.lon = args.lon
		self.verbose = args.verbose
		self.plot = args.plot
		self.destination = args.dest
		self.degree = args.degree
		self.sigma = args.sigma
		self.dest_img = args.dest_img

	def constants(self):
		with open(self.destination+self.filename,'r') as f:
			s = f.readline()
		s = s[s.find('ELA')+3]
		if s=='7':
			return self.ELA7_constants,s
		elif s=='1':
			return self.ELA10_constants,s
		print('Error of header')
		return -1

	def ELA10_constants(self):
		# FS - sampling rate, Hz = 1/sec
		CONST_FS = 887.7841
		# FN - naquist frequency
		CONST_FN = CONST_FS/2
		# SCALE - full scale, pT/scale
		CONST_SCALE = 2**16/3353e-12
		# DELTAF - energy bandwidth of the receiver, Hz = 1/sec
		CONST_DELTAF = 304.9 # NOTE: clarify
		# HI - correction coefficient of lfilter
		CONST_HI = 1.02 # NOTE: one const for ELA7/10 ??
		# WN - parameter for Cheby filters
		CONST_WN1,CONST_WN2,CONST_WN3 = 443,334,334 # NOTE: clarify

		return CONST_FS,CONST_FN,CONST_SCALE,CONST_DELTAF, \
			   CONST_HI,CONST_WN1,CONST_WN2,CONST_WN3

	def ELA7_constants(self):
		# FS - sampling rate, Hz = 1/sec
		CONST_FS = 175.96
		# FN - naquist frequency
		CONST_FN = CONST_FS/2
		# SCALE - full scale, pT/scale
		CONST_SCALE = 2**16/3826e-12 # NOTE: WTF???????
		# DELTAF - energy bandwidth of the receiver, Hz = 1/sec
		CONST_DELTAF = 51.8
		# HI - correction coefficient of lfilter
		CONST_HI = 1.02 # NOTE: one const for ELA7/10 ??
		# WN - parameter for Cheby filters
		CONST_WN1,CONST_WN2,CONST_WN3 = 45,45,45 # NOTE: clarify

		return CONST_FS,CONST_FN,CONST_SCALE,CONST_DELTAF, \
			   CONST_HI,CONST_WN1,CONST_WN2,CONST_WN3

	def date_time(self):
		# 'yy-mm-ddTHH:MM:SS.SSS'
		print(self.datetime)
		self.year = int(self.datetime[:4])
		self.month = int(self.datetime[5:7])
		self.day = int(self.datetime[8:10])
		self.hour = int(self.datetime[11:13])
		self.minute = int(self.datetime[14:16])
		self.second = float(self.datetime[17:])
		self.utime = round(float(self.datetime[11:13])+float(self.datetime[14:16])/60+float(self.datetime[17:])/3600,2)
		return self.year,self.month,self.day,self.hour,self.minute,self.second,self.utime

	def info(self):
		print('\nTGF ID',self.id)
		print('ELF file',self.filename)
		print('Stantion ELA',self.s,'\n')

		print('Year ',self.year)
		print('Month',self.month)
		print('Day  ',self.day)
		print('UTime',self.utime,'h\n')

		print('TGF Lat',str(round(self.lat,1))+' N' if self.lat>0 else str(-round(self.lat,1))+' S')
		print('TGF Lon',str(round(self.lon,1))+' E\n' if self.lon>0 else str(-round(self.lon,1))+' W\n')

		print('Stantion Lat',str(round(self.lat_s,1))+' N' if self.lat_s>0 else str(-round(self.lat_s,1))+' S')
		print('Stantion Lon',str(round(self.lon_s,1))+' E\n' if self.lon_s>0 else str(-round(self.lon_s,1))+' W\n')

		print('Distance day  ',int(self.d[0][0]/1000) if self.d[0][1]==True  else int(self.d[1][0]/1000),'km')
		print('Distance night',int(self.d[0][0]/1000) if self.d[0][1]==False else int(self.d[1][0]/1000),'km\n')

		print('Sun lat',str(round(self.p0,1))+' N' if self.p0>0 else str(-round(self.p0,1))+' S')
		print('Sun lon',str(round(self.l0,1))+' E\n' if self.l0>0 else str(-round(self.l0,1))+' W\n')

		print('B pulse',round(self.B*1e12,3),'pT')
		print('Charge moment',round(self.p/1000,3),'C*km')

	def info_terminator(self):
		print('Lon\tLat\n')
		for i in range(len(self.lx)):
			print(self.lx[i],'\t',self.px[i])

	def plot_terminator(self):
		m = Basemap(projection='mill',lon_0=0)
		m.drawcoastlines()
		m.drawparallels(np.arange(-90,90,30), labels=[1,0,0,0])
		m.drawmeridians(np.arange(m.lonmin, m.lonmax+30,60), labels=[0,0,0,1])
		m.drawmapboundary(fill_color='aqua')
		m.fillcontinents(color='coral',lake_color='aqua')
		CS = m.nightshade(dt(self.year,self.month,self.day,
								   self.hour,self.minute))
		m.drawgreatcircle(self.lon_s,self.lat_s,self.lon,self.lat,
						  linewidth=2, color='b')
		plt.title('Day/Night Map for %s' % self.datetime[:10]+' '+self.datetime[11:])
		plt.show()

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

		return str(self.year)+smonth+sday+shour+sminute+'.dat'

	def time_to_sec(self):
		return self.minute%5*60+self.second

	def main(self):
		self.year,self.month,self.day,self.hour,self.minute, \
				  self.second,self.utime = self.date_time()

		# find elf filename for tgf (data in decimal format !!!)
		self.filename = self.find_filename()

		# define the constants of stantion
		self.stantion,self.s = self.constants()

		self.lon_s = 22.55
		self.lat_s = 49.19

		# define coordinates of terminator
		terminator_class = Terminator_Class(
				utime=self.utime,year=self.year,month=self.month,day=self.day)
		self.l0,self.p0,self.lx,self.px = terminator_class.terminator()

		# define distance in day/night, azimuth
		day_night_distance_class = Day_Night_Distance_Class(
				slat1=self.lat,slon1=self.lon,flat1=self.lat_s,flon1=self.lon_s,
				lambda0=self.l0,phi0=self.p0,lambdax=self.lx,phix=self.px)
		self.d,self.A = day_night_distance_class.day_night_distance()

		# define day/night time delay
		time_delay_class = Time_Delay_Class(r=self.d[0][0]+self.d[1][0])
		dd,dn = time_delay_class.time_delay()

		# processing data and define B
		elf_data_processing_class = ELF_Data_Processing_Class(
				filename=self.destination+self.filename,delta_day=dd,delta_night=dn,
				time=self.time_to_sec(),A=self.A,stantion=self.stantion,
				degree=self.degree,sigma=self.sigma,plot=self.plot,
				idd=self.id,datetime=self.datetime,dest_img=self.dest_img)
		# self.B = elf_data_processing_class.data_processing()
		elf_data_processing_class.data_processing()

		# calculate charge moment p
		# charge_moment_class = Charge_Moment_Class(B=self.B,d=self.d,
		# 										  stantion=self.stantion)
		# self.p = charge_moment_class.charge_moment()
		# if not self.verbose:
		# 	print('\np =',self.p/1000,'C*km')
		# return self.p

if __name__ == '__main__':
	parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
			 description='Automated script for analysis of ELF electromaghetic \
			 field pulses', add_help=True, usage=EXTRA_HELP)

	parser.add_argument("-v", "--verbose", dest="verbose", action="store_true",
						help="If set, verbose information output")
	parser.add_argument("-p", "--plot", dest="plot", action="store_true",
						help="If set, graphs output")

	parser.add_argument("-id", "--id", dest="id", type=str, default='0',
						help="ID of TGF pulse in the catalogue")

	parser.add_argument("-t", "--datetime", dest="datetime", type=str,
						help="Datetime of TGF pulse")

	parser.add_argument("-lat", "--lat", dest="lat", type=float,
						help="Latitude of TGF pulse")

	parser.add_argument("-lon", "--lon ", dest="lon", type=float,
						help="Longitude of TGF pulse")

	parser.add_argument("-d", "--dest", dest="dest", type=str, default='',
							help="Destination folder of ELF data")

	parser.add_argument("-g", "--degree", dest="degree", type=int, default=10,
						help="Parameter of detrending with moving average")

	parser.add_argument("-s", "--sigma", dest="sigma", type=float, default=3,
						help="Filtering of noise parameter")

	args = parser.parse_args()
	main_class = Main_Class(args)
	res = main_class.main()
	if args.verbose:
		main_class.info()
	if args.plot:
		main_class.plot_terminator()
