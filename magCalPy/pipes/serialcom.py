#!python2
# -*- coding: UTF-8 -*-

from threading import Thread
import serial
import time
import signal
import sys
import os

FRAME_SIZE_BIN = 4
FRAME_SIZE_2 = 32
PREAMBLE_BIN = 0xAA
PREAMBLE_2 = 'M'


class SerialCom():
    """docstring for CLInfo"""
    def __init__(self):
        self.BaudRate = 115200
        self.running = True
        self.numericals = []
        self.fifo = None
        self.data = 'a\n'
        self.timeout = 0
        self.dataIsBinary = False
        self.fifoPath = '/tmp/serialPort.fifo'

    def start(self):
        try:
            self.fifo = os.mkfifo(self.fifoPath)
        except:
            pass
        # self.SP = serial.Serial('/dev/sensor_uart',  # after adding rule in /etc/udev/rules.d
        self.SP = serial.Serial('/dev/ttyUSB0',
        # self.SP = serial.Serial('COM5',
                                self.BaudRate,
                                timeout=5)

        while self.SP.is_open is False:
            try:
                self.SP.open()
            except serial.SerialException:
                print('Serial port opening failed.')
                return

        # be sure the sensor is in the right mode
        #  n = 0
        #  while n < 1000:
            #  self.SP.write('mag\n')
            #  n += 1

        self.SP.flush()
        self.SP.flushInput()

        return self

    def stop(self):
        self.running = False
        # join means wait here for the thread to end
        return

    def update(self):
        c = 'a'
        data = list()

        while 1:
            if self.running is False:
                break

            # clear data list
            c = 'a'
            data = list()

            if self.dataIsBinary:
                # read data if there is enough in buffer
                if self.SP.in_waiting > FRAME_SIZE_BIN:

                    # block here until gets to PREAMBLE_BIN or timesout
                    while ord(c) != PREAMBLE_BIN:
                        c = self.SP.read(1)
                        # print('{0} : {1}'.format(ord(c), self.timeout))
                        self.timeout += 1
                        if self.timeout > 9000:
                            break

                    self.timeout = 0

                    for x in xrange(1, FRAME_SIZE_BIN):
                        data.append(ord(self.SP.read(1)))

                    if self.queueSRL is not None:
                        self.queueSRL.put(data)

            elif not self.dataIsBinary:
                # read data if there is enough in buffer
                if self.SP.in_waiting > FRAME_SIZE_2:

                    # block here until gets to PREAMBLE_BIN or timesout
                    while c != PREAMBLE_2:
                        c = self.SP.read(1)
                        # print('{0} : {1}'.format(ord(c), self.timeout))
                        self.timeout += 1
                        if self.timeout > 9000:
                            break

                    self.timeout = 0

                    # get rid of 'AG.'
                    c = self.SP.read(3)
                    # read the data
                    c = self.SP.read(28)
                    c = c.strip()

                    try:
                        data = c.split('.')
                        data = map(int, data)
                    except:
                        continue

                    try:
                        print('Data = {0}'.format(data))
                        self.fifo = open(self.fifoPath, 'w')
                        self.fifo.write(str(data[0]))
                        self.fifo.write(';')
                        self.fifo.write(str(data[1]))
                        self.fifo.write(';')
                        self.fifo.write(str(data[2]))
                        self.fifo.write('\n')
                        self.fifo.close()
                    except IOError as e:
                        continue

        self.SP.close()

    def clean(self):
        self.SP.flush()
        self.SP.flushInput()
        return


if __name__ == '__main__':
    try:
        serial_port = SerialCom()
        serial_port.start()
        while 1:
            serial_port.update()
    except Exception as e:
        print('---- Exception : {0}'.format(e))
        serial_port.stop()
