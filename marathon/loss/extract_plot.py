import numpy as np
Iter=list()
file = open('iteration.txt', 'r' )
while True:
	line = file.readline()
	if not line:
		break
	Iter.append(float(line.split(' ')[-4].split(',')[0]))

loss=list()
file = open('loss.txt', 'r' )
while True:
	line = file.readline()
	if not line:
		break
	loss.append(float(line.split(' ')[-1]))

loss_bbx=list()
file = open('loss_bbx.txt', 'r' )
while True:
	line = file.readline()
	if not line:
		break
	loss_bbx.append(float(line.split(' ')[-6]))

loss_cls=list()
file = open('loss_cls.txt', 'r' )
while True:
	line = file.readline()
	if not line:
		break
	loss_cls.append(float(line.split(' ')[-6]))
 
rpn_loss_bbx=list()
file = open('rpn_loss_bbx.txt', 'r' )
while True:
	line = file.readline()
	if not line:
		break
	rpn_loss_bbx.append(float(line.split(' ')[-6]))
rpn_loss_cls=list()
file = open('rpn_loss_cls.txt', 'r' )
while True:
	line = file.readline()
	if not line:
		break
	rpn_loss_cls.append(float(line.split(' ')[-6]))

#get moving average 

def runningMeanFast(x, N):
    return np.convolve(x, np.ones((N,))/N)[(N-1):] 

loss_cls_mean = runningMeanFast(loss_cls, 10 )

loss_bbx_mean = runningMeanFast(loss_bbx, 10 )


import matplotlib.pyplot as plt
#
#start = -4750
#end = -3500
#
start = -4065
end = -1
x = Iter[ start: end]
#head = [i for i,s in enumerate(x) if s ==0 ]
#for i ,d in enumerate(head):
#    xlist = x[d:head[i+1]]
#    print xlist
plt.plot(x ,loss_bbx_mean[ start: end],'-',label='loss_bbox')
plt.plot(x ,loss_cls_mean[ start: end],'-',label='loss_cls')
plt.plot(x ,rpn_loss_bbx[start: end],'-',label='rpn_loss_bbox')
plt.plot(x ,rpn_loss_cls[start: end],'-', label='rpn_loss_cls')
plt.plot(x ,loss[ start : end],'-',label='loss')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),
          ncol=5, fancybox=True, shadow=True,numpoints=1, handlelength=1 )
plt.ylim([0,1])
plt.show()

