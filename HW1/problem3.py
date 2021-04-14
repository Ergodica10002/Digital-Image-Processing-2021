import cv2
import numpy as np
from matplotlib import pyplot as plt
import math

sample6_img = cv2.imread('sample6.jpg')
sample7_img = cv2.imread('sample7.jpg')

imgInfo = sample6_img.shape
height = imgInfo[0]
width = imgInfo[1]

result8_img = np.zeros((height, width, 3), np.uint8)

mask = [[1, 1, 1],
		[1, 1, 1],
		[1, 1, 1]]

for i in range(0,height):
	for j in range(0,width):
		image_sec = [[0, 0, 0],
					 [0, 0, 0],
					 [0, 0, 0]]
		if i == 0 and j == 0:
			image_sec[0][0] = sample6_img[i,j][0]
			image_sec[0][1] = sample6_img[i,j][0]
			image_sec[0][2] = sample6_img[i,j][0]
			image_sec[1][0] = sample6_img[i,j][0]
			image_sec[2][0] = sample6_img[i,j][0]
		elif i == 0 and j == width-1:
			image_sec[0][0] = sample6_img[i,j][0]
			image_sec[0][1] = sample6_img[i,j][0]
			image_sec[0][2] = sample6_img[i,j][0]
			image_sec[1][2] = sample6_img[i,j][0]
			image_sec[2][2] = sample6_img[i,j][0]
		elif i == height-1 and j == 0:
			image_sec[0][0] = sample6_img[i,j][0]
			image_sec[1][0] = sample6_img[i,j][0]
			image_sec[2][0] = sample6_img[i,j][0]
			image_sec[2][1] = sample6_img[i,j][0]
			image_sec[2][2] = sample6_img[i,j][0]
		elif i == height-1 and j == width-1:
			image_sec[0][2] = sample6_img[i,j][0]
			image_sec[1][2] = sample6_img[i,j][0]
			image_sec[2][0] = sample6_img[i,j][0]
			image_sec[2][1] = sample6_img[i,j][0]
			image_sec[2][2] = sample6_img[i,j][0]
		elif i == 0:
			image_sec[0][0] = sample6_img[i,j][0]
			image_sec[0][1] = sample6_img[i,j][0]
			image_sec[0][2] = sample6_img[i,j][0]
		elif i == height-1:
			image_sec[2][0] = sample6_img[i,j][0]
			image_sec[2][1] = sample6_img[i,j][0]
			image_sec[2][2] = sample6_img[i,j][0]
		elif j == 0:
			image_sec[0][0] = sample6_img[i,j][0]
			image_sec[1][0] = sample6_img[i,j][0]
			image_sec[2][0] = sample6_img[i,j][0]
		elif j == width-1:
			image_sec[0][2] = sample6_img[i,j][0]
			image_sec[1][2] = sample6_img[i,j][0]
			image_sec[2][2] = sample6_img[i,j][0]
		else:
			image_sec[0][0] = sample6_img[i-1,j-1][0]
			image_sec[0][1] = sample6_img[i-1,j][0]
			image_sec[0][2] = sample6_img[i-1,j+1][0]
			image_sec[1][0] = sample6_img[i,j-1][0]
			image_sec[1][1] = sample6_img[i,j][0]
			image_sec[1][2] = sample6_img[i,j+1][0]
			image_sec[2][0] = sample6_img[i+1,j-1][0]
			image_sec[2][1] = sample6_img[i+1,j][0]
			image_sec[2][2] = sample6_img[i+1,j+1][0]

		newval = 0
		for k in range(2):
			for l in range(2):
				newval += + (mask[k][l] * image_sec[k][l])
		newval = newval / 9
		newattr = (newval, newval, newval)
		result8_img[i,j] = np.uint8(newattr)

cv2.imwrite('8_result.jpg', result8_img)

MSE = 0
for i in range(0,height):
	for j in range(0,width):
		MSE += (int(result8_img[i,j][0])-int(sample6_img[i,j][0]))**2
MSE = MSE / (height * width)
PSNR = 10 * math.log((255**2)/MSE, 10)
print("the PSNR of 8_result.jpg is", PSNR)


imgInfo = sample7_img.shape
height = imgInfo[0]
width = imgInfo[1]

result9_img = np.zeros((height, width, 3), np.uint8)

for i in range(0,height):
	for j in range(0,width):
		image_sec = [[0, 0, 0],
					 [0, 0, 0],
					 [0, 0, 0]]
		if i == 0 and j == 0:
			image_sec[0][0] = sample7_img[i,j][0]
			image_sec[0][1] = sample7_img[i,j][0]
			image_sec[0][2] = sample7_img[i,j][0]
			image_sec[1][0] = sample7_img[i,j][0]
			image_sec[2][0] = sample7_img[i,j][0]
		elif i == 0 and j == width-1:
			image_sec[0][0] = sample7_img[i,j][0]
			image_sec[0][1] = sample7_img[i,j][0]
			image_sec[0][2] = sample7_img[i,j][0]
			image_sec[1][2] = sample7_img[i,j][0]
			image_sec[2][2] = sample7_img[i,j][0]
		elif i == height-1 and j == 0:
			image_sec[0][0] = sample7_img[i,j][0]
			image_sec[1][0] = sample7_img[i,j][0]
			image_sec[2][0] = sample7_img[i,j][0]
			image_sec[2][1] = sample7_img[i,j][0]
			image_sec[2][2] = sample7_img[i,j][0]
		elif i == height-1 and j == width-1:
			image_sec[0][2] = sample7_img[i,j][0]
			image_sec[1][2] = sample7_img[i,j][0]
			image_sec[2][0] = sample7_img[i,j][0]
			image_sec[2][1] = sample7_img[i,j][0]
			image_sec[2][2] = sample7_img[i,j][0]
		elif i == 0:
			image_sec[0][0] = sample7_img[i,j][0]
			image_sec[0][1] = sample7_img[i,j][0]
			image_sec[0][2] = sample7_img[i,j][0]
		elif i == height-1:
			image_sec[2][0] = sample7_img[i,j][0]
			image_sec[2][1] = sample7_img[i,j][0]
			image_sec[2][2] = sample7_img[i,j][0]
		elif j == 0:
			image_sec[0][0] = sample7_img[i,j][0]
			image_sec[1][0] = sample7_img[i,j][0]
			image_sec[2][0] = sample7_img[i,j][0]
		elif j == width-1:
			image_sec[0][2] = sample7_img[i,j][0]
			image_sec[1][2] = sample7_img[i,j][0]
			image_sec[2][2] = sample7_img[i,j][0]
		else:
			image_sec[0][0] = sample7_img[i-1,j-1][0]
			image_sec[0][1] = sample7_img[i-1,j][0]
			image_sec[0][2] = sample7_img[i-1,j+1][0]
			image_sec[1][0] = sample7_img[i,j-1][0]
			image_sec[1][1] = sample7_img[i,j][0]
			image_sec[1][2] = sample7_img[i,j+1][0]
			image_sec[2][0] = sample7_img[i+1,j-1][0]
			image_sec[2][1] = sample7_img[i+1,j][0]
			image_sec[2][2] = sample7_img[i+1,j+1][0]
		MINR = min(min(image_sec[1][0], image_sec[1][1]), image_sec[1][2])
		MINC = min(image_sec[0][1], image_sec[1][1], image_sec[2][1])
		MAXMIN = max(MINR, MINC)
			     
		MINMAX = min(max(image_sec[1][0], image_sec[1][1], image_sec[1][2]),
			     max(image_sec[0][1], image_sec[1][1], image_sec[2][1]))
		PMED = 0.5 * MAXMIN + 0.5 * MINMAX
		newattr = (PMED, PMED, PMED)
		result9_img[i,j] = np.uint8(newattr)

cv2.imwrite('9_result.jpg', result9_img)

MSE = 0
for i in range(0,height):
	for j in range(0,width):
		MSE += (int(result9_img[i,j][0])-int(sample7_img[i,j][0]))**2
MSE = MSE / (height * width)
PSNR = 10 * math.log((255**2)/MSE, 10)
print("the PSNR of 9_result.jpg is", PSNR)