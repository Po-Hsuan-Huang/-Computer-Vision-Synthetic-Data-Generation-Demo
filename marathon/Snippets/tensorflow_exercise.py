#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 18:01:05 2017

@author: pohsuan
"""

import tensorflow as tf
#%%
start =1
stop = 1000
num = 1000
delta = 0.001
lim = 10
tensor = tf.zeros([3,4], dtype = 'int32')

a = tf.zeros_like(tensor)

b = tf.ones([2,3], 'int32')

c = tf.fill([2,3], 9)

d = tf.constant( -1.0, shape=[2,3] )

e = tf.lin_space(start, stop, num)

f = tf.range(start, lim, delta)

norm = tf.random_normal([2,3], mean = 0.1 , stddev  =4 
                        
#%%
# Create a tensor of shape [2, 3] consisting of random normal values, with mean
# -1 and standard deviation 4.
norm = tf.random_normal([2, 3], mean= -1, stddev=4)

# Shuffle the first dimension of a tensor
c = tf.constant([[1, 2], [3, 4], [5, 6]])
shuff = tf.random_shuffle(c)

# Each time we run these ops, different results are generated
sess = tf.Session()
print(sess.run(norm))
print(sess.run(norm))
#%%
value = tf.fill([5,30],'9')
num_feat = 4096
num_predict = 6 # final output of LSTM 6 loc parameters
num_input = num_feat + num_predict # data input: 4096+6= 5002
istate = tf.placeholder("float32", [None, 2*num_input]) #state & cell => 2x num_input
x = tf.placeholder("float32", [None, 3, num_input])

cell = tf.nn.rnn_cell.LSTMCell.__init__( )

for step in range(3):
    outputs, state = tf.nn.rnn(cell, [x[step]], istate)
    tf.get_variable_scope().reuse_variables()
