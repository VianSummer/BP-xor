# -*- coding: utf-8 -*-
import numpy as np


# coded by yijunzhang 2017
class SquareLoss:
    def forward(self, y, t):
        self.loss = y - t
        return np.sum(self.loss * self.loss) /  self.loss.shape[1] / 2
    def backward(self):
        return self.loss

class FC:
    def __init__(self, in_num, out_num, lr = 0.1):
        self._in_num = in_num
        self._out_num = out_num
        self.w = np.random.randn(in_num, out_num)
        self.b = np.zeros((out_num, 1))
        self.lr = lr
    def _sigmoid(self, in_data):
        return 1 / (1 + np.exp(-in_data))
    def forward(self, in_data):
        self.topVal = self._sigmoid(np.dot(self.w.T, in_data) + self.b)
        self.bottomVal = in_data
        return self.topVal
    def backward(self, loss):
        residual_z = loss * self.topVal * (1 - self.topVal)
        grad_w = np.dot(self.bottomVal, residual_z.T)
        grad_b = np.sum(residual_z)
        self.w -= self.lr * grad_w
        self.b -= self.lr * grad_b
        residual_x = np.dot(self.w, residual_z)
        return residual_x

class Net:
    def __init__(self, input_num, hidden_num, out_num, lr):
        self.fc1 = FC(input_num, hidden_num, lr)
        #self.fc1.w = np.array([[0.0543,0.0579],[-0.0291,0.0999]])
        #self.fc1.b = np.array([[-0.0703],[-0.0939]])
        self.fc2 = FC(hidden_num, out_num, lr)
        #self.fc2.w = np.array([[0.0801],[-0.0605]])
        #self.fc2.b = np.array([[-0.0109]])
        self.loss = SquareLoss()
    def train(self, X, y): # X are arranged by col
        for i in range(20000):
            # forward step
            layer1out = self.fc1.forward(X)
            layer2out = self.fc2.forward(layer1out)
            loss = self.loss.forward(layer2out, y)
            # backward step
            layer2loss = self.loss.backward()
            layer1loss = self.fc2.backward(layer2loss)
            saliency = self.fc1.backward(layer1loss)
            if loss < 0.008:
                print i
                break

        layer1out = self.fc1.forward(X)
        layer2out = self.fc2.forward(layer1out)
        print self.fc1.w
        print self.fc1.b
        print self.fc2.w
        print self.fc2.b
        print loss
        print 'X={0}'.format(X)
        print 't={0}'.format(y)
        print 'y={0}'.format(layer2out)

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]]).T
y = np.array([[0],[1],[1],[0]]).T

net = Net(2,2,1,0.6)
net.train(X,y)
