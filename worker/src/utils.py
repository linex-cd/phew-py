import time

def log(text):

	now = time.strftime("%Y-%m-%d %H:%M:%S")
	text = "["+now+"] "+text

	print(text)

#enddef
