import numpy as np

class Time_Delay_Class(object):
    CONST_C = 299792458
    # VD - day velocity of hight frequency component
    CONST_VD = CONST_C/1.26528744052
    # VN - night velocity of hight frequency component
    CONST_VN = CONST_C/1.14237601638

    def __init__(self,r,stantion):
        self.r = r
        _, _, _, self.CONST_DELTAF, _, _, _, _ = stantion()

    def signal_delay(self):
        return 1/self.CONST_DELTAF

    def group_delay(self):
        return self.r/self.CONST_VD, self.r/self.CONST_VN

    def time_delay(self):
        tau_day,tau_night = self.group_delay()
        tau_rec = self.signal_delay()
        return round(tau_day+tau_rec,3),round(tau_night+tau_rec,3)

if __name__ == '__main__':
    r = 5253e3

    time_delay_class = Time_Delay_Class(r=r)
    dd,dn = time_delay_class.time_delay()
    print('Delta day  ',dd)
    print('Delta night',dn)
