import urllib.request, urllib.parse, urllib.error
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

url = "http://164.100.158.135/ExamResults/ExamResultsmain.htm"
html = urlopen(url).read()
#print(html)
soup = BeautifulSoup(html, 'html.parser')
print(soup)
