import numpy as np
import cv2
import math
import sys

if len(sys.argv) < 3:
    print("error!")
    print("usage: python3 edge_detect.py in_image out_image")
    exit()

filename = sys.argv[1]

img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
img_info = img.shape
height = img_info[0]
width = img_info[1]

#start of Canny edge detection

N = np.zeros((height, width), np.uint8)

H = [[2,4,5,4,2],[4,9,12,9,4],[5,12,15,12,5],[4,9,12,9,4],[2,4,5,4,2]]

for i in range(height):
	for j in range(width):
		if (i < 2) or (i >= height-3) or (j < 2) or (j >= width-3):
			N[i,j] = img[i,j]
			continue
		sum = 0
		for h in range(0,5):
			for k in range(0,5):
				sum += img[i-2+h,j-2+k]*H[h][k]
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
			G_r_1 = img[i-1,j+1]+K*img[i,j+1]+img[i+1,j+1]
			G_r_2 = img[i-1,j-1]+K*img[i,j-1]+img[i+1,j-1]
			G_c_1 = img[i-1,j-1]+K*img[i-1,j]+img[i-1,j+1]
			G_c_2 = img[i+1,j-1]+K*img[i+1,j]+img[i+1,j+1]
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

edge_map = np.zeros((height, width), np.uint8)

TH = 20
TL = 10
candidate_list = []
for i in range(height):
	for j in range(width):
		if i == 0 or i == height-1 or j == 0 or j == width-1:
			edge_map[i,j] = 0
		elif (GN[i,j] > TH):
			edge_map[i,j] = 255
		elif (GN[i,j] < TL):
			edge_map[i,j] = 0
		else:
			candidate_list.append((i,j))
for c in candidate_list:
	if (GN[c[0],c[1]] > TH):
		continue
	if (GN[c[0]-1,c[1]] > TH) or (GN[c[0],c[1]-1] > TH) or (GN[c[0],c[1]+1] > TH) or (GN[c[0]+1,c[1]] > TH):
		GN[c[0],c[1]] = TH + 1
		edge_map[c[0],c[1]] = 255
for c in candidate_list:
	if (GN[c[0],c[1]] > TH):
		continue
	if (GN[c[0]-1,c[1]] > TH) or (GN[c[0],c[1]-1] > TH) or (GN[c[0],c[1]+1] > TH) or (GN[c[0]+1,c[1]] > TH):
		GN[c[0],c[1]] = TH + 1
		edge_map[c[0],c[1]] = 255
	else:
		edge_map[c[0],c[1]] = 0
        
#end of Canny edge detection
out_name = sys.argv[2]
cv2.imwrite(out_name, edge_map)