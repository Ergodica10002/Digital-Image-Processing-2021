import cv2
import numpy as np
import sys

if len(sys.argv) < 3:
	print("error!")
	print("usage: python3 fourier.py in_image out_image")
	exit()
filename = sys.argv[1]

img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
img_info = img.shape
height = img_info[0]
width = img_info[1]

fourier = np.zeros((height, width))
for i in range(height):
	for j in range(width):
		fourier[i][j] = img[i,j]

fourier = np.fft.fftshift(np.fft.fft2(fourier))

fmax = -1

for i in range(height):
	for j in range(width):
		if abs(fourier[i][j]) > fmax:
			fmax = abs(fourier[i][j])
log_fmax = np.log(1+fmax)

result_img = np.zeros((height, width))

for i in range(height):
	for j in range(width):
		result_img[i,j] = (np.log(1+abs(fourier[i][j])) / log_fmax) * 255

out_name = sys.argv[2]
cv2.imwrite(out_name, result_img)