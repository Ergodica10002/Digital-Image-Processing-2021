#The twiel-method used is referenced from the following
#website: https://web.cs.wpi.edu/~emmanuel/courses/cs545/S14/slides/lecture11.pdf
import numpy as np
import cv2
from matplotlib import pyplot as plt
import math

sample5_img = cv2.imread("hw2_sample_images/sample5.jpg")
img_info = sample5_img.shape
height = img_info[0]
width = img_info[1]

def img2cartesian(p,q):
    u = q - 0.5
    v = height + 0.5 - p
    return (u,v)

result7_img = np.zeros((height, width, 3), np.uint8)

center = (width/2, height/2)
rmax = (center[0]**2 + center[1]**2)**0.5
alpha = -0.9
gamma = 0.3



for i in range(height):
    for j in range(width):
        (x,y) = img2cartesian(i,j)

        (dx,dy) = (x-center[0], y-center[1])
        r = (dx**2 + dy**2)**0.5
        
        theta = 3 * math.exp(-1 * r / rmax)
        mag = 1
        rotate = np.array([[math.cos(theta), -1*mag*math.sin(theta)],[mag*math.sin(theta), math.cos(theta)]])
        rotate_inv = np.linalg.inv(rotate)
        du = dx
        dv = dy
        u = rotate_inv[0][0] * du + rotate_inv[0][1] * dv + center[0]
        v = rotate_inv[1][0] * du + rotate_inv[1][1] * dv + center[1]
        
        
        #(du,dv) = (u-center[0], v-center[1])
        #r_uv = (du**2 + dv**2)**0.5
        #u = (rmax/r)**gamma * 0.7 * (u-center[0])+center[0]
        #v = (rmax/r)**gamma * 0.7 * (v-center[1])+center[1]
        
        q = u + 0.5
        p = height + 0.5 -v
        q1 = min(width-1, max(0, math.floor(q)))
        q2 = min(width-1, q1+1)
        p1 = min(height-1, max(0, math.floor(p)))
        p2 = min(height-1, p1+1)
        (a,b) = (p-p1, q-q1)
        newval = (1-a)*(1-b)*sample5_img[p1,q1][0]+(1-a)*b*sample5_img[p1,q2][0]+a*(1-b)*sample5_img[p2,q1][0]+a*b*sample5_img[p2,q2][0]
        newval = math.ceil(newval)
        
        result7_img[i,j] = ((newval, newval, newval))

cv2.imwrite("hw2_result_images/result7_t.jpg", result7_img)