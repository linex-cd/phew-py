from operator import itemgetter
import fitz
def parse(pdf_file):
	all_text = ""
	doc = fitz.open(pdf_file)
	
	for page in doc:
		blocks = page.getTextBlocks()
		
		sb = sorted(blocks, key=itemgetter(1, 0))
		for b in sb:
			#print (b)
			text = b[4]
			lines = text.split('\n')
			for line in lines:
				if line[-1:] in ["。", "：", "？", "！"]:
					line = line + '\n'
				if len(line) < 28:
					line = line + '\n'
				all_text = all_text + line
			
			all_text = all_text + '\n'

	return all_text;

if __name__ == '__main__':


	pdf_file ="4.pdf"

	rs = parse(pdf_file)
	print(rs)
