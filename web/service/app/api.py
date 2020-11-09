from django.http import HttpResponse, HttpResponseRedirect
import time



from ocr import Ocr
from pdf import Pdf

from base64 import b64decode
import json

import cv2
import numpy as np

from app import mergelines

ocr_engine = Ocr()
pdf_engine = Pdf()

def test(request):
	return HttpResponse("the service is online.")
	
def index(request):
	return HttpResponseRedirect("/index.html")

def table(request):
	return HttpResponseRedirect("/table.html")


def ocr(request):
	in_memory_file = request.FILES['img'].read()
	#in_memory_file = io.BytesIO()

	nparr = np.fromstring(in_memory_file, np.uint8)
	img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

	print('Image size: {}x{}'.format(img.shape[1], img.shape[0]))
	
	table = request.POST.get('table','no') 
	istable = False 
	if table == 'yes':
		istable =  True
	#data = ocr_engine.runtime_ocr(img, istable)
	
	start_time = time.time()
	ocr_result, rois, hocr = ocr_engine.run_ocr(img, istable)

	print("CRNN time: %.03fs" % (time.time() - start_time))
	
	
	data = {"results": []}
	for i in range(len(rois)):
		data["results"].append({
			'position': rois[i],
			'text': ocr_result[i],
			'hocr': hocr[i]
		})
		
	pages = []
	page = {'content':[ocr_result], 'hocr': [hocr], 'bbox': [rois]}
	
	pages.append(page)
	dl = mergelines.Hocr_DL(pages)
	content = dl.get_content()
	
	data['dl'] = content

	return HttpResponse(json.dumps(data), content_type='application/json')



	
def rtocr(request):
	
	data = {'code':403, 'msg':'No image data passthrough'}
	
	#if 'img' in request.POST and request.POST['img']:
	#	img_base64 = request.POST['img']
	if request.method == 'POST':
		jsondata = json.loads(request.body.decode())
		img_base64 = jsondata['img'];
		
		imgdata = b64decode(img_base64)

		'''
		file=open('1.png','wb')
		file.write(imgdata)
		file.close()
		'''
		
		nparr = np.fromstring(imgdata, np.uint8)
		img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
		
		#cv2.imshow("ori", img)
		#cv2.waitKey(0)
		print('Image size: {}x{}'.format(img.shape[1], img.shape[0]))
		
		#create frame
		WHITE = [255,255,255]
		frame = cv2.copyMakeBorder(img,400,400,30,30,cv2.BORDER_CONSTANT,value=WHITE)
		#cv2.imshow("frame", frame)
		#cv2.waitKey(0)
		
		istable = False
		#data = ocr_engine.runtime_ocr(frame, istable)
		ocr_result, rois, hocr = ocr_engine.run_ocr(img, istable)
		
			
		data = {"results": []}
		for i in range(len(rois)):
			data["results"].append({
				'position': rois[i],
				'text': ocr_result[i],
				'hocr': hocr[i]
			})
			
		pages = []
		page = {'content':[ocr_result], 'hocr': [hocr], 'bbox': [rois]}
	
		pages.append(page)
		dl = mergelines.Hocr_DL(pages)
		content = dl.get_content()
		
		data['dl'] = content

	response = HttpResponse(json.dumps(data), content_type='application/json')
	response["Access-Control-Allow-Origin"] = "*"
	response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
	response["Access-Control-Max-Age"] = "1800"
	response["Access-Control-Allow-Headers"] = "*"
	
	return response
	
def rtpdf(request):
	
	data = {'code':403, 'msg':'No pdf data passthrough'}
	
	#if 'img' in request.POST and request.POST['img']:
	#	img_base64 = request.POST['img']
	if request.method == 'POST':
		
		pdf = request.FILES.get('file')
		if pdf != None:
			data['data'] = pdf_engine.runtime_pdf(pdf)
			data['msg'] = 'OK'
			data['code'] = '200'
		else:
			data['data'] = ''
			data['msg'] = 'OK'
			data['code'] = '200'
		

	response = HttpResponse(json.dumps(data), content_type='application/json')
	response["Access-Control-Allow-Origin"] = "*"
	response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
	response["Access-Control-Max-Age"] = "1800"
	response["Access-Control-Allow-Headers"] = "*"
	
	return response
	
	
	
	