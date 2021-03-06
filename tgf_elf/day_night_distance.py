from __future__ import division
from __future__ import print_function
from numpy import pi,sin,cos,arctan2
from distance import Distance_Class
from terminator import Terminator_Class


class Day_Night_Distance_Class(object):
	# P = pi/180
	CONST_P = pi/180

	def __init__(self,slat1,slon1,flat1,flon1,
					  lambda0,phi0,lambdax,phix):
		self.slat1 = round(slat1,1)
		self.slon1 = round(slon1,1)
		self.flat1 = round(flat1,1)
		self.flon1 = round(flon1,1)
		self.lambda0 = lambda0
		self.phi0 = phi0
		self.lambdax = lambdax
		self.phix = phix

	def find_point(self,lon):
		for i in range(len(self.lambdax)):
			if self.lambdax[i]==lon:
				return self.phix[i],self.lambdax[i]

	def terminator_points(self):
		self.slat2,self.slon2 = self.find_point(self.slon1)
		self.flat2,self.flon2 = self.find_point(self.flon1)
		return self.slat2,self.slon2,self.flat2,self.flon2

	def day_or_night(self,lat,lon):
		U = sin(lat*self.CONST_P)*sin(self.phi0*self.CONST_P) + \
			cos(lat*self.CONST_P)*cos(self.phi0*self.CONST_P)* \
			cos((lon-self.lambda0)*self.CONST_P)
		if U<0:
			return False
		else:
			return True

	def azimuth(self):
		x = sin((self.slon1-self.flon1)*self.CONST_P)* \
			cos(self.slat1*self.CONST_P)
		y = cos(self.flat1*self.CONST_P)*sin(self.slat1*self.CONST_P)- \
			sin(self.flat1*self.CONST_P)*cos(self.slat1*self.CONST_P)* \
			cos((self.slon1-self.flon1)*self.CONST_P)
		A = arctan2(x,y)/self.CONST_P
		# NOTE: CHECK!!! 
		return (A+360)%360

	def intersection_point(self):
		# NOTE: costul'
		if self.flon1==self.slon1: self.slon1 += 0.01
		if self.flat1==self.slat1: self.slat1 += 0.01
		if self.flon2==self.slon2: self.slon2 += 0.01
		if self.flat2==self.slat2: self.slat2 += 0.01

		t2 = -((self.flat1 - self.slat1) * (self.slon1 - self.slon2) - \
			  (self.slat2 - self.slat1) * (self.flon1 - self.slon1))/ \
			 ((self.flat1 - self.slat1) * (self.flon2 - self.slon2) - \
			  (self.flon1 - self.slon1) * (self.flat2 - self.slat2))

		if t2>=0 and t2<=1:
			t1 = (self.slat2 - self.slat1) / (self.flat1 - self.slat1) + \
			  t2*(self.flat2 - self.slat2) / (self.flat1 - self.slat1)
			if t1>=0 and t1<=1:
				return self.slat1 + (self.flat1 - self.slat1)*t1, \
					   self.slon1 + (self.flon1 - self.slon1)*t1
		return -1,-1

	def day_night_distance(self):
		self.slat2,self.slon2,self.flat2,self.flon2 = self.terminator_points()
		self.lat,self.lon = self.intersection_point()
		self.A = self.azimuth()
		if self.lat==-1 and self.lon==-1:
			day = self.day_or_night(self.slat1,self.slon1)
			r = Distance_Class(self.slat1,self.slon1,
							   self.flat1,self.flon1).distance()
			return [[r,day],[0,not day]],self.A
		day1 = self.day_or_night(self.slat1,self.slon1)
		day2 = self.day_or_night(self.flat1,self.flon1)
		r1 = Distance_Class(self.slat1,self.slon1,
							self.lat,self.lon).distance()
		r2 = Distance_Class(self.lat,self.lon,
							self.flat1,self.flon1).distance()
		if day1!=day2:
			return [[r1,day1],[r2,day2]],self.A
		print('Error day night distance')
		return -1

if __name__ == '__main__':
	# latitude  N +, S -
	# longitude E +, W -

	slat1 = -5.25
	slon1 = 24

	flat1 = 49.19
	flon1 = 22.55

	utime = 12
	year = 2009
	month = 5
	day = 10

	terminator_class = Terminator_Class(utime=utime,year=year,month=month,day=day)
	l0,p0,lx,px = terminator_class.terminator()
	day_night_distance_class = Day_Night_Distance_Class(slat1=slat1,slon1=slon1,
				  flat1=flat1,flon1=flon1,lambda0=l0,phi0=p0,lambdax=lx,phix=px)
	res,A = day_night_distance_class.day_night_distance()
	# print ('d =',res)
	# print('A =',A)
