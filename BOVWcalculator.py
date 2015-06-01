import cv2, os, sys
from VectorSerializer import VectorSerializer
import operator
import math
import numpy as np

if len(sys.argv) < 5:
	print "Usage: python %s <number_of_clusters> <out_folder> <descriptors_folder_1> <class_name1> [<descriptors_folder_2> <class_name_2> ...]" %(sys.argv[0])
	exit()

clusters = int(sys.argv[1])
folder_out = sys.argv[2]
folders_start = 3 # one over the last parameter number read.
folder_cluster = {}
class_dictionary = {}
for i in xrange(folders_start,len(sys.argv),2):
	folder = sys.argv[i]
	clustername = sys.argv[i+1]
	class_dictionary[i-folders_start] = clustername
	folder_cluster[folder] = i-folders_start

# With class_amount_list array keep track of the amount of descriptors found
# per image so we can match descriptors with single images later on.
# Actually we store the class of the image and the amount of descriptors
# found in it as pairs in this array since that is the info we need later.
class_amount_list = []

descriptors = []

print "Reading descriptors"
for folder, clusternumber in folder_cluster.items():
	#navigate through the descriptors in the folder
	for dir, subdirlist, filelist in os.walk(folder):
		for file in [f for f in filelist if not f.endswith('vindex.npy')]:
			with VectorSerializer(os.path.join(dir,file)) as serializer:
				arr = serializer.get(0)
				class_amount_list.append((clusternumber,len(arr)))
				descriptors.extend(arr)#=read descriptors from disk
					
descriptors = np.array(descriptors)

print "Running k-means"
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.1)
compactness, labels, centers = cv2.kmeans(descriptors, clusters, criteria, 1, cv2.KMEANS_PP_CENTERS)

# transform labels: [[x], [y], [z]] ->  [x, y, z]
labels = [x[0] for x in labels]


with VectorSerializer(os.path.join(folder_out, 'centers')) as serializer:
	serializer.append(centers)

print "Precalculating term appearances count in documents"
word_in_doc_count = [0] * clusters
i=0
# Find out number of documents that contain each word for idf term
for clusternumber, amount in class_amount_list:
	aux = [0] * clusters
	for word in labels[i:i+amount]:
		aux[word] = 1
	word_in_doc_count = map(operator.add, aux, word_in_doc_count)
	i+=amount
idf = [math.log(1.0*len(class_amount_list)/x) for x in word_in_doc_count]
# Free memory
aux = None
word_in_doc_count = None

print "Writing cached IDF"
with VectorSerializer(os.path.join(folder_out,'out.idf')) as serializer:
	serializer.append(idf)

print "Writing dictionary"
#Write dictionary
with VectorSerializer(os.path.join(folder_out,'out.dict')) as serializer:
	serializer.append(class_dictionary)

print "Writing BOVW"
i=0
with VectorSerializer(os.path.join(folder_out, 'out')) as serializer:
	for clusternumber, amount in class_amount_list:
		hist = [0] * clusters
		for j in xrange(i,i+amount):
			hist[labels[i]]+=1
		
		# Normalize by tf-idf
		hist = [1.0*x/amount * idf[idx] for idx,x in enumerate(hist)]
		
		serializer.append((hist, clusternumber))
		i+=amount