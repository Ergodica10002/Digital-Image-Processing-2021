import numpy as np
import cv2
import math
import sys

if len(sys.argv) < 3:
    print("error!")
    print("usage: python3 Canny_edge_detect.py in_image out_image")
    exit()

filename = sys.argv[1]

img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
img_info = img.shape
height = img_info[0]
width = img_info[1]

#start of Canny edge detection

TH = 20
TL = 10
blurred = cv2.GaussianBlur(img, (5, 5), 0)
canny_edge_map = cv2.Canny(blurred, TL, TH)
        
#end of Canny edge detection
out_name = sys.argv[2]
cv2.imwrite(out_name, canny_edge_map)