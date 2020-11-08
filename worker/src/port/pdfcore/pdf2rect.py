
import fitz #pip install PyMuPDF
import os
import cv2

def get_rect_with_word(pdf_file, text):
	pagenum = -1
	rect = None
	
	doc = fitz.open(pdf_file)
	
	for page in doc:
		pagenum = pagenum + 1
	
		linelist = page.getTextWords()
		for line in linelist:
			if text in line[4]:
				rectline = fitz.Rect(line[:4])
				
				start = line[4].find(text)
				char_width = (rectline[2] - rectline[0]) / len(line[4])

				rect = [int(rectline[0] + char_width*start), int(rectline[1]), int(rectline[0] + char_width*len(text)), int(rectline[3])]
				
				#page.addUnderlineAnnot(rect)  # underline
				#doc.save("n1.pdf")
				
				break
			#endif
		#endfor
	#endfor
	
	return pagenum, rect
	
#enddef


def get_image_with_rect(pdf_file, rect, pagenum):
	
	doc = fitz.open(pdf_file)
	page = doc[0];

	tmpfile = "%s-%i.png" % (pdf_file, page.number)

	pix = page.getPixmap(alpha = False)  # render page to an image
	pix.writePNG(tmpfile)

	img = cv2.imread(tmpfile)


	img1=img[rect[1]:rect[3],rect[0]:rect[2]]
	#img1 = cv2.rectangle(img, (rect[0],rect[1]), (rect[2], rect[3]),(0, 255, 0), 2)
	
	#cv2.imshow("img1",img1)
	#cv2.waitKey(0)

	os.remove(tmpfile)
	
	return img1;
		

#enddef	

if __name__ == '__main__':

	pdf_file ="4.pdf"

	pagenum, rect = get_rect_with_word(pdf_file, "群众")
	
	print(pagenum, rect)
	
	get_image_with_rect(pdf_file, rect, pagenum)
	
