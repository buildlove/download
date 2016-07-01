#-*- coding:utf8 -*-
import urllib
import os

localPath = os.getcwd()
#不存在该文件就创建该文件
def opendir(filePath):
  if not os.path.isdir(filePath):
    os.mkdir(filePath)

#下载进度条回调
def callbackfunc(blocknum, blocksize, totalsize):
    percent = 100.0 * blocknum * blocksize / totalsize
    if percent > 100:
        percent = 100
    print "%.2f%%" % percent

#下载只存在url的txt文件
def onlyUrl(filePath):
  opendir('test')
  filePath = localPath + filePath
  messages = open(filePath).read().split('\n')
  count = 1
  for message in messages:
    if message:
      local = localPath + '/test/index' + str(count) + '.html'
      urllib.urlretrieve(message, local, callbackfunc)
      count += 1
      print u"addPage: " + message

def onlyAll(filePath):
  filePath = localPath + filePath
  messages1 = open(filePath).read().split('\n')
  count = 1
  for message in messages1[1:]:
    if message:
      arr = message.split(',')
      urllib.urlretrieve(arr[0], arr[1], callbackfunc)
      print u"下载存在路径url的txt文件：" + arr[0]

# onlyAll('/message1.txt')
onlyUrl('/message.txt')