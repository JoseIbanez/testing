#!/bin/python
import numpy as np
import tensorflow as tf

# Model parameters
W = tf.Variable([.3], tf.float32)
b = tf.Variable([-.3], tf.float32)

W1 = tf.Variable([.3], tf.float32)
b1 = tf.Variable([-.3], tf.float32)
W2 = tf.Variable([.3], tf.float32)
b2 = tf.Variable([-.3], tf.float32)
V1 = tf.Variable([.3], tf.float32)
V2 = tf.Variable([-.3], tf.float32)



# Model input and output
x = tf.placeholder(tf.float32)
y = tf.placeholder(tf.float32)

l1 = W1 * x + b1
l2 = W2 * x + b2
model = V1 * l1 + V2 * l2

# loss
loss = tf.reduce_sum(tf.square(model - y)) # sum of the squares
# optimizer
optimizer = tf.train.GradientDescentOptimizer(0.01)
train = optimizer.minimize(loss)
# training data
x_train = [1,2,3,4]
y_train = [0,-1,-2,-3]
# training loop
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init) # reset values to wrong
for i in range(1000):
  sess.run(train, {x:x_train, y:y_train})

# evaluate training accuracy
curr_W, curr_b, curr_loss  = sess.run([W, b, loss], {x:x_train, y:y_train})
print("W: %s b: %s loss: %s"%(curr_W, curr_b, curr_loss))


curr_W1, curr_W2, curr_V1, curr_V2, curr_loss  = sess.run([W1, W2, V1, V2, loss], {x:x_train, y:y_train})
print("W1: %s W2: %s loss: %s"%(curr_W1, curr_W2, curr_loss))
