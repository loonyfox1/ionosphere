from __future__ import print_function
import threading
import pyxhook
import time
class HotKeysDetector(threading.Thread):
	"""
		This is the main class. Instantiate it, and you can hand HotKeys
		(functions in your own code).

		parameters      : Drop parameter to handle function?
		position        : Is the order of keys pressed important?
		deamon          : Work as deamon?
	"""
	def __init__(self,parameters=False,position=False,deamon=True):
		threading.Thread.__init__(self)
		self.finished = threading.Event()
		# self.parameters={
		# 'pressed':'',
		# 'maximum_length':0,
		# 'list_hot_keys':{},
		# 'parameters':parameters_flag,
		# 'running':True
		# }

		self.position=position
		self.pressed=[]
		self.maximum_length=0
		self.list_hot_keys={}
		self.parameters=parameters
		self.running=True
		self.last=[]

		self.hookman = pyxhook.HookManager()
		# Define our callback to fire when a key is pressed down
		self.hookman.KeyDown = self.key_press_event
		self.hookman.KeyUp = self.key_release_event
		# Hook the keyboard
		self.hookman.HookKeyboard()
		# Start our listener
		self.hookman.start()

	def key_release_event(self,event):

		key=event.Key.upper()
		# print(key)

		if(key in self.pressed):
			self.pressed.remove(key)
			#self.pressed='+'.join(time_array)


		if(key in self.last):
			self.last.remove(key)
		#    self.last
		# print(self.pressed)

	def key_press_event(self,event):
		if not (event.Key.upper() in self.last):

			self.pressed.append(event.Key.upper())
			self.last.append(event.Key.upper())

			for dict_keys in self.list_hot_keys:
				if(len(self.list_hot_keys[dict_keys].get_hotkey())==len(self.pressed)):

					compare=[]
					if self.position:
						compare=[True for i in range(len(self.pressed))] if self.list_hot_keys[dict_keys].get_hotkey()==self.pressed else compare.append(False)

					else:
						for keys in self.list_hot_keys[dict_keys].get_hotkey():
							compare.append(True) if keys in self.pressed else compare.append(False)

					if((compare is not None) and (all(compare)) and (len(compare)==len(self.pressed))):
						#print('HotKeys detect '+keys)
						self.list_hot_keys[dict_keys].pressed()
						self.pressed=self.last[:]
						break
			#print(self.pressed)


	def run(self):
		while self.running:
			time.sleep(0.1)
		self.cancel()

	def cancel(self):
		self.running=False
		self.hookman.cancel()
		self.finished.set()

	def delete_key(self,first=True,number=1):
		#print('Before '+self.pressed)
		time_array=self.pressed.split('+')
		#print(time_array)
		if first:
			self.pressed='+'.join(time_array[number:])
		else:
			self.pressed='+'.join(time_array[:len(time_array)-number])
		#print('After '+self.pressed)

	def addhotkeys(self,string_key,events,parameter=None):
		string_key=string_key.upper()
		self.list_hot_keys[string_key]=HotKey(string_key,events,parameter,string_key.split('+'))




class HotKey:
	"""
		This class create for every new HotKeys

		name        : String which return to handle function (name)
		function    : Handle function
		parameter   : Dictionary wich dropen in handle function
		hotkey      : Array, use to compare with pressed key
	"""
	def __init__(self, name,function,parameter,hotkey):

		self.name=name
		self.function=function
		self.parameter=parameter
		self.hotkey=hotkey
	def __str__(self):
		return '\n'.join((
			'Name: {s.name}',
			'Function: {s.function}',
			'Parameter: {s.parameter}',
			'Hotkey: {s.hotkey}',
		)).format(s=self)
	def get_name(self):
		return self.name

	def get_parameter(self):
		return self.parameter

	def get_hotkey(self):
		return self.hotkey

	def pressed(self):
		if(self.parameter is None):
			self.function(self)
		else:
			self.function(self,self.parameter)
