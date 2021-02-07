import sys
import os
import shutil
import pathlib
from pathlib import Path
import glob
import re

#############################################################
print(f'\ncwd:     {os.path.dirname(__file__)}\n')

PATH = sys.argv[1]
if not os.path.exists(PATH):
    print(f'specified folder does not exist')
    sys.exit()
os.chdir(PATH)

print(f'Folder location:     {os.getcwd()}')

# 'tmp/**\\' , recursive=True
dirname = [os.path.basename(p.rstrip(os.sep)) for p in glob.iglob('**' + os.sep)]

print(f'list of directory name:     {dirname}\n')

path_and_dirname = []

for i in dirname:
    sublist =[]
    for j in range(2):
        sublist.append(i)
    path_and_dirname.append(sublist)

folder_len = len(path_and_dirname)

print(f'number of directories:     {folder_len}\n')

#############################################################
def moveFolder(folder, dst):
    os.makedirs(dst, exist_ok=True)
    if not Path(dst + '/' + folder).exists():
        shutil.move(folder, dst)

#############################################################
target = '(?<=\[).+?(?=\])'
pattern = re.compile(target)

moved = 0
delete = []

for i in range(folder_len):
    m = pattern.search(path_and_dirname[i][0])
    if m: #include[]
        path_and_dirname[i][1] = m.group()
    else: #not include[]
        moveFolder(path_and_dirname[i][0], 'Unsorted/')
        delete.append(i)
        moved += 1
    #end condition
    if folder_len - (i + moved) <= 1:
        break

#正順(プラス方向)にリストの要素をdeleteするとインデックスが一つずつずれていってしまうので逆順にリストを参照させる([::-1]と同じ)
for i in reversed(delete):
    del path_and_dirname[i]

net_folder_num = len(path_and_dirname)

print(f'path_and_dirname:        {len(path_and_dirname)}\n')
print(f'net_folder_num:        {net_folder_num}\n')

#############################################################
for i in range(net_folder_num):
    target = str(path_and_dirname[i][1])
    originalFolder = True
    print(f'target:     {target}')
    for j in range(i+1, net_folder_num):
        print(f'Folder name:     {path_and_dirname[j][1]}\n')
        if target in path_and_dirname[j][0]:
            if originalFolder:
                moveFolder(str(path_and_dirname[i][0]), 'Sorted/' + str(path_and_dirname[i][1]))
                originalFolder = False
            moveFolder(str(path_and_dirname[j][0]), 'Sorted/' + str(path_and_dirname[j][1]))
        else:
            continue
