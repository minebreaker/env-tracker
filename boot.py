import sys
from machine import Pin # type: ignore
import time

import mhz19c
import bme680
from net import connect_wifi, remote_log
import config as c

def main():
  try:
    connect_wifi()

    remote_log("INFO", f"starting up device ...\n{get_device_info()}")

    while True:
      try:
        bme680.read_tph()
      except Exception as e:
        handle_exception(e)
      try:
        mhz19c.read_co2()
      except Exception as e:
        handle_exception(e)

      time.sleep(30)

  except Exception as e:
    try:
      sys.print_exception(e)
      remote_log("ERROR", "uncaught error:\n" + str(e))
      led_error()
    except Exception as e2:
      try:
        print("exception during handling exception")
        sys.print_exception(e2)
      finally:
        led_serious_error()


def get_device_info():
  import machine # type: ignore

  try:
    freq = machine.freq()
    unique_id = machine.unique_id()
    return f"device_id: {c.DEVICE_ID}\nfrep: {freq}\nunique_id: {unique_id}"
  except Exception as e:
    import sys
    sys.print_exception(e)
    return "failed to read"


def handle_exception(e):
  try:
    sys.print_exception(e)
    led_exception()
  except Exception as e2:
    print("exception during handling exception")
    sys.print_exception(e2)


def led_exception():
  ledPin = Pin(2, Pin.OUT)
  count = 2
  while count > 0:
    ledPin.on()
    time.sleep_ms(1000)
    ledPin.off()
    time.sleep_ms(1000)
    count -= 1

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
