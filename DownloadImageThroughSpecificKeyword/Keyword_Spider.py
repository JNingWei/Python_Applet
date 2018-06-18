# coding:utf-8

import os
import re
import urllib
import shutil
import requests
import itertools


# ------------------------ Hyperparameter ------------------------

ROOT_DIR = '/Users/megvii/Desktop/'

# 存放所下载图片的文件夹
SAVE_DIR = ROOT_DIR + 'Keyword_Spider'
# 如有多个关键字，需用空格进行分隔
KEYWORD = '面包'
# 保存后的图片格式
SAVE_TYPE = '.jpg'
# 需要下载的图片数量
MAX_NUM = 100


# ------------------------ URL decoding ------------------------
str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}

char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}
char_table = {ord(key): ord(value) for key, value in char_table.items()}

# ------------------------ Encoding ------------------------
def decode(url):
    for key, value in str_table.items():
        url = url.replace(key, value)
    return url.translate(char_table)

# ------------------------ Page scroll down ------------------------
def buildUrls():
    word = urllib.parse.quote(KEYWORD)
    url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=60"
    urls = (url.format(word=word, pn=x) for x in itertools.count(start=0, step=60))
    return urls

re_url = re.compile(r'"objURL":"(.*?)"')

# ------------------------ Get imgURL ------------------------
def resolveImgUrl(html):
    imgUrls = [decode(x) for x in re_url.findall(html)]
    return imgUrls

# ------------------------ Download imgs ------------------------
def downImgs(imgUrl, dirpath, imgName):
    filename = os.path.join(dirpath, imgName)
    try:
        res = requests.get(imgUrl, timeout=15)
        if str(res.status_code)[0] == '4':
            print(str(res.status_code), ":", imgUrl)
            return False
    except Exception as e:
        print(e)
        return False
    with open(filename + SAVE_TYPE, 'wb') as f:
        f.write(res.content)

# ------------------------ Check save dir ------------------------
def mkDir():
    try:
        shutil.rmtree(SAVE_DIR)
    except:
        pass
    os.makedirs(SAVE_DIR)


# ------------------------ Main ------------------------
if __name__ == '__main__':

    print('\n\n', '= = ' * 25, ' Keyword Spider ', ' = =' * 25, '\n\n')
    mkDir()
    urls = buildUrls()
    idx = 0
    for url in urls:
        html = requests.get(url, timeout=10).content.decode('utf-8')
        imgUrls = resolveImgUrl(html)
        # Ending if no img
        if len(imgUrls) == 0:
            break
        for url in imgUrls:
            downImgs(url, SAVE_DIR, '{:>05d}'.format(idx + 1))
            print('  {:>05d}'.format(idx + 1))
            idx += 1
            if idx >= MAX_NUM:
                break
        if idx >= MAX_NUM:
            break
    print('\n\n', '= = ' * 25, ' Download ', idx, ' pic ', ' = =' * 25, '\n\n')
