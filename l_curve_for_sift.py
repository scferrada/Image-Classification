import cv2
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from VectorSerializer import VectorSerializer

folder = sys.argv[1] #check if folder

sample = []
for dir, subdirlist, filelist in os.walk(folder):
	for file in [f for f in filelist if not f.endswith('vindex.npy')]:
		with VectorSerializer(os.path.join(dir,file)) as serializer:
			for i in xrange(serializer.size()):
				sample.extend(serializer.get(i))#=read descriptors from disk
#sample = np.float32(sample)
print len(sample)
sample = np.array(sample)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.1)
wss = []
for k in xrange(10, 200, 5): #this is only to determine
	compactness, labels, centers = cv2.kmeans(sample, k, criteria, 1, cv2.KMEANS_PP_CENTERS) #maybe more attempts are required, watch for memory limit
	wss.append(compactness)
	if k%10 == 0:
		print k
	
plt.plot(range(10,200,5), wss, '-ro')
plt.show()