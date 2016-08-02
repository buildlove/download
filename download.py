#-*-coding=utf8-*-
import sys
import urllib
import os
import re
import time
from PyQt4 import QtGui, QtCore
localPath = os.getcwd()
ISOTIMEFORMAT="%Y-%m-%d %X"   #设置时间格式

class OpenFile(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        QtGui.QMainWindow.__init__(self)
        self.resize(600, 600)                    #窗口大小
        self.setWindowTitle('OpenFile')          #窗口title
        self.center()                            #窗口位置
        self.textEdit = QtGui.QTextEdit()        #文本
        self.statusTxt(self.textEdit)            #设置状态栏文本
        self.setWindowIcon(QtGui.QIcon('icons/news.png')) #设置窗口图标
        self.menubar()                           #菜单栏

    # 状态栏
    def statusTxt(self, text):
        self.setCentralWidget(text)              #设置状态栏文本
        self.statusBar()                         #状态栏
        self.setFocus()

    # 菜单栏
    def menubar(self):
        #子菜单
        esc = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
        esc.setShortcut('Ctrl+Q')
        esc.setStatusTip('exit the program')
        esc.connect(esc, QtCore.SIGNAL('triggered()'), QtGui.qApp, QtCore.SLOT('quit()'))

        opt = QtGui.QAction(QtGui.QIcon('icons/news.png'),'Open', self)  #图标
        opt.setShortcut('Ctrl+O')                                        #快捷键
        opt.setStatusTip('Open new file')                                #标题
        opt.connect(opt, QtCore.SIGNAL('triggered()'), self.readFile)    #opt部件绑定readFile函数
        #创建菜单栏，把exit作为子菜单加入菜单栏
        menubar = self.menuBar()
        File = menubar.addMenu('&File')
        File.addAction(opt)
        File.addAction(esc)

    # 下载进度条回调
    def callback(self, blocknum, blocksize, totalsize):
        percent = abs(100.0 * blocknum * blocksize / totalsize)
        if percent > 100:
            percent = 100
        print '%.2f%%' % percent

    def uniqList(self, ids):
        news_ids = []
        for ids in ids:
            if ids not in news_ids:
                news_ids.append(ids)
        return news_ids

    # 读取文件
    def readFile(self):
        if not os.path.isdir('test'):
            os.mkdir('test')
        self.textEdit.append(u"正在下载....")
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file', './') or ''
        File = open(filename, 'r')
        data = File.read()
        Urltxt = self.uniqList(data.split('\n'))
        count = 0
        start_page = time.clock()
        self.textEdit.clear()
        Urltxt = filter(None,Urltxt)
        for message in Urltxt:
            # self.textEdit.append(message) #加入textEdit组件，setText()是替换所有text
            print '1'
            x,y = os.path.split(message)
            if y:
                local = localPath + '/test/' + y
            else:
                local = localPath + '/test/index' + str(count) + '.html'
            urllib.urlretrieve(message, local, self.callback)
            count += 1
        end_page = time.clock()
        self.textEdit.append(u"共有任务数: %s, 用时: %f" % (str(count), (end_page - start_page)))

    # 移动主窗口到屏幕中心
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2,(screen.height()-size.height())/2)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    cd = OpenFile()
    cd.show()
    sys.exit(app.exec_())


