#!python2
# -*- coding: UTF-8 -*-

from threading import Thread
import serial
import time
import signal

FRAME_SIZE_BIN = 4
FRAME_SIZE_2 = 32
PREAMBLE_BIN = 0xAA
PREAMBLE_2 = 'M'


class SerialCom():
    """docstring for CLInfo"""
    def __init__(self, q):
        self.BaudRate = 115200
        self.running = True
        self.numericals = []
        self.queueSRL = q
        self.data = 'a\n'
        self.timeout = 0
        self.dataIsBinary = False

        self.t = Thread(target=self.update, args=())

    def start(self):
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

        self.SP.flush()
        self.SP.flushInput()

        self.t = Thread(target=self.update, args=())

        # deamon so the ctrl + c works ok
        # if self.queueSRL is None:
        self.t.daemon = True

        self.t.start()
        return self

    def stop(self):
        self.running = False
        # join means wait here for the thread to end
        self.t.join()
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
                    data = c.split('.')
                    data = map(int, data)

                    # data.append(ord(self.SP.read(29)))

                    if self.queueSRL is not None:
                        self.queueSRL.put(data)
                    else:
                        print(data)

        self.SP.close()

    def clean(self):
        self.SP.flush()
        self.SP.flushInput()
        return


if __name__ == '__main__':
    try:
        serial_port = SerialCom(None)
        serial_port.start()
        while 1:
            continue
    except:
        serial_port.stop()
