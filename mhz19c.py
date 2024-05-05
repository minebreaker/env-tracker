import time
from machine import UART

def read_co2():
  serial = UART(1, tx=21, rx=20, baudrate=9600, bits=8, parity=None, stop=1)
  res = serial.write(b"\xFF\x01\x86\x00\x00\x00\x00\x00\x79")
  print(f"written bytes: {res}")
  # Arbitrary timeout
  time.sleep_ms(1000)
  result = serial.read(9)
  print("co2: " + str(result))
