import PyPDF2
import sqlite3
import re
import os


errors = open('error.txt', 'w')
conn = sqlite3.connect('student_dat_test.sqlite')
cur = conn.cursor()

cur.executescript('''

CREATE TABLE IF NOT EXISTS sdata (
    roll INTEGER NOT NULL PRIMARY KEY UNIQUE,
    name TEXT
    --sid INTEGER,
    --scheme_id INTEGER
);
CREATE TABLE IF NOT EXISTS  ex_scheme (
    paper_id INTEGER NOT NULL PRIMARY KEY UNIQUE,
    code TEXT,
    subject TEXT,
    credit INTEGER,
    type TEXT,
    minor INTEGER,
    major INTEGER,
    pass_m INTEGER,
    sem INTEGER
);
''')

#finding exam scheme
def exam(line):
    _idx = [i for i, item in enumerate(line) if re.search('./Year',item) or re.search('SEMESTER',item)]
    try:
        _l = list()
        for l in _idx:
            _l.append(line[l])
        _idx = ''.join(_l)
        #_idx = line[_idx].split()
        sem = int(re.findall(' 0\d ',_idx)[0])
    except:
        errors.write(pdfpath + ':' + str(j) + '\n' + 'Sem not found\n')
        sem = None
        pass
    line_idx = [i for i, item in enumerate(line) if item.startswith('Pass Marks')]
    try:
        del line[:line_idx[0]+1]
    except:
        errors.write(pdfpath + ':' + str(j) + '\n' + 'Formatting wrong\n')
        return 0
    sr_idx = [i for i, item in enumerate(line) if re.search('^\d{2}$', item)]
    i = 0
    for k in sr_idx:
        try:
            del line[k-i]
        except:
            pass
        i = i + 1

    for l in line:
        sub_idx = [i for i, item in enumerate(line) if re.search('^\d{5,7}$', item)]
    sub = list()
    a = 0
    b = 1
    for l in sub_idx:
        x = sub_idx[a]
        if a == len(sub_idx)-1 :
            y = len(line)
        else :
            y = sub_idx[b]
        sub.append(line[x:y])
        a = a + 1
        b = b + 1

    for s in sub:
        #print(s)
        try:
            paper_id = int(s[0])
        except:
            errors.write(pdfpath+':'+str(j)+'\n'+s[0])
            continue
        code = s[1]
        subject = s[2]
        try:
            credit = int(s[3])
        except:
            errors.write(pdfpath+':'+str(j)+'\n'+s[3])
            continue
        type_ = s[4]
        if s[8] != '--':
            try:
                minor = int(s[8])
            except:
                errors.write(pdfpath+':'+str(j)+'\n'+s[8]+':minor')
                continue
        else:
            minor = None
        if s[9] != '--':
            try:
                major = int(s[9])
            except:
                errors.write(pdfpath+':'+str(j)+'\n'+s[9]+':major')
                continue
        else:
            major = None
        try:
            pass_m = int(s[11])
        except:
            errors.write(pdfpath+':'+str(j)+'\n'+s[11]+':pass_m')
            continue

        #print(paper_id, code, subject, credit, type_, minor, major, pass_m, sem)
        cur.execute('''INSERT OR IGNORE INTO ex_scheme (paper_id, code, subject, credit, type, minor, major, pass_m, sem) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',(paper_id, code, subject, credit, type_, minor, major, pass_m, sem))
        conn.commit()
        print("commited")
#function to check data and save it to sql database
def check_data(dat, n):
    if not (re.search("^\d{10,11}",dat[0]) and re.search("^SID: \d{12}",dat[2]) and re.search("^SchemeID: \d{12}",dat[3])): #checks the values of roll no nd ol
        return n
    roll_no = int(re.findall("\d{10,11}", dat[0])[0])
    name = dat[1]
    #sid = int(re.findall("\d+", dat[2])[0])
    #scheme_id = int(re.findall("\d+", dat[3])[0])
    #print(name, roll_no[0], sid[0], scheme_id[0])
    cur.execute('''INSERT OR IGNORE INTO sdata (roll, name) VALUES (?, ?)''',(roll_no, name))
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
        cur.execute('''CREATE TABLE IF NOT EXISTS ''' + '"' + str(roll_no) + '"' +''' (
            sub INTEGER NOT NULL PRIMARY KEY UNIQUE,
            internal TEXT,
            external TEXT
        )''')
        cur.execute('''REPLACE INTO ''' + '"' + str(roll_no) + '"' +''' (sub, internal, external) VALUES (?, ?, ?)''',(int(key),subs[key][0],subs[key][1]))
        conn.commit()
for files in os.listdir('./res_pdf'):
    global pdfpath
    pdfpath= os.path.join('res_pdf', files)
    pdfres = PyPDF2.PdfFileReader(open(pdfpath, 'rb'))
    pg = pdfres.getNumPages()
    global    j
    j = 0
    count = 0
    while j < pg:

        try:
            res = pdfres.getPage(j)
        except:
            print("Done!")
        j = j + 1
        txt = res.extractText()
        txt = txt.strip()
        #print(txt)
        line = txt.split('\n')
        while '' in line:
            line.remove('')
        print(line)
        if txt.startswith('(SCHEME OF EXAMINATIONS)'):
            if exam(line) == 0:
                break
            continue
        line_idx = [i for i, item in enumerate(line) if item.startswith('RTSID:')] #finding all the unnecessary data
        if len(line_idx) < 1: continue
        del line[:line_idx[0]+1] #removing all the unnecessary data
        #finding positions of roll no
        stud = list()
        for l in line:
            roll_idx = [i for i, item in enumerate(line) if re.search('^\d{10,11}', item)]
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
    #print (len(stud[0]),count)
errors.close()
