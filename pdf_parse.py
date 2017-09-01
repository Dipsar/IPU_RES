import PyPDF2
import sqlite3
import re

conn = sqlite3.connect('student_dat.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS sdata;
DROP TABLE IF EXISTS ex_scheme;

CREATE TABLE sdata (
    roll INTEGER NOT NULL PRIMARY KEY UNIQUE,
    name TEXT
    --sid INTEGER,
    --scheme_id INTEGER
);
CREATE TABLE ex_scheme (
    paper_id INTEGER NOT NULL PRIMARY KEY UNIQUE,
    code TEXT,
    subject TEXT,
    credit INTEGER,
    type TEXT,
    minor INTEGER,
    major INTEGER,
    sem INTEGER
);
''')
#finding exam scheme
def exam(line):
    line_idx = [i for i, item in enumerate(line) if item.startswith('Pass Marks')]
    del line[:line_idx[0]+1]
    sr_idx = [i for i, item in enumerate(line) if re.search('^\d{22}', item)]
    for j in sr_idx:
        try:
            del line[j]
        except:
            pass
    print(line)
#    for i in line_n:
#        print (i)
#function to check data and save it to sql database
def check_data(dat, n):
    if not (re.search("^\d{11}",dat[0]) and re.search("^SID: \d{12}",dat[2]) and re.search("^SchemeID: \d{12}",dat[3])): #checks the values of roll no nd ol
        return n
    roll_no = int(re.findall("\d{11}", dat[0])[0])
    name = dat[1]
    #sid = int(re.findall("\d+", dat[2])[0])
    #scheme_id = int(re.findall("\d+", dat[3])[0])
    #print(name, roll_no[0], sid[0], scheme_id[0])
    cur.execute('''INSERT OR IGNORE INTO sdata (roll, name, sid, scheme_id) VALUES (?, ?, ?, ?)''',(roll_no, name, sid, scheme_id))
    conn.commit()
    for l in dat:
        sub = [i for i, item in enumerate(dat) if re.search('^.?\d{5}\(\d\)$', item)] #finding indices of all the subjects
    subs = dict()
    for l in sub:
        mark = dat[l+1].split()
        if len(mark) != 2:
            del mark[:]
            mark.append(dat[l+1][0])
            mark.append(dat[l+1][1])
        subs[re.findall("\d{5}",dat[l])[0]] = mark #creating dictionary of subject and its respective internal and external marks
    for key in subs:
        print(key,subs[key])


pdfres = PyPDF2.PdfFileReader(open('028_ECE_4_SEM.pdf', 'rb'))
pg = pdfres.getNumPages()
j = 0
count = 0
while j < 1:

    try:
        res = pdfres.getPage(j)
    except:
        print("Done!")
    j = j + 1
    txt = res.extractText()
    line = txt.split('\n')
    while '' in line:
        line.remove('')

    if txt.startswith('(SCHEME OF EXAMINATIONS)'):
        exam(line)
        continue
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
        #print (s)
        err = check_data(s,count)
        count = count + 1
print (len(stud[0]),count)
