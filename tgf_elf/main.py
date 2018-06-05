from __future__ import division
from __future__ import print_function
import pandas as pd
from main_process import Main_Class
# import main
from multiprocessing import Process
import argparse
import os

def process_func(args,counts,geog,dur,file_res):
	res = Main_Class(args).main()
	# table.append([idd,args.lon,args.lat,args.datetime,counts,geog,dur,res['dist'],
	# 			  res['day coef'],res['calc dd'],res['calc dn'],res['real delay'],
	# 			  res['B pulse'],res['B noise'],res['c(r)'],res['P'],res['P min']])
	with open(file_res,'a') as f:
		if res is not None:
			f.write("%d\t%f\t%f\t%s\t%d\t%d\t%f\t%d\t%f\t%d\t%d\t%d\t%f\t%f\t%f\t%f\t%f\t%d\t%d\t%d\n" % (idd,args.lon,args.lat,str(args.datetime),counts,geog,dur,res['dist'], \
			 res['day coef'],res['calc dd'],res['calc dn'],res['real delay'], \
			 res['B pulse'],res['B noise'],res['c(r)'],res['P'],res['P min'],res['Ap'],res['An'],res['A']))
			# f.write('{:04d}{:10.3f}{:10.3f}    {:.23}{:6d}{:8d}{:11.2f}{:7d}{:8.2f}{:5d}{:5d}{:5d}{:10.1f}{:6.1f}{:8.1f}{:7.1f}{:6.1f}\n'.format \
			# 	   (idd,args.lon,args.lat,args.datetime,counts,geog,dur,res['dist'],
			# 		res['day coef'],res['calc dd'],res['calc dn'],res['real delay'],
			# 		res['B pulse'],res['B noise'],res['c(r)'],res['P'],res['P min']))

		# f.write(str(idd)+'\t'+str(args.lon)+'\t\t'+str(args.lat)+'\t\t'+args.datetime+'\t\t'+
		# 		str(counts)+'\t\t'+str(geog)+'\t\t'+str(dur)+'\t\t'+str(res['dist'])+'\t\t'+
		# 		str(res['day coef'])+'\t\t'+str(res['calc dd'])+'\t\t'+str(res['calc dn'])+
		# 		'\t\t'+str(res['real delay'])+'\t\t'+str(res['B pulse'])+'\t\t'+str(res['B noise'])+
		# 		'\t\t'+str(res['c(r)'])+'\t\t'+str(res['P'])+'\t\t'+str(res['P min'])+'\n')

if __name__ == '__main__':
	file_tgf,dest_img,dest_txt,file_res,sta,end,deg = '','','','','','',''
	# DESTINATIONS #############################################################
	with open('config.txt','r') as f:
		for line in f:
			file_tgf = line[11:-1] if 'file_tgf' in line else file_tgf
			dest_img = line[11:-1] if 'dest_img' in line else dest_img
			dest_bin = line[11:-1] if 'dest_bin' in line else dest_bin
			dest_txt = line[11:-1] if 'dest_txt' in line else dest_txt
			file_res = line[11:-1] if 'file_res' in line else file_res        # delt = self.N-len(self.filter)
		# if delt>0:
		#     for i in range(len(self.filter)-1,len(self.filter)-1+delt):
		#         self.filter.append(0)
		# else:
		#     self.filter[:self.N]
		# return self.filter

			sta = int(line[6:-1]) if 'sta' in line else sta
			end = int(line[6:-1]) if 'end' in line else end
			deg = int(line[6:-1]) if 'deg' in line else deg
	############################################################################
	tgf_data = pd.read_table(file_tgf,sep=' ')

	if os.path.exists(dest_img) == False:
		os.mkdir(dest_img)

	with open(file_res,'w') as f:
		f.write('ID\tLON\tLAT\tTIMESTAMP\tCOUNTS\tGEOG\tDUR\t'+
				'DIST\tD/N\tDD\tDN'+
				'\tDELTA\tBP\tBN\tCR\tP\tPMIN\tAP\tAN\tATGF\n')
	idd_array = [i for i in range(sta,end)]
	jobs = []
	for idd in tgf_data.ID:
		if int(idd) in idd_array:
			# print('TGF',idd)
			args = argparse.Namespace()
			args.id = idd
			args.datetime = str(tgf_data.TIMESTAMP[tgf_data.ID==idd].values[0])
			args.lat = tgf_data.LATITUDE[tgf_data.ID==idd].values[0]
			args.lon = tgf_data.LONGITUDE[tgf_data.ID==idd].values[0]
			if float(args.lon>180): args.lon = round(-360+float(args.lon),5)
			args.verbose = True
			args.plot = True
			args.dest_bin = dest_bin
			args.dest_img = dest_img
			args.degree = deg
			args.sigma = 3

			# args.filt = filt

			p = Process(target=process_func,args=(args,tgf_data.COUNTS[tgf_data.ID==idd].values[0],
						tgf_data.GEOG[tgf_data.ID==idd].values[0],tgf_data.DUR[tgf_data.ID==idd].values[0],file_res))
			jobs.append(p)
			p.start()

	[x.join() for x in jobs]
