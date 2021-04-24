import cv2
import numpy as np

sample1_img = cv2.imread("sample1.png")
img_info = sample1_img.shape
height = img_info[0]
width = img_info[1]

def all_one(i,j, img):
	T0 = (img[i-1,j-1][0] == 255)
	T1 = (img[i-1, j][0] == 255)
	T2 = (img[i-1,j+1][0] == 255)
	T3 = (img[i,j-1][0] == 255)
	T4 = (img[i,j][0] == 255)
	T5 = (img[i,j+1][0] == 255)
	T6 = (img[i+1,j-1][0] == 255)
	T7 = (img[i+1, j][0] == 255)
	T8 = (img[i+1,j+1][0] == 255)
	return (T0==1) & (T1==1) & (T2==1) & (T3==1) & (T4==1) & (T5==1) & (T6==1) & (T7==1) & (T8==1)

def exist_one(i,j, img):
	T0 = (img[i-1,j-1]== 255)
	T1 = (img[i-1, j] == 255)
	T2 = (img[i-1,j+1] == 255)
	T3 = (img[i,j-1] == 255)
	T4 = (img[i,j] == 255)
	T5 = (img[i,j+1] == 255)
	T6 = (img[i+1,j-1] == 255)
	T7 = (img[i+1, j] == 255)
	T8 = (img[i+1,j+1] == 255)
	return (T1==1) | (T3==1) | (T4==1) | (T5==1) | (T7==1)

erosion = np.zeros((height,width), np.uint8)
for i in range(height):
	for j in range(width):
		if i == 0 or i == height-1 or j == 0 or j == width-1:
			erosion[i,j] = 0
		else:
			if (all_one(i,j,sample1_img) == 1):
				erosion[i,j] = 255
			else:
				erosion[i,j] = 0

result1_img = np.zeros((height,width), np.uint8)
for i in range(height):
	for j in range(width):
		if (sample1_img[i,j][0] == 255) and (erosion[i,j] == 255):
			result1_img[i,j] = 0
		elif (sample1_img[i,j][0] == 0) and (erosion[i,j] == 0):
			result1_img[i,j] = 0
		else:
			result1_img[i,j] = 255

cv2.imwrite("result1.png", result1_img)
# end of 1a

# start of 1b 
FC = np.zeros((height,width),np.uint8)
for i in range(height):
	for j in range(width):
		if sample1_img[i,j][0] == 0:
			FC[i,j] = 255
		else:
			FC[i,j] = 0

FOUND = 0
for i in range(1,height-1):
	for j in range(1,width-1):
		if sample1_img[i,j][0] == 0:
			hole_start = [i,j]
			FOUND = 1
			break;
	if FOUND == 1:
		break;

G0 = np.zeros((height,width),np.uint8)
G_back = np.zeros((height,width),np.uint8)
G0[hole_start[0],hole_start[1]] = 255

for k in range(3000):
	for i in range(height):
		for j in range(width):
			if (i == 0) or (i == height-1) or (j == 0) or (j == width-1):
				G_back[i,j] = 0
			else:
				if (exist_one(i,j,G0) == 1):
					G_back[i,j] = 255
				else:
					G_back[i,j] = 0
	for i in range(height):
		for j in range(width):
			if (FC[i,j] == 255) and (G_back[i,j] == 255):
				G_back[i,j] = 255
			else:
				G_back[i,j] = 0
	KEEP = 0
	for i in range(height):
		for j in range(width):
			if (G0[i,j] != G_back[i,j]):
				G0[i,j] = G_back[i,j]
				KEEP = 1
	if KEEP == 0:
		break

fill_background_img = np.zeros((height, width), np.uint8)
for i in range(height):
	for j in range(width):
		if (sample1_img[i,j][0] == 255) or (G0[i,j] == 255):
			fill_background_img[i,j] = 255
		else:
			fill_background_img[i,j] = 0

# cv2.imwrite("fill_background.png", fill_background_img)

result2_img = np.zeros((height, width), np.uint8)
for i in range(height):
	for j in range(width):
		if fill_background_img[i,j] == 0 or sample1_img[i,j][0] == 255:
			result2_img[i,j] = 255
		else:
			result2_img[i,j] = 0

cv2.imwrite("result2.png", result2_img)
# end of 1b