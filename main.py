from __future__ import print_function
from config import Config
from main_process import Main_Class
from multiprocessing import Process, Manager, Lock
import pandas as pd
import pprint
import csv
import os

def process_func(args,result,lock_result):
	res = Main_Class(args).main()
	with lock_result:
		if res is not None:
			result.append(res)
		# print(str(len(result))+' from '+str(args['end']-args['start'])+' complete')

def main(args):
	# read tgf data
	tgf_data = pd.read_table(args['file_tgf'],sep=' ')

	# create result images folder
	if os.path.exists(args['dest_img']) == False:
		os.mkdir(args['dest_img'])

	# create result dictionary
	manager = Manager()
	result = manager.list()
	lock_result = Lock()

	# create and start processes
	id_array = [i for i in range(args['start'],args['end']+1)]
	jobs = []

	for id_ in tgf_data.ID:
		if id_ in id_array:
			process_args = args.copy()
			process_args['id'] = id_
			process_args['timestamp'] = tgf_data.TIMESTAMP[tgf_data.ID==id_].values[0]
			process_args['counts'] = tgf_data.COUNTS[tgf_data.ID==id_].values[0]
			process_args['geog'] = tgf_data.GEOG[tgf_data.ID==id_].values[0]
			process_args['dur'] = tgf_data.DUR[tgf_data.ID==id_].values[0],
			process_args['lat'] = tgf_data.LATITUDE[tgf_data.ID==id_].values[0]
			process_args['lon'] = tgf_data.LONGITUDE[tgf_data.ID==id_].values[0]
			if float(process_args['lon']>180):
				process_args['lon'] = round(-360+float(process_args['lon']),5)

			# start process_funct in processes
			p = Process(target=process_func,args=(process_args,result,lock_result))
			jobs.append(p)
			p.start()

	# wait of processes finish
	[p.join() for p in jobs]

	# write results to csv file
	keys = ['ID','LON','LAT','TIMESTAMP','COUNTS','GEOG','DUR', \
			'DIST','DC','DD','DN','DELTA','BP','BN','CR','P', \
			'PMIN','AP','AN','ATGF']

	with open(args['file_res'], 'w') as res_file:
	    dict_writer = csv.DictWriter(res_file, keys)
	    dict_writer.writeheader()
	    dict_writer.writerows(result)


if __name__ == '__main__':
	args = Config().get_args()
	main(args)
