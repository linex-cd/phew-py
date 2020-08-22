
import os
import time
import cv2
import numpy as np
import logging
import traceback


from ocrcore.helper.image import read_url_img,base64_to_PIL,get_now
from ocrcore.fix import fix
from ocrcore.table import detect_table
from ocrcore.main import text_ocr
from ocrcore.conf import scale,maxScale,TEXT_LINE_SCORE


class Ocr:
	def __new__(cls, *args, **kw):
		if not hasattr(cls, '_instance'):
			orig = super(Ocr, cls)
			cls._instance = orig.__new__(cls, *args, **kw)
		return cls._instance
	#enddef
	
	def __init__(self):
		pass
	#enddef

	def run_ocr(self, img):
	
		result = {'text':[],'box':[],'hocr':[]}
		img =  cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
		data = []

		image = np.array(img)
		data = text_ocr(image, scale, maxScale, TEXT_LINE_SCORE)
		
		if len(data) == 0:
			return result['text'], result['box'], result['hocr']
				
		for item in data:
			result['text'].append(item['text'])
			result['box'].append(item['box'])
		#endfor
		
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
		

		
		#移除特殊符号
		tmp = list(result['text'])
		for i in range(len(tmp)):
			pre = ""
			if i > 0:
				pre = tmp[i-1]
			
			#endif
			tmp[i] = fix(pre, tmp[i])
		#endfor
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
			#endfor
			hocr.append(hocr_item)
			
			#print(sentence)
			#print(box)
			#print(hocr_item0)
			#print(hocr_item)
		#endfor
		result['hocr'] = hocr
		
		return result['text'], result['box'], result['hocr']
	#enddef		

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
		#endfor
		
		return res
	#enddef

#endclass

ocr_engine = Ocr()

def run(filename):
	
	image_file = filename
	
	ocr, bbox, hocr = [], [], []
	
	try:
		img = cv2.imdecode(np.fromfile(image_file, dtype=np.uint8), cv2.IMREAD_COLOR);
		ocr, bbox, hocr = ocr_engine.run_ocr(img)
	except:
		pass
	#endtry
	

	ocr = list(ocr)
	bbox = list(bbox)
	hocr = list(hocr)
	
	result = {}
	result['ocr'] = ocr
	result['bbox'] = bbox
	result['hocr'] = hocr
	
	return result
#enddef

if __name__ == "__main__":

	pass

#enddef















