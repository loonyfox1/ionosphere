from read_elf_file import Read_ELF_Class
import pandas as pd
from multiprocessing import Process

def find_filename(datetime):
	# 'yy-mm-ddTHH:MM:SS.SSS'
	year = int(datetime[:4])
	month = int(datetime[5:7])
	day = int(datetime[8:10])
	hour = int(datetime[11:13])
	minute = int(datetime[14:16])
	second = float(datetime[17:])
	utime = round(float(datetime[11:13])+float(datetime[14:16])/60+float(datetime[17:])/3600,2)

	if month<10: smonth = '0'+str(month)
	else: smonth = str(month)

	if day<10: sday = '0'+str(day)
	else: sday = str(day)

	if hour<10: shour = '0'+str(hour)
	else: shour = str(hour)

	sminute = minute//5*5
	if sminute<10: sminute = '0'+str(sminute)
	else: sminute = str(sminute)

	return str(year)+smonth+sday+'/', str(year)+smonth+sday+shour+sminute+'.dat'

def read(datetime,dest_bin,dest_txt):
	folder,filename = find_filename(datetime)
	dest_bin = dest_bin+folder
	print(datetime,'\n'+dest_bin+filename,'\n')
	filename = Read_ELF_Class(filename=filename,destination_in=dest_bin,destination_out=dest_txt).read_and_save()

if __name__ == '__main__':
	file_tgf,dest_bin,dest_txt,sta,end = '','','','',''
	# DESTINATIONS #############################################################
	with open('config.txt','r') as f:
		for line in f:
			file_tgf = line[11:-1] if 'file_tgf' in line else file_tgf
			dest_bin = line[11:-1] if 'dest_bin' in line else dest_bin
			dest_txt = line[11:-1] if 'dest_txt' in line else dest_txt
			sta = int(line[6:-1]) if 'sta' in line else sta
			end = int(line[6:-1]) if 'end' in line else end
	############################################################################

	tgf_data = pd.read_table(file_tgf,sep=' ')

	idd_array = [i for i in range(sta,end)]

	jobs = []

	for idd in tgf_data.ID:
		if int(idd) in idd_array:
			try:
				datetime = str(tgf_data.TIMESTAMP[tgf_data.ID==idd].values[0])
				p = Process(target=read,args=(str(datetime),dest_bin,dest_txt,))
				jobs.append(p)
				p.start()
				# p.join()
			except FileNotFoundError:
				pass

	[x.join() for x in jobs]
