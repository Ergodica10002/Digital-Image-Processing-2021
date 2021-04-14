import numpy as np
import cv2
from matplotlib import pyplot as plt
import math

sample2_img = cv2.imread("sample2.jpg")
img_info = sample2_img.shape
height = img_info[0]
width = img_info[1]

'''
#start of histogram equalization

pdf = np.zeros(256)
for i in range(height):
	for j in range(width):
		pdf[sample2_img[i,j][0]] += 1

cdf = np.zeros(256)
cdf[0] = pdf[0]
last_zero = 0
for i in range(1,256):
	cdf[i] = cdf[i-1] + pdf[i]
	if cdf[i] == 0:
		last_zero = i

sample2_hist = np.zeros((height, width, 3), np.uint8)

N = height * width
for i in range(height):
    for j in range(width):
        index = sample2_img[i,j][0]
        newval = ((cdf[index] - last_zero) / (N - last_zero)) * 255
        newattr = (newval, newval, newval)
        sample2_hist[i,j] = np.uint8(newattr)

cv2.imwrite("sample2_hist.jpg", sample2_hist)
#end of histogram equalization
'''

#start of transfer function
def transfer(val):
	newval = (val/255)**4 * 255
	return math.ceil(newval)
lowest = 255
highest = 0
sample2_hist = np.zeros((height, width, 3), np.uint8)
for i in range(height):
    for j in range(width):
        val = sample2_img[i,j][0]
        newval = transfer(val)
        if newval < lowest:
        	lowest = newval
        if newval > highest:
        	highest = newval
print("low", lowest, "high", highest)
factor = 255 / (highest - lowest)

for i in range(height):
	for j in range(width):
		val = sample2_img[i,j][0]
		newval = transfer(val)
		newattr = (newval, newval, newval)
		sample2_hist[i,j] = np.uint8(newattr)   
cv2.imwrite("sample2_transfer.jpg", sample2_hist)    		
#end of transfer function

#start of Canny edge detection
sample2_hist = cv2.imread("sample2_hist.jpg")
img_info = sample2_hist.shape
height = img_info[0]
width = img_info[1]

N = np.zeros((height, width), np.uint8)

H = [[2,4,5,4,2],[4,9,12,9,4],[5,12,15,12,5],[4,9,12,9,4],[2,4,5,4,2]]

for i in range(height):
	for j in range(width):
		if (i < 2) or (i >= height-3) or (j < 2) or (j >= width-3):
			N[i,j] = sample2_hist[i,j][0]
			continue
		sum = 0
		for h in range(0,5):
			for k in range(0,5):
				sum += sample2_hist[i-2+h,j-2+k][0]*H[h][k]
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
			G_r_1 = sample2_hist[i-1,j+1][0]+K*sample2_hist[i,j+1][0]+sample2_hist[i+1,j+1][0]
			G_r_2 = sample2_hist[i-1,j-1][0]+K*sample2_hist[i,j-1][0]+sample2_hist[i+1,j-1][0]
			G_c_1 = sample2_hist[i-1,j-1][0]+K*sample2_hist[i-1,j][0]+sample2_hist[i-1,j+1][0]
			G_c_2 = sample2_hist[i+1,j-1][0]+K*sample2_hist[i+1,j][0]+sample2_hist[i+1,j+1][0]
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

sample2_edge_map = np.zeros((height, width, 3), np.uint8)
'''
X = range(0,256)
Y = np.zeros(256)
for i in range(height):
    for j in range(width):
        if (0 <= int(GN[i,j])) and (int(GN[i,j]) < 256):
            Y[int(GN[i,j])] += 1
plt.figure()
plt.plot(X,Y)
plt.show()
'''
TH = 10
TL = 2
candidate_list = []
for i in range(height):
	for j in range(width):
		if i == 0 or i == height-1 or j == 0 or j == width-1:
			sample2_edge_map[i,j] = (0,0,0)
		elif (GN[i,j] > TH):
			sample2_edge_map[i,j] = (255,255,255)
		elif (GN[i,j] < TL):
			sample2_edge_map[i,j] = (0,0,0)
		else:
			candidate_list.append((i,j))
for c in candidate_list:
	if (GN[c[0],c[1]] > TH):
		continue
	if (GN[c[0]-1,c[1]] > TH) or (GN[c[0],c[1]-1] > TH) or (GN[c[0],c[1]+1] > TH) or (GN[c[0]+1,c[1]] > TH):
		GN[c[0],c[1]] = TH + 1
		sample2_edge_map[c[0],c[1]] = (255,255,255)
for c in candidate_list:
	if (GN[c[0],c[1]] > TH):
		continue
	if (GN[c[0]-1,c[1]] > TH) or (GN[c[0],c[1]-1] > TH) or (GN[c[0],c[1]+1] > TH) or (GN[c[0]+1,c[1]] > TH):
		GN[c[0],c[1]] = TH + 1
		sample2_edge_map[c[0],c[1]] = (255,255,255)
	else:
		sample2_edge_map[c[0],c[1]] = (0,0,0)
        

cv2.imwrite("sample2_edge_map.jpg", sample2_edge_map)
#end of Canny edge detection

