import cv2
import numpy as np

def check(text, box, check):
	
	#shouxiezi nayin qianzhang
	for check_item in check.keys():


		for i in range(check[check_item]):
			
			type = check[check_item][i]['type']
			if type == 'words':
				key = check[check_item][i]['key']
				#每个关键字都搜索
				for keyword in key:
					
					for text, box in zip(texts, boxes):
						#是否包含关键字
						if text.find(keyword):
							#扩大查找面积
							'''
							1███
							↓
							0████████
							1████████
							2████████
							
							'''
							#rect = [box[0]-box[2], box[1]-box[3], box[2]*3, box[3]*3]
							rect = box
							s = check_area(img, rect)
							
							#面积阈值
							if s > 5:
								check[check_item][i]['exist'] == 'yes'
							#endif
							
						#endif
					#endfor
				#endfor
			#endif
			
			if type == 'pos':
				rect = check[check_item][i]['key']

				s = check_area(img, rect)
				
				#面积阈值
				if s > 5:
					check[check_item][i]['exist'] == 'yes'
				#endif
			#endif
			
			if type == 'scan':
				w = img.shape[1]
				h = img.shape[0]
				rect = [0, 0, w ,h]

				s = check_area(img, rect)
				
				#面积阈值
				if s > 1:
					check[check_item][i]['exist'] == 'yes'
				#endif
			#endif
			
			
		#endfor
	#endfor
		
	return check
	


def check_area(img, rect):
	
	# set thresh
	lower_blue=np.array([70,30,30])
	upper_blue=np.array([240,220,220])

	#cv2.imshow('img', img)
	
	# get a frame and show
	frame = img[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
	#cv2.imshow('Capture', frame)

	# change to hsv model
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# get mask
	mask = cv2.inRange(hsv, lower_blue, upper_blue)
	#cv2.imshow('Mask', mask)

	# detect
	res = cv2.bitwise_and(frame, frame, mask=mask)
	#cv2.imshow('Result', res)
	
	gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)  
	ret, binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)  

	img, contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
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
	image_file = "seal.jpg"
	img = cv2.imdecode(np.fromfile(image_file, dtype=np.uint8), cv2.IMREAD_COLOR)
	rect = [76, 528, 164, 26]
	rect = [240, 553, 142, 28]
	#rect = [0, 0, 480-1, 676-1]
	s = check_area(img, rect)
	print('s=%.1f' % s)
















