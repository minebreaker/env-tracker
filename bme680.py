from machine import Pin, I2C


def read_tph():
  sda = Pin(6, Pin.PULL_UP)
  scl = Pin(7, Pin.PULL_UP)
  i2c = I2C(0, sda = sda, scl = scl)
  DEV = 0x77
  # print("scan: " +  str(i2c.scan()))
  id = i2c.readfrom_mem(DEV, 0xD0, 1)
  print(f"i2c id: {id}")
  ctrl_meas = i2c.readfrom_mem(DEV, 0x74, 1)
  print(f"ctrl_meas: {ctrl_meas}")
  data = i2c.readfrom_mem(DEV, 0x1F, 8)
  print(f"data: {data}")
