#!/usr/bin/env python3

import os
import datetime
from time import sleep
from syslog import syslog

def set_wlan0_down_up():
    os.system('sudo ip link set wlan0 down')
    sleep(5)
    os.system('sudo ip link set wlan0 up')

address = '172.16.0.1'
action1_attempt_count = 4
action2_attempt_count = 8

failed_pings = 0

while True:
    response = os.system('ping -c 1 ' + address)
#    print(response)
    if response != 0:
        failed_pings += 1
        syslog(f"ping {address} failure: {failed_pings}")
    
    if failed_pings == action1_attempt_count:
        syslog(f"4x pings {address} failed, bouncing wlan0")
        set_wlan0_down_up()
        
    if failed_pings == action2_attempt_count:
        syslog(f"8x pings {address} failed, rebooting CatFlapPi")
        os.system('/sbin/reboot')
        
    if response == 0 and failed_pings != 0:
        syslog(f"ping {address} success, after {failed_pings} failures, " \
            "reset failed ping count to 0")
        failed_pings = 0
    
    sleep(30)