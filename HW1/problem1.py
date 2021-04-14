import cv2
import numpy as np

sample1_img = cv2.imread('sample1.jpg')
imgInfo = sample1_img.shape
height = imgInfo[0]
width = imgInfo[1]

gray_img = np.zeros((height, width, 3), np.uint8)
flip_img = np.zeros((height, width, 3), np.uint8)

for i in range(0,height):
    for j in range(0,width):
        (b,g,r) = sample1_img[i,j]
        gray = (int(b)+int(g)+int(r))/3
        gray_img[i,j] = np.uint8(gray)
        
for i in range(0,height):
    for j in range(0,width):
        flip_img[i,j] = sample1_img[i, width-j-1]

cv2.imwrite('1_result.jpg', gray_img)
cv2.imwrite('2_result.jpg', flip_img)