import numpy as np
import os, sys
from VectorSerializer import VectorSerializer
from collections import Counter

results = sys.argv[1]
with VectorSerializer(os.path.join('.', results)) as serializer:
	tuples = serializer.get(0).tolist()
	print tuples
	stats = Counter(tuples)
	print stats
	