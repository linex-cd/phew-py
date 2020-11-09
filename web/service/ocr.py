
import os
import time
import cv2
import numpy as np
import logging
import traceback

import sys
sys.path.append("ocrcore")


from ocrcore.helper.image import read_url_img,base64_to_PIL,get_now
from ocrcore.fix import fix
from ocrcore.table import detect_table
from ocrcore.dnn.main import text_ocr
from ocrcore.conf import scale,maxScale,TEXT_LINE_SCORE


class Ocr:
	def __new__(cls, *args, **kw):
		if not hasattr(cls, '_instance'):
			orig = super(Ocr, cls)
			cls._instance = orig.__new__(cls, *args, **kw)
		return cls._instance
		
	def __init__(self):
		pass
	

	def run_ocr(self, img, istable):
		result = {'text':[],'box':[],'hocr':[]}
		img =  cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
		data = []
		if istable:
			
			resized_img, resized_boxes, absolute_boxes = detect_table(img)
			
			#表头：以表格最上方区域为准
			height = absolute_boxes[0][1]
			width = img.shape[0]
			
			title_area = [0, 0, 0+width, 0+height]
			title_img = img[:0+height, :]
			title_data = text_ocr(title_img, scale, maxScale, TEXT_LINE_SCORE)
			title_text = ""
			for title_tmp in title_data:
				title_text = title_text + title_tmp['text']
			#endfor
			title_item = {'box':title_area, 'text':title_text}
			data.append(title_item)
			
					
			#表格
			for resized_box, absolute_box in zip(resized_boxes, absolute_boxes):
				x,y,w,h = resized_box
				tmp_img = resized_img[y:y+h, x:x+w]
				WHITE = [255,255,255]
				tmp_img = cv2.copyMakeBorder(tmp_img,400,400,30,30,cv2.BORDER_CONSTANT,value=WHITE)
				tmp_data = text_ocr(tmp_img, scale, maxScale, TEXT_LINE_SCORE)
				
				text = ""
				for temp_item in tmp_data:
					text = text + temp_item['text']
				
				x,y,w,h = absolute_box
				absolute_box = [x, y, x+w, y+h]
				item = {'box':absolute_box, 'text':text}
				data.append(item)
				
			#endfor
			
			if len(data) == 0:
				return result['text'], result['box'], result['hocr']
					
			for item in data:
				result['text'].append(item['text'])
				result['box'].append(item['box'])
					
		else:
			image = np.array(img)
			data = text_ocr(image, scale, maxScale, TEXT_LINE_SCORE)
			
			if len(data) == 0:
				return result['text'], result['box'], result['hocr']
					
			for item in data:
				result['text'].append(item['text'])
				result['box'].append(item['box'])
				
			#优化bbox的排序算法，而不是用y的精确值排序，上下应该允许平均高度误差，防止同一行文字被拆断,
			#并且注意段落换行时左侧起头较早，跟表格的左侧起头不一样，所以要用行尾计算
			# x y x+w y+h
			avg=40
			all = 0
			for item in result['box']:
				all = all + item[3] - item[1]
			#endfor
			avg = all/len(result['box'])
			offset = int(avg * 4/5)
			sorted_data = sorted(zip(result['box'], result['text']), key=lambda x: (x[0][1] // offset, x[0][0] + x[0][2]))
			result['box'], result['text'] = zip(*sorted_data)
			
			
			
			
		#endif
		
		
		#移除特殊符号
		tmp = list(result['text'])
		for i in range(len(tmp)):
			pre = ""
			if i > 0: pre = tmp[i-1]
			tmp[i] = fix(pre, tmp[i])
		result['text'] = tmp
	
		
		hocr = []
		
		for sentence, box in zip(result['text'], result['box']):
			
			count = len(sentence)
			if count == 0:
				hocr.append([])
				continue
			width = box[2] - box[0]
			height = box[3] - box[1]
			char_width = int(width / count)
			padding = 8
			hocr_item0 = []
			hocr_item = []
			for i in range(count):
				hocr_item0.append( (char_width * i + padding ,  char_width - padding) )
				hocr_item.append( (char_width * i + padding + box[0], box[1], char_width - padding, height) )
			hocr.append(hocr_item)
			
			#print(sentence)
			#print(box)
			#print(hocr_item0)
			#print(hocr_item)
		result['hocr'] = hocr
		
		return result['text'], result['box'], result['hocr']
				

	def runtime_ocr(self, img, istable):
		
		res = {"results": []}
		
		start_time = time.time()
		ocr_result, rois, hocr = self.run_ocr(img, istable)

		print("CRNN time: %.03fs" % (time.time() - start_time))


		for i in range(len(rois)):
			res["results"].append({
				'position': rois[i],
				'text': ocr_result[i],
				'hocr': hocr[i]
			})

		return res
	


if __name__ == "__main__":

	pass

















