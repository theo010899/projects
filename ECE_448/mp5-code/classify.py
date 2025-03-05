# classify.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/27/2018
# Extended by Daniel Gonzales (dsgonza2@illinois.edu) on 3/11/2020

"""
This is the main entry point for MP5. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.

train_set - A Numpy array of 32x32x3 images of shape [7500, 3072].
            This can be thought of as a list of 7500 vectors that are each
            3072 dimensional.  We have 3072 dimensions because there are
            each image is 32x32 and we have 3 color channels.
            So 32*32*3 = 3072. RGB values have been scaled to range 0-1.

train_labels - List of labels corresponding with images in train_set
example: Suppose I had two images [X1,X2] where X1 and X2 are 3072 dimensional vectors
         and X1 is a picture of a dog and X2 is a picture of an airplane.
         Then train_labels := [1,0] because X1 contains a picture of an animal
         and X2 contains no animals in the picture.

dev_set - A Numpy array of 32x32x3 images of shape [2500, 3072].
          It is the same format as train_set

return - a list containing predicted labels for dev_set
"""

import numpy as np
import heapq 

def trainPerceptron(train_set, train_labels, learning_rate, max_iter):
    # TODO: Write your code here
    # return the trained weight and bias parameters
    
    # initialize the wieght array to zero
    W = np.zeros([train_set.shape[1]])
    b = 0
    for i in range(max_iter):
        for y in range(len(train_labels)):
            signed = 0
            unsigned = np.matmul(W , train_set[y]) + b
            if unsigned > 0:
                signed = 1
            if unsigned <= 0:
                signed = 0
            if train_labels[y] != signed:
                W = W + learning_rate * (train_labels[y] - signed) * train_set[y]
                b += (train_labels[y] - signed) * learning_rate

    # print(type(W))
    # W = W.tolist()
    # print(W)
    # print(b)
    return W, b

def classifyPerceptron(train_set, train_labels, dev_set, learning_rate, max_iter):
    # TODO: Write your code here
    # Train perceptron model and return predicted labels of development set
    # print(train_set)
    W, b = trainPerceptron(train_set, train_labels, learning_rate, max_iter)
    # print(W)
    y_hat = []
    for y in range(len(dev_set)):
            unsigned = np.matmul(W , dev_set[y]) + b
            # signed = np.sign(unsigned)
            if unsigned > 0:
                y_hat.append(1)
            if unsigned <= 0:
                y_hat.append(0)

    return y_hat

def classifyKNN(train_set, train_labels, dev_set, k):
    # TODO: Write your code here
    ret_list = []
    for x in range(len(dev_set)):
        # print(dev_set[x].shape)
        # print(train_set[x].shape, train_set.shape)

        E_distance_list = np.linalg.norm(dev_set[x] - train_set, axis = 1) # calculate the euclidean distance
        priorty_indicies = np.argsort(E_distance_list)
        k_labels = []  # find the k closest neighbors
        for i in range(k):
            # print(len(train_labels))
            # print(priorty_indicies, "\n")
            # print(train_labels[priorty_indicies[i]])
            k_labels.append(train_labels[priorty_indicies[i]])
        # print(k_labels)
        count = np.bincount(k_labels)   
        # print(count)
        if len(count) == 2  and count[1] > count[0]:
            ret_list.append(1)
        else:
            ret_list.append(0) 


    return ret_list
