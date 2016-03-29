#!/usr/bin/python
from __future__ import division
from copy import deepcopy
import random
import math
import sys
import os



fileName = os.getcwd() + '/MatrixClusters/' + sys.argv[1]
firstStagePercentage = float(sys.argv[2])
print "First Stage Percentage: " + str(firstStagePercentage)
###################################### Environment Settings ##########################
mat_size = 10
incident_cnt = 50
crowd_cnt = 100 #--- current variable
####################################### Query Settings ###############################
t_setting = 30  # t people to query
firstStage_cnt = int(firstStagePercentage*t_setting)
k_setting = 5 # number of nearest neighbours
######################################## Approximation Settings #######################
trial = 10000
average_over = 100 #number of matrices in the file
#######################################################################################
NN = True # Decide which dispersion metric to use

class Point:
	row = -1
	col = -1
	dis = -1
	def __init__(self, row_1, col_1):
		self.row = float(row_1)
		self.col = float(col_1)

	def computeDistance(self, row2, col2):
		row2F = float(row2)
		col2F = float(col2)
		self.dis = math.sqrt((row2F-self.row)** 2 + (col2F-self.col)** 2)
		return self.dis

def generateRandom():
	return random.randrange(0, mat_size*mat_size)


def generateUniqueRandom(N):
	list = []
	for i in range (0, N):
		rand_num = generateRandom()
		while rand_num in list:
			rand_num = generateRandom()
		list.append(rand_num)
	print list
	return list

def returnShuffled(x):
	x_copy = list(x)
	while x == x_copy:
		random.shuffle(x)
	return x

def computeAvgDistNN(points):

	dis =[]
	for p in points:
		points_copy = list(points)
		points_copy.remove(p)
		nn = getKNN(p, 1, points_copy)
		dis.append(p.computeDistance(nn[0].row, nn[0].col))
	return sum(dis)/ len(dis)



def computeDisp(points):
	mean_x = 0
	mean_y = 0
	var_x = 0
	var_y = 0
	size = len(points)
	points_copy = list(points)
	for p in points_copy:
		p.row = p.row +1
		p.col = p.col +1
		mean_x = mean_x + p.row
		mean_y =  mean_y + p.col
	mean_x = mean_x/size
	mean_y = mean_y/size

	for p in points_copy:
		var_x += (p.row  - mean_x) **2
		var_y += (p.col  - mean_y) **2
	var_x = var_x/size
	var_y = var_y/size


	dispX = var_x/mean_x
	dispY = var_y/mean_y

	return (dispX + dispY)



def numToIndex(num):
	row = num//mat_size
	col = num%mat_size
	return Point(row, col)
	#return {'row':row, 'col':col}

def maximizeDispersion(crowdPoints, n, trial_cnt, NN):
	# crowdPoints is a list of  points
	maxDisp = 0
	maxCrowdList = []
	crowdPoints_copy = deepcopy(crowdPoints)

	for i in range (0, trial_cnt):
		random.shuffle(crowdPoints_copy) #shufflin in place
		randomCrowd =  list(crowdPoints_copy[0:n])
		if NN == True:
			disp = computeAvgDistNN(deepcopy(randomCrowd))
		else:
			disp = computeDisp(deepcopy(randomCrowd))

		if (disp > maxDisp):
			maxDisp = disp
			maxCrowdList = list(randomCrowd)
	return 	maxCrowdList

def maximizeDispersionExcludeFS(crowdPoints, n, trial_cnt, firstStagePoints, NN):
	# crowdPoints is a list of  points
	# NN is true if you want to use the Nearest neighbor dispersion metric
	maxDisp = 0
	maxCrowdList = []
	crowdPoints_copy = deepcopy(crowdPoints)
	newCrowdPoints = []
	for cp in crowdPoints_copy: #Remove the firstStagePoints
		if cp not in firstStagePoints:
			newCrowdPoints.append(cp)
	for i in range (0, trial_cnt):
		random.shuffle(newCrowdPoints) #shufflin in place
		randomCrowd =  list(newCrowdPoints[0:n])
		if NN == True:
			disp = computeAvgDistNN(deepcopy(randomCrowd))
		else:
			disp = computeDisp(deepcopy(randomCrowd))
		if (disp > maxDisp):
			maxDisp = disp
			maxCrowdList = list(randomCrowd)
	return 	maxCrowdList

def getKNN(point, k, crowdPoints):
	# crowd Points is a list objects of the class Point
	for p in crowdPoints:
		p.computeDistance(point.row, point.col)
	sortedPoints = sorted(crowdPoints, key=lambda x: x.dis, reverse=False)
	return sortedPoints[0:k]

def getKNNExcludeFS(point, k, crowdPoints, firstStagePoints):
	# crowd Points is a list objects of the class Point
	for p in crowdPoints:
		p.computeDistance(point.row, point.col)
	sortedPoints = sorted(crowdPoints, key=lambda x: x.dis, reverse=False)
	firstStagePoints_1D = TwoD_toPoints(firstStagePoints)
	sortedPoints_1D = TwoD_toPoints(sortedPoints)
	new_sortedPoints_1D = []
	for sp in sortedPoints_1D:
		if sp not in firstStagePoints_1D:
			new_sortedPoints_1D.append(sp)
	return new_sortedPoints_1D[0:k]


def indicesToNum(p):
	return p.row*mat_size + p.col

def pointsto2D(points):
	TwoD_points = []
	for p in points:
		TwoD_points.append(numToIndex(p))
	return TwoD_points

def TwoD_toPoints(TwoD_points):
	points = []
	for p in TwoD_points:
		points.append(indicesToNum(p))
	return points


def intersectCnt(points1, points2):
	return len(list(set(points1) & set(points2)))
	#cnt = 0
	#for p1 in points1:
	#	if p1 in points2:
	#		cnt += 1
	#return cnt

def mergeWithoutRepition(list1, list2):
#Assuming list1 and list2 do not have any repitiotions
	list3 = []
	for l in list1:
		if l not in list3:
			list3.append(l)
	for l in list2:
		if l not in list3:
			list3.append(l)
	return list3

def sortMergedList(merged_list, num, complementList):
	word_counter = {}
	for word in merged_list:
		if word in word_counter:
			word_counter[word] += 1
		else:
			word_counter[word] = 1
	popular_words = sorted(word_counter, key = word_counter.get, reverse = True)
	for w in popular_words:
		if w in complementList:
			popular_words.remove(w)

	if num > len(popular_words):
		return popular_words
	else:
		return popular_words[:num]

def readFromFile(matNum):
	#matNum = 1 --> lines 0:10
	#matNum = 2 --> lines 10:20
	#matNum = 3 --> lines 20:30
	i = matNum *10
	j = i+10
	with open(fileName , 'r') as f:
	 lines = f.readlines() # readlines creates a list of the lines
	 m = lines[i:j]
	 points_1D = []
	 m2 = []
	 for l in m:
		l2 = l.split(',')
		l2[9] = l2[9][0]
		m2.append(l2)
	cnt = 0
	for l in m2:
		for e in l:
			if e == '1':
				points_1D.append(cnt)
			cnt += 1
	print m
	print lines
	print m2
	return points_1D

def readFromFile_clustered(matNum):
	#matNum = 1 --> lines 0:100
	#matNum = 2 --> lines 100:200
	#matNum = 3 --> lines 200:300
	i = matNum *crowd_cnt
	j = i+crowd_cnt

	with open(fileName , 'r') as f:
		lines = f.readlines() # readlines creates a list of the lines
	m = lines[i:j]
	clusteredPoints_2D = []
	x = []
	y = []
	for cp in m:
		new_cp = cp.split(",")
		x.append(new_cp[0])
		correctedY = new_cp[1].replace('\n', '')
		y.append(correctedY)
		clusteredPoints_2D.append(Point(new_cp[0], correctedY))
	print m
	print lines
	return clusteredPoints_2D
##################################### Beginning of simulation ##########################################
secondStage_cnt = t_setting - firstStage_cnt
#secondStage_perIncidentCnt = secondStage_cnt//incident_cnt



cnt_random = 0
cnt_max_disp = 0
cnt_x_max_disp = 0

incid_random = 0
incid_max_disp = 0
incid_x_max_disp = 0

two_stage_err = 0
for j in range (0, average_over):

	incident_points_2D = readFromFile_clustered(j)
	crowd = generateUniqueRandom(crowd_cnt)


	print "Crowd: " + str(crowd)



	crowd_copy = list(crowd)
	crowd_points_2D = pointsto2D(crowd)

	crowd_copy = returnShuffled(crowd_copy)

	crowdPoints_shuffled_2D = pointsto2D(crowd_copy)

	t_random_range = crowdPoints_shuffled_2D[0:t_setting]
	t_max_coverage = maximizeDispersion(crowd_points_2D, t_setting, trial, NN)
	t_x_max_coverage = maximizeDispersion(crowd_points_2D, firstStage_cnt, trial, NN)


	#Convert numbers to points
	t_random_range_1D = TwoD_toPoints(t_random_range)
	t_random_range_1D.sort()
	print "T Radom Range: " + str(t_random_range_1D)

	t_max_coverage_1D = TwoD_toPoints(t_max_coverage)
	t_max_coverage_1D.sort()
	print "T Max Coverage: " + str(t_max_coverage_1D)

	t_x_max_coverage_1D = TwoD_toPoints(t_x_max_coverage)
	#print "T X Max Coverage: " + str(t_x_max_coverage_1D)

	t_secStage_max_covergae = []
	secondStage_people_2D = []

	#Need to get people from the first Stage with 100% feedback
	positiveFeedback_1D = []
	for incident in incident_points_2D:
		k_nearest_neighbors_2D = getKNN(incident, k_setting, crowd_points_2D)
		k_nearest_neighbors_1D = TwoD_toPoints(k_nearest_neighbors_2D)
		for p in t_x_max_coverage_1D:  #assumes 100% positive feedback
			if p in k_nearest_neighbors_1D and p not in positiveFeedback_1D:
				positiveFeedback_1D.append(p)
	positive_feedbackCnt = len(positiveFeedback_1D)
	k_pos_feed = [0] * positive_feedbackCnt


	if positive_feedbackCnt == 0: #if first stage does not yield any positive feedback maximize the dispersion
		t_x_nn_secStage = maximizeDispersionExcludeFS(crowd_points_2D, secondStage_cnt, trial, t_x_max_coverage, NN)

	else:
		quota = secondStage_cnt
		while quota > 0:
			i = 0
			for pfp in positiveFeedback_1D: #determine the share of each first stage person
				if quota > 0:
					k_pos_feed[i] += 1
					quota -= 1
				i += 1

	#Second Stage People
		i = 0
		exceptionList_2D = t_x_max_coverage
		for pfd in positiveFeedback_1D: #get the k nearest neighbors excluding fs people and previously selected second stage people
			exceptionList_2D = mergeWithoutRepition(exceptionList_2D, secondStage_people_2D)
			exceptionList_1D = TwoD_toPoints(exceptionList_2D)

			t_x_nearest_neighbors_1D = getKNNExcludeFS(numToIndex(pfd), k_pos_feed[i], crowd_points_2D, exceptionList_2D)
			t_x_nearest_neighbors_2D = pointsto2D(t_x_nearest_neighbors_1D)

			secondStage_people_2D.extend(t_x_nearest_neighbors_2D)
			secondStage_people_1D = TwoD_toPoints(secondStage_people_2D)
			i += 1

		t_x_nn_secStage_1D = secondStage_people_1D


	t_x_merged = mergeWithoutRepition(t_x_max_coverage_1D, t_x_nn_secStage_1D)
	t_x_merged_2D = pointsto2D((t_x_merged))
	t_x_merged.sort()
	print "T Two-Stage: " + str(t_x_merged)

	disp_random = computeDisp(t_random_range)
	disp_max_cov = computeDisp(t_x_max_coverage)
	disp_two_stage = computeDisp(t_x_merged_2D)

	print 'Random Dispersion: ' + str(disp_random)
	print 'Max Coverage Dispersion: ' + str(disp_max_cov)
	print 'Two Stage Dispersion: ' + str(disp_two_stage)

	#Test the success/failure of your metrics
	if len(t_x_merged) != t_setting:
		two_stage_err += 1

	for incident in incident_points_2D:
		print "Incident: " + str(indicesToNum(incident))
		k_nearest_neighbors = getKNN(incident, k_setting, crowd_points_2D)
		#print "K nearest neighbors: " + str(k_nearest_neighbors)
		k_nearest_neighbors_1D = TwoD_toPoints(k_nearest_neighbors)
		print "K Nearest Neighbors: " + str(k_nearest_neighbors_1D)

		incr_ran =  intersectCnt(t_random_range_1D, k_nearest_neighbors_1D)
		incr_max_cov = intersectCnt(t_max_coverage_1D, k_nearest_neighbors_1D)
		incr_x_max_cov = intersectCnt(t_x_merged, k_nearest_neighbors_1D)

		if incr_ran > 0:
			incid_random += 1
		if incr_max_cov > 0:
			incid_max_disp += 1
		if incr_x_max_cov > 0:
			incid_x_max_disp += 1


		cnt_random += incr_ran
		cnt_max_disp += incr_max_cov
		cnt_x_max_disp += incr_x_max_cov



print "Incidents Covered -- Cnt Random: " + str(incid_random/average_over)
print "Incidents Covered -- Cnt Maximize: " + str(incid_max_disp/average_over)
print "Incidents Covered -- Cnt Two Stage: " + str(incid_x_max_disp/average_over)



print "Cnt Random intersect KNN: " + str(cnt_random/average_over)
print "Cnt Maximize intersect KNN: " + str(cnt_max_disp/average_over)
print "Cnt Two Stage intersect KNN: " + str(cnt_x_max_disp/average_over)

print "Two Stage Error: " + str(two_stage_err)







