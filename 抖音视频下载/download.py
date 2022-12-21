import os
import subprocess
import sys
from you_get import common as you_get
import argparse

# 获取当前目录
current_directory = os.getcwd()
# 拼接出video文件夹的路径
video_directory = os.path.join(current_directory, "video")
# 如果video文件夹不存在，则创建该文件夹
if not os.path.exists(video_directory):
    try:
        os.makedirs(video_directory)
    except FileExistsError:
        # 忽略FileExistsError异常
        pass
# 输出video文件夹的路径
# print(video_directory)

# 从文本中获取所有抖音合集视频的链接url
with open('output.txt', 'r') as f:
    urls = f.readlines()[0].split(',')


def get_names():
    names = []
    # 循环输入每一条url，得到每条url链接视频的名称并重新命名
    for i in range(len(urls)):
        output = subprocess.check_output(['you-get', '-i', urls[i]]).decode('utf-8')
        names.append(str(i) + '-' + output.split('#')[0][36:].strip())
    for i in range(len(names)):
        print(names[i])
    # 输出所有视频的name,保存在names.txt中
    with open('names.txt', 'w') as fN:
        for j in range(len(names)):
            fN.write(names[j] + "\n")


# get_names()


def download():
    with open('names.txt', 'r') as f:
        names = f.readlines()
    # 下载地址
    for i in range(0, len(urls)):
        print(names[i])
        print(urls[i])
        sys.argv = ['you-get', '-o', video_directory, '-O', names[i].strip(), urls[i]]
        you_get.main()


# download()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--getName', action='store_true',
                        help="得到抖音视频合集的视频名称，并按照合集中视频顺序进行一个重命名")
    parser.add_argument('-d', '--download', action='store_true',
                        help='下载视频，并根据names.txt对下载的视频进行一个重命名')
    args = parser.parse_args()
    if args.getName:
        get_names()
    if args.download:
        download()
