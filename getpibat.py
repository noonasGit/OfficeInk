from datetime import datetime
import os
from pisugar import *
import socket

from dataclasses import dataclass

@dataclass
class battery:
    #pisugar : bool
    level : int
    state : str


def get_pibatt():
    applog("Battery subsystem","Connecting to battery ...")
    try:
        applog("Battery subsystem","Force a time sync...")
        picmd ="echo 'rtc_rtc2pi' | nc -q 0 127.0.0.1 8423"
        os.system(picmd)
    except:
        applog("Battery subsystem","Force a time sync - FAILED")

    applog("Battery subsystem","Getting battery level and state...")
    try:
        conn, event_conn = connect_tcp('127.0.0.1')
        s = PiSugarServer(conn, event_conn)

        s.register_single_tap_handler(lambda: print('single'))
        s.register_double_tap_handler(lambda: print('double'))
        battery.level = int(s.get_battery_level())
        bstate = s.get_battery_charging()
        if bstate == True:
            battery.state = "Charging"
        else:
            battery.state = "Not Charging"

        return_data = battery(level=battery.level,state=battery.state)
        applog("Battery subsystem","Battery level: "+str(battery.level)+"%")
        applog("Battery subsystem","Battery state: "+battery.state)
        event_conn.close()
    except socket.error:
        applog("System","Getting battery state error")
        battery.level = -1
        battery.state = "Unknown"
        return_data = battery(level=battery.level,state=battery.state)

    return return_data

def applog(app_section: str ,app_message: str):
    date_time_stamp = datetime.now().strftime("%d.%b.%Y, %H:%M:%S")
    print(date_time_stamp+" | "+app_section+" | "+app_message)
