cat $1 |grep "sgd_solver.cpp:138]" >iteration.txt;
cat $1 |grep "solver.cpp:238]" >loss.txt;
cat $1 |grep "Train net output #0: loss_bbox" >loss_bbx.txt;
cat $1 |grep "Train net output #1: loss_cls" >loss_cls.txt;
cat $1 |grep "Train net output #2: rpn_loss_bbox" >rpn_loss_bbx.txt;
cat $1 |grep "Train net output #3: rpn_loss_cls" >rpn_loss_cls.txt;


python extract_plot.py

