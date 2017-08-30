import PyPDF2
import sqlite3
import re


pdfres = PyPDF2.PdfFileReader(open('028_ECE_4_SEM.pdf', 'rb'))
pg = pdfres.getNumPages()
j = 0
while j < pg:

    res = pdfres.getPage(j)
    txt = res.extractText()
    if txt.startswith('(SCHEME OF EXAMINATIONS)'): continue
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
    line_idx = [i for i, item in enumerate(line) if item.startswith('RTSID:')] #finding all the unnecessary data

    del line[:line_idx[0]+1] #removing all the unnecessary data
    #finding positions of roll no
    stud = list()
    for l in line:
        roll_idx = [i for i, item in enumerate(line) if re.search('^\d{11}', item)]
    #dividing student data
    a = 0
    b = 1
    for l in roll_idx:
        x = roll_idx[a]
        if a == len(roll_idx)-1 :
            y = len(line)
        else :
            y = roll_idx[b]
        stud.append(line[x:y])
        a = a + 1
        b = b + 1
    for s in stud:
        print (s)
