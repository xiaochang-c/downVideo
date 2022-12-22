import os
import subprocess
import sys
from you_get import common as you_get
import argparse
from moviepy.editor import VideoFileClip, concatenate_videoclips
import cv2

# 获取当前目录
current_directory = os.getcwd()
# video_directory:存放下载视频的路径    new_video_directory:存放转换帧宽和帧高视频的路径    txt_directory:存放过程中产生的txt文件
video_directory = os.path.join(current_directory, "video")
new_video_directory = os.path.join(current_directory, 'new_video')
txt_directory = os.path.join(current_directory, 'txt')


def create_directory(directory):
    # 如果video文件夹不存在，则创建该文件夹
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except FileExistsError:
            # 忽略FileExistsError异常
            pass


create_directory(video_directory)
create_directory(new_video_directory)
create_directory(txt_directory)

# 从文本中获取所有抖音合集视频的链接url
with open('txt/output.txt', 'r') as f:
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
    with open('txt/names.txt', 'w') as fN:
        for j in range(len(names)):
            fN.write(names[j] + "\n")


# get_names()


def download():
    with open('txt/names.txt', 'r') as f:
        names = f.readlines()
    # 下载地址
    for i in range(0, 1):
        print(names[i])
        print(urls[i])
        sys.argv = ['you-get', '-o', video_directory, '-O', names[i].strip(), urls[i]]
        you_get.main()


# download()


def get_video_info():
    video_paths = []
    # 遍历文件名
    filenames = os.listdir(video_directory)
    filenames.sort(key=lambda x: int(x.split('-')[0]))
    for filename in filenames:
        # 分离文件名和扩展名
        name, extension = os.path.splitext(filename)
        if extension == '.mp4':
            video_paths.append(os.path.join(video_directory, filename))
    # 将所有文件路径写入list.txt文件中,用于ffmpeg命令行合并视频，但实测发现批量视频合并ffmpeg效果并不好，但这段代码没有删除，感兴趣者可以尝试
    with open('txt/list.txt', 'w') as flist:
        for path in video_paths:
            flist.write("file \'" + path + "\'\n")
    # 统计所有视频的帧高和帧宽，输出最常见的帧宽与帧高，并将不常见帧宽与帧高的视频路径写入frame.txt文件中
    # 创建一个 字典，用于记录每个帧宽和帧高 的出现次数
    frame_size_counts = {}
    # 遍历所有视频文件
    for path in video_paths:
        # 打开视频文件
        video = cv2.VideoCapture(path)
        # 获取帧宽与帧高
        frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_size = (frame_width, frame_height)
        if frame_size in frame_size_counts:
            frame_size_counts[frame_size] += 1
        else:
            frame_size_counts[frame_size] = 1
        video.release()
    # 查找出现此时最多的帧宽与帧高
    most_common_frame_size = max(frame_size_counts, key=frame_size_counts.get)
    print("most common frame size: ", most_common_frame_size)
    print("number of occurrences: ", frame_size_counts[most_common_frame_size])
    # 打开frame.txt文件，准备写入数据
    with open("txt/frame.txt", "w") as file:
        file.write(str(most_common_frame_size[0]) + "\n")
        file.write(str(most_common_frame_size[1]) + "\n")
        for video_path in video_paths:
            video = cv2.VideoCapture(video_path)
            frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            frame_size = (frame_width, frame_height)
            if frame_size != most_common_frame_size:
                file.write(video_path + "\n")
            video.release()
    return video_paths


# 视频帧宽和帧高转换，方便后面视频合并
def convert_video_rate():
    with open('txt/frame.txt') as fc:
        width = int(fc.readline().strip())
        height = int(fc.readline().strip())
        video_paths = fc.readlines()
    for path in video_paths:
        new_video_path = os.path.join(new_video_directory, path.split('\\')[-1].strip())
        subprocess.run(['ffmpeg', '-i', path.strip(), '-vf', 'scale={}:{}'.format(width, height), new_video_path])


def merge_video():
    video_paths = get_video_info()
    clips = [VideoFileClip(path) for path in video_paths[-2:]]
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile('output.mp4')


# merge_video()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--getName', action='store_true',
                        help="得到抖音视频合集的视频名称，并按照合集中视频顺序进行一个重命名")
    parser.add_argument('-d', '--download', action='store_true',
                        help='下载视频，并根据names.txt对下载的视频进行一个重命名')
    parser.add_argument('-i', '--info', action='store_true',
                        help="得到所有视频的帧宽与帧高，统计使用最多的帧宽与帧高，将其他不常用的帧宽与帧高的视频路径写入frame.txt文件中")
    parser.add_argument('-c', '--convert', action='store_true',
                        help="将所有不常见帧宽和帧高的视频转换为常见帧宽和帧高视频")
    parser.add_argument('-m', '--mergeVideo', action='store_true',
                        help="批量视频合并，默认路径为video文件夹里面的视频")
    args = parser.parse_args()
    if args.getName:
        get_names()
    if args.download:
        download()
    if args.info:
        get_video_info()
    if args.convert:
        convert_video_rate()
    if args.mergeVideo:
        merge_video()
