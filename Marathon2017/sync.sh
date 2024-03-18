#!/bin/sh
# open -u <user> <password> <host url>; mirror -c -R -L <path from> <path to>
lftp -c "open -u pohsuanh.huang,lab 10.36.169.170; mirror -c -R -L /home/pohsuanh/Documents/Computer-Vision-Synthetic-Data-Generation-Toolkit/Marathon2017/JPEGImages/TrainSet2/ /home/pohsuanh.huang/pva-faster-rcnn/data/VOCdevkit2007/sycfolder/JPEGImages"

lftp -c "open -u pohsuanh.huang,lab 10.36.169.170; mirror -c -R -L /home/pohsuanh/Documents/Computer-Vision-Synthetic-Data-Generation-Toolkit/Marathon2017/Annotations/TrainSet2/ /home/pohsuanh.huang/pva-faster-rcnn/data/VOCdevkit2007/sycfolder/Annotations"
