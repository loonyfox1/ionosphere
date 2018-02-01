import numpy as np
import matplotlib.pyplot as plt
from datetime import *
import os
import matplotlib.ticker

def all_files(directory7='D://Sesja 0151 08.10-12.11.16/', directory10='D://Sesja 0151b 08.10-12.11.16/'):
	dir7 = os.listdir(directory7)
	dir10 = os.listdir(directory10)
	delta = main_function('D://Sesja 0151 08.10-12.11.16/20161008/201610081145.dat','D://Sesja 0151b 08.10-12.11.16/20161008/201610081145.dat')
	print('--------------------' + '\n')
	print(delta)
	print('--------------------' + '\n')
	'''filetr = open('D://RESULT.txt','w')
											dir7 = os.listdir(directory7)
											dir10 = os.listdir(directory10)
											for i in dir7:
												for j in dir10:
													if i==j:
														print(i)
														files7 = os.listdir(directory7+i)
														files10 = os.listdir(directory10+j)
														for n in files7:
															for m in files10:
																if n==m:
																	print(n)
																	delta = []
																	delta = (main_function(directory7+i+'//'+n,directory10+j+'//'+m))
																	filetr.write(n + ' |  ')
																	for k in delta:
																		filetr.write(str(int(k*1000000)) + ' ms  |  ')
																	filetr.write('\n'+'_____________________________________________________________________________'+'\n')
											filetr.close()'''							
	#return TE1, TE2, T1, T2, FILENAME
							

def main_function(filename7,filename10):
	########################################################
	# 1.READ DATA FROM FILE (ch)
	########################################################
	ch7_1 = []        
	ch7_2 = []
	ch10_1 = []
	ch10_2 = []

	ch7_1, ch7_2, header7, time_cor7 = read_data_from_file(filename7)
	ch10_1, ch10_2, header10, time_cor10 = read_data_from_file(filename10)

	ch7_1 = ch7_1[1:]
	ch7_2 = ch7_2[1:]
	ch10_1 = ch10_1[18:]
	ch10_2 = ch10_2[18:]
	########################################################
	# 3.DETRENDING (cd)
	########################################################
	cd7_1 = detrend(ch7_1)                                           
	cd7_2 = detrend(ch7_2)
	cd10_1 = detrend(ch10_1)
	cd10_2 = detrend(ch10_2)
	########################################################
	# 4.PEAKING (cp)
	########################################################
	cp7_1 = peaking(cd7_1)                             
	cp7_2 = peaking(cd7_2)
	cp10_1 = peaking(cd10_1)
	cp10_2 = peaking(cd10_2)
	########################################################
	# HIGHTLIGHT PEAKS
	########################################################
	c7_1 = highlight_peaks(cp7_1)
	c7_2 = highlight_peaks(cp7_2)
	c10_1 = highlight_peaks(cp10_1)
	c10_2 = highlight_peaks(cp10_2)
	########################################################
	# 5.INVERSE ELA7 NS (cp)
	########################################################
	c7_1 = inverse(c7_1)
	########################################################
	# 6.GET TIME ERROR (cp)
	########################################################
	time_error_1, time_1 = get_time_error(c7_1,c10_1) 
	time_error_2, time_2 = get_time_error(c7_2,c10_2)
	delta1 = []
	delta2 = []
	show_graph(time_1, time_2,time_error_1,time_error_2)
	########################################################
	# 7.VISUAL CHECK
	########################################################
	Hz7 = 52787/300
	Hz10 = 266336/300
	'''for i in range(len(index7_1)):
					delta1.append(index7_1[i]- 3.28e-3 - index10_1[i] - 19.31e-3)
				for i in range(len(index7_2)):
					delta2.append(index7_2[i]- 3.28e-3 - index10_2[i]- 19.31e-3)
				delta = delta1+delta2
				print(delta)'''
	#visual_check(ch7_1, ch10_1, cp7_1, cp10_1, c7_1, c10_1, index7_1, index10_1)
	return delta

def get_time_day(header):
	#print(header[18:35])
	aa = datetime.strptime(header[18:33], '%d.%m.20%y %H:%M')
	bb = datetime.strptime("20.10.2016 00:00", "%d.%m.20%y %H:%M")
	cc = aa - bb
	dd = str(cc)
	if header[18:28]=='20.10.2016':
		return int(dd[:dd.find(":")])+int(dd[dd.find(":")+1:dd.find(":")+3])/60,0
	else:
		day = int(dd[:dd.find(' ')])
		time_hour = int(dd[dd.find(', ')+1:dd.find(":")])+int(dd[dd.find(":")+1:dd.find(":")+3])/60
		return time_hour, day

def exepted_time_error(time,day):
	if time < 12.0:
		exp_time_error = 5.37e-5*(day-1) + 110e-6
	else: 
		exp_time_error = 5.37e-5*(day-1) + 220e-6
	return exp_time_error

def inverse(data):
	for i in range(len(data)):
		data[i] = -data[i]
	return data

def peaking(data,n=3):
	mean = np.mean(data)
	d = []
	for i in range(len(data)):    
		d.append(data[i]-mean)
	std = np.std(d)
	for i in range(len(d)):
		if abs(d[i])<n*std:
			d[i] = 0
	return d

def cut_off_10(x):
	x = x[10:len(x)-10]
	return x

def cut_off_negative(x,data1,data2):
	cut = 0
	for i in range(len(x)):
		if x[i]<0:
			cut = i+1
	x = x[cut:]
	data1 = data1[cut:]
	data2 = data2[cut:]
	return x, data1, data2

def detrend(data,degree=10):                          
	detrended=[0]*degree
	for i in range(degree,len(data)-degree):
		chunk=data[i-degree:i+degree]
		chunk=sum(chunk)/len(chunk)
		detrended.append(data[i]-chunk)
	detrended = detrended+[0]*degree
	return detrended

def get_time_lists(N7, N10):
	Hz7 = 52787/300
	Hz10 = 266336/300
	x7 = []                         
	x10 = []
	for i in range(N7):
		x7.append(i/Hz7 - 19.31e-3)
	for i in range(N10):
		x10.append(i/Hz10 - 3.28e-3)
	return x7, x10

def get_time_error(st, c):
	Hz7 = 52787/300
	Hz10 = 266336/300

	standart = st[:]
	comparable = c[:]
	
	xlist7, xlist10 = get_time_lists(len(standart), len(comparable))

	time_error = []
	time = []

	for i in range(10):
		mx10 = xlist10[comparable.index(max(comparable))]
		mx7 = xlist7[standart[round(mx10*Hz7)-10:round(mx10*Hz7)+10].index(max(standart[round(mx10*Hz7)-10:round(mx10*Hz7)+10]))+round(mx10*Hz7)-10]

		mn10 = xlist10[comparable.index(min(comparable))]
		mn7 = xlist7[standart[round(mn10*Hz7)-10:round(mn10*Hz7)+10].index(min(standart[round(mn10*Hz7)-10:round(mn10*Hz7)+10]))+round(mn10*Hz7)-10]
			
		delta_mx = mx10-mx7
		delta_mn = mn10-mn7
		print('mx7 = ' + str(mx7))
		print('mx10 = ' + str(mx10)+'\n')
		print('mn7 = ' + str(mn7))
		print('mn10 = ' + str(mn10) + '\n')
		print('delta mx = ' + str(delta_mx))
		print('delta mn = ' + str(delta_mn))
		print('----------------------------'+'\n')
		if delta_mx < 0 and delta_mx > -0.01: 
			time_error.append(delta_mx)
			time.append(mx7)
		if delta_mn < 0 and delta_mn > -0.01: 
			time_error.append(delta_mn)
			time.append(mn7)
			
		standart[standart.index(max(standart))] = 0
		standart[standart.index(min(standart))] = 0
		comparable[comparable.index(max(comparable))] = 0
		comparable[comparable.index(min(comparable))] = 0
		
	return time_error, time

def get_time_error1(standart,comparable):                                #standart is Ela7 data, 175.95 Hz   comparable is Ela10 data, 887.7841 Hz
	Hz7 = 52787/300
	Hz10 = 266336/300
	A = []
	time7 = []
	time10 = []
	for i in range(len(standart)):
		datime = [abs(standart[i]),i]
		A.append(datime)
	A.sort()
	A.reverse()
	for i in range(len(A)):
		if A[i][0]==0:
			tr = i
			break
	A = A[:tr]

	x7, x10 = get_time_lists(len(standart), len(comparable))

	cur = True
	for i in range(len(A)):
		st = standart[A[i][1]]
		c = comparable[round(A[i][1]/Hz7*Hz10)]
		
		if (st>0 and c>0) or (st<0 and c<0):
			time10.append(x10[round(A[i][1]/Hz7*Hz10)])
			time7.append(x7[A[i][1]])
			print('st: '+str(st)+' c: '+str(c))
			print('\n')
			print('time7: ' + str(x7[A[i][1]]))
			print('time10: ' + str(x10[round(A[i][1]/Hz7*Hz10)]))
			print('\n')
			cur = False
		else: 
			if cur:
				for j in range(1,5):
					if cur:
						cm = comparable[round(A[i][1]/Hz7*Hz10)-j]
						cp = comparable[round(A[i][1]/Hz7*Hz10)+j]
						
						if (st>0 and cm>0) or (st<0 and cm<0):
							time10.append(x10[round(A[i][1]/Hz7*Hz10)-j])
							time7.append(x7[A[i][1]])
							print('st: '+str(st)+' cm: '+str(cm)+' cp: '+str(cp))
							print('\n')
							print('time7: ' + str(x7[A[i][1]]))
							print('time10: ' + str(x10[round(A[i][1]/Hz7*Hz10)-j]))
							print('\n')
							cur = False
						elif (st>0 and cp>0) or (st<0 and cp<0): 
							time10.append(x10[round(A[i][1]/Hz7*Hz10)+j])
							time7.append(x7[A[i][1]])
							print('st: '+str(st)+' cm: '+str(cm)+' cp: '+str(cp))
							print('\n')
							print('time7: ' + str(x7[A[i][1]]))
							print('time10: ' + str(10[round(A[i][1]/Hz7*Hz10)+j]))
							print('\n')
							cur = False
						else: pass
	return time7, time10

def highlight_peaks(A):
	N = len(A)
	data = A[:]
	cur = 0
	check = True
	while cur<N:
		s = 0
		i = cur
		while s==0:
			if i>=N:
				check = False
				cur = i
				break
			else:
				s = data[i]
				i += 1
		if check:
			start = i-1
			st = data[start]
			fn = data[start]
			k = 0
			while ((st>0 and fn>0) or (st<0 and fn<0)) and (start+k)!=N and fn!=0:
				fn = data[start+k+1]
				k += 1
			finish = start+k-1
			m = 0
			if st>0:
				m = data.index(max(data[start:finish+1]))
			elif st<0:
				m = data.index(min(data[start:finish+1]))
			for j in range(start,finish+1):
				d = data[j]
				if j!=m:
					data[j]=0
			cur = finish+1
	return data

def read_data_from_file(file_name):
	with open(file_name, "rb") as f:                   # read file bytes
		byte_array = []
		byte = f.read(1)
		while byte != b'':
			byte_array.append(byte)
			byte = f.read(1)

	with open(file_name, "rb") as f:
		header = str(f.read(46))
		time_correction = 45#int(f.read(2),16)/10*1.6e-6

	new_byte = []                                      # get 16-x code (2 bytes)

	for i in range(64, len(byte_array), 1):
		time_s = str(byte_array[i])
		time_s = repr(time_s)

		if("\\x" in time_s):
			time_s = time_s[6:8]
		else:       
			time_s = hex(ord(time_s[3:4]))[2:]

		new_byte.append(time_s)

	channel1 = []
	channel2 = []                                      # get 10-x data

	for i in range(0, len(new_byte), 4):
		time_s1 = new_byte[i] + new_byte[i+1]
		time_s2 = new_byte[i+2] + new_byte[i+3]
		c1 = int(time_s1, 16)
		c2 = int(time_s2, 16)
		channel1.append(c1)
		channel2.append(c2)
	return channel1[:channel1.index(0)], channel2[:channel2.index(0)], header, time_correction

def save(name='', fmt='png'):
	pwd = os.getcwd()
	iPath = 'D://{}'.format(fmt)
	if not os.path.exists(iPath):
		os.mkdir(iPath)
	os.chdir(iPath)
	plt.savefig('{}.{}'.format(name, fmt), fmt='png')
	os.chdir(pwd)


def visual_check(ch7, ch10, cp7, cp10, c7, c10, index7, index10):
	Hz7 = 52787/300
	Hz10 = 266336/300
	#plt.rcParams['figure.figsize'] = (15.0, 7.0)             
	plt.rcParams['figure.dpi'] = 300
	fig = plt.figure()
	xlist7 = []
	xlist10 = []
	for i in range(len(cp7)):
		xlist7.append(-19.31e-3 + i/Hz7)
	for i in range(len(cp10)):
		xlist10.append(-3.28e-3 + i/Hz10)

	plt.subplot(2,1,1)
	plt.plot(xlist10, ch10, linewidth=0.3, marker='o', markerfacecolor='red', color='red',  markersize=0.5, label='Ela10')
	for i in index10:
		plt.axvline(-3.28e-3+i/Hz10, linewidth=0.5, color='black')
	plt.plot(xlist7, ch7, linewidth=0.3, marker='o', markerfacecolor='blue', color='blue', markersize=0.5, label='Ela7')
	for i in index7:
		plt.axvline(-19.31e-3+i/Hz7, linewidth=0.5, color='green')
	

	'''plt.subplot(3,1,2)
				plt.plot(xlist10, cp10, linewidth=0.3, marker='o', markerfacecolor='red', color='red',  markersize=0.5, label='Ela10')
				plt.plot(xlist7, cp7, linewidth=0.3, marker='o', markerfacecolor='blue', color='blue', markersize=0.5, label='Ela7')
				for i in index7:
					plt.axvline(-19.31e-3+i/Hz7, linewidth=0.5, color='green')
				for i in index10:
					plt.axvline(-3.28e-3+i/Hz10, linewidth=0.5, color='black')'''

	plt.subplot(2,1,2)
	plt.plot(xlist10, c10, linewidth=0.3, marker='o', markerfacecolor='red', color='red',  markersize=0.5, label='Ela10')
	for i in index10:
		plt.axvline(i/Hz10, linewidth=0.5, color='black')
	plt.plot(xlist7, c7, linewidth=0.3, marker='o', markerfacecolor='blue', color='blue', markersize=0.5, label='Ela7')
	for i in index7:
		plt.axvline(-19.31e-3+i/Hz7, linewidth=0.5, color='green')
	


	#plt.legend()
	#plt.xlabel('Time')
	#plt.ylabel('Amplitude')
	plt.show()

def nimax(ch7,ch10,xmin,xmax):
	min7 = min(ch7[round(xmin*175.95):round(xmax*175.95)])
	max7 = max(ch7[round(xmin*175.95):round(xmax*175.95)])
	
	min10 = min(ch10[round(xmin*887.7841):round(xmax*887.7841)])
	max10 = max(ch10[round(xmin*887.7841):round(xmax*887.7841)])
	
	if min7<min10:
		mini = min7
	else: mini = min10
		
	if max7>max10:
		maxi = max7
	else: maxi = max10
		
	return mini, maxi

def show_graph(x1,x2,y1,y2):
	plt.rcParams['figure.dpi'] = 300
	fig = plt.figure()	
	plt.plot(x1,y1, linewidth=0.0, marker='o', markerfacecolor='red', color='red',  markersize=1, label='NS')
	plt.plot(x2,y2, linewidth=0.0, marker='o', markerfacecolor='blue', color='blue',  markersize=1, label='EW')
	plt.legend()
	plt.show()