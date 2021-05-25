import cv2
import numpy as np
sample2_img = cv2.imread("hw3_sample_images/sample2.png")
img_info = sample2_img.shape
height = img_info[0]
width = img_info[1]

def conv(in_img, mask, r_index, c_index):
	size = len(mask)
	half_size = int((size-1)/2)
	value = 0
	for i in range(size):
		for j in range(size):
			r = int(r_index - half_size + i)
			c = int(c_index - half_size + j)
			if r < 0:
				r = 0
			if r >= height:
				r = height -1
			if c < 0:
				c = 0
			if c >= width:
				c = width - 1
			value += in_img[r,c][0] * mask[i][j]
	if value > 255:
		value = 255
	if value < 0:
		value = 0
	return value


H = []
for i in range(10):
	H.append([])
H[1] = np.array([[1, 2, 1],[2, 4, 2],[1, 2, 1]]) / 36
H[2] = np.array([[1, 0, -1],[2, 0, -2],[1, 0, -1]]) / 12
H[3] = np.array([[-1, 2, -1],[-2, 4, -2],[-1, 2, -1]]) / 12
H[4] = np.array([[-1, -2, -1],[0, 0, 0],[1, 2, 1]]) / 12
H[5] = np.array([[1, 0, -1],[0, 0, 0],[-1, 0, 1]]) / 4
H[6] = np.array([[-1, 2, -1],[0, 0, 0],[1, -2, 1]]) / 4
H[7] = np.array([[-1, -2, -1],[2, 4, 2],[-1, -2, -1]]) / 12
H[8] = np.array([[-1, 0, 1],[2, 0, -2],[-1, 0, 1]]) / 4
H[9] = np.array([[1, -2, 1],[-2, 4, -2],[1, -2, 1]]) / 4

M = []
T = []
for i in range(10):
	M.append(np.zeros((height, width)))
	T.append(np.zeros((height, width)))


for feature in range(1, 10):
	for i in range(height):
		for j in range(width):
			M[feature][i,j] = conv(sample2_img, H[feature], i, j)
	cv2.imwrite("hw3_result_images/M_{}.png".format(feature), M[feature])


for i in range(10):
	T.append(np.zeros((height, width)))

for feature in range(1, 10):
	for i in range(height):
		for j in range(width):
			energy = 0
			for k in range(13):
				for l in range(13):
					r = i - 6 + k
					c = j - 6 + l
					if r < 0:
						r = 0
					if r > height - 1:
						r = height - 1
					if c < 0:
						c = 0
					if c > width - 1:
						c = width - 1
					energy += int(M[feature][r,c])**2
			T[feature][i,j] = energy**0.5

np.save("hw3_result_images/T.npy", T)

