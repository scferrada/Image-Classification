import numpy as np
import os
import time

class VectorSerializer:
	def __init__(self, filename):
		self.filename = filename
		self.handle = None
		self.vindex = None
		self.seek_time = 0
		self.load_time = 0
		
	def __enter__(self):
		if os.path.isfile(self.filename):
			self.handle = open(self.filename,'a+b')
		else:
			self.handle = open(self.filename,'w+b')
		if os.path.isfile(self.filename + '.vindex.npy'):
			self.vindex = np.load(self.filename + '.vindex.npy')
		else:
			self.vindex = []
		return self
		
	def __exit__(self, type, value, traceback):
		self.handle.close()
		np.save(self.filename+'.vindex.npy',self.vindex)
		self.handle = None
		self.vindex = None
		
	def append(self, descriptor):
		if(self.handle == None):
			raise Exception('Use in a with block.')
		# Move to the end of the file
		self.handle.seek(0,2)
		self.vindex.append(self.handle.tell())
		np.save(self.handle, descriptor)
		
	def get(self, i):
		if(self.handle == None):
			raise Exception('Use in a with block.')
		if i >= len(self.vindex) or i < 0:
			raise IndexError('list index out of range')
		
		start_time=time.time()
		self.handle.seek(self.vindex[i])
		self.seek_time = time.time()-start_time
		start_time=time.time()
		value = np.load(self.handle)
		self.load_time = time.time()-start_time
		return value
	
	def size(self):
		if(self.handle == None):
			raise Exception('Use in a with block.')
		return len(self.vindex)