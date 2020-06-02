import os

rootdir = './../../../Downloads/haoshangrong_step2/'
dirs = os.listdir(rootdir)
for odir in dirs:
    num =0 
    if odir=='.DS_Store':
        continue
    for fl in os.listdir( os.path.join(rootdir, odir) ):
        if fl.endswith(' (1).jpg'):
            num+=1
            print(num)
            os.remove(os.path.join(rootdir, odir,fl))
print('ok')
pass