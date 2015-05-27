import cv2
import numpy as np
import os
import sys

clusters = int(sys.argv[1])
descriptors_folder = sys.argv[2]
descriptors = np.array() #should load descriptors from folder
descriptors = np.float32(descriptors)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.1)
compactness, labels, centers = cv2.kmeans(descriptors, clusters, criteria, 10, cv2.KMEANS_PP_CENTERS)

#calculation of BOVW
	