import cv2
import numpy as np
import os
import sys
from VectorSerializer import VectorSerializer

def calc_sift(img_path):
	image = cv2.imread(img_path)
	gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	return sift.detectAndCompute(gray_img, None)

folder = sys.argv[1] #check if folder
outFolder = sys.argv[2]
sift = cv2.SIFT()
image_files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f))]
for fileName in image_files:
	filePath = os.path.join(folder,fileName)
	kp, desc = calc_sift(filePath)
	with VectorSerializer(os.path.join(outFolder,fileName)) as serializer:
		serializer.append(desc)