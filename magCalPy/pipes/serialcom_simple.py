#!python2
# -*- coding: UTF-8 -*-

import serial
import time
import os
import re
import collections

DOING = 'CALIBRATION OF MAGNETOMETER'
CONSUMER_PRESENT = True

FRAME_SIZE_BIN = 4
FRAME_SIZE_2 = 32
PREAMBLE_BIN = 0xAA

baud_rate = 115200
fifo_file = None
fifo_file_path = '/tmp/serialPort.fifo'
data = 'a\n'
running = True

incoming_data_buffer = collections.deque(maxlen=30)

if DOING == 'CALIBRATION OF MAGNETOMETER':
    PREAMBLE = '#'
    pattern = re.compile("#M-R="
                         "[+-]?[0-9]+[\.][0-9][0-9]"
                         ","
                         "[+-]?[0-9]+[\.][0-9][0-9]"
                         ","
                         "[+-]?[0-9]+[\.][0-9][0-9]")
else:
    PREAMBLE = '#'
    pattern = re.compile("#YPR="
                         "[+-]?[0-9]+[\.][0-9][0-9]"
                         ","
                         "[+-]?[0-9]+[\.][0-9][0-9]"
                         ","
                         "[+-]?[0-9]+[\.][0-9][0-9]")

try:
    fifo_file = os.mkfifo(fifo_file_path)
except OSError as e:
    if e.errno == 17:
        print(' -ex--->  Fifo file exists.')
        pass

serial_port = serial.Serial('/dev/ttyUSB1',
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
    global data
    global running
    global working_properly_trust

    while running:
        # clear data
        data_bytes = ''

        if serial_port.in_waiting > 0:
            incoming_data_buffer.append(serial_port.read(1))

        try:
            if incoming_data_buffer[0] == PREAMBLE:
                if pattern.match(''.join(incoming_data_buffer)):
                    try:
                        split_end_index = list(incoming_data_buffer).index('#', 1)
                    except ValueError:
                        continue
                    data_bytes = ''.join(incoming_data_buffer)
                    data_bytes = data_bytes[5:split_end_index]
                    data_bytes = data_bytes.strip()
                    data_bytes = data_bytes.rstrip()
                    data_bytes = data_bytes.replace('\r', '')
                    data_bytes = data_bytes.replace('\n', '')
                    data = data_bytes.split(',')
                    if DOING == 'CALIBRATION OF MAGNETOMETER':
                        data = map(float, data)
                        data = map(int, data)
                    else:
                        data = map(float, data)
                    print('Y: {0}, P: {1}, R: {2}'.format(data[0], data[1], data[2]))

                if CONSUMER_PRESENT and ((type(data[0]) == int) or (type(data[0]) == float)):
                    try:
                        fifo_file = open(fifo_file_path, 'w')
                        fifo_file.write(str(data[0]))
                        fifo_file.write(';')
                        fifo_file.write(str(data[1]))
                        fifo_file.write(';')
                        fifo_file.write(str(data[2]))
                        fifo_file.write('\n')
                        fifo_file.close()
                    except IOError as e:
                        fifo_file.close()
                        pass

                else:
                    # print('Pattern not matching.')
                    continue
        except IndexError:
            continue



if __name__ == '__main__':
    #  try:
    if start() is True:
        main()
    #  except Exception as e:
        #  print(' -ex--->  Exception, being: {0}'.format(e))
        #  serial_port.close()

