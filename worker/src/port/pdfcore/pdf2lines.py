import fitz

def parse(pdf_file):
	
	texts = []
	boxs = []
	hocrs = []
	
	
	doc = fitz.open(pdf_file)
	
	for page in doc:
		
		page_texts = []
		page_boxs = []
		page_hocrs = []
		
		linelist = page.getTextWords()
		for line in linelist:
		

			box = fitz.Rect(line[:4])
			
			box = [int(box[0]), int(box[1]), int(box[2]), int(box[3])]
			
			hocr = []
			
			text = line[4]
			
			count = len(text)
			char_width = int((box[2] - box[0]) / count)
			padding = 0
			for i in range(count):
				hocr.append( [char_width * i + padding + box[0], box[1], char_width - padding, box[3] - box[1]] )
			#endfor

			
			page_texts.append(text)
			page_boxs.append(box)
			page_hocrs.append(hocr)
			
		#endfor
		
		texts.append(page_texts)
		boxs.append(page_boxs)
		hocrs.append(page_hocrs)
	#endfor
	
	return texts, boxs, hocrs

#endif

if __name__ == '__main__':


	pdf_file ="1.pdf"

	rs = parse(pdf_file)
	print(rs)
