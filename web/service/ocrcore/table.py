#coding:utf-8

import cv2
import numpy as np



def detect_table(src_img):
	#缩放线段，尺寸越大效果越好，但是越费时间
	max_Width = 900
	
	w = src_img.shape[1]
	h = src_img.shape[0]
	
	scale_rate = max_Width /  w
	h = int(scale_rate * h)
	resized_img = cv2.resize(src_img, (max_Width, h))
	
	
	# 检测表格，使用形态学
	# 返回是表格图以及表格中交叉点的图
	if len(resized_img.shape) == 2:  # 灰度图
		gray_img = resized_img
	elif len(resized_img.shape) ==3:
		gray_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)

	thresh_img = cv2.adaptiveThreshold(~gray_img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,9,-2)
	h_img = thresh_img.copy()
	v_img = thresh_img.copy()
	scale = 50
	h_size = int(h_img.shape[1]/scale)

	h_structure = cv2.getStructuringElement(cv2.MORPH_RECT,(h_size,1)) # 形态学因子
	h_erode_img = cv2.erode(h_img,h_structure,1)

	h_dilate_img = cv2.dilate(h_erode_img,h_structure,1)
	# cv2.imshow("h_erode",h_dilate_img)
	v_size = int(v_img.shape[0] / scale)

	v_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, v_size))  # 形态学因子
	v_erode_img = cv2.erode(v_img, v_structure, 1)
	v_dilate_img = cv2.dilate(v_erode_img, v_structure, 1)

	mask_img = h_dilate_img+v_dilate_img
	joints_img = cv2.bitwise_and(h_dilate_img,v_dilate_img)
	#cv2.imshow("joints",joints_img)
	#cv2.imshow("mask",mask_img)
	

	height = mask_img.shape[0]
	weight = mask_img.shape[1]
	#print("weight : %s, height : %s" %(weight, height))
	
	# 边距控制
	padding = 0.1
	
	'''
	#修复间断区域
	#sample
	#a = '00001110011110000'
	#s=0
	#e=0
	#def replace_char(string, char, index):
	#	string = list(string)
	#	string[index] = char
	#	return ''.join(string)
	#for i in range(len(a)):
	#	pix = a[i]
	#	if pix == '1':
	#		e = i
	#		if s != 0 : #not left padding
	#			print(i,'-',e,'-',s)
	#			for i in range(s, e):
	#				#a[i]='+'
	#				a = replace_char(a, '+', i)
	#			s = 0
	#		else:
	#			pass
	#	else:
	#		if e != 0 and s == 0:
	#			s = i
	#
	#print(a)

	
	frame = mask_img
	
	#线段补全阈值
	miss_line = 15
	
	#修复行
	for row in range(int(height*padding), int(height*(1-padding))):
		s = 0
		e = 0

		for col in range(int(weight*padding), int(weight*(1-padding))):
			pix = frame[row][col]
			if pix >= 200:
				e = col
				if s != 0 : #not left padding
					if e - s < miss_line:
						for i in range(s, e):
							frame[row][i] = 230

					s = 0
				else:
					pass
			else:
				if e != 0 and s == 0:
					s = col
					

	
	#修复列
	for col in range(int(weight*padding), int(weight*(1-padding))):
		s = 0
		e = 0

		for row in range(int(height*padding), int(height*(1-padding))):
			pix = frame[row][col]
			if pix >= 200:
				e = row
				if s != 0 : #not left padding
					if e - s < miss_line:
						for i in range(s, e):
							frame[i][col] = 230

					s = 0
				else:
					pass
			else:
				if e != 0 and s == 0:
					s = row
	cv2.imshow("fix", frame)
	'''
	
	#裁剪单元格
	ret, binary = cv2.threshold(mask_img,1,50,cv2.THRESH_BINARY)  

	contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	boxes = []

	for c in contours:

		rect = cv2.boundingRect(c)
		x,y,w,h = rect
		x = int(x)
		y = int(y)
		w = int(w)
		h = int(h)

		if w > 30 and h > 20 and w < weight*(1-padding) and h < height*(1-padding) and h < height*0.5:
			boxes.append([x,y,w,h])
	
	#重新排序
	resized_boxes = sorted(boxes, key=lambda x: (x[1]//10, x[0]))
	absolute_boxes = []
	for resized_box in resized_boxes:
		absolute_box = [0,0,0,0]
		absolute_box[0] = int(resized_box[0] / scale_rate)
		absolute_box[1] = int(resized_box[1] / scale_rate)
		absolute_box[2] = int(resized_box[2] / scale_rate)
		absolute_box[3] = int(resized_box[3] / scale_rate)
		absolute_boxes.append(absolute_box)
	
	return resized_img, resized_boxes, absolute_boxes



if __name__=='__main__':
	
	import time

	s0=time.time()
	
	img = cv2.imread('0016.jpg')
	resized_img, resized_boxes, absolute_boxes = detect_table(img)
	
	
	s1=time.time()
	print('detect time=%.3f' % (s1-s0))
	
	'''
	for box in resized_boxes:
		x,y,w,h = box
		tmp_img = resized_img[y:y+h, x:x+w]
		print('resized_img shape:', resized_img.shape[1], 'x', resized_img.shape[0])
		print('shape:', tmp_img.shape[1], 'x', tmp_img.shape[0])
		print(box)
		print(tmp_img.shape)

		resized_img = cv2.rectangle(resized_img, (x,y), (x+w,y+h), (0,255,0), 2)
		cv2.imshow("img2", resized_img)  
		#cv2.waitKey(0)  
	cv2.waitKey(0) 
	'''
	
	cv2.namedWindow('img3', cv2.WINDOW_NORMAL)
	for box in absolute_boxes:
		x,y,w,h = box
		tmp_img = img[y:y+h, x:x+w]
		print('img shape:', img.shape[1], 'x', img.shape[0])
		print('shape:', tmp_img.shape[1], 'x', tmp_img.shape[0])
		print(box)
		print(tmp_img.shape)
		#cv2.imwrite("tmp.jpg", tmp_img)
		img = cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
	cv2.imshow("img3", img)  
	cv2.waitKey(0)  
	
	height = absolute_boxes[0][1]
	width = img.shape[0]
	title_area = [0, 0, width, height]
	title_img = img[:height, :]
	
	cv2.namedWindow('title_img', cv2.WINDOW_NORMAL)
	cv2.imshow("title_img", title_img)  
	cv2.waitKey(0)  



