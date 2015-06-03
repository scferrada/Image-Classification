import numpy as np
import os, sys
from VectorSerializer import VectorSerializer
from collections import Counter

results = sys.argv[1]
# out = sys.argv[2]
with VectorSerializer(os.path.join('.', results)) as serializer:
	tuples = serializer.get(0).tolist()
	#print tuples
	#c0 = [1 for [x,y] in tuples if x == 0].count(1)
	#c1 = [1 for [x,y] in tuples if x == 1].count(1)
	#c2 = [1 for [x,y] in tuples if x == 2].count(1)
	m00 = [1 for [x,y] in tuples if x == 0 and y == 0].count(1)
	m11 = [1 for [x,y] in tuples if x == 1 and y == 1].count(1)
	m22 = [1 for [x,y] in tuples if x == 2 and y == 2].count(1)
	m01 = [1 for [x,y] in tuples if x == 0 and y == 1].count(1)
	m12 = [1 for [x,y] in tuples if x == 1 and y == 2].count(1)
	m20 = [1 for [x,y] in tuples if x == 2 and y == 0].count(1)
	m02 = [1 for [x,y] in tuples if x == 0 and y == 2].count(1)
	m10 = [1 for [x,y] in tuples if x == 1 and y == 0].count(1)
	m21 = [1 for [x,y] in tuples if x == 2 and y == 1].count(1)
	
	# with VectorSerializer(os.path.join('.', out)) as m_serializer:
		# m = [[m00, m01, m02], [m10, m11, m12], [m20, m21, m22]]
		# m_serializer.append(m)
	
	print "\t bicycle boat\t cow"
	print "bicycle\t %d\t %d\t %d" % (m00, m01, m02)
	print "boat\t %d\t %d\t %d" % (m10, m11, m12)
	print "cow\t %d\t %d\t %d" % (m20, m21, m22)
	