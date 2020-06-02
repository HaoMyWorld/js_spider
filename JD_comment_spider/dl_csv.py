import wget
import csv
import os
import shutil

csvdir = './生鲜_medium.csv'
filename = os.path.basename(csvdir).split('.')[0]
savedir = './' + filename

def isExist(savedpath):
    isExists = os.path.exists(savedpath)
    if not isExists:
        os.makedirs(savedpath)
        print('path of %s is build'%(savedpath))
    else:
        shutil.rmtree(savedpath)
        os.makedirs(savedpath)
        print('path of %s already exist and rebuild'%(savedpath))
isExist(savedir)
with open(csvdir) as f:
    lines = f.readlines()
    for line in lines:
        linestr = line.strip()
        lineurllist = linestr[linestr.find('https:'):].split(' ')
        for url in lineurllist:
            wget.download(url, out= savedir)
    print('ok')