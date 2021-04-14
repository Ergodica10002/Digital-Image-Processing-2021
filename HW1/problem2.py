import cv2
import numpy as np
from matplotlib import pyplot as plt

sample2_img = cv2.imread('sample2.jpg')
sample3_img = cv2.imread('sample3.jpg')
sample4_img = cv2.imread('sample4.jpg')

imgInfo = sample2_img.shape
height = imgInfo[0]
width = imgInfo[1]
decrease_img = np.zeros((height, width, 3), np.uint8)
increase_img = np.zeros((height, width, 3), np.uint8)

for i in range(0,height):
    for j in range(0,width):
        (b,g,r) = sample2_img[i,j]
        decrease_val = int(b/5)
        newattr = (decrease_val, decrease_val, decrease_val)
        decrease_img[i,j] = np.uint8(newattr)
        increase_val = int(decrease_val * 5)
        newattr = (increase_val, increase_val, increase_val)
        increase_img[i,j] = np.uint8(newattr)

cv2.imwrite('3_result.jpg', decrease_img)
cv2.imwrite('4_result.jpg', increase_img)

X = range(0,256)
sample2_Y = np.zeros(256)
result3_Y = np.zeros(256)
result4_Y = np.zeros(256)

for i in range(0,height):
	for j in range(0,width):
		sample2_Y[sample2_img[i, j][0]] += 1
		result3_Y[decrease_img[i, j][0]] += 1
		result4_Y[increase_img[i, j][0]] += 1

plt.figure()
plt.title('sample2.jpg')
plt.plot(X, sample2_Y)
plt.figure()
plt.title('3_result.jpg')
plt.plot(X, result3_Y)
plt.figure()
plt.title('4_result.jpg')
plt.plot(X, result4_Y)
plt.show()


imgInfo = sample3_img.shape
height = imgInfo[0]
width = imgInfo[1]

global_equal_img = np.zeros((height, width, 3), np.uint8)
local_equal_img = np.zeros((height, width, 3), np.uint8)
p = np.zeros(256)

for i in range(0, height):
    for j in range(0, width):
        p[sample3_img[i,j][0]] += 1
        
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
        index = sample3_img[i,j][0]
        newval = ((c[index] - cdf_min) / (N - cdf_min)) * 255
        newattr = (newval, newval, newval)
        global_equal_img[i,j] = np.uint8(newattr)

window_size = 20
for i in range(0,height):
    for j in range(0,width):
    	p = np.zeros(256)
    	up_border = max(0, i-window_size)
    	down_border = min(height, i+window_size)
    	left_border = max(0, j-window_size)
    	right_border = min(width, j+window_size)
    	N = 0
    	for k in range(up_border, down_border):
    		for l in range(left_border, right_border):
        		p[sample3_img[k,l][0]] += 1
        		N += 1
    	c = np.zeros(256)
    	c[0] = p[0]
    	for m in range(1, 256):
    		c[m] = c[m-1] + p[m]
    	for m in range(0,256):
    		if c[m] != 0:
    			cdf_min = m
    			break
		
    	index = sample3_img[i,j][0]
    	newval = ((c[index] - cdf_min) / (N - cdf_min)) * 255
    	newattr = (newval, newval, newval)
    	local_equal_img[i,j] = np.uint8(newattr)

        
X = range(0,256)
result5_Y = np.zeros(256)
result6_Y = np.zeros(256)

for i in range(0,height):
	for j in range(0,width):
		result5_Y[global_equal_img[i, j][0]] += 1
		result6_Y[local_equal_img[i, j][0]] += 1


plt.figure()
plt.title('5_result.jpg')
plt.plot(X, result5_Y)
plt.figure()
plt.title('6_result.jpg')
plt.plot(X, result6_Y)
plt.show()
cv2.imwrite('5_result.jpg', global_equal_img)
cv2.imwrite('6_result.jpg', local_equal_img)


imgInfo = sample4_img.shape
height = imgInfo[0]
width = imgInfo[1]

def transfer_func(val):
	if val < 100:
		return (val ** 0.5) * (100 ** 0.5)
	else:
		return ((val - 100) ** 3) / (155 ** 2) + 100

result7_img = np.zeros((height, width, 3), np.uint8)

for i in range(0,height):
	for j in range(0,width):
		val = sample4_img[i,j][0]
		newval = transfer_func(val)
		newattr = (newval, newval, newval)
		result7_img[i,j] = np.uint8(newattr)

cv2.imwrite('7_result.jpg', result7_img)

X = range(0,256)
sample4_Y = np.zeros(256)
result7_Y = np.zeros(256)

for i in range(0,height):
	for j in range(0,width):
		sample4_Y[sample3_img[i, j][0]] += 1
		result7_Y[result7_img[i, j][0]] += 1

plt.figure()
plt.title('sample4.jpg')
plt.plot(X, sample4_Y)
plt.figure()
plt.title('7_result.jpg')
plt.plot(X, result7_Y)
plt.show()