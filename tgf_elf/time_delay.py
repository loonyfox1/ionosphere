from __future__ import division
from __future__ import print_function
import numpy as np


class Time_Delay_Class(object):
    CONST_C = 299792458
    # VD - day velocity of hight frequency component
    CONST_VD = CONST_C/1.26528744052
    # VN - night velocity of hight frequency component
    CONST_VN = CONST_C/1.14237601638

    def __init__(self,r):
        self.r = r

    def time_delay(self):
        return self.r/self.CONST_VD, self.r/self.CONST_VN

if __name__ == '__main__':
    r = 5253e3

    time_delay_class = Time_Delay_Class(r=r)
    dd,dn = time_delay_class.time_delay()
    print('Delta day  ',dd)
    print('Delta night',dn)
