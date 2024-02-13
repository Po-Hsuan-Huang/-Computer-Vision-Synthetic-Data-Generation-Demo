# -*- coding: utf-8 -*-
"""
Created on Wed Apr 05 16:58:51 2017

@author: 1609070

@author: pohsuanh huang

parameters :
    folder : string
        destinatoin folder containing the data
"""

#####過濾異常資料#####
import  os, glob
import  xml.dom.minidom
from xml.parsers.expat import ParserCreate, ExpatError, errors
'''parameters'''

folder = 'TrainSet7'



'''code'''
#%%
os.chdir('/home/acer/Documents/Marathon/data/Annotations/' + folder)
n=len(glob.glob(os.getcwd()+"/*.xml"))
n2=0
n3=0

f = open('/home/acer/Documents/Marathon/data/ImageSets/broken.txt', 'w')

for str2 in sorted(glob.glob(os.getcwd()+"/*.xml")):
    nnn=0
    n2=n2+1
    #print('%d/%d'%(n2,n))
    xmlname=str2[(len(os.getcwd())+1):]
    
    #jpgname='D:\\data\\cutdata\\JPEGImages\\%s.jpg'%k
    try :
        dom = xml.dom.minidom.parse(xmlname)
    except ExpatError as err:
        print(("Error:", err.message[err.code]))        
        print(('junk after document element: ', xmlname)) 
        nnn +=1
        
    #得到文档元素对象
    root = dom.documentElement
      
    xmin=dom.getElementsByTagName('xmin')
    ymin=dom.getElementsByTagName('ymin')
    xmax=dom.getElementsByTagName('xmax')
    ymax=dom.getElementsByTagName('ymax')
    name=dom.getElementsByTagName('name')
    wid=dom.getElementsByTagName('width')
    hei=dom.getElementsByTagName('height')
    w1=int(wid[0].firstChild.data)
    h1=int(hei[0].firstChild.data)
    nnn=0
    for i in range(1,len(xmin)+1):
        nn=name[i-1].firstChild.data
        x1=int(xmin[i-1].firstChild.data)
        y1=int(ymin[i-1].firstChild.data)
        x2=int(xmax[i-1].firstChild.data)
        y2=int(ymax[i-1].firstChild.data)
        if x1>=x2:
            nnn=nnn+1
#            print '1'
            break # break instantly if any error occurs 
        elif y1>=y2:
            nnn=nnn+1
#            print '2'
            break
        elif (x1<0)|(x2<0)|(y1<0)|(y2<0):
            nnn=nnn+1
#            print '3'
            break
        elif (x1>w1)|(x2>w1)|(y1>h1)|(y2>h1):
            nnn=nnn+1
#            print '4'
            break
        
    if(nnn>0):
        print((xmlname.strip('.xml')))
        f.write(xmlname.strip('.xml')+'\n')
        
f.close()