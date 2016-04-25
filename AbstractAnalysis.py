import json
import sys
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import TruncatedSVD

def main(data):
	vectorizer = CountVectorizer(min_df = 5)
	transformer = TfidfTransformer(norm = 'l2')
	svd = TruncatedSVD(n_components = 500)

	abstracts = []
	for key in data.keys():
		if data[key].has_key('Abstract'):
			abstracts.append(data[key]['Abstract'])
	N = len(abstracts)

	print 'Extracting Document Features'
	X = vectorizer.fit_transform(abstracts)
	Y = transformer.fit_transform(X).toarray()
	Z = svd.fit_transform(Y)
	print 'Calculating Distances'
	dist_mat = np.zeros((N,N))
	for i in range(N):
		if i%10 == 0:
			print i
		for j in range(i+1,N):
			dist_mat[i,j] = np.linalg.norm(Z[i,:] - Z[j,:])

	dist_mat += dist_mat.transpose()
	return (Z,dist_mat)


if __name__ == "__main__":
	data = sys.argv[1]
	with open(data,'r') as f:
		data = json.load(f)
	dKeys = data.keys()
	(Z,dist) = main(data)
