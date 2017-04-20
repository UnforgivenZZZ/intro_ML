import numpy as np
import math
from lxml.html import document_fromstring
from io import StringIO
import sys, getopt
import regex as re

def dotProduct(w,data):
	v1 = w
	v2 = data
	if len(v1) != len(v2):
		print('bad dimension: vector has different size:',len(v1), " ", len(v2))
		# return -99
		# print(len(minLen))
	else:
		res = 0
		for i in range(0,len(v1)):
			res += v1[i] * v2[i]
		return res


def percept(trainSet, l):
	w = np.empty(shape=[0,2])
	w = np.append(w,[[ trainSet[0][0], trainSet[0][1] ]],axis=0)
	
	for i in range(1,len(trainSet)):
		# print(w)
		print(i,'--->',len(w))

		s = trainSet[i][0]
		j = 0
		d = np.array(s[j:j+l])
		while j <= len(trainSet[i][0])-l:
			d = np.append(d,s[j:j+l])
			j+=1

		d = np.unique(d)
		a = []
		for x in d:
			a.append(len(re.findall(x, trainSet[i][0], overlapped=True)))

		temp = 0
		for item in w:
			b = kernel1(item[0],d)
			temp += int(item[1])*dotProduct(a,b)

		if (int(trainSet[i][1]) * temp) <= 0:
			w = np.append(w,[[ trainSet[i][0],trainSet[i][1] ]],axis=0)
	
	return w


def kernel1(s1,substr):
	res = []
	for item in substr:
		res.append(len(re.findall(item, s1, overlapped=True)))
	return res


def readData():

	l = int(sys.argv[1])

	f = open('hw5train.txt', 'r')
	arr = np.loadtxt(f, dtype=bytes,delimiter=' ').astype(str)
	f.close()
	print(l)
	w = percept(arr,l)
	err = 0
	size = len(arr)
	
	c = 1
	for item in arr:
		print(c)
		c+=1

		s = item[0]
		j = 0
		d = np.array(s[j:j+l])
		while j <= len(s)-l:
			d = np.append(d,s[j:j+l])
			j+=1

		d = np.unique(d)
		a = []
		for x in d:
			a.append(len(re.findall(x, s, overlapped=True)))

		temp = 0
		for i in w:
			b = kernel1(i[0], d)
			temp += int(i[1]) * dotProduct(a,b)

		if (int(item[1]) * temp) <= 0:
			err+=1
	print(err / size)


	

readData();