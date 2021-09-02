#_*_ coding:utf-8 _*_

import re


with open(u'book.txt','r') as f:
    book = f.read()

# book = book.decode('utf-8','ignore')

subbook = re.sub(r'<.*?>.*?</.*?>','',book,)

print subbook




