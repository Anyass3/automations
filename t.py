import string as s
import json
import random
from itertools import chain#from_iterable
'''
this is just ti help me automate adding users to and user post to my website
'''
path = '/home/abdullah/Projects/automation/'
file = open(path + 'notes.txt')
note=list(file)
splitted=note[0].split(' ')
splitted.__delitem__(0)
note[0]=' '.join(splitted)
#print(note)
file.close()
with open(path+'data/f_names.json', encoding='utf-8') as f:
    f_names=json.loads(f.read())
with open(path+'data/l_names.json', encoding='utf-8') as f:
    l_names=json.loads(f.read())
def paragraph(num=None):
    num = 1 if num == None else num
    paras=[]
    for i in  range(num):
        paras.append(random.choice(note))
    return paras
    
def sentence(i):
    p=paragraph()
    s=p[:i]
    return s

def words_from_para(num=None):
    paras=paragraph(num)
    words=[]
    for para in paras:
        para=list(para.strip())
        puncs=list(s.punctuation+'”“')
        for p in puncs:
            while p in para:
                para.remove(p)
        para=''.join(para)
        para = para.split(' ')
        para = [w for w in para if len(w)>3]
        for pr in para:
            for p in puncs:
                while p in pr:
                    para.remove(pr)
        words.append(para)
    words = list(chain.from_iterable(words))
    words = list(dict.fromkeys(words))
    return words
