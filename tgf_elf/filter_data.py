import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def get_filter(FS,WN1,WN2,WN3):
        N = int(FS*300)
        FN = FS/2
        z0 = np.zeros(N)
        z0[0] = 1

        b, a = signal.cheby1(N=2, rp=3, Wn=WN1/FN, analog=False)
        z1 = signal.lfilter(b, a, z0)

        b, a = signal.cheby1(N=3, rp=3, Wn=WN2/FN, analog=False)
        z2 = signal.lfilter(b, a, z1)

        b, a = signal.cheby1(N=3, rp=3, Wn=WN3/FN, analog=False)
        z3 = signal.lfilter(b, a, z2)

        res = np.fft.rfft(z3)
        return res/max(res)

if __name__ == '__main__':
    # filter data for ELA 7
    filt = get_filter(FS=175.96,WN1=45,WN2=45,WN3=45)

    with open('/root/ELF_data/filter/filter_data_7.dat', "w") as f:
        for i in range(len(filt)-1):
            f.write(str(filt[i])+'\n')
        f.write(str(filt[-1]))

    # filter data for ELA 10
    filt = get_filter(FS=887.7841,WN1=443,WN2=334,WN3=334)

    with open('/root/ELF_data/filter/filter_data_10.dat', "w") as f:
        for i in range(len(filt)-1):
            f.write(str(filt[i])+'\n')
        f.write(str(filt[-1]))
