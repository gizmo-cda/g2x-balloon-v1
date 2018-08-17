#!/usr/bin/env python

import time
import serial

# configuration
delay = 5
output_path = "g2x-balloon-{}.csv".format(int(time.time()))

# open serial connection
ser = serial.Serial(
    port     = '/dev/ttyACM0',
    baudrate = 9600,
    parity   = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout  = 1
)

# read data forever
while True:
    ser.flushInput()
    text = ser.readline()
    data = text.decode('UTF-8').strip().split(' ')

    if len(data) > 10:
        with open(output_path, 'a') as output:
            output.write("{},{}\r\n".format(
                time.strftime("%Y/%m/%d %H:%M:%S"),
                join(",", data[2:10])
            ))

    time.sleep(delay);
