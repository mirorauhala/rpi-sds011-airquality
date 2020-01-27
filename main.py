#!/usr/bin/env python3
import requests
from phue import Bridge
from sds011 import SDS011
import psycopg2
import json
import schedule
import time
from datetime import datetime
import os

def setReading(reading, type):
    try:
        connection = psycopg2.connect(
            host=os.environ['PG_HOST'],
            port=os.environ['PG_PORT'],
            dbname=os.environ['PG_DB'],
            user=os.environ['PG_USER'],
            password=os.environ['PG_PASS']
        )
        cursor = connection.cursor()
        cursor.execute("INSERT INTO readings (reading, type) VALUES (%s, %s);", (float(reading), type) )
        connection.commit()
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()

def getAirQuality():
    on()
    time.sleep(15)
    sensor = SDS011(os.environ['USB_DEVICE'], use_query_mode=True)
    data = sensor.query()
    off()
    return data

def getTemperature():
    hue = Bridge(os.environ['HUE_IP'])
    return hue.get_sensor(22)['state']['temperature'] / 100

def off():
    sensor = SDS011(os.environ['USB_DEVICE'], use_query_mode=True)
    sensor.sleep(sleep=True)

def on():
    sensor = SDS011(os.environ['USB_DEVICE'], use_query_mode=True)
    sensor.sleep(sleep=False)

def measurement():
    print("Getting temperature")

    if os.environ['USE_HUE']:
        temperature = getTemperature()

    print("Getting air quality")
    airquality = getAirQuality()

    setReading(temperature, 'temp')
    setReading(airquality[0], 'pm25')
    setReading(airquality[1], 'pm10')

    print("Temp: " + str(temperature) + "C")
    print("PM2.5: " + str(airquality[0]))
    print("PM10: " + str(airquality[1]))


schedule.every(1).hour.do(measurement)

print("PG_HOST: " + os.environ['PG_HOST'])
print("PG_PORT: " + os.environ['PG_PORT'])
print("PG_DB: " + os.environ['PG_DB'])
print("PG_USER: " + os.environ['PG_USER'])
print("PG_PASS: " + os.environ['PG_PASS'])
print("USE_HUE: " + os.environ['USE_HUE'])

while True:
    schedule.run_pending()
    time.sleep(1)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)