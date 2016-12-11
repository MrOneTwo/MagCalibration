#!python2
# -*- coding: UTF-8 -*-

from threading import Thread
import serial
import time

FRAME_SIZE = 4
PREAMBLE = 0xAA


class SerialCom():
    """docstring for CLInfo"""
    def __init__(self, q):
        self.BaudRate = 115200
        self.running = True
        self.numericals = []
        self.queueSRL = q
        self.data = 'a\n'
        self.timeout = 0

        self.t = Thread(target=self.update, args=())

    def start(self):
        self.SP = serial.Serial('/dev/ttyACM0',
                                self.BaudRate,
                                timeout=5)

        while self.SP.is_open is False:
            try:
                self.SP.open()
            except serial.SerialException:
                pass

        self.SP.flush()
        self.SP.flushInput()

        self.t = Thread(target=self.update, args=())
        # self.t.daemon = True
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

            # read data if there is enough in buffer
            if self.SP.in_waiting > FRAME_SIZE:

                # block here until gets to preamble or timesout
                while ord(c) != PREAMBLE:
                    c = self.SP.read(1)
                    # print('{0} : {1}'.format(ord(c), self.timeout))
                    self.timeout += 1
                    if self.timeout > 9000:
                        break

                self.timeout = 0

                # be sure data after preamble arrived
                # if ord(c) == PREAMBLE:
                #     while self.SP.in_waiting < 3:
                #         self.timeout += 1
                #         if self.timeout > 9000:
                #             break

                #     self.timeout = 0

                # fill data with 3 bytes
                # if self.SP.in_waiting == FRAME_SIZE - 1:
                for x in xrange(1, FRAME_SIZE):
                    data.append(ord(self.SP.read(1)))

                self.queueSRL.put(data)

        self.SP.close()

    def clean(self):
        self.SP.flush()
        self.SP.flushInput()
        return
