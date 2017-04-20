import numpy as np
import math
import sys, getopt
import copy
from copy import deepcopy
import queue as q
from lxml.html import document_fromstring

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
		# print('-->',len(v2))

# return v1 + label*data
def addition(v1,data,label):
	v2 = data
	if len(v1) != len(v2):
		print('bad dimension: vector has different size:',len(v1), " ", len(v2))
		# return -99
		# print(len(minLen))
	else:
		for i in range(0,len(v1)):
			v1[i] += label * v2[i]
		return v1


def regPerceptron(w, dataSet):
	# print(w)
	# print(len(w))
	for item in dataSet:
		label = item[len(item)-1]
		# dotProduct(w,item[0:819])
		if label * dotProduct(item[0:819],w) <= 0:
			w = addition(w,item[0:819],label)
			# print(w==w1)
	return w;

def votePercept(pairs, dataSet):
	for item in dataSet:
		latest = pairs[len(pairs)-1]
		label = item[len(item)-1]
		w = latest[0]
		if label * dotProduct(w, item[0:819]) <= 0:
			new_w = addition(w.copy(), item[0:819],label)
			# print(w==new_w, item)
			pairs.append([new_w,1])
		else:
			pairs[len(pairs)-1][1] += 1
	return pairs

def vote(pairs, x):
	res = 0
	for item in pairs:
		c = item[1]
		w = item[0].copy()
		sign = dotProduct(w,x)
		if sign != 0:
			sign = sign / abs(sign)
		res += c * sign
	return res

def avg(pairs):
	wavg = [0] * len(pairs[0][0])
	for item in pairs:
		c = item[1]
		w = item[0].copy()
		w = addition(wavg, w.copy(), c)

	return wavg

def interpret(wavg):
	print("After 3 passes: ")
	dictSet = []
	f = open('hw4dictionary.txt','r')
	for line in f.readlines():
		line.strip('\n')
		dictSet.append(line)
	f.close()
	pq = q.PriorityQueue()
	maxHeap = q.PriorityQueue()
	for i in wavg:
		pq.put(i)
		maxHeap.put(-i)

	print("Three lowest coordinate: ")
	for i in range(0,3):
		item = pq.get()
		print("index\t",item,"name\t",dictSet[wavg.index(item)])

	print("Three largest coordiante: ")
	for i in range(0,3):
		item = maxHeap.get()
		print("index\t",item, "name\t", dictSet[wavg.index(-item)])

def printMatrix(matrix):
	for i in matrix:
		print('[',end=' ')
		for j in i:
			print(round(j,5),end='\t')
		print('\b]')
def predict(res):
	p = 7
	for i in [1,2,3,4,5,6]:
		if res[i-1] == i and sum(res) == i:
			p = i
	return p


def readData():
	dataSet = []
	f = open('hw4train.txt', 'r')
	for line in f.readlines():
		line = line.strip('\n')

		floats = line.split(' ')

		vecs = [float(i) for i in floats[0:len(floats)]]
		# print(len(vecs))

		dataSet.append(vecs)
		
	f.close()

	print("one vs all calssifier")
	cm = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
	
	wall = []
	for one in [1,2,3,4,5,6]:
		data = deepcopy(dataSet)
		# print(train == dataSet)
		classify = []
		for item in data:		
			if item[len(item)-1] == one:
				item[819] = 1
				classify.append(item);
				# adads=0
			else:
				item[len(item)-1] = -1
				classify.append(item);
		w = [0] * (len(dataSet[0])-1)
		w = regPerceptron(w,classify)
		wall.append(w)
	# print(len(wall), len(wall[0]))
	# print(train)

	train = []
	t = open('hw4test.txt', 'r')
	for line in t.readlines():
		line = line.strip('\n')

		floats = line.split(' ')

		vecs = [float(i) for i in floats[0:len(floats)]]
		# print(len(vecs))

		train.append(vecs)
	t.close()

	Nj = []
	Cij = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],
	       [0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],
	       [0,0,0,0,0,0]]

	for i in [1,2,3,4,5,6]:
		j = 0
		for item in train:
			# print(item[819])
			if int(item[819]) == i:
				j += 1
		# print(j)
		Nj.append(j)
	# print(Nj)


	for item in train:
		res = [-1,-1,-1,-1,-1,-1]
		for index in range(0,6):
			pred = 0
			sign = dotProduct(wall[index],item[0:819])
			if(sign > 0):
				pred = index+1
			else:
				pred = 0
			res[index] = pred

		prediction = predict(res)
		# print(prediction)
		Cij[prediction-1][int(item[819]-1)] += 1

	for i in [1,2,3,4,5,6,7]:
		for j in [1,2,3,4,5,6]:
			cm[i-1][j-1] = Cij[i-1][j-1] / Nj[j-1]
	printMatrix(cm)




readData()



