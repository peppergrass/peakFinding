# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 15:12:00 2018

@author: pec12003
"""
import numpy as np
from matplotlib import pyplot as plt

def SlidingWindow(y, winsize, threshold, influence,lag):
    signals = np.zeros(len(y))
    filteredY = np.array(y)
    runningAvg = [0]*len(y)
    runningStd = [0]*len(y)
    index = []
    height = []
    lagTemp = []
    runningAvg[winsize - 1] = np.mean(y[0:winsize])
    runningStd[winsize - 1] = np.std(y[0:winsize])
    for i in range(winsize, len(y)-lag):
        if (y[i] - runningAvg[i-1]) > threshold * runningStd[i-1]:
            lagTemp = np.array(y[i-lag:i+lag+1])
            trend = lagTemp[1:]-lagTemp[:-1]            
            if np.array_equal(trend[:lag],trend[trend>0]) \
            and (y[i]-runningAvg[i-1])>3:
                signals[i] = 1 
                index.append(i)
                height.append(y[i] - runningAvg[i-1])          
            filteredY[i] = influence * y[i] + (1 - influence) * filteredY[i-1]
            runningAvg[i] = np.mean(filteredY[(i-winsize):i])
            runningStd[i] = np.std(filteredY[(i-winsize):i])
        else:
            filteredY[i] = y[i]
            runningAvg[i] = np.mean(filteredY[(i-winsize):i])
            runningStd[i] = np.std(filteredY[(i-winsize):i])
    return dict(signals = np.asarray(signals),
                index = index,height = height)
    
input = np.loadtxt('Q1 Dataset 1.txt',skiprows = 2)
x = input[:,0]
y = input[:,1]

inrange = range(6200,6700)
winsize = len(y)//50
lag = 20
threshold = 3
influence = 0

result = SlidingWindow(y, winsize, threshold, influence, lag)
output = np.column_stack((result['index'],result['height']))

plt.plot(x,y)

plt.figure(2)
plt.plot(x,result['signals'])

plt.figure(3)
plt.plot(x[inrange],y[inrange])

plt.figure(4)
plt.plot(x[inrange],result['signals'][inrange])