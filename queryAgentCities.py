#!/usr/bin/python
from __future__ import division
from math import radians, cos, sin, asin, sqrt, atan2
from copy import deepcopy
import random
import math
import sys
import os

city = sys.argv[1]
firstStagePercentage = sys.argv[2]

fileCnt = 10

peopleFileDirectory = os.getcwd() + '/'+ city + 'People/' # Directory for people because of 10 different people for each city
incidFile = os.getcwd() + '/KML files/Incid-Hollaback-'+ city + '.csv' # Only one incident file for each city


#firstStagePercentage = float(sys.argv[2])
#print "First Stage Percentage: " + str(firstStagePercentage)
###################################### Environment Settings ##########################
crowd_cnt = 100 #--- current variable
####################################### Query Settings ###############################
t_setting = 30  # t people to query
firstStage_cnt = int(float(firstStagePercentage)*t_setting)
k_setting = 5 # number of nearest neighbours
######################################## Approximation Settings #######################
trial = 1000
average_over = 100 #number of matrices in the file
#######################################################################################
NN = True # Decide which dispersion metric to use

class Point:
    lat = -1
    lon = -1
    id = -1
    def __init__(self, row_1, col_1, id1):
		self.lat = float(row_1)
		self.lon = float(col_1)
		self.id = id1
		self.dis = -1

    def calculateGPSDistance (self, gps2):
		lat1 = self.lat
		lon1 = self.lon
		lat2 = gps2.lat
		lon2 = gps2.lon

        # convert decimal degrees to radians
		lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula
		dlon = lon2 - lon1
		dlat = lat2 - lat1
		a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
		c = 2* atan2(sqrt(a), sqrt(1-a))
       # c = 2 * asin(sqrt(a))
		r = 6371 # Radius of earth in kilometers. Use 3956 for miles
		self.dis = c*r
		return c * r

def readPeopleOrIncidents(fileName, people):
    gpsPoints = []
    index = 0
    if(people): # if people = true then the lat and long reside at 0 and 1 respectively
        cnt = 0
    else: # if people = false then we are reading Incidents then the lat and long lie at 6 and 7
        cnt = 1

    with open(fileName , 'r') as f:
	lines = f.readlines()
        for line in lines:
            if cnt != 0:
                l2 = line.split(',')

                #print((l2[0][1:-1]), (l2[1]))
                #print float(l2[0])
                #print float(l2[1])
                if(people):
                    gpsPoints.append(Point(float(l2[index]),float(l2[index+1]), cnt-1))
                else:
                    gpsPoints.append(Point(float(l2[index+1][1:-1]),float(l2[index][1:-1]), cnt-1))
            cnt += 1
    return gpsPoints




'''
peoplePoints = readPeopleOrIncidents(peopleFileName, True)
print("The people points are: ")
print(len(peoplePoints))
for p in peoplePoints:
    print(p.lat, p.lon, p.id, "\n")

print("***************************************************************")
print("The incident points are: ")
incidPoints = readPeopleOrIncidents(incidFile, False)
print(len(incidPoints))
for i in incidPoints:
    print(i.lat, i.lon, i.id, "\n")

print("Calculating distances: *********************************************")
# Test that calculating the distance using gps coordinates is working
p1 = Point(40.76, -73.984, 0)
p2 = Point(41.89, 12.492, 1)
dis = p1.calculateGPSDistance(p2)
print(dis)
'''


def pointInList(p, pList): #checks if a point p is in the pList or not by ID
	pId = p.id
	pIdList = []
	for pp in pList:
		pIdList.append(pp.id)
	return pId in pIdList

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
		dis.append(p.calculateGPSDistance(nn[0]))
	return sum(dis)/ len(dis)



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
		#else:
		#	disp = computeDisp(deepcopy(randomCrowd))

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
		if not pointInList(cp,firstStagePoints):
			newCrowdPoints.append(cp)
	for i in range (0, trial_cnt):
		random.shuffle(newCrowdPoints) #shufflin in place
		randomCrowd =  list(newCrowdPoints[0:n])
		if NN == True:
			disp = computeAvgDistNN(deepcopy(randomCrowd))
		if (disp > maxDisp):
			maxDisp = disp
			maxCrowdList = list(randomCrowd)
	return 	maxCrowdList

def getKNN(point, k, crowdPoints):
	# crowd Points is a list objects of the class Point
	for p in crowdPoints:
		p.calculateGPSDistance(point)
	sortedPoints = sorted(crowdPoints, key=lambda x: x.dis, reverse=False)
	return sortedPoints[0:k]

def getKNNExcludeFS(point, k, crowdPoints, firstStagePoints):
	# crowd Points is a list objects of the class Point
	for p in crowdPoints:
		p.calculateGPSDistance(point)
	sortedPoints = sorted(crowdPoints, key=lambda x: x.dis, reverse=False)
	new_sortedPoints = []
	for sp in sortedPoints:
		if not pointInList(sp, firstStagePoints):
			new_sortedPoints.append(sp)
	return new_sortedPoints[0:k]


def intersectCnt(points1, points2):
	points1Ids = []
	points2Ids = []
	for p in points1:
		points1Ids.append(p.id)
	for p in points2:
		points2Ids.append(p.id)

	return len(list(set(points1Ids) & set(points2Ids)))

def mergeWithoutRepition(list1, list2):
#Assuming list1 and list2 do not have any repitiotions
	list3 = []
	for l in list1:
		if not pointInList(l, list3):
			list3.append(l)
	for l in list2:
		if not pointInList(l, list3):
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







##################################### Beginning of simulation ##########################################
secondStage_cnt = t_setting - firstStage_cnt


cnt_random = 0
cnt_max_disp = 0
cnt_x_max_disp = 0

incid_random = 0
incid_max_disp = 0
incid_x_max_disp = 0

two_stage_err = 0

for i in range(0, fileCnt):
	print ("================File: " + str(i))
	peopleFileName =  peopleFileDirectory + city.lower() + 'People' + str(i) +'.csv'
	for j in range (0, average_over):
		print ("================Trial: " + str(j))
		peoplePoints = readPeopleOrIncidents(peopleFileName, True)
		print("***************************************************************")
		incidPoints = readPeopleOrIncidents(incidFile, False)
		crowd = list(peoplePoints)
		crowd = returnShuffled(crowd)
		t_random_range = crowd[0:t_setting]
		disp_random = computeAvgDistNN(t_random_range)

		t_max_coverage = maximizeDispersion(crowd, t_setting, trial, NN)
		t_x_max_coverage = maximizeDispersion(crowd, firstStage_cnt, trial, NN)


		t_secStage_max_covergae = []
		secondStage_people_2D = []

		#Need to get people from the first Stage with 100% feedback
		positiveFeedback_2D = []
		for incident in incidPoints:
			k_nearest_neighbors_2D = getKNN(incident, k_setting, crowd)
			for p in t_x_max_coverage:  #assumes 100% positive feedback
				if  pointInList(p, k_nearest_neighbors_2D) and not pointInList(p, positiveFeedback_2D) :
					positiveFeedback_2D.append(p)
		positive_feedbackCnt = len(positiveFeedback_2D)
		k_pos_feed = [0] * positive_feedbackCnt


		if positive_feedbackCnt == 0: #if first stage does not yield any positive feedback maximize the dispersion
			t_x_nn_secStage = maximizeDispersionExcludeFS(crowd, secondStage_cnt, trial, t_x_max_coverage, NN)
			t_x_merged = mergeWithoutRepition(t_x_max_coverage,t_x_nn_secStage)

		else:
			quota = secondStage_cnt
			while quota > 0:
				i = 0
				for pfp in positiveFeedback_2D: #determine the share of each first stage person
					if quota > 0:
						k_pos_feed[i] += 1
						quota -= 1
					i += 1

		#Second Stage People
		 # We stopped here: getKNNExcludeFS
			i = 0
			exceptionList_2D = t_x_max_coverage
			for pfd in positiveFeedback_2D: #get the k nearest neighbors excluding fs people and previously selected second stage people
				exceptionList_2D = mergeWithoutRepition(exceptionList_2D, secondStage_people_2D)
				t_x_nearest_neighbors_2D = getKNNExcludeFS(pfd, k_pos_feed[i], crowd, exceptionList_2D)
				secondStage_people_2D.extend(t_x_nearest_neighbors_2D)
				#secondStage_people_1D = TwoD_toPoints(secondStage_people_2D)
				i += 1

			t_x_merged =mergeWithoutRepition(t_x_max_coverage, secondStage_people_2D)



		disp_random = computeAvgDistNN(t_random_range)
		disp_max_cov = computeAvgDistNN(t_x_max_coverage)
		disp_two_stage = computeAvgDistNN(t_x_merged)

		print 'Random Dispersion: ' + str(disp_random)
		print 'Max Coverage Dispersion: ' + str(disp_max_cov)
		print 'Two Stage Dispersion: ' + str(disp_two_stage)

		#Test the success/failure of your metrics
		if len(t_x_merged) != t_setting:
			two_stage_err += 1

		for incident in incidPoints:
			#print "Incident: " + str(indicesToNum(incident))
			k_nearest_neighbors = getKNN(incident, k_setting, crowd)
			#print "K nearest neighbors: " + str(k_nearest_neighbors)
			#k_nearest_neighbors_1D = TwoD_toPoints(k_nearest_neighbors)
			#print "K Nearest Neighbors: " + str(k_nearest_neighbors_1D)

			incr_ran =  intersectCnt(t_random_range, k_nearest_neighbors)
			incr_max_cov = intersectCnt(t_max_coverage, k_nearest_neighbors)
			incr_x_max_cov = intersectCnt(t_x_merged, k_nearest_neighbors)

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

















