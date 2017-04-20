import numpy as np
import math
from lxml.html import document_fromstring
from io import StringIO
import sys, getopt
import regex as re
import queue as q

def highest(w,subs):
	print(len(w))
	pq = q.PriorityQueue()
	dic = {}
	for i in range(0,len(w)):
		# print(len(dic))
		st = w[i][0]
		y = int(w[i][1])
		t = subs[st]
		for k in t.keys():
			if k in dic:
				dic[k] += y*t[k]
			else:
				dic[k] = y*t[k]

	for item in dic.keys():
		val = dic[item]
		if val == 3:
			print(item)
		if pq.qsize() < 2:
			pq.put([-1*val, item])
		else:
			maxium = pq.get()

			x = pq.get()
			temp = x[0]
			if -1*val < temp:
				pq.put([-1*val, item])
			else:
				pq.put(x)
			pq.put(maxium)
	print(dic['TAGQE'])
	print(pq.qsize())
	# while not pq.empty:
	print(pq.get())
	print(pq.get())

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
		# print(i,'--->',len(w))
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

	l = 5
	print("*******************************")
	print("p = ",l)
	f = open('hw5train.txt', 'r')
	arr = np.loadtxt(f, dtype=bytes,delimiter=' ').astype(str)
	f.close()

	subs = {}
	for item in arr:
		# print(item[0])
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
	# print(subs[w[0][0]])
	highest(w,subs)




readData();