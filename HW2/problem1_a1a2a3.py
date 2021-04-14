import numpy as np
import cv2
from matplotlib import pyplot as plt
import math

sample1_img = cv2.imread("sample1.jpg")
img_info = sample1_img.shape
height = img_info[0]
width = img_info[1]

#a1
G = np.zeros((height, width), np.uint8)
K = 1
for i in range(height):
	for j in range(width):
		if i == 0 or i == height-1 or j == 0 or j == width-1:
			G_r = 0
			G_c = 0
		else:
			G_r_1 = sample1_img[i-1,j+1][0]+K*sample1_img[i,j+1][0]+sample1_img[i+1,j+1][0]
			G_r_2 = sample1_img[i-1,j-1][0]+K*sample1_img[i,j-1][0]+sample1_img[i+1,j-1][0]
			G_c_1 = sample1_img[i-1,j-1][0]+K*sample1_img[i-1,j][0]+sample1_img[i-1,j+1][0]
			G_c_2 = sample1_img[i+1,j-1][0]+K*sample1_img[i+1,j][0]+sample1_img[i+1,j+1][0]
			G_r = (G_r_1 - G_r_2)/(K+2)
			G_c = (G_c_1 - G_c_2)/(K+2)
		G[i,j] = (G_r ** 2 + G_c ** 2) ** (0.5)


result1_img = np.zeros((height, width, 3), np.uint8)




threshold = 10
for i in range(height):
	for j in range(width):
		if (G[i,j] > threshold):
			result1_img[i,j] = (255,255,255)
		else:
			result1_img[i,j] = (0,0,0)

cv2.imwrite("result1.jpg", result1_img)
#end of a1

#a2
G = np.zeros((height, width))
threshold = 5
for i in range(height):
	for j in range(width):
		if (i == 0) or (i == height-1) or (j == 0) or (j == width-1):
			G[i,j] = 0
		else:
			a1=float(-1*sample1_img[i-1,j][0])
			a2=float(-1*sample1_img[i,j-1][0])
			a3=float(-1*sample1_img[i+1,j][0])
			a4=float(-1*sample1_img[i,j+1][0])
			a5=float(-1*sample1_img[i-1,j-1][0])
			a6=float(-1*sample1_img[i-1,j+1][0])
			a7=float(-1*sample1_img[i+1,j-1][0])
			a8=float(-1*sample1_img[i+1,j+1][0])
			a=float(sample1_img[i,j][0])
			G[i,j] = (a1 + a2 + a3 + a4 + a5 + a6 + a7 + a8 + a*8)/8
		if (abs(G[i,j])<threshold):
			G[i,j]=0


result2_img = np.zeros((height, width, 3), np.uint8)
for i in range(height):
	for j in range(width):
		if i == 0 or i == height-1 or j == 0 or j == width-1:
			result2_img[i,j] = (0,0,0)
		elif (G[i-1,j] * G[i+1,j] < 0) or (G[i,j-1] * G[i,j+1] < 0):
			result2_img[i,j] = (255,255,255)
		else:
			result2_img[i,j] = (0,0,0)

cv2.imwrite("result2.jpg", result2_img)
#end of a2

#a3
N = np.zeros((height, width), np.uint8)

H = [[2,4,5,4,2],[4,9,12,9,4],[5,12,15,12,5],[4,9,12,9,4],[2,4,5,4,2]]

for i in range(2, height-3):
	for j in range(2, width-3):
		sum = 0
		for h in range(0,5):
			for k in range(0,5):
				sum += sample1_img[i-2+h,j-2+k][0]*H[h][k]
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
			G_r_1 = sample1_img[i-1,j+1][0]+K*sample1_img[i,j+1][0]+sample1_img[i+1,j+1][0]
			G_r_2 = sample1_img[i-1,j-1][0]+K*sample1_img[i,j-1][0]+sample1_img[i+1,j-1][0]
			G_c_1 = sample1_img[i-1,j-1][0]+K*sample1_img[i-1,j][0]+sample1_img[i-1,j+1][0]
			G_c_2 = sample1_img[i+1,j-1][0]+K*sample1_img[i+1,j][0]+sample1_img[i+1,j+1][0]
			G_r = (G_r_1 - G_r_2)/(K+2)
			G_c = (G_c_1 - G_c_2)/(K+2)
		G[i,j] = (G_r ** 2 + G_c ** 2) ** (0.5)
		if G_r == 0:
			Theta[i,j]=1.57
		else:
			Theta[i,j] = math.atan(G_c/G_r)

GN = np.zeros((height, width), np.uint8)
pi = 3.14
for i in range(0,height):
	for j in range(0,width):
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

result3_img = np.zeros((height, width, 3), np.uint8)

X = range(0,256)
Y = np.zeros(256)
for i in range(height):
    for j in range(width):
        if (0 <= int(G[i,j])) and (int(G[i,j]) < 256):
            Y[int(G[i,j])] += 1
plt.figure()
plt.plot(X,Y)
plt.show()

TH = 15
TL = 3
candidate_list = []
for i in range(height):
	for j in range(width):
		if i == 0 or i == height-1 or j == 0 or j == width-1:
			result3_img[i,j] = (0,0,0)
		elif (GN[i,j] > TH):
			result3_img[i,j] = (255,255,255)
		elif (GN[i,j] < TL):
			result3_img[i,j] = (0,0,0)
		else:
			candidate_list.append((i,j))
for c in candidate_list:
	if (GN[c[0],c[1]] > TH):
		continue
	if (GN[c[0]-1,c[1]] > TH) or (GN[c[0],c[1]-1] > TH) or (GN[c[0],c[1]+1] > TH) or (GN[c[0]+1,c[1]] > TH):
		GN[c[0],c[1]] = TH + 1
		result3_img[c[0],c[1]] = (255,255,255)
for c in candidate_list:
	if (GN[c[0],c[1]] > TH):
		continue
	if (GN[c[0]-1,c[1]] > TH) or (GN[c[0],c[1]-1] > TH) or (GN[c[0],c[1]+1] > TH) or (GN[c[0]+1,c[1]] > TH):
		GN[c[0],c[1]] = TH + 1
		result3_img[c[0],c[1]] = (255,255,255)
	else:
		result3_img[c[0],c[1]] = (0,0,0)

cv2.imwrite("result3.jpg", result3_img)
