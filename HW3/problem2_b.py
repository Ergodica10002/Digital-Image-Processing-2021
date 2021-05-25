import cv2
import numpy as np
import random

sample2_img = cv2.imread("hw3_sample_images/sample2.png", cv2.IMREAD_GRAYSCALE)
img_info = sample2_img.shape
height = img_info[0]
width = img_info[1]

T = np.load("hw3_result_images/T.npy")

def dist(X, Y):
	d = 0
	for i in range(1, 10):
		d += (X[i] - Y[i])**2
	return d**0.5

T_vector = []
for i in range(4):
	T_vector.append(np.zeros(10))
np.zeros(10)
for i in range(1, 10):
	maxvalue = int(np.amax(T[i]))
	T_vector[0][i] = random.randint(0,maxvalue)
	T_vector[1][i] = random.randint(0,maxvalue)
	T_vector[2][i] = random.randint(0,maxvalue)
	T_vector[3][i] = random.randint(0,maxvalue)

prev_T_vector = []
for i in range(4):
	prev_T_vector.append(np.zeros(10))

feature_set0 = []
feature_set1 = []
feature_set2 = []
feature_set3 = []

for it in range(500):
	feature_set0.clear()
	feature_set1.clear()
	feature_set2.clear()
	feature_set3.clear()
	for i in range(height):
		for j in range(width):
			feature_vector = np.zeros(10)
			for k in range(1, 10):
				feature_vector[k] = T[k][i, j]
			diff_0 = dist(feature_vector, T_vector[0])
			diff_1 = dist(feature_vector, T_vector[1])
			diff_2 = dist(feature_vector, T_vector[2])
			diff_3 = dist(feature_vector, T_vector[3])
			if (diff_0 <= diff_1) and (diff_0 <= diff_2) and (diff_0 <= diff_3):
				feature_set0.append([i,j])
			elif (diff_1 <= diff_0) and (diff_1 <= diff_2) and (diff_1 <= diff_3):
				feature_set1.append([i,j])
			elif (diff_2 <= diff_0) and (diff_2 <= diff_1) and (diff_2 <= diff_3):
				feature_set2.append([i,j])
			elif (diff_3 <= diff_0) and (diff_3 <= diff_1) and (diff_3 <= diff_2):
				feature_set3.append([i,j])

	KEEP = 0
	for i in range(1, 10):
		if (prev_T_vector[0][i] != T_vector[0][i]):
			KEEP = 1
		if (prev_T_vector[1][i] != T_vector[1][i]):
			KEEP = 1
		if (prev_T_vector[2][i] != T_vector[2][i]):
			KEEP = 1
		if (prev_T_vector[3][i] != T_vector[3][i]):
			KEEP = 1
		prev_T_vector[0][i] = T_vector[0][i]
		prev_T_vector[1][i] = T_vector[1][i]
		prev_T_vector[2][i] = T_vector[2][i]
		prev_T_vector[3][i] = T_vector[3][i]
		T_vector[0][i] = 0
		T_vector[1][i] = 0
		T_vector[2][i] = 0
		T_vector[3][i] = 0

	for i in range(1, 10):
		for point in feature_set0:
			T_vector[0][i] += T[i][point[0], point[1]]
		T_vector[0][i] = T_vector[0][i] / len(feature_set0)
		for point in feature_set1:
			T_vector[1][i] += T[i][point[0], point[1]]
		T_vector[1][i] = T_vector[1][i] / len(feature_set1)
		for point in feature_set2:
			T_vector[2][i] += T[i][point[0], point[1]]
		T_vector[2][i] = T_vector[2][i] / len(feature_set2)
		for point in feature_set3:
			T_vector[3][i] += T[i][point[0], point[1]]
		T_vector[3][i] = T_vector[3][i] / len(feature_set3)

	if KEEP == 0:
		break


result_3 = np.zeros((height,width, 3), np.uint8)
for index in feature_set0:
	result_3[index[0], index[1]] = (230,206,156)
for index in feature_set1:
	result_3[index[0], index[1]] = (123, 241, 223)
for index in feature_set2:
	result_3[index[0], index[1]] = (0, 136, 11)
for index in feature_set3:
	result_3[index[0], index[1]] = (172, 172, 249)

cv2.imwrite("hw3_result_images/result3.png", result_3)








