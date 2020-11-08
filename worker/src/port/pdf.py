
import os
import time


import logging
import traceback


from pdfcore.pdf2lines import parse


class Pdf:
	def __new__(cls, *args, **kw):
		if not hasattr(cls, '_instance'):
			orig = super(Pdf, cls)
			cls._instance = orig.__new__(cls, *args, **kw)
		return cls._instance
	#enddef
	
	def __init__(self):
		pass
	#enddef

	def run_pdf(self, pdf_file):
	
		result = {'text':[],'box':[],'hocr':[]}

		result['text'], result['box'], result['hocr'] = parse(pdf_file)
		
		return result['text'], result['box'], result['hocr']

	#enddef
	
	def runtime_pdf(self, pdf_file):
		
		res = {"results": []}
		
		start_time = time.time()
		ocr_result, rois, hocr = self.run_pdf(pdf_file)

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


pdf_engine = Pdf()

def run(filename):

	pdf_file = filename

	text, bbox, hocr = pdf_engine.run_pdf(pdf_file)

	
	result = {}
	result['ocr'] = text
	result['bbox'] = bbox
	result['hocr'] = hocr
	
	return result

#enddef


if __name__ == "__main__":

	pass
#enddef
















