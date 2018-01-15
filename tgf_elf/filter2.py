from __future__ import division

import numpy as np
import scipy
from scipy import signal
import pandas as pd
import matplotlib.pyplot as plt
import random
#import sympy


def filter(indata, N, rp, Wn):
	b, a = signal.cheby1(N=N, rp=rp, Wn=Wn, analog=True)
	zi = signal.lfilter_zi(b, a)
	z, _ = signal.lfilter(b, a, indata, zi=zi*indata[0])

n1, n2, n3 = 2, 3, 3
#Wn1, Wn2, Wn3 = 457, 334, 334
Wn1, Wn2, Wn3 = 0.3, 0.3, 0.3 # just for testing, here should real Wn

rp = 3

# initial data (delta function)
z0 = np.append([1], np.zeros(1000)) # just for testing, here should real N
t = np.linspace(0, 300.0, num=z0.size) # 300 --> 5 min
print(z0)

fs = z0.size/t[-1] # sampling rate
fn = fs/2 # Nyquist frequency

# filter 1 ====================================================================
b, a = signal.cheby1(N=2, rp=3, Wn=Wn1/fn, analog=False)
zi = signal.lfilter_zi(b, a)
z1 = signal.lfilter(b, a, z0)

# filter 2 ====================================================================
b, a = signal.cheby1(N=3, rp=3, Wn=Wn2/fn, analog=False)
zi = signal.lfilter_zi(b, a)
z2 = signal.lfilter(b, a, z1)

# filter 3 ====================================================================
b, a = signal.cheby1(N=3, rp=3, Wn=Wn3/fn, analog=False)
zi = signal.lfilter_zi(b, a)
z3 = signal.lfilter(b, a, z2)

###############################################################################
f = np.fft.rfftfreq(z0.size)

Z0 = np.abs(np.fft.rfft(z0))
Z1 = np.abs(np.fft.rfft(z1))
Z2 = np.abs(np.fft.rfft(z2))
Z3 = np.abs(np.fft.rfft(z3))

###############################################################################
# Plotting
###############################################################################

plt.subplot(211)
plt.plot(z0, label='z0')
plt.plot(scipy.signal.filtfilt(b, a, z0))
plt.legend()

plt.subplot(212)
plt.plot(f, Z0, label='Z0')
plt.legend()

plt.show()

###############################################################################
plt.subplot(211)
plt.plot(z1, label='z1')
plt.plot(scipy.signal.filtfilt(b, a, z1))
plt.legend()

plt.subplot(212)
plt.plot(f, Z1, label='Z1')
plt.legend()

plt.show()

###############################################################################
plt.subplot(211)
plt.plot(z2, label='z2')
plt.plot(scipy.signal.filtfilt(b, a, z2))
plt.legend()

plt.subplot(212)
plt.plot(f, Z2, label='Z2')
plt.legend()

plt.show()

###############################################################################
plt.subplot(211)
plt.plot(z3, label='z3')
plt.legend()

plt.subplot(212)
plt.plot(f, Z3, label='Z3')
plt.legend()

plt.show()
