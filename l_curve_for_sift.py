import cv2
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

folder = sys.argv[1] #check if folder
sift = cv2.SIFT()
image_files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f))]
for file in image_files:
	image = cv2.imread(file)
	gray_img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	kp, desc = sift.detectAndCompute(gray_img)
	#save to file

sample = np.array()#=read descriptors from disk
sample = np.float32(sample)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.1)
wss = []
for k in range(2, 100): #this is only to determine
	compactness, labels, centers = cv2.kmeans(sample, k, criteria, 1, cv2.KMEANS_PP_CENTERS) #maybe more attempts are required
	wss.append(compactness)
	
plt.plot(wss, range(1,100), '-ro')
plt.show()