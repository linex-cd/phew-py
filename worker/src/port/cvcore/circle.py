from PIL import Image
import cv2

import numpy as np


'''
img  输入矩阵
method cv2.HOUGH_GRADIENT 也就是霍夫圆检测，梯度法
dp 计数器的分辨率图像像素分辨率与参数空间分辨率的比值（官方文档上写的是图像分辨率与累加器分辨率的比值，它把参数空间认为是一个累加器，毕竟里面存储的都是经过的像素点的数量），dp=1，则参数空间与图像像素空间（分辨率）一样大，dp=2，参数空间的分辨率只有像素空间的一半大
minDist 圆心之间最小距离，如果距离太小，会产生很多相交的圆，如果距离太大，则会漏掉正确的圆
param1 canny检测的双阈值中的高阈值，低阈值是它的一半
param2 最小投票数（基于圆心的投票数）
minRadius 需要检测院的最小半径
maxRadius 需要检测院的最大半径
'''
def get_circle(src_img, rect):

	
	max_Width = 800

	w = src_img.shape[1]
	h = src_img.shape[0]

	scale_rate = max_Width /  w
	h = int(scale_rate * h)

	img = cv2.resize(src_img, (max_Width, h))
	
	rect = [int(rect[0]*scale_rate), int(rect[1]*scale_rate), int(rect[2]*scale_rate), int(rect[3]*scale_rate)]
	
	# get a frame and show
	frame = img[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 转换为灰色通道


	GrayImage=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	GrayImage= cv2.medianBlur(GrayImage,5)
	ret,th1 = cv2.threshold(GrayImage,127,255,cv2.THRESH_BINARY)
	th2 = cv2.adaptiveThreshold(GrayImage,255,cv2.ADAPTIVE_THRESH_MEAN_C,  
						cv2.THRESH_BINARY,3,5)  
	th3 = cv2.adaptiveThreshold(GrayImage,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,  
						cv2.THRESH_BINARY,3,5)


	kernel = np.ones((5,5),np.uint8)
	erosion = cv2.erode(th2,kernel,iterations=1)
	dilation = cv2.dilate(erosion,kernel,iterations=1)

	imgray=cv2.Canny(erosion,30,100)

	circles = cv2.HoughCircles(imgray,cv2.HOUGH_GRADIENT,dp=1, minDist = 50,
								param1=50,param2=30,minRadius=60,maxRadius=85)

	if circles is None:
		return 0
	circles = np.uint16(np.around(circles))
	
	s = len(circles[0,:])
	print(s)
	
	'''
	for i in circles[0,:]:
		# draw the outer circle
		cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
		# draw the center of the circle
		cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)

	cv2.imshow('detected circles',frame)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	'''
	
	return s
	
if __name__ == "__main__":
	image_file = "0006.jpg"
	img = cv2.imdecode(np.fromfile(image_file, dtype=np.uint8), cv2.IMREAD_COLOR)
	rect = [0, 0, img.shape[1], img.shape[0]]

	s = get_circle(img, rect)
	print('s=%d 圆形个数，建议值>0' % s)
