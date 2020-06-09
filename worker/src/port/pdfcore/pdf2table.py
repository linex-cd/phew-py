
import pdfplumber
def parse(pdf_file):
	all_text = ""
	with pdfplumber.open(pdf_file) as pdf:
		for page in pdf.pages:
		
			text = page.extract_text()
			if text is not None:
				text = text.replace("\n", "")
				all_text = all_text + text
	
	return all_text;

if __name__ == '__main__':


	pdf_file ="test31.pdf"

	rs = parse(pdf_file)
	print(rs)
	
	
