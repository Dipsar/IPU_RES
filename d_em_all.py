import urllib.request, urllib.parse, urllib.error
from urllib.request import urlopen
import urllib
links = open('pdf_links_.txt', 'r')
import os

def url_fix(s, charset='utf-8'):
    #if isinstance(s, unicode):
    #    s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urllib.parse.urlsplit(s)
    path = urllib.parse.quote(path, '/%')
    qs = urllib.parse.quote_plus(qs, ':&=')
    return urllib.parse.urlunsplit((scheme, netloc, path, qs, anchor))
count = 0
for link in links:
    #http://ipu.ac.in/public/ExamResults/2016/140716/8th%20Sem_128_B.Tech.(ECE)_USS_Final%20Result_MJ2016.pdf
    #print(url_fix(link))
    nm = 'res_pdf'
    nm = os.path.join(nm, str(count) + '.pdf' )
    count = count + 1
    print(nm)
    print(url_fix(link.strip()))
    urllib.request.urlretrieve(url_fix(link.strip()), nm)
