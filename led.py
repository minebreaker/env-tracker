import time
from machine import Pin # type: ignore
import pins


ledPin = Pin(pins.LED, Pin.OUT)

def led_booted():
  count = 3
  while count > 0:
    ledPin.on()
    time.sleep_ms(100)
    ledPin.off()
    time.sleep_ms(300)
    count -= 1


def led_exception():
  count = 2
  while count > 0:
    ledPin.on()
    time.sleep_ms(1000)
    ledPin.off()
    time.sleep_ms(1000)
    count -= 1

def led_error():
  ledPin.on()

def led_serious_error():
  while True:
    ledPin.on()
    time.sleep_ms(200)
    ledPin.off()
    time.sleep_ms(200)
