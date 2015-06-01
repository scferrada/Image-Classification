import cv2
import numpy as np
import os
import sys
from sklearn import svm
from CalcSift import calc_sift

def print_usage():
	print "Usage: python %s <kernel_args> <bovw_folder> <img_folder1> <class_name1> [<img_folder2> <class_name2>...]" % sys.argv[0]
	print "where kernel is one of these:"
	print "\t linear"
	print "\t rbf_gamma_c"
	exit(1)
	
def closest_center(x, centers):
	closer = 0
	min_dist = float("inf")
	for i in xrange(len(centers)):
		dist = np.sum(np.abs(x - centers[i]))
		if dist < min_dist:
			min_dist = dist
			closer = i
	return closer


if len(sys.argv < 4):
	print_usage()


if sys.argv[1].startswith("linear"):
	clf = svm.SVC(kernel="linear")
elif sys.argv[1].startswith("rbf"):
	try:
		kernel = "rbf"
		args = sys.argv[1].split("_")
		gamma = float(args[1])
		C = float(args[2])
		clf = svm.SVC(gamma=gamma, C=C)
	except ValueError:
		print "gamma and c parameters must be float numbers"
		exit(1)
else:
	print_usage()
	
bovw_folder = sys.argv[2]
bovws = []
classes = []
with VectorSerializer(os.path.join(bovw_folder,'out')) as serializer:
	for i in xrange(serializer.size()):
		(bovw, clazz) = serializer.get(i)
		bovws.append(bovw)
		classes.append(clazz)


clf.fit(bovws, classes)
centers = 0
idf = 0
with VectorSerializer(os.path.join(bovw_folder, 'out.center')) as serializer:
	centers = serializer.get(0)

with VectorSerializer(os.path.join(bovw_folder, 'out.idf')) as serializer:
	idf = serializer.get(0)

folder = 3
for i in xrange(folder, len(sys.argv), 2):
	img_folder = sys.argv[i]
	img_class = sys.argv[i+1]
	for file in [f for f in os.listdir(img_folder) if f.endswith('jpg'):
		kp, desc = calc_sift(file)
		bovw = [0] * len(centers)
		for x in desc:
			center = closest_center(x, centers)
			bovw[center] += 1
		bovw = [1.0*x/len(kp) *idf[idx] for idx, x in enumerate(bovw)]
		
		
#then query, predict and measure accuracy
