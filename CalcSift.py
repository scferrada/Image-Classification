import cv2
import numpy as np
import os
import sys
from VectorSerializer import VectorSerializer

folder = sys.argv[1] #check if folder
outFolder = sys.argv[2]
sift = cv2.SIFT()
image_files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f))]
for fileName in image_files:
	filePath = os.path.join(folder,fileName)
	image = cv2.imread(filePath)
	gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	kp, desc = sift.detectAndCompute(gray_img, None)
	with VectorSerializer(os.path.join(outFolder,fileName)) as serializer:
		serializer.append(desc)