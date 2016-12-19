#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""

.. moduleauthor:: Michal Ciesielski <ciesielskimm@gmail.com>


"""
from __future__ import division
import Queue
from threading import Thread
import os
import argparse
import signal
from serialcom import SerialCom
import time
import sys
import math

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import numpy as np


# #########################################################################
# VARS
# #########################################################################
data = list()
tempData = [0, 0, 0]
prevData = [0, 0, 0]
drawData = [0, 0, 0]

vertIndex = 0
numberOfSamples = 4000
sphereRadius = .001
updating = True
fifoPath = '/tmp/serialPort.fifo'
# #########################################################################
# FUNCTIONS
# #########################################################################


def update():
    # UPDATE SETTINGS
    global data
    global prevData
    global tempData
    global drawData
    global posPoints
    global posAvg
    global vertIndex
    global updating

    while 1:
        if not updating:
            break

        if vertIndex < numberOfSamples:

            fifo = open(fifoPath, 'r')
            for line in fifo:
                line = line.strip()
                tempData = line.split(';')
                tempData = map(int, tempData)
                data.append(tempData)
            fifo.close()

            # be sure data is the proper size
            if len(tempData) != 3:
                continue

            # check if program read the same line more than once
            if tempData == prevData:
                continue
            prevData = tempData

            # normalize
            # vectorLength = math.sqrt(tempData[0] * tempData[0] +
            #                          tempData[1] * tempData[1] +
            #                          tempData[2] * tempData[2])

            # something goes wrong here
            # tempData[0] /= vectorLength
            # tempData[1] /= vectorLength
            # tempData[2] /= vectorLength

            # rescale
            drawData[0] = tempData[0] * sphereRadius
            drawData[1] = tempData[1] * sphereRadius
            drawData[2] = tempData[2] * sphereRadius

            posPoints[vertIndex][0] = drawData[0]
            posPoints[vertIndex][1] = drawData[1]
            posPoints[vertIndex][2] = drawData[2]

            colorPoints[vertIndex][0] = 0
            colorPoints[vertIndex][1] = 1
            colorPoints[vertIndex][2] = 0.2

            vectorLength = math.sqrt(drawData[0] * drawData[0] +
                                     drawData[1] * drawData[1] +
                                     drawData[2] * drawData[2])

            # color and discard invalid points
            if vectorLength > 3.1 + 0.1 * 3.1:
                colorPoints[vertIndex][0] = 1
                colorPoints[vertIndex][1] = 0
                colorPoints[vertIndex][2] = 0
                data.pop()
            if vectorLength < 3.1 - 0.1 * 3.1:
                colorPoints[vertIndex][0] = 0
                colorPoints[vertIndex][1] = 0
                colorPoints[vertIndex][2] = 1
                data.pop()

            sp3.setData(pos=posPoints, color=colorPoints)
            posAvg[0] = sphereRadius * calculateCalib(data)
            sp2.setData(pos=posAvg)
            vertIndex += 1
            formattedList = ['%.3f' % elem for elem in drawData]
            print('Data: {0} - Idx: {1:06} - R_avg: {2:03} - =zmag=[{3:08},{4:08},{5:08}]'
                  .format(formattedList,
                          vertIndex,
                          0,
                          int(calculateCalib(data)[0]),
                          int(calculateCalib(data)[1]),
                          int(calculateCalib(data)[2])))

        else:
            updating = False


def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


def calculateCalib(unCalVals):
    if len(unCalVals) > 0:
        Xs = [row[0] for row in unCalVals]
        Ys = [row[1] for row in unCalVals]
        Zs = [row[2] for row in unCalVals]
        avgX = ((max(Xs) - min(Xs)) / 2) + min(Xs)
        avgY = ((max(Ys) - min(Ys)) / 2) + min(Ys)
        avgZ = ((max(Zs) - min(Zs)) / 2) + min(Zs)
        # print('Mag. calibration vals. - [{0:08},{1:08},{2:08}]'.format(-1 * int(avgX),
        #                                                                -1 * int(avgY),
        #                                                                -1 * int(avgZ)))
        # print('=zmag=[{0:08},{1:08},{2:08}]'.format(-1 * int(avgX),
        #                                             -1 * int(avgY),
        #                                             -1 * int(avgZ)))
        return np.array([avgX, avgY, avgZ])
    else:
        return np.array([0, 0, 0])


def averageColumn(lst, idx):
    col = [row[idx] for row in lst]
    col = sum(col) / len(col)
    return col


def averageVLength(lst):
    le = math.sqrt(lst[0][0] * lst[0] + lst[1] * lst[1] + lst[2] * lst[2])
    lst[0] = lst[0] / le
    lst[1] = lst[1] / le
    lst[2] = lst[2] / le
    return lst


# #########################################################################
# PYQT
# #########################################################################


app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.opts['distance'] = 20
# w.setBackgroundColor('w')
w.show()
w.setWindowTitle('MagCalibration')

g = gl.GLGridItem()
w.addItem(g)

# posPoints = np.zeros((100, 100, 3)) # 100 arrays of 100 arrays of 3 elements
# posPoints[:, :, :2] = np.mgrid[:100, :100].transpose(1, 2, 0) * [-0.1, 0.1]
# posPoints = posPoints.reshape(10000, 3)
# position needs to be an array of arrays of 3 elements so this should work:
posPoints = np.zeros((numberOfSamples, 3))
# color is built similarly but for every element RGBA needs to be defined
colorPoints = np.ones((numberOfSamples, 4))
# points
sp3 = gl.GLScatterPlotItem(pos=posPoints,
                           color=(0, 1, 0.1, .7),
                           size=0.1,
                           pxMode=False)

# AXIS
posAxisPoints = np.zeros((3, 3))
color4 = np.zeros((3, 4))
# pos
posAxisPoints[0][0] = 1
posAxisPoints[1][1] = 1
posAxisPoints[2][2] = 1
# color
color4[0][0] = 1
color4[1][1] = 1
color4[2][2] = 1
# alpha
color4[0][3] = 1
color4[1][3] = 1
color4[2][3] = 1
sp4 = gl.GLScatterPlotItem(pos=posAxisPoints,
                           color=color4,
                           size=0.4,
                           pxMode=False)
sp4.setData(pos=posAxisPoints, color=color4)


# CALIBRATION POINT
# pos
posAvg = np.ones((1, 3))
sp2 = gl.GLScatterPlotItem(pos=posAvg,
                           color=(1, 1, 1, .9),
                           size=0.2,
                           pxMode=False)


w.addItem(sp2)
w.addItem(sp3)
w.addItem(sp4)

# this needs to be here - after all this pyqt shit above
# maybe not timer but thread so its faster
# t = QtCore.QTimer()
# t.timeout.connect(update)
t = Thread(target=update)
t.start()


# #########################################################################
# RUN
# #########################################################################
if __name__ == '__main__':
    try:
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()
        updating = False
        t.join()
        calculateCalib(data)
        sys.exit()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(' --- Exception: {0}'.format(e))
        print(exc_type, fname, exc_tb.tb_lineno)
        updating = False
        t.join()
        sys.exit()
