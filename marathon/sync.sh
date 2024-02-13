#!/bin/sh
# open -u <user> <password> <host url>; mirror -c -R -L <path from> <path to>
lftp -c "open -u pohsuan.huang,acer 10.36.169.170; mirror -c -R -L /home/pohsuan/disk1/Marathon/JPEGImages/TrainSet8/ /home/pohsuan.huang/pva-faster-rcnn/data/VOCdevkit2007/sycfolder/JPEGImages"

lftp -c "open -u pohsuan.huang,acer 10.36.169.170; mirror -c -R -L /home/pohsuan/disk1/Marathon/Annotations/TrainSet8/ /home/pohsuan.huang/pva-faster-rcnn/data/VOCdevkit2007/sycfolder/Annotations"
