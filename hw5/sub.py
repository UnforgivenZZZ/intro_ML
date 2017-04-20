import numpy as np
import math
from lxml.html import document_fromstring
from io import StringIO
import sys, getopt
import regex as re
import queue as q

def percept(trainSet,subs):
	w = np.empty(shape=[0,2])
	w = np.append(w,[[ trainSet[0][0], trainSet[0][1] ]],axis=0)
	# w = np.zeros(len(phi[0][0]))
	for i in range(1,len(trainSet)):
		# print(len(w))
		# p = phi[i][0]
		# l = phi[i][1]
		s = trainSet[i][0]
		l = trainSet[i][1]
		print(i,'˚∆˚',len(w))
		# print(w)
		# print(p)
		temp = 0
		# a = kernel1(s, subs[i])
		for item in w:
			# b = kernel1(item[0], subs[i])
			temp += int(item[1]) * kernel1(s,subs,item[0],subs)
		if int(l)*temp <= 0:
			w = np.append(w,[[ trainSet[i][0],trainSet[i][1] ]],axis=0)

	return w


def kernel1(s1,subs1,s2,subs2):

	# d = []
	# # for s in s1:
	# 	# print(item[0])
		
	# j = 0
	# # print(len(s1))
	# while j <= len(s1)-l:
	# 	# print(s[j:j+l])
	# 	d.append(s1[j:j+l])
	# 	j+=1

	# res = 0
	# substr = list(set(d))
	# for item in substr:
	# 	# res.append(len(re.findall(item, s1, overlapped=True)))
	# 	res += len(re.findall(item, s1, overlapped=True)) * len(re.findall(item, s2, overlapped=True))
	res = 0
	d = subs1[s1]
	t = subs2[s2]
	for item in d.keys():
		if item in t:
			res += d[item] * t[item]
	return res


def readData():

	l = int(sys.argv[1])
	print("*******************************")
	print("p = ",l)
	f = open('hw5train.txt', 'r')
	arr = np.loadtxt(f, dtype=bytes,delimiter=' ').astype(str)
	f.close()

	subs = {}
	print("forming substring hash table")
	for item in arr:
		print("substring hash table for string ",item[0])
		s = item[0]
		j = 0
		d = []
		dt = {}
		while j <= len(s)-l:
			# print(s[j:j+l])
			d.append(s[j:j+l])
			j+=1
		d = list(set(d))
		for ss in d:
			dt[ss] = len(re.findall(ss, s, overlapped=True))
		
		subs[s] = dt



	# print(subs[arr[0][0]])
	
	w = percept(arr,subs)
	err = 0
	size = len(arr)
	
	c = 1
	for i in range(0,len(arr)):
		print(c)
		c+=1
		s = arr[i][0]
		y = arr[i][1]
		
		# a = kernel1(s, subs[i])
		temp = 0
		for item in w:
			temp += int(item[1]) * kernel1(s,subs,item[0],subs)
	
		if int(y)*temp < 0:
			err+=1
	trainerr = err / size

	f = open('hw5test.txt', 'r')
	test = np.loadtxt(f, dtype=bytes,delimiter=' ').astype(str)
	f.close()

	testSub = {}
	for item in test:
		s = item[0]
		j = 0
		d = []
		dt = {}
		while j <= len(s)-l:
			# print(s[j:j+l])
			d.append(s[j:j+l])
			j+=1
		d = list(set(d))
		for ss in d:
			dt[ss] = len(re.findall(ss, s, overlapped=True))
		testSub[s] = dt

	c = 1
	err = 0
	size = len(test)
	for i in range(0,len(test)):
		print(c)
		c+=1
		s = test[i][0]
		y = test[i][1]
		
		# a = kernel1(s, subs[i])
		temp = 0
		for item in w:
			temp += int(item[1]) * kernel1(s,testSub,item[0],subs)
	
		if int(y)*temp < 0:
			err+=1

	print('training error: ',trainerr)
	print("test error: ", err/size)



readData();