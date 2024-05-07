from time import sleep_ms
from machine import UART # type: ignore
from net import http_post
import config as c
from binascii import b2a_base64 as base64


def read_co2():
  serial = UART(1, tx=21, rx=20, baudrate=9600, bits=8, parity=None, stop=1)

  done = False
  retry_limit = 100
  result = b""
  while not done:
    if retry_limit <= 0:
      raise Exception("MHZ19C read retry limit exceeded. partial read: " + str(result))

    # FIXME: should check written bytes
    res = serial.write(b"\xFF\x01\x86\x00\x00\x00\x00\x00\x79")
    print(f"written bytes: {res}")

    sleep_ms(50)

    read = serial.read(9 - len(result))
    if read is None:
      pass
    else:
      result += read
      if len(result) == 9:
        done = True
        pass

    retry_limit -= 1


  print(f"co2: {result}")

  body = {
    "deviceId": c.DEVICE_ID,
    "roomId": c.ROOM_ID,
    "value": base64(result, False)
  }
  http_post("/log/mhz19c", body)
