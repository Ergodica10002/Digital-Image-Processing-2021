import numpy as np
import cv2
from matplotlib import pyplot as plt
import math

sample3_img = cv2.imread("hw2_sample_images/sample3.jpg")
img_info = sample3_img.shape
height = img_info[0]
width = img_info[1]

def img2cartesian(p,q):
    u = q - 0.5
    v = height + 0.5 - p
    return (u,v)

result6_img = np.zeros((height, width, 3), np.uint8)

theta = 1.3
(tx,ty) = (-200, -100)
rotate = np.array([[math.cos(theta), -1*math.sin(theta)],[math.sin(theta), math.cos(theta)]])
rotate_inv = np.linalg.inv(rotate)
mag = 1.4

center = (width/2, height/2)

for i in range(height):
    for j in range(width):
        (x,y) = img2cartesian(i,j)
        x = (x - center[0]) * (1/mag) + center[0]
        y = (y - center[1]) * (1/mag) + center[1]
        x = x - tx
        y = y - ty
        u = rotate_inv[0][0] * (x-center[0]) + rotate_inv[0][1] * (y-center[1]) + center[0]
        v = rotate_inv[1][0] * (x-center[0]) + rotate_inv[1][1] * (y-center[1]) + center[1]
        q = u + 0.5
        p = height + 0.5 -v
        q1 = min(width-1, max(0, math.floor(q)))
        q2 = min(width-1, q1+1)
        p1 = min(height-1, max(0, math.floor(p)))
        p2 = min(height-1, p1+1)
        (a,b) = (p-p1, q-q1)
        newval = (1-a)*(1-b)*sample3_img[p1,q1][0]+(1-a)*b*sample3_img[p1,q2][0]+a*(1-b)*sample3_img[p2,q1][0]+a*b*sample3_img[p2,q2][0]
        newval = math.ceil(newval)
        
        result6_img[i,j] = ((newval, newval, newval))

cv2.imwrite("hw2_result_images/result6.jpg", result6_img)