import numpy as np
import os

class VectorSerializer:
	def __init__(self, filename, overwrite = False):
		self.filename = filename
		self.handle = None
		self.vindex = None
		self.overwrite = overwrite
		
	def __enter__(self):
		if not self.overwrite and os.path.isfile(self.filename):
			self.handle = open(self.filename,'a+b')
		else:
			self.handle = open(self.filename,'w+b')
		if not self.overwrite and os.path.isfile(self.filename + '.vindex.npy'):
			self.vindex = np.load(self.filename + '.vindex.npy').tolist()
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
		
		self.handle.seek(self.vindex[i])
		value = np.load(self.handle)
		
		# Handle dictionaries saved as 0-dimensional arrays
		if value.shape == ():
			value = value.item()
		return value
	
	def size(self):
		if(self.handle == None):
			raise Exception('Use in a with block.')
		return len(self.vindex)