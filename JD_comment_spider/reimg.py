import os

# dir_1 = './../../../Downloads/haoshangrong/鸡排'
# dir_2 = './../../../Downloads/haoshangrong/鸡翅'

# dir_1_list = os.listdir(dir_1)
# dir_2_list = os.listdir(dir_2)

# res = set(dir_1_list) & set(dir_2_list)
# print(len(res))



dir_all = './../../../Desktop/shengxian/'
dir_all_list = os.listdir(dir_all)
dir_all_list = [x for x in dir_all_list if not (x.endswith('.zip') or x.endswith('.DS_Store'))]
dir_all_list_ = [ os.path.join(dir_all, x) for x in dir_all_list ] 
dir_all_list__ = []
for i in dir_all_list_:
    for r,d,f in os.walk(i):
        dir_all_list__.extend([os.path.join(r,name) for name in d ])

# res = [dit_t for onedir in dir_all_list__ for dit_t in os.listdir(onedir)]
# res_set = set(res)
dict__ = {}
dict__small = []
for onedir in dir_all_list__:
    for r,d,f in os.walk(onedir):
        if '.DS_Store' in f:
            f.remove('.DS_Store')
        if len(f) < 50:
            dict__small.append(r.split('/')[-1])
        if len(f) == 0:
            # print(f)
            continue
        dict__[r] = f
        # print('r,d,f')
allkeys = list(dict__.keys())
print(type(allkeys))
fewtxt = ' '.join(dict__small)
with open('./few.txt', 'a+') as fw:
    fw.writelines(fewtxt)

savetxt = './res.txt'
fw = open(savetxt,'a+')
for dict_key_index,dict_key in enumerate(allkeys):
    onelist = dict__[dict_key]
    oneset = set(onelist)
    oneset_l = len(oneset)
    anotherkeys = allkeys[dict_key_index+1:]
    for dict_j in anotherkeys:
        another_list = dict__[dict_j]
        anotherset_l = len(another_list)
        res =  oneset & set(another_list)
        l = len(res)
        if l<10:
            continue
        label = dict_key.split('/')[-1] + ' ' + dict_j.split('/')[-1] + ' ' + str(l) + '\n'
        # label = dict_key.split('/')[-1] + ' ' + str(oneset_l) + ' ' + dict_j.split('/')[-1] + ' ' + str(anotherset_l) + ' ' + str(l) + '\n'
        fw.writelines(label)
fw.close()
pass
