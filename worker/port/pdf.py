
import os
import time


import logging
import traceback


from pdfcore.pdf2text import parse


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

	def run_pdf(self, pdf):
		text = parse(pdf)
		
		ocr = text
		bbox = []
		hocr = []
		
		return ocr, bbox, hocr
	#enddef
	
	def runtime_pdf(self, pdf):
		
		text = parse(pdf)

		return text
	#enddef
#endclass


pdf_engine = Pdf()

def run(filename):

	pdf_file = filename

	text, bbox, hocr = pdf_engine.run_pdf(pdf_file)
	ocr = [text]
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
















