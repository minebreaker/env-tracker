from machine import Pin, ADC # type: ignore
from time import sleep_ms
import time
from binascii import b2a_base64 as base64

from net import http_post
import config as c
import pins


def read():
  pulse = Pin(pins.GPIO_TSG8100_PULSE, Pin.OUT)
  adc_pin = Pin(pins.GPIO_TGS8100_ADC)
  adc = ADC(adc_pin, atten=ADC.ATTN_11DB)


  start_time = time.ticks_ms()
  pulse.on()

  sleep_ms(1)
  value = adc.read_uv()

  pulse.off()

  print(f"TSG8100 ADC {value}")

  body = {
    "deviceId": c.DEVICE_ID,
    "roomId": c.ROOM_ID,
    "value": str(value)
  }
  http_post("/log/tgs8100", body)
