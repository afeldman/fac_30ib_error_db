#!/usr/bin/env python3

from bs4 import BeautifulSoup
import os
import os.path as path
import tempfile
import shutil

def get_documents(rootdir = './asset'):
    document_list = list()
    
    for dirName, subdirList, fileList in os.walk(rootdir):
        for fname in fileList:
            document_list.append(path.join(dirName,fname))

    return document_list

#for file safty.
# make a copy and work with the copy
def create_temporary_copy(src):
    temp_dir = tempfile.gettempdir()

    tf = tempfile.TemporaryFile(mode='r+b',
                                prefix='__',
                                suffix='.tmp')

    with open(src,'r+b') as f:
        shutil.copyfileobj(f,tf)

    tf.seek(0) 
    return tf

def get_plain_text(soup):
    plain_text = ''
    lines = soup.findall('br')
    for line in lines.findAll('br'):
        plain_text+=line
    return plain_text

class FANUC_ERROR:

    def __init__(self, label ):
        self.titel = label
       

for doc in get_documents():
    name = None
    with create_temporary_copy(doc) as temp:
        name = temp.name

        soup = BeautifulSoup(temp,'html.parser')
        entries = [br.next for br in soup.find_all('p')]

        print (entries)
  
