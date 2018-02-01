from distance import Distance_Class
from terminator import Terminator_Class
from day_night_distance import Day_Night_Distance_Class
from charge_moment import Charge_Moment_Class
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from datetime import datetime as dt

class Main_Class(object):
	def __init__(self,ID,datetime,lon,lat,B):
		self.id = ID
		self.datetime = datetime
		self.lat = lat
		self.lon = lon
		self.B = B

	def date_time(self):
		# 'yy-mm-ddTHH:MM:SS.SSS'
		self.year = int(self.datetime[:4])
		self.month = int(self.datetime[5:7])
		self.day = int(self.datetime[8:10])
		self.hour = int(self.datetime[11:13])
		self.minute = int(self.datetime[14:16])
		self.utime = round(float(self.datetime[11:13])+float(self.datetime[14:16])/60+float(self.datetime[17:])/3600,2)
		return self.year,self.month,self.day,self.hour,self.minute,self.utime

	def info(self):
		print('ID',self.id,'\n')

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

	def main(self):
		self.year,self.month,self.day,self.hour,self.minute,self.utime = self.date_time()

		self.lon_s = 22.55
		self.lat_s = 49.19

		terminator_class = Terminator_Class(
				utime=self.utime,year=self.year,month=self.month,day=self.day)
		self.l0,self.p0,self.lx,self.px = terminator_class.terminator()

		day_night_distance_class = Day_Night_Distance_Class(
				slat1=self.lat,slon1=self.lon,flat1=self.lat_s,flon1=self.lon_s,
				lambda0=self.l0,phi0=self.p0,lambdax=self.lx,phix=self.px)
		self.d = day_night_distance_class.day_night_distance()

		charge_moment_class = Charge_Moment_Class(B=self.B,d=self.d)
		self.p = charge_moment_class.charge_moment()
		self.dd,self.dn = charge_moment_class.time_delay()

		return self.p

if __name__ == '__main__':
	ID = '090510'
	datetime = '2009-05-10T11:57:15.985'
	lat = -5.25
	lon = 24.08
	B = 4.5e-12

	main_class = Main_Class(ID=ID,datetime=datetime,lon=lon,lat=lat,B=B)
	res = main_class.main()
	main_class.info()
	main_class.plot_terminator()
