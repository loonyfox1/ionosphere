from __future__ import division
from __future__ import print_function
from numpy import pi,log,fft,zeros,sin,exp,sqrt,trapz,array,transpose,absolute,imag,real
from scipy import signal,special,integrate
import pandas as pd
import matplotlib.pyplot as plt
import time


class Charge_Moment_Class(object):
    CONST_MU0 = 4e-7*pi
    # A - Earth's radius, m
    CONST_A = 6372795
    # C - velocity of light, m/sec
    CONST_C = 299792458
    # FS - sampling rate, Hz = 1/sec
    CONST_T = 300

    def __init__(self,B,d,stantion):
        # B - B_pulse
        self.B = B
        # d - array/tuple of distance like ((r_day,day=True),(r_night,day=False))
        self.d = d
        self.CONST_FS,self.CONST_FN,_,self.CONST_DELTAF,self.CONST_HI, \
        self.CONST_WN1,self.CONST_WN2,self.CONST_WN3 = stantion()
        # f - array of frequencies
        self.f = self.frequency_array()
        # self.filter = list(filt)

    def charge_moment(self):
        c = float(self.c_fun())
        res = {
            'p': float(self.B/c),
            'c': c
        }
        return res

    def number_of_point(self):
        return int(round(self.CONST_FS*self.CONST_T))

    def omega(self,fi):
        return 2*pi*fi

    def frequency_array(self):
        self.N = self.number_of_point()
        return fft.rfftfreq(n=self.N,d=1/self.CONST_FS)[1:]

    def receiver_transfer_function(self):
        z0 = zeros(self.N)
        z0[0] = 1

        b, a = signal.cheby1(N=2, rp=3, Wn=self.CONST_WN1/self.CONST_FN, analog=False)
        z1 = signal.lfilter(b, a, z0)

        b, a = signal.cheby1(N=3, rp=3, Wn=self.CONST_WN2/self.CONST_FN, analog=False)
        z2 = signal.lfilter(b, a, z1)

        b, a = signal.cheby1(N=3, rp=3, Wn=self.CONST_WN3/self.CONST_FN, analog=False)
        z3 = signal.lfilter(b, a, z2)

        res = fft.rfft(z3)
        return res/max(res)

    def ionosphere_transfer_function(self):
        res = []
        itf2 = sqrt(self.r/self.CONST_A/sin(self.r/self.CONST_A))
        for fi in self.f:
            itf1 = -1j*pi*self.CONST_MU0*fi/2/self.magnetic_altitude(fi)/self.phase_velocity(fi)
            itf3 = special.hankel2([1],[2*pi*self.r*fi/self.phase_velocity(fi)])
            itf4 = exp(-self.attenuation_factor(fi)*self.r)
            res.append(itf1*itf2*itf3*itf4)
        return res

    def total_distance(self):
        return self.d[0][0]+self.d[1][0]

    def c_fun(self):
        res = 0
        k = 2
        for check_day in self.d:
            self.day = check_day[1]
            self.r = check_day[0]
            if self.r==0:
                res += 0
                k -= 1
            else:
                res_c = sqrt(pi*self.CONST_DELTAF/self.CONST_HI* \
                        trapz(transpose(array(self.integrand())),
                        x=self.f, axis=1))
                res += res_c/self.r
        self.total_r = self.total_distance()
        return res/k*self.total_r

    def integrand(self):
        res_rtf = self.receiver_transfer_function()
        res_itf = self.ionosphere_transfer_function()
        return [absolute(res_itf[i]*res_rtf[i])*absolute(res_itf[i]*res_rtf[i])
                for i in range(int(len(res_itf)))]

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
        if self.day:
            res = (101.5 - 3.1*log(fi/7.7) + \
                1j*(7.0 - 0.9*log(fi/7.7)))*1e3
        else:
            res = (114.7 - 8.4*log(fi/7.7) + \
                1j*(13.2 - 2.0*log(fi/7.7)))*1e3
        return res

    def electric_characteristic_altitude(self,fi):
        if self.day:
            res = (51.1 + 1.9*log(fi/1.7) - 2.45*(1.7/fi)**0.822 - 2.84*(1.7/fi)**1.645 + \
                1j*(-2.98 - 8.8*(1.7/fi)**0.822 + 1.86*(7.7/fi)**1.645))*1e3
        else:
            res = (67.5 + 2.0*log(fi/7.7) - 2.54*(7.7/fi)**0.813 - 2.72*(7.7/fi)**1.626 + \
                1j*(-3.14 - 8.7*(7.7/fi)**0.813 + 1.92*(7.7/fi)**1.626))*1e3
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
