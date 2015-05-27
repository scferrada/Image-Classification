import cv2
import numpy as np
import os
import sys
from sklearn import svm

def serialize(x):
	pass
	
def deserialize(x):
	pass

clusters = int(sys.argv[1])
descriptors_folder = sys.argv[2]
descriptors = np.array() #should load descriptors from folder
descriptors = np.float32(descriptors)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.1)
compactness, labels, centers = cv2.kmeans(descriptors, clusters, criteria, 10, cv2.KMEANS_PP_CENTERS)

#calculation of BOVW
index = 0
for descriptor in [f for f in os.listdir(descriptors_folder) if os.path.isfile(os.path.join(descriptors_folder,f))]:
	keypoints = deserialize(descriptor)#.getNbofKeypoints() #something like it
	bovw = [0 for x in range(clusters)]
	for point in range(keypoints):
		bovw[labels[i+point]] += 1
	serialize(normalize(bovw))
	i += keypoints

bovws = [] #should read them from disk
classes = [] #vector with the class of each photo, should be read from disk
clf = svm.SVC()
print clf.fit(bovws, classes)

#then query, predict and measure accuracy
