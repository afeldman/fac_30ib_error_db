# Import the os module, for the os.walk function
import os
import os.path
import fileinput

# Set the directory you want to start from
rootDir = './asset/'
for dirName, subdirList, fileList in os.walk(rootDir):
    for fname in fileList: #loop over the file list
        print ('process file %s' % fname)
        for line in fileinput.input(os.path.join(dirName,fname), inplace=1):
            print line.replace('<p>________________________________________________________________</p>', '<br />'),
