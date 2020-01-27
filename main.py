import requests
from phue import Bridge
from sds011 import SDS011
import psycopg2
import json
import schedule
import time
from datetime import datetime

def setReading(reading, type):
    try:
        connection = psycopg2.connect(
            host="192.168.86.89",
            port=5433,
            dbname="airquality",
            user="postgres",
            password="postgres"
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
    sensor = SDS011("/dev/tty.usbserial-14310", use_query_mode=True)
    data = sensor.query()
    off()
    return data

def getTemperature():
    hue = Bridge('192.168.86.157')
    return hue.get_sensor(22)['state']['temperature'] / 100

def off():
    sensor = SDS011("/dev/tty.usbserial-14310", use_query_mode=True)
    sensor.sleep(sleep=True)

def on():
    sensor = SDS011("/dev/tty.usbserial-14310", use_query_mode=True)
    sensor.sleep(sleep=False)

def measurement():
    print("Getting temperature")

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

while True:
    schedule.run_pending()
    time.sleep(1)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)