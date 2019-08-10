#-*- coding:utf-8 -*-

from  PyQt4.QtGui  import *
from  PyQt4.QtCore  import *
import sys,re
import urllib2
import argparse
import os
import random
import requests

reload(sys)
sys.setdefaultencoding("utf-8")

headers = {
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36",
   'Referer':'http://m.mzitu.com/15309'}

PIC=[".jpg",".JPG",".PNG",".png",".JPEG",".jpeg",".bmp",".BMP",".gif",".GIF"]




import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class SwitchBtn(QWidget):
    #信号
    checkedChanged = pyqtSignal(bool)
    def __init__(self,parent=None):
        super(QWidget, self).__init__(parent)

        self.checked = False
        self.bgColorOff = QColor(30, 30, 30)
        self.bgColorOn = QColor(0, 200, 0)

        self.sliderColorOff = QColor(100, 100, 100)
        self.sliderColorOn = QColor(100, 184, 255)

        self.textColorOff = QColor(143, 143, 143)
        self.textColorOn = QColor(255, 255, 255)

        self.textOff = "off"
        self.textOn = "on"

        self.space = 2
        self.rectRadius = 5

        self.step = self.width() / 50
        self.startX = 0
        self.endX = 0

        self.timer = QTimer(self)  # 初始化一个定时器
        self.timer.timeout.connect(self.updateValue)  # 计时结束调用operate()方法

        #self.timer.start(5)  # 设置计时间隔并启动

        self.setFont(QFont("Microsoft Yahei", 10))

        #self.resize(55,22)

    def updateValue(self):
        if self.checked:
            if self.startX < self.endX:
                self.startX = self.startX + self.step
            else:
                self.startX = self.endX
                self.timer.stop()
        else:
            if self.startX  > self.endX:
                self.startX = self.startX - self.step
            else:
                self.startX = self.endX
                self.timer.stop()

        self.update()


    def mousePressEvent(self,event):
        self.checked = not self.checked
        #发射信号
        self.checkedChanged.emit(self.checked)

        # 每次移动的步长为宽度的50分之一
        self.step = self.width() / 50
        #状态切换改变后自动计算终点坐标
        if self.checked:
            self.endX = self.width() - self.height()
        else:
            self.endX = 0
        self.timer.start(5)

    def paintEvent(self, evt):
        #绘制准备工作, 启用反锯齿
            painter = QPainter()



            painter.begin(self)

            painter.setRenderHint(QPainter.Antialiasing)


            #绘制背景
            self.drawBg(evt, painter)
            #绘制滑块
            self.drawSlider(evt, painter)
            #绘制文字
            self.drawText(evt, painter)

            painter.end()


    def drawText(self, event, painter):
        painter.save()

        if self.checked:
            painter.setPen(self.textColorOn)
            painter.drawText(0, 0, self.width() / 2 + self.space * 2, self.height(), Qt.AlignCenter, self.textOn)
        else:
            painter.setPen(self.textColorOff)
            painter.drawText(self.width() / 2, 0,self.width() / 2 - self.space, self.height(), Qt.AlignCenter, self.textOff)

        painter.restore()


    def drawBg(self, event, painter):
        painter.save()
        painter.setPen(Qt.NoPen)

        if self.checked:
            painter.setBrush(self.bgColorOn)
        else:
            painter.setBrush(self.bgColorOff)

        rect = QRect(0, 0, self.width(), self.height())
        #半径为高度的一半
        radius = rect.height() / 2
        #圆的宽度为高度
        circleWidth = rect.height()

        path = QPainterPath()
        path.moveTo(radius, rect.left())
        path.arcTo(QRectF(rect.left(), rect.top(), circleWidth, circleWidth), 90, 180)
        path.lineTo(rect.width() - radius, rect.height())
        path.arcTo(QRectF(rect.width() - rect.height(), rect.top(), circleWidth, circleWidth), 270, 180)
        path.lineTo(radius, rect.top())

        painter.drawPath(path)
        painter.restore()

    def drawSlider(self, event, painter):
        painter.save()

        if self.checked:
            painter.setBrush(self.sliderColorOn)
        else:
            painter.setBrush(self.sliderColorOff)

        rect = QRect(0, 0, self.width(), self.height())
        sliderWidth = rect.height() - self.space * 2
        sliderRect = QRect(self.startX + self.space, self.space, sliderWidth, sliderWidth)
        painter.drawEllipse(sliderRect)

        painter.restore()







#*******************************************************************
#*******************************************************************
#***************************布局类**********************************
#*******************************************************************
#*******************************************************************
class graphicsView(QGraphicsView):
    def __init__(self,parent=None):
        super(graphicsView,self).__init__(parent)
        self._parent=parent
        self.zoomscale=1
        self.pos=0
        
    
    def read_txt(self,path):
        mt=[]
        f=open(path,'r')
        for t in f.readlines():
            mt.append(t)
        f.close()
        return mt
    def mouseDoubleClickEvent(self,event):
        try:
                path="data.txt"
                #if event.button()==Qt.RightButton:
                #drag = QDrag()
                mt=self.read_txt(path)
                self._parent._tree.zoomscale=1
                url=mt[random.randrange(0,len(mt))]
                url=url.replace("\n","")
                self.pos+=1
                self._parent.pic_address.setText(url)
                
   
                request =  urllib2.Request(url, headers=headers)
                response = urllib2.urlopen(request,timeout=2)
                                       
                self.image=QPixmap()
                
                self.image.loadFromData(response.read())

                
                self.graphicsView= QGraphicsScene()            
                self._parent._tree.item = QGraphicsPixmapItem(self.image)
                self._parent._tree.item.setFlag(QGraphicsItem.ItemIsMovable)  
                self._parent._tree.graphicsView.addItem(self._parent._tree.item)

                self._parent._tree.setAlignment(Qt.AlignCenter)
                if self.image.width()!=500:
                    try:
                        self._parent._tree.item.setScale(400.0/self.image.width())
                    except:
                        self._parent._tree.item.setScale(0.7)
                self._parent._tree.setScene(self.graphicsView)
                #drag.exec_() #exec()函数并不会阻塞主函数
        except Exception as e:
            print e
    def refresh_pic(self):
        try:
            if self._parent.switchBtn.checked ==True:
                path="data.txt"
                #if event.button()==Qt.RightButton:
                #drag = QDrag()
                mt=self.read_txt(path)
                self._parent._tree.zoomscale=1
                url=mt[random.randrange(0,len(mt))]
                url=url.replace("\n","")
                self.pos+=1
                self._parent.pic_address.setText(url)
                
   
                request =  urllib2.Request(url, headers=headers)
                response = urllib2.urlopen(request,timeout=2)
                                       
                self.image=QPixmap()
                
                self.image.loadFromData(response.read())

                
                self.graphicsView= QGraphicsScene()            
                self._parent._tree.item = QGraphicsPixmapItem(self.image)
                self._parent._tree.item.setFlag(QGraphicsItem.ItemIsMovable)  
                self._parent._tree.graphicsView.addItem(self._parent._tree.item)

                self._parent._tree.setAlignment(Qt.AlignCenter)
                if self.image.width()!=500:
                    try:
                        self._parent._tree.item.setScale(400.0/self.image.width())
                    except:
                        self._parent._tree.item.setScale(0.7)
                self._parent._tree.setScene(self.graphicsView)
                #drag.exec_() #exec()函数并不会阻塞主函数
        except Exception as e:
            print e
     
            
            
 


    def dragEnterEvent( self, event ):
            data = event.mimeData()
            urls = data.urls()
            if ( urls and urls[0].scheme() == 'file' ):
                event.acceptProposedAction()
    def dragMoveEvent( self, event ):
            data = event.mimeData()
            urls = data.urls()
            if ( urls and urls[0].scheme() == 'file' ):
                event.acceptProposedAction()

    def dropEvent( self, event ):
            data = event.mimeData()
            urls = data.urls()
            if ( urls and urls[0].scheme() == 'file' ):
                filepath = str(urls[0].path())[1:]
                temp=0
                for pic in PIC:
                    if pic == os.path.splitext(filepath)[1]:
                        temp=1
                if temp==1 :
                    self._parent.pic_address.setText(filepath)
                    print(filepath)
                    self.image=QPixmap(filepath)
                    self.graphicsView= QGraphicsScene()            
                    self._parent._tree.item = QGraphicsPixmapItem(self.image)
                    
                    self._parent._tree.item.setFlag(QGraphicsItem.ItemIsMovable)  # 使图元可以拖动，非常关键！！！！！
                    #self.item.setScale(self.zoomscale)
                    self._parent._tree.graphicsView.addItem(self.item)
                    #self.setAlignment(Qt.AlignLeft and Qt.AlignTop)
                    self._parent._tree.setAlignment(Qt.AlignLeft)
                    if self.image.width()!=500:
                        self._parent._tree.item.setScale(500.0/self.image.width()) 
                    self._parent._tree.setScene(self.graphicsView)
                else:
                    QMessageBox.information(self,u"提示", u"不是图片")


    def wheelEvent(self, event):
            angle=event.delta()                        
  
            #print(angleX,angleY)
            if angle >= 0:
                if self.zoomscale<1.5:
                    try:
                        self.zoomscale=self.zoomscale+0.1
                        self._parent._tree.item.setScale(self.zoomscale)
                        #self.setAlignment(Qt.AlignCenter and Qt.AlignTop)
                    except:
                        pass
           
           
            elif angle <=  0:
                if self.zoomscale>0.2:
                    try:
                        self.zoomscale=self.zoomscale-0.1
                        self._parent._tree.item.setScale(self.zoomscale)
                        #self.setAlignment(Qt.AlignCenter and Qt.AlignTop)
                    except:
                        pass
           
                
#*******************************************************************
#*******************************************************************
#***************************拖拽类**********************************
#*******************************************************************
#*******************************************************************

class MyLineEdit(QLineEdit):
        def __init__( self, parent=None ):
            super(MyLineEdit, self).__init__(parent)
            self.setDragEnabled(True)

        def dragEnterEvent( self, event ):
            
            data = event.mimeData()
            urls = data.urls()
            if ( urls and urls[0].scheme() == 'file' ):
                event.acceptProposedAction()
        def dragMoveEvent( self, event ):
            data = event.mimeData()
            urls = data.urls()
            if ( urls and urls[0].scheme() == 'file' ):
                event.acceptProposedAction()

        def dropEvent( self, event ):
            data = event.mimeData()
            urls = data.urls()
            if ( urls and urls[0].scheme() == 'file' ):
                filepath = str(urls[0].path())[1:]
                filepath=filepath.decode("utf-8")
                self.setText(filepath)

#*******************************************************************
#*******************************************************************
#***************************功能类**********************************
#*******************************************************************
#*******************************************************************
class Nude_transform_gui(QWidget):
    
    def __init__(self):
        super(Nude_transform_gui,self).__init__()
        #self.setWindowFlags(Qt.Window)
        self.setWindowTitle(u"ネットご覧程式")
        
        self.initUI()
    def initUI(self):


        pic_address=QLabel(u'图片地址：')
        self.pic_address=MyLineEdit(r'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1566046461&di=eb7e24fbbd31054e8b19de7f3b7ac117&imgtype=jpg&er=1&src=http%3A%2F%2Fb-ssl.duitang.com%2Fuploads%2Fitem%2F201509%2F08%2F20150908181705_QGcWt.jpeg')
        pic_button=QPushButton(u"加载")

        save_address=QLabel(u'图片地址：')
        address=str(os.path.abspath(os.path.dirname(__file__)))
        address=address.decode("GBK")
        self.save_address=MyLineEdit(address)
        save_button=QPushButton(u"浏览")

        
        self._tree=graphicsView(self)
 
        
        start_work=QPushButton(u"下载图片")
 

        switchBtn_name=QLabel(u"自动切换")
        self.switchBtn = SwitchBtn(self)

        time_v=QLabel(u"时间间隔")
        self.time_v=QLineEdit(u"6")

        pbar=QLabel(u"进度")
        self.pbar = QProgressBar()

        self.timer = QTimer(self)

        #print dir(self.pbar)

        
        #groupNameData.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        

        
        laty_1=QHBoxLayout()
        laty_1.addWidget(pic_address)
        laty_1.addWidget(self.pic_address)
        laty_1.addWidget(pic_button)
     

        laty_2=QHBoxLayout()
        laty_2.addWidget(self._tree)
        
        
      

        laty_3=QHBoxLayout()
        laty_3.addWidget(save_address)
        laty_3.addWidget(self.save_address)
        laty_3.addWidget(save_button)


        laty_4=QHBoxLayout()
        laty_4.addWidget(switchBtn_name,1)
        laty_4.addWidget(self.switchBtn,3)
        laty_4.addWidget(time_v,1)
        laty_4.addWidget(self.time_v,1)
        laty_4.addStretch(10)
        laty_4.addSpacing(10)
        #laty_4.addWidget(self.time_pos,1)
        laty_4.addWidget(pbar,1)
        laty_4.addWidget(self.pbar ,3)
        laty_4.addWidget(start_work,2)




        all_lay=QVBoxLayout()
        all_lay.addLayout(laty_1)
        all_lay.addLayout(laty_2)
        all_lay.addLayout(laty_3)
        all_lay.addLayout(laty_4)


      
        self.setLayout(all_lay)
        
        self.resize(550,650)


        pic_button.clicked.connect(self.get_pic_address)
        save_button.clicked.connect(self.get_save_address)
        start_work.clicked.connect(self.transform_nude)
        self._tree.connect(self.timer,SIGNAL("timeout()"),self._tree.refresh_pic)
        self.time_v.textChanged.connect(self.changetime)
        self.timer.start(6000) #设置计时
        #self.timer.start(5000) #设置计时
   
   

    def changetime(self):
        try:
            time=int(str(self.time_v.text()))
            self.timer.start(1000*time) #设置计时
        except:
            pass
        
    def get_pic_address(self):
            pic_address=self.pic_address.text()
            if(pic_address==""):
                QMessageBox.information(self,u"提示", u"请输入图片地址")
                return
            name=pic_address
            if os.path.exists(name):
                self._tree.zoomscale=1
                self._tree.image=QPixmap(name)
                self._tree.graphicsView= QGraphicsScene()            
                self._tree.item = QGraphicsPixmapItem(self._tree.image)
                self._tree.item.setFlag(QGraphicsItem.ItemIsMovable)  # 使图元可以拖动，非常关键！！！！！
                self._tree.graphicsView.addItem(self._tree.item)
                #self._tree.setAlignment(Qt.AlignLeft and Qt.AlignTop)
                self._tree.setAlignment(Qt.AlignLeft)
                if self._tree.image.width()!=500:
                    self._tree.item.setScale(500.0/self._tree.image.width()) 
                self._tree.setScene(self._tree.graphicsView)
            else:
                self._tree.zoomscale=1
                req = requests.get(name,headers=headers)
                self._tree.image=QPixmap()
                self._tree.image.loadFromData(req.content)

                
                self._tree.graphicsView= QGraphicsScene()            
                self._tree.item = QGraphicsPixmapItem(self._tree.image)
                self._tree.item.setFlag(QGraphicsItem.ItemIsMovable)  # 使图元可以拖动，非常关键！！！！！
                self._tree.graphicsView.addItem(self._tree.item)
                #self._tree.setAlignment(Qt.AlignLeft and Qt.AlignTop)
                self._tree.setAlignment(Qt.AlignLeft)
                if self._tree.image.width()!=500:
                    try:
                        self._tree.item.setScale(500.0/self._tree.image.width())
                    except:
                        self._tree.item.setScale(0.7)
                self._tree.setScene(self._tree.graphicsView)

                
                
    def get_save_address(self):
        filename = QFileDialog.getExistingDirectory()
        if filename:
            filename=filename.replace("\\",'/')

    def createRandomString(self,len):
        print ('wet'.center(10,'*'))
        raw = ""
        range1 = range(58, 65) # between 0~9 and A~Z
        range2 = range(91, 97) # between A~Z and a~z

        i = 0
        while i < len:
            seed = random.randint(48, 122)
            if ((seed in range1) or (seed in range2)):
                continue;
            raw += chr(seed);
            i += 1
        return raw
    


    def transform_nude(self):
        self.pbar.setValue(5)
        if str(self.pic_address.text())=="" or str(self.save_address.text())=="":
            QMessageBox.information(self,u"提示", u"请输入图片储存地址，视频名称可不写")
            return
        pic_address=str(self.pic_address.text())
        output_address=str(self.save_address.text())
        if "." in str(self.save_address.text()):
            output_address=str(self.save_address.text())
        else:
            
            output_address=str(self.save_address.text())+"/" +"_"+self.createRandomString(5)+"."+pic_address.split(".")[-1]
        if os.path.exists(pic_address):
            QMessageBox.information(self,u"提示", u"本地图片不可下载!")
            return
        else:
            request =  urllib2.Request(url=pic_address, headers=headers)
            response = urllib2.urlopen(request)
            output_address=output_address.decode("utf-8")
            with open(output_address, "wb") as f:
                f.write(response.read())

            self.box = QMessageBox(QMessageBox.Information, u"提示", u"下载成功！")
            self.box.addButton(u"确定", QMessageBox.YesRole).animateClick(1*1000)
            self.box.exec_()


#*******************************************************************
#*******************************************************************
#***************************主函数***********************************
#*******************************************************************
#******************************************************************* 

if __name__ == '__main__': 
    app = QApplication(sys.argv)
    bili = Nude_transform_gui()
    bili.show()
    sys.exit(app.exec_())


