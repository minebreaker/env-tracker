import network
import config as c
import socket
import json

def connect_wifi():
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  if not wlan.isconnected():
    print("connecting to network...")
    wlan.connect(c.WIFI_SSID, c.WIFI_PASSWORD)
    while not wlan.isconnected():
      pass
  print("network config: ", wlan.ifconfig())


def http_post(path, body):

  s = socket.socket()
  ai = socket.getaddrinfo(c.SERVER, c.PORT)
  addr = ai[0][-1]
  s.connect(addr)

  body_str = json.dumps(body)
  msg = b"POST " + path + " HTTP/1.0\r\n" + \
         "Content-Type: application/json\r\n" + \
         "Content-Length: " + str(len(body_str)) + "\r\n" + \
         "\r\n" + \
         body_str

  print("http request: " + str(msg))
  a_len = len(msg)
  w_len = s.send(msg)
  if a_len != w_len:
    raise Exception(f"written length does not match. probably the bug. actual: {a_len}, written: {w_len}")

  res = s.read()
  print("http response: " + str(res))

  if res.startswith("HTTP/1.1 204"):
    pass
  elif res.startswith("HTTP/1.1 4"):
    raise Exception("4xx client error", res)
  elif res.startswith("HTTP/1.1 5"):
    raise Exception("5xx server error", res)
  else:
    raise Exception("unknown response", res)


def remote_log(level, value):
  body = {"deviceId": c.DEVICE_ID, "level": level, "value": value}
  http_post("/logger", body)
