import PyPDF2
import sqlite3
import re

pdfres = PyPDF2.PdfFileReader(open('028_ECE_4_SEM.pdf', 'rb'))
res = pdfres.getPage(3)
txt = res.extractText()
#print(txt)
#conn = sqlite3.connect('result.sqlite')
#cur = conn.cursor()

#cur.executescript('''
#DROP TABLE IF EXISTS sdata;

#CREATE TABLE sdata (
#    roll INTEGER NOT NULL PRIMARY KEY UNIQUE,
#    name TEXT
#    sid INTEGER
#    scheme_id INTEGER
#);
#''')
line = txt.split('\n')
while '' in line:
    line.remove('')
line_idx = [i for i, item in enumerate(line) if item.startswith('RTSID:')]

del line[:line_idx[0]+1]
print(line)
    #line.remove(l)
#for l in line:
#print(line)
