#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def replace_char(string, char, index):
	string = list(string)
	string[index] = char
	return ''.join(string)
	


def fix(pre, text):
		
	map = []
	
	map.append(('出笙', '出生'))
	map.append(('笙日', '生日'))
	map.append(('讯间', '讯问'))
	map.append(('被间', '被问'))
	
	map.append(('时间', '@time@'))
	map.append(('间:', '问：'))
	map.append(('间：', '问：'))
	map.append(('@time@', '时间'))
	
	map.append(('O', '0'))
	map.append(('=', '二'))
	map.append(('+', '十'))
	map.append(('二0', '二〇'))

	for item in map:
		
		text = text.replace(item[0], item[1])


	if len(text) > 2 and list(text)[0] in ['问','答']:
		if list(text)[1] in [':', ',', '，']:
			#text[1] = '：'
			text = replace_char(text , '：', 1)
		
		if list(text)[2] in [':', ',', '，']:
			#text[2] = '：'
			text = replace_char(text , '：', 2)
	
	
	#处理识别掉 “至”的问题
	p1 = pre.find('年')
	p2 = pre.find('月')
	p3 = pre.find('日')
	p4 = pre.find('时')
	p5 = pre.find('分')
	
	t1 = text.find('年')
	t2 = text.find('月')
	t3 = text.find('日')
	t4 = text.find('时')
	t5 = text.find('分')
	
	if p1>0 and p2>0 and p3>0 and p4>0 and p5>0 and t1>0 and t2>0 and t3>0 and t4>0 and t5>0 :
		text = '至' + text
	
	return text

    