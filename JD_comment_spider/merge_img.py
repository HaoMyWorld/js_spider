"""用python将不同文件夹下的图片合并"""

# # 导入相应的包
import os
import shutil

# print('输入格式：E:/myprojectnew/jupyter/整理文件夹/示例')
# path = input('请输入原始文件夹路径：')
# new_path = input('请输入你想复制图片的新文件存储路径：')

# for root, dirs, files in os.walk(path):
#         for i in range(len(files)):
#             # print(files[i])
#             if (files[i][-3:] == 'jpg') or (files[i][-3:] == 'png') or (files[i][-3:] == 'JPG'):
#                 file_path = root + '/' + files[i]
#                 new_file_path = new_path + '/' + files[i]
#                 shutil.copy(file_path, new_file_path)

dir_all = './../../../Desktop/shengxian/'
dir_all_list = os.listdir(dir_all)
dir_all_list = [x for x in dir_all_list if not (x.endswith('.zip') or x.endswith('.DS_Store'))]
dir_all_list_ = [ os.path.join(dir_all, x) for x in dir_all_list ] 
dir_all_list__ = []
for i in dir_all_list_:
    for r,d,f in os.walk(i):
        dir_all_list__.extend([os.path.join(r,name) for name in d ])
dict__ = {}
for onedir in dir_all_list__:
    for r,d,f in os.walk(onedir):
        if '.DS_Store' in f:
            f.remove('.DS_Store')
        if len(f) == 0:
            # print(f)
            continue
        dict__[r] = f

savedir = './../../../Desktop/fresh_merge/'
for dict_key in list(dict__.keys()):
    for imgname in dict__[dict_key]:
        imgdir = os.path.join(dict_key,imgname)
        shutil.copy(imgdir, savedir)
pass