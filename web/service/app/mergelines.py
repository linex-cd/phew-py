#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	针对基于深度学习的OCR结果处理
"""
import copy,difflib,re


class Hocr_DL(object):
	def __init__(self, pages, file_type='', table_type='',file_title=''):
		self.__ocr = []
		self.__hocr = []
		self.file_type = file_type
		self.table_type = table_type
		self.__param = [-1, -1, -1]
		self.__page_border = []
		self.__content = ''
		self.__content_type = 0  # 0-text; 1-table
		self.__content_min_border = 0
		self.__content_max_border = 0
		self.__tag = False
		self.__start_index = 0
		self.__file_title = self.__clean_file_title(file_title)
		self.__table_diff_num =0.75 if len(self.__file_title)<=4 else 0.8
		self.__split_flag = False
		self.__process(pages)
		self.__format_content()


	def get_ocr(self):
		return self.__ocr

	def get_content(self):
		return self.__content


	def __clean_file_title(self,file_title):
		if re.findall(r'\(|（',file_title):
			file_title = re.split(r'\(|（',file_title)[0]

		return file_title


	def __process(self, pages):
		if pages is None:
			return
		self.__content_type = 1 if self.table_type else 0
		# k代表第几张图片
		for k in range(len(pages)):
			page = pages[k]
			self.__split_flag = True
			temp_ocr = self.__build_ocr_info(page)
			page['is_valid'] = 1
			self.__param[0] = k
			if len(page['content']) == 0:
				page['content'] = [['内容为空']]






			# self.__start_index = 1 if self.__content_type else 0

			if self.__content_type and page['content'][0] and self.__file_title!='扣押决定书':

				self.__ocr_table_name = page['content'][0][0] if len(page['content'][0])>0 else ''
				self.__ocr_table_name = re.sub(r'\s','',self.__ocr_table_name)
				self.__ocr_table_name = re.sub(r'\n','',self.__ocr_table_name)
				diff_num = len(set(self.__ocr_table_name)&set(self.__file_title))/len(self.__file_title)
				# print(self.__ocr_table_name, self.__file_title,diff_num,sep='*****')
				if diff_num<self.__table_diff_num:
					page['is_valid'] = 0

			self.__build_ocr_flag(page,temp_ocr)
			# i 代表单个图片内的内容，表格和非表格都统一

			for i in range(len(page['content'])):
				hocr = [[[0, 0, 0, 0]]] if i >= len(page['hocr']) else page['hocr'][i]
				if not hocr:
					hocr = [[[0, 0, 0, 0]]]
				self.__param[1] = i
				self.__start_index = min(1, len(page['content'][i])) if self.__content_type and self.__file_title!='扣押决定书' else 0
				self.__get_cell_content(hocr, page['content'][i])
		return

	# 构造ocr数据包
	def __build_ocr_info(self, page):
		ocr = {}
		ocr['hocr'] = page['hocr']
		ocr['bbox'] = page['bbox']
		ocr['content'] = page['content']
		return ocr
		# self.__ocr.append(ocr)

	def __build_ocr_flag(self,page,ocr):
		ocr['is_valid'] = page['is_valid']

		self.__ocr.append(ocr)


	def __get_whole_hocr(self, hocr):
		return {'page': self.__param[0],
				'cell': self.__param[1],
				'line': self.__param[2],
				'hocr': copy.deepcopy(hocr)}

	def __add_picture_begin(self):
		temp = '$PICTURESPLIT$'
		if self.__content == '':
			pass
		else:
			self.__content += temp
			self.__hocr[len(self.__hocr):len(self.__hocr)] = [self.__get_whole_hocr([0, 0, 0, 0]) for i in
															  range(len(temp))]

		self.__split_flag = False


	def __add_cell_begin(self, cell_index):
		temp = '@C' + str(cell_index) + 'B'
		self.__content += temp
		self.__hocr[len(self.__hocr):len(self.__hocr)] = [self.__get_whole_hocr([0, 0, 0, 0]) for i in range(len(temp))]

	def __add_cell_end(self, cell_index):
		temp = '@C' + str(cell_index) + 'E'
		self.__content += temp
		self.__hocr[len(self.__hocr):len(self.__hocr)] = [self.__get_whole_hocr([0, 0, 0, 0]) for i in range(len(temp))]

	def __get_cell_content(self, cell_hocr, cell_content):
		self.__content_min_border, self.__content_max_border = Hocr_DL.get_cell_border(cell_content, cell_hocr)
		#
		# self.__start_index = 1 if self.__content_type else 0
		# if self.__content_type and cell_content:
		#	 self.__ocr_table_name = cell_content[0]
		#	 self.__ocr_table_name = re.sub(r'\s','',self.__ocr_table_name)
		#	 self.__ocr_table_name = re.sub(r'\n','',self.__ocr_table_name)
		#	 diff_num = difflib.SequenceMatcher(None, self.__ocr_table_name, self.__file_title)
		#	 if diff_num<self.__table_diff_num:
		#		 return True

		for line_index in range(self.__start_index,len(cell_content)):
		# for line_index in range(len(cell_content)):
			self.__param[2] = line_index
			self.__get_line_content(cell_content, cell_hocr, line_index)
		return

	def __get_line_content(self, cell_content, cell_hocr, line_index):
		if self.__content_type == 0:
			self.__get_line_content_of_text(cell_content, cell_hocr, line_index)
		else:
			self.__get_line_content_of_table(cell_content, cell_hocr, line_index)
		return

	def __add_prefix(self, cell_content, cell_hocr, line_index, single_char_width):
		if self.file_type == '询问笔录' or self.file_type == '嫌疑人讯问笔录':
			self.__add_prefix_for_xunwenbilu(cell_content, cell_hocr, line_index)
			return
		line_hocr = cell_hocr[line_index]
		if line_index > 0:
			last_line_hocr = cell_hocr[line_index - 1]
			if len(last_line_hocr) > 0 and abs(line_hocr[0][1] - last_line_hocr[0][1]) < (
					last_line_hocr[0][3]) / 2:
				return
		if line_hocr[0][0] > self.__content_min_border + single_char_width:
			if not self.__content.endswith('\n'):
				self.__content += '\n'
				self.__hocr.append(self.__get_whole_hocr([0, 0, 0, 0]))

	def __add_suffix(self, cell_content, cell_hocr, line_index, single_char_width):
		if self.file_type == '询问笔录' or self.file_type == '嫌疑人讯问笔录':
			self.__add_suffix_for_xunwenbilu(cell_content, cell_hocr, line_index)
			return
		line_hocr = cell_hocr[line_index]
		if len(cell_hocr) > 0 and line_index < len(cell_hocr) - 1:
			next_line_hocr = cell_hocr[line_index + 1]
			if len(next_line_hocr) > 0 and abs(line_hocr[0][1] - next_line_hocr[0][1]) < (
					line_hocr[0][3]) / 2:
				return
		if line_hocr[0][0]+len(line_hocr)*line_hocr[0][2] + single_char_width * 2 < self.__content_max_border:
			self.__content += '\n'
			self.__hocr.append(self.__get_whole_hocr([0, 0, 0, 0]))

	def __add_prefix_for_xunwenbilu(self, cell_content, cell_hocr, line_index):
		line_content = cell_content[line_index]
		if line_content.startswith('问:') or line_content.startswith('答:'):
			self.__content += '\n'
			self.__hocr.append(self.__get_whole_hocr([0, 0, 0, 0]))
			self.__tag = True

	def __add_suffix_for_xunwenbilu(self, cell_content, cell_hocr, line_index):
		if self.__tag:
			return
		line_hocr = cell_hocr[line_index]
		if len(cell_hocr) > 0 and line_index < len(cell_hocr) - 1:
			next_line_hocr = cell_hocr[line_index + 1]
			if len(next_line_hocr) > 0 and abs(line_hocr[0][1] - next_line_hocr[0][1]) > (
					line_hocr[0][3]) / 2:
				self.__content += '\n'
				self.__hocr.append(self.__get_whole_hocr([0, 0, 0, 0]))

	def __get_line_content_of_text(self, cell_content, cell_hocr, line_index):
		line_content, line_hocr = cell_content[line_index], cell_hocr[line_index]
		if line_content == '':
			return
		single_char_width = line_hocr[0][2]
		self.__add_prefix(cell_content, cell_hocr, line_index, single_char_width)
		self.__content += line_content
		line_content_len = len(str(line_content))
		if line_content_len < len(line_hocr):
			self.__hocr[len(self.__hocr):len(self.__hocr)] = [self.__get_whole_hocr(hocr) for hocr in
															  line_hocr[:line_content_len]]
		elif line_content_len > len(line_hocr):
			self.__hocr[len(self.__hocr):len(self.__hocr)] = [self.__get_whole_hocr(hocr) for hocr in line_hocr]
			self.__hocr[len(self.__hocr):len(self.__hocr)] = [self.__get_whole_hocr([0, 0, 0, 0]) for i in
															  range((line_content_len - len(line_hocr)))]
		else:
			self.__hocr[len(self.__hocr):len(self.__hocr)] = [self.__get_whole_hocr(hocr) for hocr in line_hocr]
		self.__add_suffix(cell_content, cell_hocr, line_index, single_char_width)
		return

	def __get_line_content_of_table(self, cell_content, cell_hocr, line_index):
		if self.__split_flag:
			self.__add_picture_begin()
		self.__add_cell_begin(line_index)
		line_content, line_hocr = cell_content[line_index], cell_hocr[line_index]

		if line_content == '':
			self.__add_cell_end(line_index)
			return
		invalid_uchar = [u'|', u'!', u'^', u'〖', u'[', u'』', u'I', u'、', u'~', u'-', u'<', u'_']
		# temp = line_content.encode('utf-8')
		temp = line_content
		start, end = -1, -1
		for i in range(len(temp)):
			uchar = temp[i]
			if uchar not in invalid_uchar:
				start = i
				break

		for i in range(len(temp))[::-1]:
			uchar = temp[i]
			if uchar not in invalid_uchar:
				end = i + 1
				break
		if start != -1 and end != -1:
			self.__content += temp[start:end]
			self.__hocr[len(self.__hocr):len(self.__hocr)] = [self.__get_whole_hocr(hocr) for hocr in
															  line_hocr[start:end]]
		self.__add_cell_end(line_index)
		return

	@staticmethod
	def get_cell_border(cell_content, cell_hocr):
		min_border, max_border = [0, 0], [0, 0]
		default = [0, 0]
		for i in range(len(cell_content)):
			if len(cell_content[i]) > 0:
				if default == [0, 0]:
					default = [cell_hocr[i][0][0], cell_hocr[i][0][0]+len(cell_hocr[i])*cell_hocr[i][0][2]]
				if cell_content[i].endswith('.'):
					min_border[0] += cell_hocr[i][0][0]
					min_border[1] += 1
				if not (cell_content[i].endswith('.') or cell_content[i].endswith('?')
						or cell_content[i].endswith(':')):
					max_border[0] += (cell_hocr[i][0][0]+len(cell_hocr[i])*cell_hocr[i][0][2])
					max_border[1] += 1
		return min_border[0] / min_border[1] if min_border[1] > 0 else default[0], \
			   max_border[0] / max_border[1] if max_border[1] > 0 else default[1]


	def __format_content(self):
		# 此处的处理必须保证字符是等长替换
		replace_list = [
			['二O', '二〇'],
			['二C', '二〇'],
			['二o', '二〇'],
			['mg/100m1', 'mg/100ml'],
			['mg/m1', 'mg/ml']
		]
		self.__content = self.__str_replace_by_list(self.__content, replace_list)


	@staticmethod
	def __str_replace_by_list(str, replace_list):
		ret = str
		for r in replace_list:
			ret = ret.replace(r[0], r[1])
		return ret

	@staticmethod
	def list_get(item,index):
		try:
			return item[index]
		except Exception as e:
			print(e)
			return None


	
	
	
