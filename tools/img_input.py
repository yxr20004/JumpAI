from matplotlib import pyplot as py
from PIL import Image
import os
import pandas as pd
from sklearn.utils import shuffle
import math
import time
import csv

IMAGE_W_SIZE = 1080
IMAGE_H_SIZE = 1920
pNum = 0

xy_t = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

def data2csv(x1='0',y1='0',x2='0',y2='0',file='name'):
    print(x1)
    with open('data.csv','a') as csvfile: 
        writer = csv.writer(csvfile,dialect = 'excel')

        #先写入columns_name
        #writer.writerow(["x1","y1","x2","y2","file"])
        #写入多行用writerows
        writer.writerow([x1,y1,x2,y2,file])

def on_press(event):
    global num,pNum,xy_t,IMAGE_W_SIZE,IMAGE_H_SIZE
    print('event',event.button)
    #鼠标中建跳
    if event.button == 2:
        x = (xy_t[2] - xy_t[0])
        y = (xy_t[3] - xy_t[1])
        d = x*x + y*y
        print('x:',x,'y:',y,'d:',d)
        c = int(math.sqrt(d))
        t = c * 2.75
        print('t:',int(t))
        ig = Image.open("screen.png")
        cmd = 'adb shell input swipe 500 500 501 501 ' + str(int(t))
        os.popen(cmd)
        py.clf()
        time.sleep(2.5)
        file = str(time.time()) + '.png'
        ig.save(file)
        data2csv(str(xy_t[0]),str(xy_t[1]),str(xy_t[2]),str(xy_t[3]),file)
        os.popen('adb shell screencap /sdcard/screen.png')
        time.sleep(0.5)
        os.popen('adb pull /sdcard/screen.png')
        time.sleep(1)
        
        ig = Image.open("screen.png")
        img = ig.resize([IMAGE_W_SIZE,IMAGE_H_SIZE])
        ax1 = fig.add_subplot(121)
        ax1.imshow(img)
        py.draw()
        #py.show()
        pNum = 0

        #鼠标左键定位
    elif event.button == 1:
        print(event.xdata)
        print(event.ydata)
        py.plot(event.xdata, event.ydata, '.')
        py.text(100,200+pNum*100, (str(pNum)+ " " + str(event.xdata) + " " + str(event.ydata)))
        py.draw()
        if pNum < 4:
            
            xy_t[2*pNum] = event.xdata/2.0
            xy_t[2*pNum+1] = event.ydata/2.0
            xy = xy_t[:]
            pNum = pNum + 1
        
        
        print("p:",pNum,event.xdata,event.ydata)
        #鼠标右键刷新
    elif event.button == 3:
        
        py.clf()
        os.popen('adb shell screencap /sdcard/screen.png')
        time.sleep(1)
        os.popen('adb pull /sdcard/screen.png')
        time.sleep(2)
        print("event")
        ig = Image.open("screen.png")
        
        img = ig.resize([IMAGE_W_SIZE,IMAGE_H_SIZE])
        ax1 = fig.add_subplot(121)
        ax1.imshow(img)
        py.draw()
        print("event")
        #py.show()
        pNum = 0
        print('pNum:',pNum)
        
    
if __name__ == "__main__":
    #getfile()
    os.popen('adb shell screencap /sdcard/screen.png')
    time.sleep(1)
    os.popen('adb pull /sdcard/screen.png')
    time.sleep(1)
    ig = Image.open("screen.png")
    img = ig.resize([IMAGE_W_SIZE,IMAGE_H_SIZE])
    fig = py.figure()
    fig.canvas.mpl_connect("button_press_event", on_press)
    ax1 = fig.add_subplot(121)
    ax1.imshow(img)
    py.show()
