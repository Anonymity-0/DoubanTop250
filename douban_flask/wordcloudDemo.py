# -*- coding = utf-8 -*-
# @Time:2021/3/31 20:17
# @Author:anonymity
# @File:wordcloudDemo.py
# @Software:PyCharm

import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import  numpy as np
import sqlite3

con = sqlite3.connect('douban.db')
cur = con.cursor()
sql = '''
    select inp from book
'''
data = cur.execute(sql)
text = ""

for item in data:
    text = text+item[0]

cur.close()
con.close()

cut = jieba.cut(text)
string = ' '.join(cut)
print(cut)

img = Image.open(r'.\static\assets\img\test.jpg')
img_array = np.array(img)
wc = WordCloud(
    background_color= 'white',
    mask = img_array,
    font_path="msyh.ttc"

)


fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')


plt.savefig(r'.\static\assets\img\word_book.png',dpi=600)