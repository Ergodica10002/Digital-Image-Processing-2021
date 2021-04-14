import numpy as np
import cv2
from matplotlib import pyplot as plt
import math

#a4
sample1_img = cv2.imread("sample1.jpg")
img_info = sample1_img.shape
height = img_info[0]
width = img_info[1]

F_L = np.zeros((height, width), np.uint8)

H = [[2,4,5,4,2],[4,9,12,9,4],[5,12,15,12,5],[4,9,12,9,4],[2,4,5,4,2]]

for i in range(height):
	for j in range(width):
		if (i < 2) or (i >= height-3) or (j < 2) or (j >= width-3):
			F_L[i,j] = sample1_img[i,j][0]
			continue
		sum = 0
		for h in range(0,5):
			for k in range(0,5):
				sum += sample1_img[i-2+h,j-2+k][0]*H[h][k]
		sum = sum / 159
		F_L[i,j] = sum
        
c = 0.7
G = np.zeros((height, width, 3), np.uint8)
for i in range(height):
    for j in range(width):
        newval = (c/(2*c-1)) * sample1_img[i,j][0] - ((1-c)/(2*c-1)) * F_L[i,j] 
        G[i,j] = (newval, newval, newval)


cv2.imwrite("result4.jpg", G)

#finish edge crispening


result4_img = cv2.imread("result4.jpg")
img_info = result4_img.shape
height = img_info[0]
width = img_info[1]

N = np.zeros((height, width), np.uint8)

H = [[2,4,5,4,2],[4,9,12,9,4],[5,12,15,12,5],[4,9,12,9,4],[2,4,5,4,2]]

for i in range(height):
	for j in range(width):
		if (i < 2) or (i >= height-3) or (j < 2) or (j >= width-3):
			N[i,j] = result4_img[i,j][0]
			continue
		sum = 0
		for h in range(0,5):
			for k in range(0,5):
				sum += result4_img[i-2+h,j-2+k][0]*H[h][k]
		sum = sum / 159
		N[i,j] = sum
        
G = np.zeros((height, width), np.uint8)
Theta = np.zeros((height, width))
K = 1
for i in range(height):
	for j in range(width):
		if i == 0 or i == height-1 or j == 0 or j == width-1:
			G_r = 0
			G_c = 0
		else:
			G_r_1 = result4_img[i-1,j+1][0]+K*result4_img[i,j+1][0]+result4_img[i+1,j+1][0]
			G_r_2 = result4_img[i-1,j-1][0]+K*result4_img[i,j-1][0]+result4_img[i+1,j-1][0]
			G_c_1 = result4_img[i-1,j-1][0]+K*result4_img[i-1,j][0]+result4_img[i-1,j+1][0]
			G_c_2 = result4_img[i+1,j-1][0]+K*result4_img[i+1,j][0]+result4_img[i+1,j+1][0]
			G_r = (G_r_1 - G_r_2)/(K+2)
			G_c = (G_c_1 - G_c_2)/(K+2)
		G[i,j] = (G_r ** 2 + G_c ** 2) ** (0.5)
		if G_r == 0:
			Theta[i,j]=1.57
		else:
			Theta[i,j] = math.atan(G_c/G_r)

GN = np.zeros((height, width), np.uint8)
pi = 3.14
for i in range(height):
	for j in range(width):
		if i == 0 or i == height-1 or j == 0 or j == width-1:
			GN[i,j] = G[i,j]
		elif (abs(Theta[i,j]) < pi/8):
			if (G[i,j-1] > G[i,j]) or (G[i,j+1] > G[i,j]):
				GN[i,j] = 0
			else:
				GN[i,j] = G[i,j]
		elif (abs(Theta[i,j]) > 3*pi/8):
			if (G[i-1,j] > G[i,j]) or (G[i+1,j] > G[i,j]):
				GN[i,j] = 0
			else:
				GN[i,j] = G[i,j]
		elif (Theta[i,j] > 0):
			if (G[i-1,j+1] > G[i,j]) or (G[i+1,j-1] > G[i,j]):
				GN[i,j] = 0
			else:
				GN[i,j] = G[i,j]
		else:
			if (G[i-1,j-1] > G[i,j]) or (G[i+1,j+1] > G[i,j]):
				GN[i,j] = 0
			else:
				GN[i,j] = G[i,j]

result5_img = np.zeros((height, width, 3), np.uint8)


TH = 15
TL = 3
candidate_list = []
for i in range(height):
	for j in range(width):
		if i == 0 or i == height-1 or j == 0 or j == width-1:
			result5_img[i,j] = (0,0,0)
		elif (GN[i,j] > TH):
			result5_img[i,j] = (255,255,255)
		elif (GN[i,j] < TL):
			result5_img[i,j] = (0,0,0)
		else:
			candidate_list.append((i,j))
for c in candidate_list:
	if (GN[c[0],c[1]] > TH):
		continue
	if (GN[c[0]-1,c[1]] > TH) or (GN[c[0],c[1]-1] > TH) or (GN[c[0],c[1]+1] > TH) or (GN[c[0]+1,c[1]] > TH):
		GN[c[0],c[1]] = TH + 1
		result5_img[c[0],c[1]] = (255,255,255)
for c in candidate_list:
	if (GN[c[0],c[1]] > TH):
		continue
	if (GN[c[0]-1,c[1]] > TH) or (GN[c[0],c[1]-1] > TH) or (GN[c[0],c[1]+1] > TH) or (GN[c[0]+1,c[1]] > TH):
		GN[c[0],c[1]] = TH + 1
		result5_img[c[0],c[1]] = (255,255,255)
	else:
		result5_img[c[0],c[1]] = (0,0,0)
        

cv2.imwrite("result5.jpg", result5_img)
#end of a4