# neuralnet.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/29/2019
"""
This is the main entry point for MP6. You should only modify code
within this file and neuralnet_part2 -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as np
import torch


class NeuralNet(torch.nn.Module):
    def __init__(self, lrate,loss_fn,in_size,out_size):
        """
        Initialize the layers of your neural network

        @param lrate: The learning rate for the model.
        @param loss_fn: A loss function defined in the following way:
            @param yhat - an (N,out_size) tensor
            @param y - an (N,) tensor
            @return l(x,y) an () tensor that is the mean loss
        @param in_size: Dimension of input
        @param out_size: Dimension of output

        For Part 1 the network should have the following architecture (in terms of hidden units):

        in_size -> 32 ->  out_size
        We recommend setting the lrate to 0.01 for part 1

        """
        super(NeuralNet, self).__init__()
        self.loss_fn = loss_fn
        self.lrate = lrate
        self.in_size = in_size
        self.out_size = out_size
        self.model = torch.nn.Sequential(
            torch.nn.Linear(in_size, 32 , True),
            torch.nn.ReLU(),
            torch.nn.Linear(32, out_size, True)
        )
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=lrate)


    def forward(self, x):
        """ A forward pass of your neural net (evaluates f(x)).

        @param x: an (N, in_size) torch tensor

        @return y: an (N, out_size) torch tensor of output from the network
        """
        output = self.model(x)
        # relu = self.relu(output)
        # output = self.fc2(relu)
        return output   #torch.ones(x.shape[0], 1)

    def step(self, x,y):
        """
        Performs one gradient step through a batch of data x with labels y
        @param x: an (N, in_size) torch tensor
        @param y: an (N,) torch tensor
        @return L: total empirical risk (mean of losses) at this time step as a float
        """
        self.optimizer.zero_grad()   # zero the gradient buffers
        output = self.forward(x)
        loss = self.loss_fn(output,y.long())
        loss.backward()
        self.optimizer.step()
        return loss.item()


def fit(train_set,train_labels,dev_set,n_iter,batch_size=100):
    """ Make NeuralNet object 'net' and use net.step() to train a neural net
    and net(x) to evaluate the neural net.

    @param train_set: an (N, in_size) torch tensor
    @param train_labels: an (N,) torch tensor
    @param dev_set: an (M,) torch tensor
    @param n_iter: int, the number of iterations of training
    @param batch_size: The size of each batch to train on. (default 100)

    # return all of these:

    @return losses: Array of total loss at the beginning and after each iteration. Ensure len(losses) == n_iter
    @return yhats: an (M,) NumPy array of binary labels for dev_set
    @return net: A NeuralNet object

    # NOTE: This must work for arbitrary M and N
    """
    # print(train_set.shape)
    # standardization
    train_set = (train_set - train_set.mean(dim=0)) / train_set.std(dim=0)
    dev_set = (dev_set - train_set.mean(dim=0)) / train_set.std(dim=0)

    # num_batches = len(train_set)/batch_size
    # start_index = (i%num_batches)*batch_size
    loss = []
    yhat = [] 
    N_Net = NeuralNet(0.0001,torch.nn.CrossEntropyLoss(),3072, 2)
    
    cur_batch = []
    cur_labels = []
    for j in range(n_iter):
        # print(j)
        for i in range(len(train_set)):
            if len(cur_batch) < batch_size:
                cur_batch.append(train_set[i])
                cur_labels.append(train_labels[i].item())
            else:
                tensor_batch = torch.stack(cur_batch)
                tensor_labels = torch.Tensor(cur_labels)
                # print(tensor_batch.shape,tensor_labels.shape)
                loss.append(N_Net.step(tensor_batch,tensor_labels))
                cur_batch = []
                cur_labels = []
        if len(cur_batch) != 0:
            tensor_batch = torch.stack(cur_batch)
            tensor_labels = torch.Tensor(cur_labels)
            # print(tensor_batch.shape(),)
            loss.append(N_Net.step(tensor_batch,tensor_labels))
            cur_batch = []
            cur_labels = []

    N_Net.eval()
    output = N_Net.forward(dev_set)
    # print(output)
    for pair in output:
        yhat.append(torch.argmax(pair))

    yhat = np.array(yhat)

    return loss,yhat,N_Net
