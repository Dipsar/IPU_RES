import urllib.request, urllib.parse, urllib.error

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import time
while(1):
    fwrite = open('pdf_links_.txt', 'a')
    fread = open('pdf_links_.txt', 'r')
    line= list()
    #    line = l
    #    for l in fread:
    line = list()
    for l in fread:
        line.append(l)
    #print (line)
    url = "http://164.100.158.135/ExamResults/ExamResultsmain.htm"

    html = urlopen(url).read()

    soup = BeautifulSoup(html, 'html.parser')

    tags = soup('a')

    for tag in tags:
        h = tag.get('href', '')
        if h.endswith('.pdf') and (re.search('B.Tech', h) or re.search('b.tech', h)  or re.search('B.tech', h) or re.search('BTECH', h)):
            if not h.startswith('http'):
                if h.startswith('/ExamResults'):
                    h = 'http://164.100.158.135' + h
                else:
                    h = 'http://164.100.158.135/ExamResults/' + h
            h = h + '\n'
            flag = 1
            if h  not in line:
               fwrite.write(h)
               print(h)
               flag = 0
    if flag != 0:
        print("No new Record")
    fwrite.close()
    time.sleep(30)
