import argparse
import serial
import time
import logging
import os

def check_confd_init (connection):
    while True:
        connection.write("<given command>\r".encode("utf-8"))
        result = connection.read_until("#".encode("utf-8"))
        result = result.decode("utf-8", "ignore")
        logging.info(result)
        if "<checking message>" in result:
            logging.info("Device is ready.")
            break
        else:
            time.sleep(10)
    return

def mesure_switch_time (switch, connection):

    time_start = time.time()
    connection.write((switch+'\r').encode("utf-8"))
    output=connection.read_until("#".encode("utf-8"))
    time_finish = time.time()
    logging.info(output.decode("utf-8", errors="ignore"))
    switch_time = get_duration(time_start,time_finish)

    return switch_time

def get_duration(start,finish):
    time_duration = finish-start
    time_duration = float(str(time_duration))
    return time_duration

def connect(serial_name):
    """This function is create serial connection and check the time duration of commands."""
    try:
        serial_connect=serial.Serial()
        serial_connect.baudrate=115200
        serial_connect.port=serial_name
        serial_connect.timeout=60
        serial_connect.open()
        if serial_connect.isOpen():
            logging.info('Connection is established\nStarting test')
            logging.info("Sending device to restart")
            serial_connect.write("<given command>\r".encode("utf-8"))
            output=serial_connect.readline()
            logging.info(output.decode("utf-8", errors="ignore"))

            serial_connect.write("<given command>\r".encode("utf-8"))
            output = serial_connect.read_until("<checking message>".encode("utf-8"))
            #logging.info(output.decode("utf-8", errors="ignore"))

            check_confd_init(serial_connect)

            time.sleep(6)

            serial_connect.write('<given command>\r'.encode("utf-8"))
            output=serial_connect.read_until("<checking message>".encode("utf-8"))
            logging.info(output.decode("utf-8", errors="ignore"))

    except serial.SerialException:
        print('ERROR: Connection could not be established.\nPlease check serial_name or make sure that device is connected.') 

def args_parser():
    """This function is parsing serial line name from terminal and send that"""
    parser = argparse.ArgumentParser(description='Checking time duration for confd prompt')
    parser.add_argument('serial_name', type=str, help='name of the serial line')
    args = parser.parse_args()
    serial_line = args.serial_name
    return serial_line

if __name__ == "__main__":
    if os.path.exists("file.log"):
        os.remove("file.log")
    logging.basicConfig(filename='file.log', level=logging.INFO)
    serial_name = args_parser()
    connect(serial_name)