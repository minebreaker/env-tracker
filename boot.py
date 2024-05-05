from machine import Pin
import time

import mhz19c
import bme680
from net import connect_wifi, remote_log
import config as c

def main():
  try:
    connect_wifi()

    remote_log("INFO", f"starting up device ...\n{get_device_info()}")

    mhz19c.read_co2()
    bme680.read_tph()

    ledPin = Pin(2, Pin.OUT)
    while True:
      ledPin.on()
      time.sleep(1)
      ledPin.off()
      time.sleep(1)

  except Exception as e:
    import sys
    try:
      sys.print_exception(e)
      led_error()
      remote_log("ERROR", "uncaught error:\n" + str(e))
    except Exception as e2:
      print("exception during handling exception")
      try:
        sys.print_exception(e2)
      finally:
        led_serious_error()


def get_device_info():
  import machine

  try:
    freq = machine.freq()
    unique_id = machine.unique_id()
    return f"device_id: {c.DEVICE_ID}\nfrep: {freq}\nunique_id: {unique_id}"
  except Exception as e:
    import sys
    sys.print_exception(e)
    return "failed to read"


def led_error():
  ledPin = Pin(2, Pin.OUT)
  ledPin.on()

def led_serious_error():
  ledPin = Pin(2, Pin.OUT)
  while True:
    ledPin.on()
    time.sleep_ms(200)
    ledPin.off()
    time.sleep_ms(200)


main()
