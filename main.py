#!/usr/bin/env python3

from bs4 import BeautifulSoup
import re
import os
import os.path as path
import tempfile
import shutil
import json

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

def build_FANUC_ERR(ep):

    title = ''
    cause = ''
    remedy = ''
    
    try:
        title = ep[0].text
        cause = ep[1].text
        remedy= ep[2].text
    except:
        print ('somthing went wrong with:{}'.format(ep))

    til_tmp = None
    cau_tmp = None
    rem_tmp = None
    
    try:
        til_tmp = re.search('(.*)-(\d*) (\w*) (.*)', title)
        #print (til_tmp.group(0))
    except Exception as e:
        print ('TITLE: ' + str(e))

    try:
        cau_tmp = re.search('(cause:) (.*)', cause, re.I)
        #print (cau_tmp.group(0))
    except Exception as e:
        print ('CAUSE: ' + str(e))

    try:
        rem_tmp = re.search('(remedy:) (.*)', remedy, re.I)
        #print (rem_tmp.group(0))
    except Exception as e:
        print ('REMEDY: ' + str(e))
        
    tit=None
    no=None
    ty=None
    bri=None
    cau=None
    rem=None
    
    try:
        til = til_tmp.group(1)
    except Exception as e:
        print ('No Title ' + str(e))
        
    try:
        no = til_tmp.group(2)
    except Exception as e:
        print ('no No. ' + str(e))

    try:
        ty = til_tmp.group(3)
    except Exception as e:
        print ('no type' + str(e))
        
    try:
        bri = til_tmp.group(4)
    except Exception as e:
        print ('No brief ' + str(e))

    try:
        cau = cau_tmp.group(2)
    except Exception as e:
        print ('No cau ' + str(e))

    try:
        rem = rem_tmp.group(2)
    except Exception as e:
        print ('No rem ' + str(e))  

    return {'title': til, 'number': no, 'type':ty, 'desc':bri, 'cause':cau, 'remedy':rem}

error_list=list()

for doc in get_documents():
    name = None
    with create_temporary_copy(doc) as temp:
        name = temp.name

        soup = BeautifulSoup(temp,'lxml')

        entries = [errormessage for errormessage in soup.find_all("div", attrs={'class':'pyton'})]

        for entry in entries:
            p_tags = [p for p in entry.find_all('p')]

            fe = build_FANUC_ERR(p_tags)
            error_list.append(fe)

with open('./asset/fanuc_error.json', 'w') as outfile:
    json.dump(error_list, outfile)
