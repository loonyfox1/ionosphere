from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path
import matplotlib as mpl

class Read_ELF_Class(object):
	def __init__(self,filename,destination_in,destination_out):
		self.filename = filename
		self.dest_in = destination_in
		self.dest_out = destination_out

	def header(self):
		with open(self.dest_in+self.filename, "rb") as f:
			header = str(f.read(46))
		return header[:-14]

	def read_bytes(self):
		byte_array = []
		try:
			with open(self.dest_in+self.filename, "rb") as f:
				byte = f.read(1)
				while byte != b'':
					byte_array.append(byte)
					byte = f.read(1)
			return byte_array
		except:
			pass

	def bytes_to_hex(self):
		byte_array = self.read_bytes()
		new_byte = []
		for i in range(64,len(byte_array),1):
			time_s = str(byte_array[i])
			if len(time_s)<=1:
				time_s = str(hex(ord(byte_array[i])))
			time_s = repr(time_s)
			if(len(time_s)==6):
				time_s = time_s[3:5]
			else:
				time_s = time_s[3:4]+"0"
			new_byte.append(time_s)
		return new_byte

	def hex_to_decimal(self):
		channel1 = []
		channel2 = []
		new_byte = self.bytes_to_hex()
		for i in range(0, len(new_byte), 4):
			time_s1 = new_byte[i] + new_byte[i+1]
			time_s2 = new_byte[i+2] + new_byte[i+3]
			c1 = int(time_s1, 16)
			c2 = int(time_s2, 16)
			channel1.append(c1)
			channel2.append(c2)
		k = 0
		rev1 = channel1[::-1][1:]
		while rev1[k]==0:
			k += 1
		return channel1[:-k-1],channel2[:-k-1]

	def read(self):
		self.fileheader = self.header()
		self.channel1,self.channel2 = self.hex_to_decimal()
		if len(self.channel1)>len(self.channel2):
			self.channel1 = self.channel1[:len(self.channel2)]
		if len(self.channel1)<len(self.channel2):
			self.channel2 = self.channel2[:len(self.channel1)]
		# self.plot()

		path = Path(self.dest_out+self.filename[:-16])
		path.mkdir(parents=True)
		with open(self.dest_out+self.filename, "w") as f:
			f.write(self.fileheader+'\n')
			for i in range(len(self.channel1)-1):
				f.write(str(self.channel1[i])+'\t'+str(self.channel2[i])+'\n')
			f.write(str(self.channel1[-1])+'\t'+str(self.channel2[-1]))

		return np.array(self.channel1),np.array(self.channel2)

	def plot(self):
		# plt.rc('axes', titlesize=15)
		# plt.rc('legend', fontsize=15)
		# plt.rc('axes', labelsize=15)

		t = [i*300./len(self.channel1) for i in range(len(self.channel1))]
		plt.clf()
		plt.plot(t,np.array(self.channel1),color='red',label='NS')
		plt.plot(t,np.array(self.channel2),color='blue', label='EW')
		plt.legend()
		# plt.grid()
		plt.ylabel('Amplitude')
		h = self.header()
		plt.xlabel('Time, sec')
		# plt.xticks(range(0,301,10))
		# plt.yticks(range(20000,46001,2000))
		plt.xlim(0,300)
		plt.title(h[:16]+' '+h[16:])
		plt.show()

if __name__ == '__main__':
	destination = '/home/foxy/ELF_data/bin_files/'
	# filename = '200811130740.dat'
	# filename = '200905101155.dat'
	# filename = '201109062210.dat'
	# filename = '201308160900.dat'
	# filename = '201308201525.dat'
	filename = '201506301700.dat'

	read_elf_class = Read_ELF_Class(filename=filename,
				destination_in=destination)
	f = read_elf_class.read_and_save()
	# read_elf_class.plot()
