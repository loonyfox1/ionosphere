import numpy as np
import scipy as sc

# DELTAF - energy bandwidth of the receiver, Hz = 1/sec
DELTAF = 51.8
# HI - correction coefficient of lfilter
HI = 1.02
# MU0 - vacuum permeability, H/m = kg*m*m/(sec*sec*A*A)/m (SI)
MU0 = 4e-7*np.pi
# A - Earth's radius, m
A = 6375e3
# OMEGA - WTF is omega ???
OMEGA = 0
# C - velocity of light, m/sec
C = 3e8
# TAUr = 1/DELTAF - signal delay in the receiver, sec
TAUr = 19.3e-3
# FS - sampling rate, Hz = 1/sec
FS = 175.96
# FN = FS/2 - Nyquist frequency, Hz = 1/sec
FN = 87.98

# t - time array
t = np.linspace(0, 300.0, num=z0.size)
# f - frequency array
f = np.fft.rfftfreq(z0.size)

#fs = z0.size/t[-1] - sampling rate

def receiver_transfer_function(f):
    pass 

def receiver_filter(z0):
    b, a = sc.signal.cheby1(N=2, rp=3, Wn=Wn1/FN, analog=False)
    z1 = sc.signal.lfilter(b, a, z0)

    b, a = sc.signal.cheby1(N=3, rp=3, Wn=Wn2/FN, analog=False)
    z2 = sc.signal.lfilter(b, a, z1)

    b, a = sc.signal.cheby1(N=3, rp=3, Wn=Wn3/FN, analog=False)
    z3 = sc.signal.lfilter(b, a, z2)

    return np.abs(np.fft.rfft(z3))

def spectral_density(f):
    pass

def ionosphere_transfer_function(r,f):
    return -j*np.pi*MU0*f/2/magnetic_altitude(f)/phase_velocity(f)*np.sqrt(r/A/np.sin(r/A))*
            sc.special.hankel2(v=1,z=2*np.pi*r*f/phase_velocity(f))*np.exp(-attenuation_factor(f)*r)

def magnetic_field_altitude(r,p):
    return c(r)*p

def c(r):
    return np.sqrt(np.pi*DELTAF/HI*sc.integrate.quad(integrand, 0, np.inf, args=(r)))

def integrand(f,r):
    return np.absolute(ionosphere_transfer_function(r,f)*receiver_transfer_function(f))**2

def magnetic_altitude(f):
    return np.real(magnetic_characteristic_altitude(f))

def phase_velocity(f):
    return C/np.real(propagation_parameter(f))

def attenuation_factor(f):
    return OMEGA/C*np.imag(propagation_parameter(f))

def propagation_parameter(f):
    return np.sqrt(magnetic_characteristic_altitude(f)/electric_characteristic_altitude(f))

def magnetic_characteristic_altitude(f,day):
    if day:
        return 101.5 - 3.1*np.log(f/7.7) +
            j*(7.0 - 0.9*np.log(f/7.7))
    else:
        return 114.7 - 8.4*np.log(f/7.7) +
            j*(13.2 - 2.0*np.log(f/7.7))

def electric_characteristic_altitude(f,day):
    if day:
        return 51.1 + 1.9*np.log(f/1.7) - 2.45*(1.7/f)**0.822 - 2.84*(1.7/f)**1.645 +
            j*(-2.98 - 8.8*(1.7/f)**0.822 + 1.86*(7.7/f)**1.645)
    else:
        return 67.5 + 2.0*np.log(f/7.7) - 2.54*(7.7/f)**0.813 - 2.72*(7.7/f)**1.626 +
            j*(-3.14 - 87*(7.7/f)**0.813 + 1.92*(7.7/f)**1.626)

def group_delay():
    pass
