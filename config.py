class Config(object):
    def __init__(self):
        self.args = {
            # destinations of data
            # NOTE: CHECK ALL DATA OF STANTION THE SAME
            'dest_bin': '/home/foxy/ELF_data/bin_files/',
            'dest_txt': '/home/foxy/ELF_data/txt_files/',
            'file_tgf': '/home/foxy/ELF_data/eventlist_modified_Ela7.dat',

            # destinations of results
            'dest_img': '/home/foxy/ELF_data/results/img/',
            'file_res': '/home/foxy/ELF_data/results/result.csv',

            # range of analyzed data
            # including first and last
            'start': 0,
            'end': 1196,

            # analyzed stantion
            'ela': 7,

            # data processing constants
            # NS - x, EW - y
            'sigma_x': 3,
            'sigma_y': 3,
            'sigma_iter': 4,

            'degree_x': 15,
            'degree_y': 30,

            # configuration of result
            # save the plots
            'plot': True,
            # print information
            'verbose': False,

            # stantion coordinates
            'lon_s': 22.55,
    	    'lat_s': 49.19,
            }

        if self.args['ela']==7:
            # FS - sampling rate, Hz = 1/sec
            self.args['CONST_FS'] = 175.96

            # FN - naquist frequency
            self.args['CONST_FN'] = 175.96/2

            # SCALE - full scale, pT/scale
            self.args['CONST_SCALE'] = 2**16/3826e-12

            # DELTAF - energy bandwidth of the receiver, Hz = 1/sec
            self.args['CONST_DELTAF'] = 51.8

            # HI - correction coefficient of lfilter
            self.args['CONST_HI'] = 1.02 # NOTE: one const for ELA7/10 ??

            # WN - parameter for Cheby filters
            self.args['CONST_WN'] = (45,45,45) # NOTE: clarify

            # indent of peak finding
            self.args['CONST_INDENT'] = 1

            # NS coefficients for Ela7 = -1
            self.args['NS_COEFF'] = -1

        elif self.args['ela']==10:
            # FS - sampling rate, Hz = 1/sec
            self.args['CONST_FS'] = 887.7841

            # FN - naquist frequency
            self.args['CONST_FN'] = 887.7841/2

            # SCALE - full scale, pT/scale
            self.args['CONST_SCALE'] = (2**16/3353e-12,2**16/3906e-12)

            # DELTAF - energy bandwidth of the receiver, Hz = 1/sec
            self.args['CONST_DELTAF'] = 304.9 # NOTE: clarify

            # HI - correction coefficient of lfilter
            self.args['CONST_HI'] = 1.02 # NOTE: one const for ELA7/10 ??

            # WN - parameter for Cheby filters
            self.args['CONST_WN'] = (443,334,334) # NOTE: clarify

            # indent of peak finding
            self.args['CONST_INDENT'] = 3

            # NS coefficients for Ela10 = 1
            self.args['NS_COEFF'] = 1


    def get_args(self):
        return self.args
