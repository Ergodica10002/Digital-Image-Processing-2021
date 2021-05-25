import cv2
import numpy as np

sample1_img = cv2.imread("hw3_sample_images/sample1.png")
img_info = sample1_img.shape
height = img_info[0]
width = img_info[1]

def exist_one_eight_neighbor(i,j, img):
	T0 = (img[i-1,j-1] == 255)
	T1 = (img[i-1, j] == 255)
	T2 = (img[i-1,j+1] == 255)
	T3 = (img[i,j-1] == 255)
	T4 = (img[i,j] == 255)
	T5 = (img[i,j+1] == 255)
	T6 = (img[i+1,j-1] == 255)
	T7 = (img[i+1, j] == 255)
	T8 = (img[i+1,j+1] == 255)
	return (T0==1) | (T1==1) | (T2==1) | (T3==1) | (T4==1) | (T5==1) | (T6==1) | (T7==1) | (T8==1)

def exist_one_four_neighbor(i,j, img):
	T0 = (img[i-1,j-1]== 255)
	T1 = (img[i-1, j] == 255)
	T2 = (img[i-1,j+1] == 255)
	T3 = (img[i,j-1] == 255)
	T4 = (img[i,j] == 255)
	T5 = (img[i,j+1] == 255)
	T6 = (img[i+1,j-1] == 255)
	T7 = (img[i+1, j] == 255)
	T8 = (img[i+1,j+1] == 255)
	return (T1==1) | (T2==1) | (T3==1) | (T4==1) | (T5==1) | (T7==1)
'''
# fill the background
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
				if (exist_one_four_neighbor(i,j,G0) == 1):
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

filling_img = np.zeros((height, width), np.uint8)
for i in range(height):
	for j in range(width):
		if (sample1_img[i,j][0] == 255) or (G0[i,j] == 255):
			filling_img[i,j] = 255
		else:
			filling_img[i,j] = 0


for i in range(height):
	for j in range(width):
		if filling_img[i,j] == 0 or sample1_img[i,j][0] == 255:
			filling_img[i,j] = 255
		else:
			filling_img[i,j] = 0
# end of filling background
'''
# start of counting
# To use definition 2, uncomment the following
filling_img = cv2.imread("hw3_sample_images/sample1.png", cv2.IMREAD_GRAYSCALE)

count = 0
for i in range(1, height-1):
	for j in range(1, width-1):
		if filling_img[i,j] == 255:
			count += 1
			label_start = [i,j]
			G0 = np.zeros((height, width), np.uint8)
			G_back = np.zeros((height, width), np.uint8)
			G0[label_start[0],label_start[1]] = 255
			for limit_times in range(300):
				for k in range(1, height-1):
					for l in range(1, width-1):
						if exist_one_eight_neighbor(k,l, G0):
							G_back[k,l] = 255
						else:
							G_back[k,l] = 0
				for k in range(1, height-1):
					for l in range(1, width-1):
						if G_back[k,l] == 255 and filling_img[k,l] == 255:
							G_back[k,l] = 255
						else:
							G_back[k,l] = 0
				KEEP = 0
				for k in range(height):
					for l in range(width):
						if (G0[k,l] != G_back[k,l]):
							G0[k,l] = G_back[k,l]
							KEEP = 1
				if KEEP == 0:
					break
			#cv2.imwrite("removed_object/def2_remove_{}.png".format(count), G0)
			for k in range(1, height-1):
				for l in range(1, width-1):
					if G0[k,l] == 255:
						filling_img[k,l] = 0

print("Number of Objects:", count)
# end of counting

