import numpy as np
from scipy import signal,special,integrate
import pandas as pd
import matplotlib.pyplot as plt
import time
from main import Main_Class

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

class Charge_Moment_Class(object):
    CONST_MU0 = 4e-7*np.pi
    # A - Earth's radius, m
    CONST_A = 6372795
    # C - velocity of light, m/sec
    CONST_C = 299792458
    # FS - sampling rate, Hz = 1/sec
    CONST_T = 300

    def __init__(self,r,stantion):
        self.r = r
        self.CONST_FS,self.CONST_FN,_,self.CONST_DELTAF,self.CONST_HI, \
        self.CONST_WN1,self.CONST_WN2,self.CONST_WN3 = stantion()
        self.f = self.frequency_array()

    def number_of_point(self):
        return int(round(self.CONST_FS*self.CONST_T))

    def omega(self,fi):
        return 2*np.pi*fi

    def frequency_array(self):
        self.N = self.number_of_point()
        return np.fft.rfftfreq(n=self.N,d=1/self.CONST_FS)[1:]

    def receiver_transfer_function(self):
        z0 = np.zeros(self.N)
        z0[0] = 1

        b, a = signal.cheby1(N=2, rp=3, Wn=self.CONST_WN1/self.CONST_FN, analog=False)
        z1 = signal.lfilter(b, a, z0)

        b, a = signal.cheby1(N=3, rp=3, Wn=self.CONST_WN2/self.CONST_FN, analog=False)
        z2 = signal.lfilter(b, a, z1)

        b, a = signal.cheby1(N=3, rp=3, Wn=self.CONST_WN3/self.CONST_FN, analog=False)
        z3 = signal.lfilter(b, a, z2)

        res = np.fft.rfft(z3)
        return res/max(res)

    def ionosphere_transfer_function(self):
        res = []
        itf2 = np.sqrt(self.r/self.CONST_A/np.sin(self.r/self.CONST_A))
        for fi in self.f:
            itf1 = -1j*np.pi*self.CONST_MU0*fi/2/self.magnetic_altitude(fi)/self.phase_velocity(fi)
            itf3 = special.hankel2([1],[2*np.pi*self.r*fi/self.phase_velocity(fi)])
            itf4 = np.exp(-self.attenuation_factor(fi)*self.r)
            res.append(itf1*itf2*itf3*itf4)
        return res


    def c_fun(self):
        res = np.sqrt(np.pi*self.CONST_DELTAF/self.CONST_HI* \
                      np.trapz(np.transpose(np.array(self.integrand())),
                      x=self.f, axis=1))
        return res

    def integrand(self):
        res_rtf = self.receiver_transfer_function()
        res_itf = self.ionosphere_transfer_function()
        return [np.absolute(res_itf[i]*res_rtf[i])**2
                for i in range(int(len(res_itf)))]

    def magnetic_altitude(self,fi):
        return np.real(self.magnetic_characteristic_altitude(fi))

    def phase_velocity(self,fi):
        return self.CONST_C/np.real(self.propagation_parameter(fi))

    def attenuation_factor(self,fi):
        return self.omega(fi)/self.CONST_C*abs(np.imag(self.propagation_parameter(fi)))

    def propagation_parameter(self,fi):
        return np.sqrt(self.magnetic_characteristic_altitude(fi)/ \
                       self.electric_characteristic_altitude(fi))

    def magnetic_characteristic_altitude(self,fi):
        if self.day:
            res = (101.5 - 3.1*np.log(fi/7.7) + \
                1j*(7.0 - 0.9*np.log(fi/7.7)))*1e3
        else:
            res = (114.7 - 8.4*np.log(fi/7.7) + \
                1j*(13.2 - 2.0*np.log(fi/7.7)))*1e3
        return res

    def electric_characteristic_altitude(self,fi):
        if self.day:
            res = (51.1 + 1.9*np.log(fi/1.7) - 2.45*(1.7/fi)**0.822 - 2.84*(1.7/fi)**1.645 + \
                1j*(-2.98 - 8.8*(1.7/fi)**0.822 + 1.86*(7.7/fi)**1.645))*1e3
        else:
            res = (67.5 + 2.0*np.log(fi/7.7) - 2.54*(7.7/fi)**0.813 - 2.72*(7.7/fi)**1.626 + \
                1j*(-3.14 - 8.7*(7.7/fi)**0.813 + 1.92*(7.7/fi)**1.626))*1e3
        return res

if __name__ == '__main__':
    for i in range(1,20000):
        
