import cv2
import numpy as np
import random

problem_2c = True

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

if problem_2c == True:
	K_feature_point = [[25, 200], [120, 185], [190, 220], [350, 210]]
# K[f][i,j] is the (i,j) index of feature f

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
	if problem_2c == True:
		T_vector[0][i] = T[i][K_feature_point[0][0], K_feature_point[0][1]]
		T_vector[1][i] = T[i][K_feature_point[1][0], K_feature_point[1][1]]
		T_vector[2][i] = T[i][K_feature_point[2][0], K_feature_point[2][1]]
		T_vector[3][i] = T[i][K_feature_point[3][0], K_feature_point[3][1]]


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


sample3_img = cv2.imread("hw3_sample_images/sample3.png", cv2.IMREAD_GRAYSCALE)
pattern_img_info = sample3_img.shape
pattern_height = pattern_img_info[0]
pattern_width = pattern_img_info[1]

result_5 = np.zeros((height,width))

for pixel in feature_set3:
	pattern_r = pattern_height - (height - pixel[0]) % pattern_height - 1
	pattern_c = pixel[1] % pattern_width
	result_5[pixel[0],pixel[1]] = sample3_img[pattern_r,pattern_c]

for pixel in feature_set0:
	result_5[pixel[0],pixel[1]] = sample2_img[pixel[0], pixel[1]]
for pixel in feature_set1:
	result_5[pixel[0],pixel[1]] = sample2_img[pixel[0], pixel[1]]
for pixel in feature_set2:
	result_5[pixel[0],pixel[1]] = sample2_img[pixel[0], pixel[1]]

cv2.imwrite("hw3_result_images/result5.png", result_5)


