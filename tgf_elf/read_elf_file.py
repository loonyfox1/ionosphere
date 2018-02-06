import matplotlib.pyplot as plt

class Read_ELF_Class(object):
	def __init__(self,filename,destination):
		self.filename = filename
		self.destination = destination

	def header(self):
		with open(self.destination+self.filename, "rb") as f:
			header = str(f.read(46))
		return header[2:-13]

	def read_bytes(self):
		byte_array = []
		with open(self.destination+self.filename, "rb") as f:
			byte = f.read(1)
			while byte != b'':
				byte_array.append(byte)
				byte = f.read(1)
		return byte_array

	def bytes_to_hex(self):
		byte_array = self.read_bytes()
		new_byte = []
		for i in range(64,len(byte_array),1):
			time_s = str(byte_array[i])
			time_s = repr(time_s)
			if("\\x" in time_s):
				time_s = time_s[6:8]
			else:
				time_s = hex(ord(time_s[3:4]))[2:]
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
		return channel1[:channel1.index(0)],channel2[:channel2.index(0)]

	def read_and_save(self):
		self.fileheader = self.header()
		self.channel1,self.channel2 = self.hex_to_decimal()
		with open(self.filename, "w") as f:
			f.write(self.fileheader+'\n')
			for i in range(len(self.channel1)-1):
				f.write(repr(self.channel1[i])+'\t'+repr(self.channel2[i])+'\n')
			f.write(repr(self.channel1[-1])+'\t'+repr(self.channel2[-1]))
		return self.filename

	def plot(self):
		t = [i*300/len(self.channel1) for i in range(len(self.channel1))]
		plt.clf()
		plt.plot(t,self.channel1,color='blue',label='NS')
		plt.plot(t,self.channel2,color='red', label='EW')
		plt.legend()
		plt.grid()
		plt.ylabel('Amplitude')
		plt.xlabel('Time, sec')
		plt.title(self.header())
		plt.show()

if __name__ == '__main__':
	destination = '/root/ELF_data/'
	# filename = '200811130740.dat'
	# filename = '200905101155.dat'
	# filename = '201109062210.dat'
	filename = '201308160900.dat'
	# filename = '201308201525.dat'

	read_elf_class = Read_ELF_Class(filename=filename,
									destination=destination)
	f = read_elf_class.read_and_save()
	read_elf_class.plot()
