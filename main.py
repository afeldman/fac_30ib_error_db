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
    lines = soup.find("body")
    for line in lines.findAll('p'):
        line = replace_with_newlines(line)
        plain_text+=line
    return plain_text

for doc in get_documents():
    name = None
    with create_temporary_copy(doc) as temp:
        name = temp.name

        soup = BeautifulSoup(temp)
        print (get_plain_text(soup))
        
        # read all lines from the file
 #       i = 0
 #       for line in temp:
 #           print (i, line.strip())
 #           i += 1
