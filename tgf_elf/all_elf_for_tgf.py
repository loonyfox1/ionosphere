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

def read(datetime):
	dest_in = '/root/ELF_data/bin_files/'
	dest_out = '/root/ELF_data/txt_files/'
	folder,filename = find_filename(datetime)
	dest_in = dest_in+folder
	print(datetime,'\n'+dest_in+filename,'\n')
	filename = Read_ELF_Class(filename=filename,destination_in=dest_in,destination_out=dest_out).read_and_save()

if __name__ == '__main__':
	tgf_file = '/root/Downloads/eventlist.dat'
	tgf_data = pd.read_table(tgf_file,sep=' ')
	# print(tgf_data)

	idd_array = [i for i in range(678,687)]

	jobs = []

	for idd in tgf_data.ID:
		if int(idd) in idd_array:
			try:
				datetime = str(tgf_data.TIMESTAMP[tgf_data.ID==idd].values[0])
				p = Process(target=read,args=(str(datetime),))
				jobs.append(p)
				p.start()
				# p.join()
			except FileNotFoundError:
				break

	[x.join() for x in jobs]
