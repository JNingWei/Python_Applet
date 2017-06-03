#!/usr/bin/python  
# -*- coding: utf-8 -*-

import urllib
import json
import socket
import os  
import sys
import re
import argparse


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
add_arg = parser.add_argument
add_arg('--keyword', '-kw', default='pretty girl', help='输入关键字')
add_arg('--download_page', '-dp', default=1, type=int, help='希望下载的页数(其中每页60张图)')
add_arg('--dir', default='./Images/', help='输入图片存放地址')
args = parser.parse_args()

valid_type = ['.png', '.jpg', '.PNG', '.JPG', '.gif', '.GIF', '.jpeg', '.JPEG']
download_page = args.download_page
socket.setdefaulttimeout(10)

keyword = args.keyword

tmpurl = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + keyword + '&pn='
# tmpurl = 'http://image.baidu.com/search/flip?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1496473221479_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&ctd=1496473221479%5E00_1840X966&word='+keyword

dir = args.dir
try:
	if not os.path.isdir(dir):
		os.mkdir(dir)
except OSError:
	print 'Can not make dir!'
	sys.exit()
i = 0

for dp in xrange(download_page):
	url = tmpurl+str(dp*60)
	pattern = re.compile(r'setData\(\'imgData\', (\{[\s\S]*?\})\);')
	try:
		ipdata = urllib.urlopen(url).read()
	except IOError:
		print 'can not open this url!'
		sys.exit() 
	ipdata = pattern.search(ipdata)
	ipdata = ipdata.group(1)
	_regex = re.compile(r'\\(?![/u"])')  
	ipdata = _regex.sub(r"\\\\", ipdata) 
	imgData = json.loads(ipdata, strict=False)

	if imgData['data']:
		for obj in imgData['data']:
			if obj and obj['objURL']:
				try:
					data_img = urllib.urlopen(obj['objURL']).read()
				except IOError:
					print '--- Meet damaged image.'
				else:
					fPostfix = os.path.splitext(obj['objURL'])[1]
					if fPostfix in valid_type:
						filename = dir + os.path.basename(obj['objURL'])
					else:
						filename = dir + os.path.basename(obj['objURL']) + '.jpg'
					try:
						file_obj = open(filename, 'w')
						file_obj.write(data_img)
						file_obj.close()
					except socket.timeout, e:
						print 'socket time out!'
					else:
						i += 1
						print '+++ Img '+ str(i) + ' is downloaded .'
					finally:
						pass

print 'All images have been downloaded!'
