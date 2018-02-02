import numpy as np

class Time_Delay_Class(object):
    # DELTAF - energy bandwidth of the receiver, Hz = 1/sec
    CONST_DELTAF = 51.8
    # FS - sampling rate, Hz = 1/sec
    CONST_FS = 175.96
    # T - time of data, sec
    CONST_T = 300
    # C - velocity of light, m/sec
    CONST_C = 299792458

    def __init__(self,r):
        self.r = r

    def signal_delay(self):
        return 1/self.CONST_DELTAF

    def group_delay(self):
        self.f = self.frequency_array()
        self.day = True
        # print('vel day = ',self.CONST_C/self.phase_velocity(self.f[-1]))
        gd = self.r/self.phase_velocity(self.f[-1])
        self.day = False
        # print('vel nig = ',self.CONST_C/self.phase_velocity(self.f[-1]))
        gn = self.r/self.phase_velocity(self.f[-1])
        return gd,gn

    def time_delay(self):
        tau_day,tau_night = self.group_delay()
        tau_rec = self.signal_delay()
        return round(tau_day+tau_rec,3),round(tau_night+tau_rec,3)

    def number_of_point(self):
        return int(round(self.CONST_FS*self.CONST_T))

    def frequency_array(self):
        self.N = self.number_of_point()
        return np.fft.rfftfreq(n=self.N,d=1/self.CONST_FS)[1:]

    def phase_velocity(self,fi):
        return self.CONST_C/np.real(self.propagation_parameter(fi))

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
    r = 5352e3

    time_delay_class = Time_Delay_Class(r=r)
    dd,dn = time_delay_class.time_delay()
    print('Delta day  ',dd)
    print('Delta night',dn)
