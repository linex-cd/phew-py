#referrence
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
# https://www.pyimagesearch.com/2016/02/08/opencv-shape-detection/
# https://hub.packtpub.com/opencv-detecting-edges-lines-shapes/

import cv2
import numpy as np

def check_handwrite(img, rect):
	
	#cv2.imshow('img', img)
	
	# get a frame and show
	frame = img[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
	#cv2.imshow('Capture', frame)
	
	
	#字迹分离
	ret,thresh = cv2.threshold(frame,100,255,cv2.THRESH_BINARY)

	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
	eroded = cv2.erode(thresh, kernel)
	#cv2.imshow('eroded', eroded)

	edges = cv2.Canny(eroded,50,130,apertureSize = 3)

	_, thresh = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	contours, hierarchy = cv2.findContours(thresh, 3, 2)

	result= cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

	#笔迹数
	trace_count = 0

	#高度差
	dhmax = 0
	dhmin = 0
	
	for cnt in contours:
		#多边形逼近，得到多边形的角点
		#epsilon=3 多边曲线拟合动态参数
		epsilon = 0.01 * cv2.arcLength(cnt, True)
		approx = cv2.approxPolyDP(cnt, epsilon, True)
		
		#忽略x或y离心小于10的直线
		vx = []
		vy = []
		for p in approx:
			
			vx.append(p[0][0])
			vy.append(p[0][1])
			
		dx = max(vx) - min(vx)
		dy = max(vy) - min(vy)
		
		if dx > 10 and dy > 10:
			
			trace_count = trace_count + 1
			
			dhmax = max(vy) if max(vy) > dhmax else dhmax
			dhmin = min(vy) if min(vy) < dhmin else dhmin
			
			'''	

			print('----')
			print(clen)
			print(dx)
			print(dy)
			
			color = (int(approx[0][0][0]%255), int(approx[0][0][1]%255), int((approx[0][0][0]+approx[0][0][1])%255))
			cv2.polylines(result, [approx], True, color, 2)
			'''	
		
		
	#cv2.imshow("result", result)
	#cv2.waitKey(0)
	
	dh = dhmax - dhmin
	
	return trace_count, dh

if __name__ == "__main__":
	image_file = "0331.jpg"
	img = cv2.imdecode(np.fromfile(image_file, dtype=np.uint8), cv2.IMREAD_COLOR)

	rect = [719, 2157, 1313, 121] 
	rect = [119, 3016, 870, 166] 
	#rect = [1245, 2063, 627, 98] 

	s,h = check_handwrite(img, rect)
	print('s=%d,%d, 建议值>3 ,90' % (s, h))
