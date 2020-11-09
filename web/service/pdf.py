
import os
import time


import logging
import traceback


from ocrcore.pdf2text import parse


class Pdf:
	def __new__(cls, *args, **kw):
		if not hasattr(cls, '_instance'):
			orig = super(Pdf, cls)
			cls._instance = orig.__new__(cls, *args, **kw)
		return cls._instance
		
	def __init__(self):
		pass


	

	def run_pdf(self, pdf):
		text = parse(pdf)
		
		ocr = text
		bbox = []
		hocr = []
		
		return ocr, bbox, hocr

	def runtime_pdf(self, pdf):
		
		text = parse(pdf)

		return text

	
	


if __name__ == "__main__":

	pass

















