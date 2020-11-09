
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
	
	
	# 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
	zoom_x = 1.33333333 #(1.33333333-->1056x816)   (2-->1584x1224)
	zoom_y = 1.33333333
	
	# 此处若是不做设置，默认图片大小为：792X612, dpi=96
	#2480 3509
	
	zoom_y = 3500/800
	zoom_x = zoom_y
	mat = fitz.Matrix(zoom_x, zoom_y)
	
	pix = page.getPixmap(matrix = mat, alpha = False)  # render page to an image
	pix.writePNG(tmpfile)

	img = cv2.imread(tmpfile)
	

	img1=img[int(rect[1]*zoom_y):int(rect[3]*zoom_y),int(rect[0]*zoom_x):int(rect[2]*zoom_x)]
	
	
	#cv2.imshow("img1",img1)
	#cv2.waitKey(0)

	os.remove(tmpfile)
	
	return img1;
		

#enddef	


def get_image_with_pagenum(pdf_file, pagenum):
	
	doc = fitz.open(pdf_file)
	page = doc[0];

	tmpfile = "%s-%i.png" % (pdf_file, page.number)
	
	
	# 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
	zoom_x = 1.33333333 #(1.33333333-->1056x816)   (2-->1584x1224)
	zoom_y = 1.33333333
	
	# 此处若是不做设置，默认图片大小为：792X612, dpi=96
	#2480 3509
	
	zoom_y = 3500/800
	zoom_x = zoom_y
	mat = fitz.Matrix(zoom_x, zoom_y)
	
	pix = page.getPixmap(matrix = mat, alpha = False)  # render page to an image
	pix.writePNG(tmpfile)

	img = cv2.imread(tmpfile)
	
	os.remove(tmpfile)
	
	return img;
		

#enddef	

if __name__ == '__main__':
	
	'''
	pdf_file ="4.pdf"

	pagenum, rect = get_rect_with_word(pdf_file, "群众")
	
	print(pagenum, rect)
	
	get_image_with_rect(pdf_file, rect, pagenum)
	'''
	
	img = get_image_with_rect("test2.pdf",  [400,500,550,650], 0)
	
	cv2.imshow("img",img)
	cv2.waitKey(0)
	
	
	img = get_image_with_pagenum("test3.pdf", -1)
	
	cv2.imshow("img",img)
	cv2.waitKey(0)
	


























