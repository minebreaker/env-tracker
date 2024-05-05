from machine import Pin, I2C
from time import sleep_ms
from net import http_post

import config as c
from binascii import b2a_base64 as base64


# BEM680 I2C addr
DEV = 0x77

def read_tph():
  sda = Pin(6, Pin.PULL_UP)
  scl = Pin(7, Pin.PULL_UP)
  i2c = I2C(0, sda = sda, scl = scl)
  # print("scan: " +  str(i2c.scan()))

  # device id
  id = i2c.readfrom_mem(DEV, 0xD0, 1)

  # calibration data
  par_t1 = i2c.readfrom_mem(DEV, 0xE9, 2)
  par_t2t3 = i2c.readfrom_mem(DEV, 0x8A, 3)
  par_p = i2c.readfrom_mem(DEV, 0x8E, 19)
  par_h = i2c.readfrom_mem(DEV, 0xE1, 8)

  i2c.writeto_mem(DEV, 0x72, b"\x01") # set osrs_h x1
  i2c.writeto_mem(DEV, 0x74, ((0x01 << 5) | (0x01 << 2) | 0x01).to_bytes(1, "big")) # set osrs_t x1, osrs_p x2, force mode

  limit = 100
  done = False
  while not done:
    sleep_ms(10)
    state = int.from_bytes(i2c.readfrom_mem(DEV, 0x74, 1), "big") & 0x01
    print(f"mode: {state}")
    if state == 0:
      done = True
    
    limit -= 1
    if limit <= 0:
      raise Exception("BME680 read retry limit exceeded.")
  
  temp_adc = i2c.readfrom_mem(DEV, 0x22, 3)
  press_adc = i2c.readfrom_mem(DEV, 0x1F, 3)
  hum_adc = i2c.readfrom_mem(DEV, 0x25, 2)

  from binascii import b2a_base64 as base64
  print(f"i2c id:    {id}")
  print(f"par_t1:    {par_t1}")
  print(f"par_t2t3:  {par_t2t3}")
  print(f"par_p:     {par_p}")
  print(f"par_h:     {par_h}")
  print(f"temp_adc:  {temp_adc}")
  print(f"press_adc: {press_adc}")
  print(f"hum_adc:   {hum_adc}")

  body = {
    "deviceId": c.DEVICE_ID,
    "roomId": c.ROOM_ID,
    "parT1": base64(par_t1, False),
    "parT2T3": base64(par_t2t3, False),
    "parP": base64(par_p, False),
    "parH": base64(par_h, False),
    "tempAdc": base64(temp_adc, False),
    "pressAdc": base64(press_adc, False),
    "humAdc": base64(hum_adc, False)
  }
  http_post("/log/bme680", body)
