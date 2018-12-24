# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 13:43:40 2018

@author: Mark
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from time import time
from mpl_toolkits.mplot3d import Axes3D


import matplotlib.pylab as pylab
params = {'legend.fontsize': 'x-large',
         'axes.labelsize': 50,
         'axes.titlesize':'x-large',
         'xtick.labelsize': 25,
         'ytick.labelsize': 25}
pylab.rcParams.update(params)
#%% Functions


def Gaus(X):
    FirstPart = 1/np.power(2*np.pi,len(X)/2)*1/(np.power(np.linalg.det(Sigma),0.5))
    Exp = -(1/2)*np.matmul(np.transpose(X-Mu),np.matmul(np.linalg.inv(Sigma),X-Mu))
    return FirstPart*np.exp(Exp)

def Plot(X,Y,Name):
    x,y = np.hsplit(X,2)
    x = np.reshape(x,(41,41))
    y = np.reshape(y,(41,41))
    z = np.reshape(Y,(41,41))
    fig = plt.figure(Name)
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(x, y, z, cmap=cm.coolwarm,linewidth=1, antialiased=True)
    fig.colorbar(surf, shrink=0.5, aspect=5,pad=-0.07)
    ax.view_init(azim=-120,elev = 70)
    ax.set_zlabel('\nY  ',fontsize=50)
    ax.set_ylabel('\n$X_1$  ',fontsize=50)
    ax.set_xlabel('\n\n$X_0$',fontsize=50)

    




class NeuralNW():
    def __init__(self,X,Y,eta):
        self.w1 = np.random.random_sample((D+1,M))-0.5
        self.w2 = np.random.random_sample(M+1)-0.5
        self.X = X
        self.Y = Y
        self.TrainX = []
        for x in self.X:
            self.TrainX.append(np.array([1,x[0],x[1]]))
        self.TrainX = np.array(self.TrainX)

    def setNetworkOnce(self,Num):
        self.HiddenLayer = np.tanh(np.dot(self.w1[0], self.TrainX[Num][0]) + np.dot(self.w1[1] , self.TrainX[Num][1]) + np.dot(self.w1[2],self.TrainX[Num][2]))
        self.HiddenLayer = np.insert(self.HiddenLayer,0,1)
        self.Output = np.sum(self.HiddenLayer*self.w2)

    def TrainNetwork(self,Num):
        self.setNetworkOnce(Num)
        Delta2 = self.Output - Y[Num]
        Delta1 = (1-np.square(self.HiddenLayer))*self.w2*Delta2
        Der2 = Delta2*self.HiddenLayer
        Delta1 = Delta1[1:]
        Der1 = np.array([Delta1*self.TrainX[Num][0],Delta1*self.TrainX[Num][1] , Delta1*self.TrainX[Num][2]])
        self.w2 -= eta*Der2
        self.w1 -= eta*Der1
        
    def TrainNetworkAll(self):
        for i in range(len(self.X)):
            self.TrainNetwork(i)
            
    def PlotOutput(self,Name):
        Out = []
        for i in range(len(X)):
            self.setNetworkOnce(i)
            Out.append(self.Output)
        Out = np.array(Out)
        Plot(self.X,Out,Name)
#%%Constants

Sigma = (2/5)*np.identity(2)
Mu = np.zeros(2)
x = y = np.arange(-2,2+0.1,0.1)
x,y = np.meshgrid(x,y)
X = []
for i in range(len(x)):
    for j in range(len(x[0])):
        X.append(np.array([x[i][j],y[i][j]]))
X = np.array(X)
Y = np.array([Gaus(x) for x in X])

Plot(X,Y,"Plot Gaussian")


eta = 0.1
D = 2
M = 8



#%%

Network = NeuralNW(X,Y,eta)
Now = time()
#Network.setNetworkOnce(0,Printen=True)

#Network.TrainNetwork(0)
Plot(X,Y,"Real")
Network.PlotOutput("First")

for i in range(1000):
    Network.TrainNetworkAll()

Network.PlotOutput("Second")
print(time()-Now)