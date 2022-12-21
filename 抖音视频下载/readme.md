# 抖音视频下载
## 1.视频url获取
  浏览器添加脚本运行“抖音合集视频下载.js”或者“抖音主页视频下载.js”，获取视频链接
## 2.安装you-get
  1. 由于单视频下载用的是you-get方式，需要先安装下you-get
  2. pip install you-get
## 命令行运行download.py
  1. 得到视频名称：python download.py -g
  2. 下载所需视频：python download.py -d
## 注意
  1. 由于多视频得到视频名称时速度较慢，耐心等待程序运行即可。
  2. python download.py -d下载过程中程序可能会终止，这是由于抖音服务器主动断开连接导致，可修改download.py中第47行“for i in range(0, len(urls)):”，将前面的0修改为中断视频之后的视频顺序即可。
  例如，程序在下载第23个视频时中断，修改代码为“for i in range(23, len(urls)):”。
  3. 修改完毕重新运行python download.py -d即可。
