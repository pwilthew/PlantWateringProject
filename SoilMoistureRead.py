#!/usr/bin/env python2

"""Waters a plant when its soil moisture is less than 10% until
it is 75%."""

import Adafruit_ADS1x15
import datetime
import RPi.GPIO as GPIO
import time


def get_percent_wet():
    """Reads the Capacitive Soil Moisture Sensor value to
    determine the percentage of moisture.
    
    The sensor outputs an analog signal that is converted
    into digital by the ADS1115 ADC (Analog to Digital) 
    chip. This digital value is compared to the minimum
    (most wet) value and the maximum (most dry) to get
    the percentage.
    
    Choose a gain of 1 for reading voltages from 0 to 
    4.09V, or pick a different gain to change the range
    of voltages that are read:
    - 2/3 = +/-6.144V
    -   1 = +/-4.096V
    -   2 = +/-2.048V
    -   4 = +/-1.024V
    -   8 = +/-0.512V
    -  16 = +/-0.256V"""
    # Create an ADS1115 ADC (16-bit) instance.
    adc = Adafruit_ADS1x15.ADS1115()

    GAIN = 1
    DRY = 20280 # 100% Dry
    WET = 10140 # 100% Wet

    value = adc.read_adc(0, gain=GAIN)
    
    # print "value: %d" % value
    
    percent_dry = ((value - WET)*100)/(DRY-WET)
    percent_wet = 100 - percent_dry

    return percent_wet


def pump_water(pump_pin, delay=1):
    """Sends the water pump motor a high signal until
    the soil is 75% wet."""
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pump_pin, GPIO.OUT)
    timeout = time.time() + 1.5*60  # 1.5 minutes

    try:
        print "Watering plant..."
        GPIO.output(pump_pin, GPIO.HIGH)

        while get_percent_wet() < 75:
            time.sleep(delay)
            if time.time() > timeout:
                break

        GPIO.output(pump_pin, GPIO.LOW)
        GPIO.cleanup(pump_pin)
        return

    except:
        GPIO.cleanup(pump_pin)

    return

def get_last_watered():
    """Returns the date when the last watering ocurred."""
    with open("last_watered.txt", "r") as f:
        last_watered = f.read()
    return last_watered


def main():
    """Steps to determine if the soil of a plant needs water
    or not. If it does, then water it."""
    percent_wet = get_percent_wet()

    if percent_wet <= 10:
        message = "Water needed, moisture is at %d%%." % percent_wet
        print message
    else:
        message = "Water not needed, moisture is at %d%%." % percent_wet
        print message
        return message

    pump_water(37)

    with open("last_watered.txt", "w") as f:
        f.write("Last watered on %s because moisture was at %s." % (
            datetime.datetime.today().strftime("%A, %d. %B %Y %I:%M%p"),
            percent_wet))

    return message


if __name__ == '__main__':
    main()
