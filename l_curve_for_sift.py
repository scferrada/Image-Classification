import cv2
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

folder = sys.argv[1] #check if folder

sample = []
for dir, subdirlist, filelist in os.walk(folder):
	for file in [f for f in filelist if not f.endswith('vindex.npy')]:
		with VectorSerializer(os.path.join(folder,file)) as serializer:
			for i in xrange(serializer.size()):
				sample.append(serializer.get(i))#=read descriptors from disk
sample = np.float32(sample)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.1)
wss = []
for k in range(2, 100): #this is only to determine
	compactness, labels, centers = cv2.kmeans(sample, k, criteria, 1, cv2.KMEANS_PP_CENTERS) #maybe more attempts are required, watch for memory limit
	wss.append(compactness)
	
plt.plot(wss, range(1,100), '-ro')
plt.show()