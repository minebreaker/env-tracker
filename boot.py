from machine import Pin
import time

DEVICE_ID = "device0"
WIFI_SSID =
WIFI_PASSWORD =
SERVER = "192.168.0.5"
PORT = "8080"

def main():
  try:
    connect_wifi()

    remote_log("INFO", f"starting up device ...\n{get_device_info()}")

    read_co2()
    read_tph()

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


def connect_wifi():
  import network

  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  if not wlan.isconnected():
    print("connecting to network...")
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
      pass
  print("network config: ", wlan.ifconfig())


def remote_log(level, value):
  import socket
  import json

  s = socket.socket()
  ai = socket.getaddrinfo(SERVER, PORT)
  addr = ai[0][-1]
  s.connect(addr)

  body = {"deviceId": DEVICE_ID, "level": level, "value": value}
  body_str = json.dumps(body)
  print(body_str)
  msg = b"POST /logger HTTP/1.0\r\n" + \
         "Content-Type: application/json\r\n" + \
         "Content-Length: " + str(len(str(body_str))) + "\r\n" + \
         "\r\n" + \
         body_str

  a_len = len(msg)
  print(f"msglen {a_len}")
  w_len = s.send(msg)
  print(f"written len {w_len}")
  if a_len != w_len:
    raise Exception(f"written length does not match. actual: {a_len}, written: {w_len}")

  res = s.read()
  print(res)

  if res.startswith("HTTP/1.1 204"):
    pass
  elif res.startswith("HTTP/1.1 4"):
    raise Exception("4xx client error", res)
  elif res.startswith("HTTP/1.1 5"):
    raise Exception("5xx server error", res)
  else:
    raise Exception("unknown response", res)


def get_device_info():
  import machine

  try:
    freq = machine.freq()
    unique_id = machine.unique_id()
    return f"device_id: {DEVICE_ID}\nfrep: {freq}\nunique_id: {unique_id}"
  except Exception as e:
    import sys
    sys.print_exception(e)
    return "failed to read"


def read_co2():
  from machine import UART
  serial = UART(1, tx=21, rx=20, baudrate=9600, bits=8, parity=None, stop=1)
  res = serial.write(b"\xFF\x01\x86\x00\x00\x00\x00\x00\x79")
  print(f"written bytes: {res}")
  # Arbitrary timeout
  time.sleep_ms(1000)
  result = serial.read(9)
  print("co2: " + str(result))


def read_tph():
  from machine import I2C
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
