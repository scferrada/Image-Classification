import cv2
import numpy as np
import os
import sys
from sklearn import svm
from CalcSift import calc_sift

def print_usage():
	print "Usage: python %s <kernel_args> <bovw_folder> <img_folder>" % sys.argv[0]
	print "where kernel is one of these:"
	print "\t linear"
	print "\t rbf_gamma_c"
	exit(1)


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
files = [f for f in os.listdir(bovw_folder) if not (f.endswith("npy") and f.endswith("dict"))]
bovws = []
classes = []
for file in files:
	with VectorSerializer(os.path.join(bovw_folder,file)) as serializer:
		for i in xrange(serializer.size()):
			(bovw, clazz) = serializer.get(i)
			bovws.append(bovw)
			classes.append(clazz)


clf.fit(bovws, classes)

img_folder = sys.argv[3]
for dir, subdirlist, filelist in os.walk(img_folder):
	for file in [f for f in filelist if f.endswith('jpg')]:
		kp, desc = calc_sift(file)
		

#then query, predict and measure accuracy
