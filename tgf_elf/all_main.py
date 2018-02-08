from main import Main_Class
from multiprocessing import Process
import pandas as pd
import argparse
import numpy as np

def process_func(args,counts,geog,dur):
	res = Main_Class(args).main()
	with open('/root/ELF_data/results/result.txt','a') as f:
		f.write(str(idd)+'\t'+str(args.lon)+'\t'+str(args.lat)+'\t'+args.datetime+'\t'+
				str(counts)+'\t'+str(geog)+'\t'+str(dur)+'\t'+str(res['dist'])+'\t'+
				str(res['day coef'])+'\t'+str(res['calc dd'])+'\t'+str(res['calc dn'])+
				'\t'+str(res['real delay'])+'\t'+str(res['B pulse'])+'\t'+str(res['B noise'])+
				'\t'+str(res['c(r)'])+'\t'+str(res['P'])+'\t'+str(res['P min'])+'\n')

	print(res)

if __name__ == '__main__':
	tgf_file = '/root/Downloads/eventlist.dat'
	dest_img = '/root/ELF_data/img/'
	dest_elf = '/root/ELF_data/txt_files/'
	tgf_data = pd.read_table(tgf_file,sep=' ')
	# tgf_data = np.loadtxt(tgf_file)
	ela = 10

	# filt = []
	# if ela==7:
	# 	filt = np.loadtxt('/root/ELF_data/filter/filter_data_7.dat',dtype=complex)
	# elif ela==10:
	# 	filt = np.loadtxt('/root/ELF_data/filter/filter_data_10.dat',dtype=complex)

	with open('/root/ELF_data/results/result.txt','w') as f:
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
						tgf_data.GEOG[tgf_data.ID==idd].values[0],tgf_data.DUR[tgf_data.ID==idd].values[0]))
			jobs.append(p)
			p.start()

	[x.join() for x in jobs]
