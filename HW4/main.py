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
		print(dictSet[wavg.index(item)].strip('\n'))

	print("Three largest coordiante: ")
	for i in range(0,3):
		item = maxHeap.get()
		print(dictSet[wavg.index(-item)].strip('\n'))

def norm(vec):
	res = 0
	for i in vec:
		res += i * i
	return math.sqrt(res)

def readData():
	dataSet = []
	train = []
	f = open('hw4train.txt', 'r')
	for line in f.readlines():
		line = line.strip('\n')

		floats = line.split(' ')

		vecs = [float(i) for i in floats[0:len(floats)]]
		# print(len(vecs))

		dataSet.append(vecs)

	# print(dataSet[0][819])
	# print(len(dataSet))
	train = deepcopy(dataSet)
	firstClass = []
	for item in dataSet:			# define: labe 1 --> +1, label 2 --> -1
		if item[len(item)-1] == 1:
			firstClass.append(item);
		if item[len(item)-1] == 2:
			item[len(item)-1] = -1
			firstClass.append(item);

	fileName = str(sys.argv[1])
	print('file name-->',fileName)
	testdata = []
	testSet = []
	t = open(fileName, 'r')
	for line in t.readlines():
		line = line.strip('\n')

		floats = line.split(' ')

		vecs = [float(i) for i in floats[0:len(floats)]]
		# print(len(vecs))

		testdata.append(vecs)
	t.close()
	testSet = deepcopy(testdata)
	testclass = []
	for item in testdata:			# define: labe 1 --> +1, label 2 --> -1
		if item[len(item)-1] == 1:
			testclass.append(item);
		if item[len(item)-1] == 2:
			item[len(item)-1] = -1
			testclass.append(item);

	if(fileName == 'hw4test.txt'):
		train = testSet
		size = len(testclass)
	else:
		size = len(firstClass)

	################### Regular Perceptron ###########################
	# 3.1
	print("------------- regular perceptron --------------")
	w = [0] * (len(dataSet[0])-1)	#intialize w to 0 vector
	for count in range(0,4):
		w = regPerceptron(w, firstClass.copy())
		size
		err = 0
		for item in train:
			if item[len(item)-1] == 1 or item[len(item)-1] == 2:
				sign = dotProduct(w,item[0:819])
				# print(sign)
				pred = 0
				if sign > 0:
					pred = 1
				else:
					pred = 2
				if(pred != item[len(item)-1]):
					err += 1
		print(count+1, "th perception:")
		print(err/size)

	#################### voted Percetron ############################
	print("------------- voted and average perceptron --------------")
	w = [0] * (len(dataSet[0])-1)
	pairs = [[w,1]]
	size
	for i in range(0,4):
		pairs = votePercept(pairs, firstClass.copy())
		vote_err = 0
		avg_err = 0
		w_avg = avg(pairs.copy())
		for item in train:
			if item[len(item)-1] == 1 or item[len(item)-1] == 2:
				sign = vote(pairs.copy(),item[0:819])
				pred = 0
				if sign > 0:
					pred = 1
				else:
					pred = 2
				if pred != item[len(item)-1]:
					vote_err += 1

				sign = dotProduct(w_avg.copy(), item[0:819])
				pred = 0
				if sign > 0:
					pred = 1
				else:
					pred = 2
				if pred != item[len(item)-1]:
					avg_err += 1

		print(i+1, "pass voted perceptron error: ", vote_err / size)
		print(i+1, "pass average perceptron error: ", avg_err / size)
		if i == 2 and fileName == 'hw4train.txt':
			interpret(w_avg.copy())
		print('--------->')


	f.close()

readData()
