
import cv2
import numpy as np

def check_gray(img, rect):
	
	#cv2.imshow('img', img)
	
	# get a frame and show
	frame = img[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
	#cv2.imshow('Capture', frame)

	
	#################################
	
	#words contours
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

	ret,thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY)

	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
	eroded = cv2.erode(thresh, kernel)
	#cv2.imshow('eroded', eroded)
	

	merge = cv2.bitwise_and(gray, eroded)
	#cv2.imshow('merge', merge)
	
	
	frametmp = cv2.cvtColor(merge,cv2.COLOR_GRAY2BGR)
	#################################
	#thumbprint
	
	# set thresh
	lower_gray = np.array([0, 0, 20], np.uint8)
	upper_gray = np.array([179, 50, 200], np.uint8)

	
	# change to hsv model
	hsv = cv2.cvtColor(frametmp, cv2.COLOR_BGR2HSV)

	# get mask
	mask = cv2.inRange(hsv, lower_gray, upper_gray)
	#cv2.imshow('Mask', mask)

	# detect
	res = cv2.bitwise_and(frametmp, frametmp, mask=mask)
	#cv2.imshow('Result', res)

	gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)  
	ret, binary = cv2.threshold(gray,150,255,cv2.THRESH_BINARY)  

	contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
	#cv2.drawContours(res, contours,-1,(0,0,255),3)  
	#cv2.imshow('check', res)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()
	
	#轮廓面积计算
	area = 0
	for i in range(len(contours)):
		area += cv2.contourArea(contours[i])
	return area

if __name__ == "__main__":
	image_file = "0331.jpg"
	image_file = "0337.jpg"
	img = cv2.imdecode(np.fromfile(image_file, dtype=np.uint8), cv2.IMREAD_COLOR)

	rect = [123, 2073, 601, 111] #6493
	rect = [982, 2060, 1130, 123] #985
	#rect = [128, 1870, 1452, 103] #83
	#rect = [119, 3080, 1072, 117] #180
	#rect = [194, 1457, 461, 78] #76
	#rect = [194, 1152, 461, 82] #38
	#rect = [1245, 2063, 727, 98] #4257
	#rect = [127, 2165, 393, 100] #500
	#rect = [719, 2157, 1313, 121] #5900

	s = check_gray(img, rect)
	print('s=%.1f, 建议值>700' % s)
