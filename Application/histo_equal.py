import cv2
import numpy as np
import sys

if len(sys.argv) < 3:
    print("error!")
    print("usage: python3 histo_equal.py in_image out_image")
    exit()
filename = sys.argv[1]

img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
imgInfo = img.shape
height = imgInfo[0]
width = imgInfo[1]

global_equal_img = np.zeros((height, width), np.uint8)
p = np.zeros(256)

for i in range(0, height):
    for j in range(0, width):
        p[img[i,j]] += 1
        
c = np.zeros(256)
c[0] = p[0]
for i in range(1,256):
    c[i] = c[i-1] + p[i]

for i in range(0,256):
	if c[i] != 0:
		cdf_min = i
		break

N = height * width
for i in range(0,height):
    for j in range(0,width):
        index = img[i,j]
        newval = ((c[index] - cdf_min) / (N - cdf_min)) * 255
        global_equal_img[i,j] = newval

out_name = sys.argv[2]
cv2.imwrite(out_name, global_equal_img)