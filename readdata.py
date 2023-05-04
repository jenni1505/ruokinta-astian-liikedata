import json, requests
from time import sleep
import matplotlib.pyplot as plt # pip install matplotlib
import os
import sys
import time
import smbus
from time import time, sleep
from urllib.request import urlopen
import sys

from imusensor.MPU9250 import MPU9250
#import bmp280 as BMP280

address = 0x68
bus = smbus.SMBus(1)
imu = MPU9250.MPU9250(bus, address)
#temp = BMP280.BMP280(bus, address)

imu.begin()
alfa = 0
while True:
    rotta = 0
    imu.readSensor()
    imu.computeOrientation()
    #temp = temp.get_temperature()
    #print(temp)

    print ("Kiihtyvyysmittari x: {0:.2f} ; y : {1:.2f} ; z : {2:.2f}".format(imu.AccelVals[0], imu.AccelVals[1], imu.AccelVals[2]))
    print ("Pyörimismäärä: x: {0:.2f} ; y : {1:.2f} ; z : {2:.2f}".format(imu.GyroVals[0], imu.GyroVals[1], imu.GyroVals[2]))
    print ("Kallistuminen: {0:.2f} ; Nyökkääminen : {1:.2f}".format(imu.roll, imu.pitch))

    

    s = {}
    s['alfa'] = alfa
    s['x'] = imu.roll
    s['y'] = imu.pitch
    #s['z'] = 0
    ss = json.dumps(s)
    response = requests.post("http://localhost:5000/uusimittaus", data = ss)
    print(ss)
    alfa += 1
    
    sleep(1)
