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


def save_packet_to_file(file_name, timestamp, data):
    log_packet = timestamp + data  # Concatenate local time
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

charge_profile = 2
normal_profile = 1
not_configure_profile = 0
# tag_setup_mode = not_configure_profile
configure_mode = 0
all_tag_confirmed = 0

log_time_format = "%m:%d:%Y %H:%M:%S "

# print(time_now)
# if time_now < return_time:
#     print("time_now < return_time")
# else:
#     print("No, wrong")

button = 0

# Wake up every 15s for charging
if button == 2:
    print("Sending 2")
    serial_port.write("2".encode())  # Sending charging configure packet

# Wake up every 5m
if button == 1:
    print("Sending 1")
    serial_port.write("1".encode())  # Sending normal configure packet

# No config
if button == 0:
    print("Sending 0")
    serial_port.write("0".encode())  # Stop sending Lora configure packets

# Read from UART and print line-by-line
while True:
    # if True:
    try:
        # Catch the data from UART
        lora_packet = str(serial_port.readline(), "utf8")

        time_now = datetime.now()
        # charge_time = time_now.replace(hour=15, minute=27, second=30, microsecond=0)
        # return_time = time_now.replace(hour=15, minute=28, second=30, microsecond=0)
        # stop_time   = time_now.replace(hour=15, minute=29, second=30, microsecond=0)
        log_time = time_now.strftime(log_time_format)

        # Only process correct packages with starting 'I'
        if lora_packet[0] == "I":
            # Data analysis
            # data from the nodes (coming from UART)
            data = lora_packet
            # depending on the calibration for each device
            offset = 0

            data["SOC"] = data["Vbat"]
            display_log = log_time + str(data)
            print(display_log)

            save_packet_to_file(log_file, log_time, lora_packet)  # Save to log file
        else:
            if lora_packet[0] == "A":  # We want to see 'A' packets
                data = lora_packet
                save_packet_to_file(log_file, log_time, lora_packet)  # Save to log file
            if lora_packet[0] != "S":
                print(str(lora_packet))

    except Exception:
        print("Retrying...")
        time.sleep(TIMEOUT)

# End
