import time
from machine import Pin # type: ignore


def led_booted():
  ledPin = Pin(2, Pin.OUT)
  count = 3
  while count > 0:
    ledPin.on()
    time.sleep_ms(100)
    ledPin.off()
    time.sleep_ms(300)
    count -= 1


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
