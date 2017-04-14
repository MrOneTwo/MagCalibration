#!python2
# -*- coding: UTF-8 -*-

import serial
import time
import os

FRAME_SIZE_BIN = 4
FRAME_SIZE_2 = 32
PREAMBLE_BIN = 0xAA
PREAMBLE_2 = 'M'

baud_rate = 115200
fifo_file = None
fifo_file_path = '/tmp/serialPort.fifo'
data = 'a\n'
running = True

try:
    fifo_file = os.mkfifo(fifo_file_path)
except OSError as e:
    if e.errno == 17:
        print(' -ex--->  Fifo file exists.')
        pass

serial_port = serial.Serial('/dev/sensor_uart',
                            baud_rate,
                            timeout=0.5)


def start():
    """TODO: Docstring for start.
    :returns: TODO

    """

    try:
        serial_port.close()
        print('Trying to open the port which is opened: {0}'.format(serial_port.is_open))
        time.sleep(2)
        serial_port.open()
    except Exception as e:
        print(' -ex--->  Serial port opening failed, because: {0}'.format(e))
        return False

    return True


def main():
    """TODO: Docstring for main.
    :returns: TODO

    """
    global running
    global working_properly_trust

    # n = 0
    # while n < 1000:
    # serial_port.write('mag\n')
    # n += 1

    while running:
        # clear data
        c = 'a'
        d = 'a'
        data = list()

        c = serial_port.read(1)
      
        if c == PREAMBLE_2:
            d = serial_port.read(31)

        # get rid of 'AG.'
        d = d[3:]
        # read the data
        d = d.strip()

        try:
            data = d.split('.')
            data = map(int, data)
        except:
            continue

        print('Data = {0}'.format(data))
        fifo_file = open(fifo_file_path, 'w')
        fifo_file.write(str(data[0]))
        fifo_file.write(';')
        fifo_file.write(str(data[1]))
        fifo_file.write(';')
        fifo_file.write(str(data[2]))
        fifo_file.write('\n')
        fifo_file.close()


if __name__ == '__main__':
    try:
        if start() is True:
            main()
    except Exception as e:
        print(' -ex--->  Exception, being: {0}'.format(e))
        serial_port.close()

