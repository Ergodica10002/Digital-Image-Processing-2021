# this program is referenced by @Charles Ma on Stack Overflow
# white balance for every channel independently

import cv2
import numpy as np
import sys

if len(sys.argv) < 3:
    print("error!")
    print("usage: python3 wb.py in_image out_image")
    exit()
filename = sys.argv[1]

def wb(channel, perc = 0.05):
    mi, ma = (np.percentile(channel, perc), np.percentile(channel,100.0-perc))
    channel = np.uint8(np.clip((channel-mi)*255.0/(ma-mi), 0, 255))
    return channel

image = cv2.imread(filename) # load color
imWB  = np.dstack([wb(channel, 0.05) for channel in cv2.split(image)] )

out_name = sys.argv[2]
cv2.imwrite(out_name, imWB)