import numpy as np

class Terminator_Class(object):
    # P = pi/180
    CONST_P = np.pi/180
    # WTF ???
    CONST_OMEGA = 1.002737909350795

    def __init__(self,utime,year,month,day):
        self.utime = utime
        self.year = year
        self.month = month
        self.day = day

    def modified_julian_date(self):
        return 367*self.year-int(7*(self.year+int((self.month+9)/12))/4) + \
               int(275*self.month/9) + self.day-678987

    def t(self):
        self.jdate = self.modified_julian_date()
        return (self.jdate - 51544.5)/36525

    def geo_sun_vector(self):
        W = (357.528 + 35999.05*self.T + 0.04107*self.utime)*self.CONST_P
        L = (280.46 + 36000.772*self.T + 0.04107*self.utime + \
             (1.915 - 0.0048*self.T)*np.sin(W) + 0.02*np.sin(2*W))*self.CONST_P
        return np.cos(L),np.sin(L),0

    def equ_sun_vector(self):
        # epsilon - inclination of ecliptic to equator
        epsilon = (84381.488 - 46.815*self.T - 0.00059*self.T**2 + \
                   0.001813*self.T**3)/3600*self.CONST_P
        X,Y,Z = self.geo_sun_vector()
        return X, Y*np.cos(epsilon)-Z*np.sin(epsilon), \
                  Y*np.sin(epsilon)+Z*np.cos(epsilon)

    def avg_stars_time(self):
        self.T = self.t()
        # S0 - gst at midnight in seconds
        S0 = 24110.54841 + 8640184.812*self.T + 0.093104*self.T**2 - \
             0.0000062*self.T**3
        deltaT = self.utime/24*86400*self.CONST_OMEGA
        return (S0+deltaT)/240*self.CONST_P

    def gsc_sun_vector(self):
        # stime - star time
        self.stime = self.avg_stars_time()
        X,Y,Z = self.equ_sun_vector()
        return X*np.cos(self.stime)+Y*np.sin(self.stime), \
              -X*np.sin(self.stime)+Y*np.cos(self.stime),Z

    def angulation(self):
        X,Y,Z = self.gsc_sun_vector()
        return np.arctan2(Y,X)/self.CONST_P, \
               np.arctan2(Z,np.sqrt(X**2+Y**2))/self.CONST_P

    def terminator(self):
        # lambda0, phi0 - Sun's coordinates on Earth
        lambda0,phi0 = self.angulation()
        step = 0.1
        lambdax = [-180+i*step for i in range(0,int(360/step)+1)]
        phix = [np.arctan(-np.cos((lx-lambda0)*self.CONST_P)/
                np.tan(phi0*self.CONST_P))/self.CONST_P for lx in lambdax]
        return lambdax, phix

if __name__ == '__main__':
    utime = 10.57
    year = 2010
    month = 1
    day = 27

    terminator_class = Terminator_Class(utime=utime,year=year,month=month,day=day)
    lx,px = terminator_class.terminator()
    for i in range(len(lx)):
        print(lx[i],px[i])
