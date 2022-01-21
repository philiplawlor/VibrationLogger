#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import sqlite3
from datetime import datetime

__version__ = "0.1.0"

debug = False

DTS_FORMAT = '%Y%m%d%H%M%S'
msg = "Movement Detected!!!!"
#GPIO SETUP
channel = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

def callback(channel):
        d = datetime.now()
        if GPIO.input(channel):
                
                if (debug): print(msg, d)
                log_to_db(d)
                if (debug): list_log(d)
        else:
                if (debug): print(msg, d)
                log_to_db(d)
                if (debug): list_log(d)

def log_to_db(when):
    try:
        con = sqlite3.connect('logs.db')
        cur = con.cursor()
        cur.execute('''CREATE TABLE log
                   (date text, text text, calledBy text)''')
        con.commit()
    except:
        if (debug): print('tables exist')
    finally:
        if (debug): print('db connected')
        
    now = datetime.now()
    if (debug): print("INSERT INTO log VALUES ('%s','%s','%s')" % (when , msg, 'motion'))
    cur.execute("INSERT INTO log VALUES ('%s','%s','%s')" % (when , msg, 'motion'))
    con.commit()

def list_log(when):
    con = sqlite3.connect('logs.db')
    for row in con.execute("select count(*) from log ORDER BY 1 desc LIMIT 5"):
        print(row[0])
#    con.close
    for row in con.execute("select * from log ORDER BY 1 desc LIMIT 5"):
        print(row)
    con.close
    
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change


# infinite loop
while True:
        time.sleep(1)
