from main import Main_Class
from multiprocessing import Process
import pandas as pd
import argparse
import numpy as np

def process_func(args,counts,geog,dur,file_res):
	res = Main_Class(args).main()
	with open(file_res,'a') as f:
		f.write(str(idd)+'\t'+str(args.lon)+'\t'+str(args.lat)+'\t'+args.datetime+'\t'+
				str(counts)+'\t'+str(geog)+'\t'+str(dur)+'\t'+str(res['dist'])+'\t'+
				str(res['day coef'])+'\t'+str(res['calc dd'])+'\t'+str(res['calc dn'])+
				'\t'+str(res['real delay'])+'\t'+str(res['B pulse'])+'\t'+str(res['B noise'])+
				'\t'+str(res['c(r)'])+'\t'+str(res['P'])+'\t'+str(res['P min'])+'\n')

	print(res)

if __name__ == '__main__':
	# DESTINATIONS #############################################################
	file_tgf = '/root/Downloads/eventlist.dat'
	dest_img = '/root/ELF_data/img/'
	dest_txt = '/root/ELF_data/txt_files/'
	file_res = '/root/ELF_data/results/result.txt'
	############################################################################

	tgf_data = pd.read_table(file_tgf,sep=' ')
	ela = 10

	# filt = []
	# if ela==7:
	# 	filt = np.loadtxt('/root/ELF_data/filter/filter_data_7.dat',dtype=complex)
	# elif ela==10:
	# 	filt = np.loadtxt('/root/ELF_data/filter/filter_data_10.dat',dtype=complex)

	with open(file_res,'w') as f:
		f.write('ID\tLON\tLAT\tTIMESTAMP\tCOUNTS\tGEOG\tDUR\t'+
				'DIST\tD/N\tDD\tDN'+
				'\tDELTA\tBp\tBn\tcr\tp\tpmin\n')

	idd_array = [i for i in range(1042,1052)]

	jobs = []
	for idd in tgf_data.ID:
		if int(idd) in idd_array:
			print('TGF',idd)
			args = argparse.Namespace()
			args.id = idd
			args.datetime = str(tgf_data.TIMESTAMP[tgf_data.ID==idd].values[0])
			args.lat = tgf_data.LATITUDE[tgf_data.ID==idd].values[0]
			args.lon = tgf_data.LONGITUDE[tgf_data.ID==idd].values[0]
			if float(args.lon>180): args.lon = round(-360+float(args.lon),5)
			args.verbose = False
			args.plot = True
			args.dest = dest_elf
			args.dest_img = dest_img
			args.degree = 35
			args.sigma = 3
			# args.filt = filt

			p = Process(target=process_func,args=(args,tgf_data.COUNTS[tgf_data.ID==idd].values[0],
						tgf_data.GEOG[tgf_data.ID==idd].values[0],tgf_data.DUR[tgf_data.ID==idd].values[0],file_res))
			jobs.append(p)
			p.start()

	[x.join() for x in jobs]
