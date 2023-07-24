# import bisect
# import json
# import os
# import re
import time
from datetime import datetime

# import pandas as pd  # sudo apt-get install python3-pandas
import serial
import serial.tools.list_ports

# from os import path
# from sys import displayhook


log_file = "test.log"


def save_packet_to_file(file_name, log_packet):
    # log_packet = timestamp + data  # Concatenate local time
    with open(file=file_name, mode="a") as f:
        f.write(log_packet)


# Main from here:
ports = list(serial.tools.list_ports.grep("ACM"))
if len(ports) == 0:
    print("Cannot find UART port, exiting...")
    exit(-1)

BAUD_RATE = 115200

print("Serial ports: " + str(ports))
UART_PORT_0 = ports[0].device
serial_port = serial.Serial(port=UART_PORT_0, baudrate=BAUD_RATE)

TIMEOUT = 2

log_time_format = "%Y/%m/%d %H:%M:%S | "

# Read from UART and print line-by-line
while True:
    # if True:
    try:
        # Catch the data from UART
        uart_buff = str(serial_port.readline(), "utf8")[:-2]

        time_now = datetime.now()
        # charge_time = time_now.replace(hour=15, minute=27, second=30, microsecond=0)
        # return_time = time_now.replace(hour=15, minute=28, second=30, microsecond=0)
        # stop_time   = time_now.replace(hour=15, minute=29, second=30, microsecond=0)
        log_time = time_now.strftime(log_time_format)

        if uart_buff.find("fP") != -1 or uart_buff.find("fR") != -1 or uart_buff.find("fL") != -1: 
            message = " ==> Failed"
        elif uart_buff.find("t") != -1:
            message = " -> Test"
        elif uart_buff.find("-1") != -1:
            message = " ==> Anchor failed"
        elif uart_buff.find("fA") != -1:
            if uart_buff.find("T13") != -1 or uart_buff.find("T14") != -1:
                dummy = 1
            else:
                message = " ==> Anchor failed"
        else:
            message = " "

        log_content = log_time + uart_buff + message
        save_packet_to_file(log_file, log_content + '\n')  # Save to log file
        print(log_content)

    except Exception:
        print("Retrying...")
        time.sleep(TIMEOUT)

# End
