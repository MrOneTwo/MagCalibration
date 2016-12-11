#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""

.. moduleauthor:: Michal Ciesielski <ciesielskimm@gmail.com>


"""
from __future__ import division
import Queue
from threading import Thread
import os
import logging
import argparse
import signal
from serialcom import SerialCom
import time
import sys
import math
import random

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import numpy as np


# #########################################################################
# VARS
# #########################################################################


data = list()
queue_SRL_2_MAIN = Queue.Queue()

serial_port = SerialCom(queue_SRL_2_MAIN)
serial_port.start()

vertIndex = 0
numberOfSamples = 10000
sphereRadius = 50

# #########################################################################
# FUNCTIONS
# #########################################################################


def update():
    # UPDATE SETTINGS
    global data
    global pos3
    global vertIndex

    if not queue_SRL_2_MAIN.empty() and vertIndex < numberOfSamples:
        data = queue_SRL_2_MAIN.get()
        queue_SRL_2_MAIN.task_done()
        # normalize
        vectorLength = math.sqrt(data[0] * data[0] +
                                 data[1] * data[1] +
                                 data[2] * data[2])
        data[0] /= vectorLength
        data[1] /= vectorLength
        data[2] /= vectorLength

        # rescale
        data[0] *= sphereRadius
        data[1] *= sphereRadius
        data[2] *= sphereRadius

        # make it a sphere
        data[0] *= random.choice([-1, 1])
        data[1] *= random.choice([-1, 1])
        data[2] *= random.choice([-1, 1])

        pos3[vertIndex][0] = data[0] / 10
        pos3[vertIndex][1] = data[1] / 10
        pos3[vertIndex][2] = data[2] / 10

        color[vertIndex][0] = data[0] / 100
        color[vertIndex][1] = data[1] / 100
        color[vertIndex][2] = data[2] / 100

        sp3.setData(pos=pos3, color=color)
        vertIndex += 1
        print(data)
    else:
        pass


def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper

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

# pos3 = np.zeros((100, 100, 3)) # 100 arrays of 100 arrays of 3 elements
# pos3[:, :, :2] = np.mgrid[:100, :100].transpose(1, 2, 0) * [-0.1, 0.1]
# pos3 = pos3.reshape(10000, 3)
# position needs to be an array of arrays of 3 elements so this should work:
pos3 = np.zeros((numberOfSamples, 3))
# color is built similarly but for every element RGBA needs to be defined
color = np.ones((numberOfSamples, 4))

sp3 = gl.GLScatterPlotItem(pos=pos3,
                           color=(1, 1, 1, .6),
                           size=0.1,
                           pxMode=False)

w.addItem(sp3)

# this needs to be here - after all this pyqt shit above
# maybe not timer but thread so its faster
t = QtCore.QTimer()
t.timeout.connect(update)
t.start(1)
# t = Thread(target=update)
# t.start()


# #########################################################################
# RUN
# #########################################################################
if __name__ == '__main__':
    try:
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()
        serial_port.stop()
        # t.join()
        sys.exit()
    except KeyboardInterrupt:
        serial_port.stop()
        sys.exit()
