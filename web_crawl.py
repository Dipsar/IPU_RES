import urllib.request, urllib.parse, urllib.error

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

fwrite = open('pdf_links_.txt', 'a')
fread = open('pdf_links_.txt', 'r')
line= list()
#    line = l
#    for l in fread:

url = "http://ipu.ac.in/exam_results.php"
html = urlopen(url).read()

soup = BeautifulSoup(html, 'html.parser')

tags = soup('a')

for tag in tags:
    h = tag.get('href', '')
    if h.endswith('.pdf') and (re.search('B.Tech', h) or re.search('b.tech', h)  or re.search('B.tech', h) or re.search('BTECH', h)):
        line.append(h)

for i in line:
    print(i)
    if re.search('/public/', i):
        i = 'http://ipu.ac.in' + i

    fwrite.write(i+"\n")
fwrite.close()
