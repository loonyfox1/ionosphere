from main import Main_Class
from multiprocessing import Process
import pandas as pd
import argparse

def process_func(args):
	p = Main_Class(args).main()
	print(p)

if __name__ == '__main__':
	tgf_file = '/root/Downloads/eventlist.dat'
	tgf_data = pd.read_table(tgf_file,sep=' ')

	# print(tgf_data.TIMESTAMP.values[4])
	jobs = []
	for idd in tgf_data.ID:
		args = argparse.Namespace()
		args.id = idd
		args.datetime = str(tgf_data.TIMESTAMP[tgf_data.ID==idd].values[0])
		args.lat = tgf_data.LATITUDE[tgf_data.ID==idd].values[0]
		args.lon = tgf_data.LONGITUDE[tgf_data.ID==idd].values[0]
		if float(args.lon>180): args.lon = -360+float(args.lon)
		args.verbose = True
		args.plot = False
		args.dest = ''
		args.degree = 10
		args.sigma = 1

		p = Process(target=process_func,args=(args,))
		jobs.append(p)
		p.start()

	[x.join() for x in jobs]
