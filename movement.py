import serial
import logging
from time import sleep

board = serial.Serial('/dev/ttyUSB1', 9600)

x = 0
y = 0
z = 0

def movexclock(distance):
    global x
    try:
        command = "xclk,{}".format(distance)
        board.write(command.encode("utf-8"))
        while True:
            data = board.readline()
            if data == b'Done\r\n':
                break
        board.reset_input_buffer()
        x += distance
    except serial.SerialException as e:
        logging.error("Serial communication error: %s", e)
    except Exception as e:
        logging.error("Unexpected error: %s", e)

def movexanticlock(distance):
    global x
    try:
        command = "xcclk,{}".format(distance)
        board.write(command.encode("utf-8"))
        while True:
            data = board.readline()
            if data == b'Done\r\n':
                break
        board.reset_input_buffer()
        x -= distance
    except serial.SerialException as e:
        logging.error("Serial communication error: %s", e)
    except Exception as e:
        logging.error("Unexpected error: %s", e)

def movey(steps):
    global y
    try:
        command = "yclk,{}".format(steps)
        board.write(command.encode("utf-8"))
        while True:
            data = board.readline()
            if data == b'Done\r\n':
                break
        y += steps
        sleep(1)
    except serial.SerialException as e:
        logging.error("Serial communication error: %s", e)
    except Exception as e:
        logging.error("Unexpected error: %s", e)

def moveycc(steps):
    global y
    try:
        command = "ycclk,{}".format(steps)
        board.write(command.encode("utf-8"))
        while True:
            data = board.readline()
            if data == b'Done\r\n':
                break
        y += steps
        sleep(1)
    except serial.SerialException as e:
        logging.error("Serial communication error: %s", e)
    except Exception as e:
        logging.error("Unexpected error: %s", e)


def movezclock(distance):
    global z
    try:
        command = "zclk,{}".format(distance)
        board.write(command.encode("utf-8"))
        while True:
            data = board.readline()
            if data == b'Done\r\n':
                break
        z -= distance
    except serial.SerialException as e:
        logging.error("Serial communication error: %s", e)
    except Exception as e:
        logging.error("Unexpected error: %s", e)

def movezanticlock(distance):
    global z
    try:
        command = "zcclk,{}".format(distance)
        board.write(command.encode("utf-8"))
        while True:
            data = board.readline()
            if data == b'Done\r\n':
                break
        z += distance
    except serial.SerialException as e:
        logging.error("Serial communication error: %s", e)
    except Exception as e:
        logging.error("Unexpected error: %s", e)

