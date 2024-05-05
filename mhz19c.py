import time
from machine import UART
from net import http_post
import config as c
from binascii import b2a_base64 as base64

def read_co2():
  serial = UART(1, tx=21, rx=20, baudrate=9600, bits=8, parity=None, stop=1)
  res = serial.write(b"\xFF\x01\x86\x00\x00\x00\x00\x00\x79")
  print(f"written bytes: {res}")
  # Arbitrary timeout
  time.sleep_ms(1000)
  result = serial.read(9)
  print(f"co2: {result}")


  body = {
    "deviceId": c.DEVICE_ID,
    "roomId": c.ROOM_ID,
    "value": base64(result, False)
  }
  http_post("/log/mhz19c", body)
