# 抖音视频下载
## 1.视频url获取
  1. 浏览器添加脚本运行“抖音合集视频下载.js”或者“抖音主页视频下载.js”，获取视频链接
  2. 运行js脚本后，浏览器会下载一个output.txt文件。文件包含所需的视频链接
## 2.安装you-get
  1. 由于单视频下载用的是you-get方式，需要先安装下you-get
  2. pip install you-get
## 3.安装moviepy
  1. 使用mouviepy库来进行视频的合并
  2. pip install moviepy
  3. 在程序测试中发现，不同帧宽和帧高的视频合并过程中会错误，错误表现为视频的后半段会只有声音正常但是画面不正常，为了解决这个问题，仍需要ffmpeg来进行一个视频帧宽和帧高的调整
## 4. 安装ffmpeg
  1. ffmpeg下载地址：https://ffmpeg.org/download.html
  2. 下载完成后解压打开ffmpeg文件夹，将bin目录(也就是ffmpeg.exe所在目录)添加到环境变量中
  3. 测试：ffmpeg -h
## 5.安装opencv-python
  1. 为了自动化统计视频列表中常用帧宽和帧高以及其余不同帧宽和帧高的视频路径，需要安装一下opencv-python库来实现这个目标
  2. pip install opencv-python
  3. 如果按照之后发现cv2并没有相关函数，可以下载编译好的opencv
  4. 地址：https://www.lfd.uci.edu/~gohlke/pythonlibs/
  5. 选择对应python版本进行下载。
  6. 安装(例)：pip install opencv_python-4.5.5-cp39-cp39-win_amd64.whl

## 命令行运行download.py
  1. 得到视频名称：python download.py -g
  2. 下载所需视频：python download.py -d
  3. 统计视频信息：python download.py -i
  4. 转换帧宽帧高：python download.py -c
  5. 批量视频合并：python download.py -m
## 注意
  1. 由于多视频得到视频名称时速度较慢，耐心等待程序运行即可。
  2. python download.py -d下载过程中程序可能会终止，这是由于抖音服务器主动断开连接导致，可修改download.py中第47行“for i in range(0, len(urls)):”，将前面的0修改为中断视频之后的视频顺序即可。
  例如，程序在下载第23个视频时中断，修改代码为“for i in range(23, len(urls)):”。
  3. 修改完毕重新运行python download.py -d即可。
  4. 程序运行中会产生三个文件夹和几个过程中文件txt。
