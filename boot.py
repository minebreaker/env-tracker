import sys
import machine # type: ignore
import network # type: ignore

import config as c
from led import led_booted, led_error, led_serious_error
from net import remote_log, HTTPError

def main():
  
  try:
    wlan = connect_wifi()

    remote_log("INFO", f"starting up device ...\n{get_device_info(wlan)}")
    led_booted()
  except Exception as e:
    try:
      remote_log("ERROR", "uncaught error during boot:\n" + str(e))
      led_error()
    except Exception as e2:
      try:
        print("exception during handling exception during boot")
        sys.print_exception(e2)
      finally:
        led_serious_error()
    raise e


def connect_wifi():
  network.hostname("esp32-env-tracker-" + c.DEVICE_ID)
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  if not wlan.isconnected():
    print("connecting to network...")
    wlan.connect(c.WIFI_SSID, c.WIFI_PASSWORD)
    while not wlan.isconnected():
      pass
  print("network config: ", wlan.ifconfig())
  return wlan


def get_device_info(wlan):
  from binascii import hexlify
  try:
    freq = machine.freq()
    unique_id = hexlify(machine.unique_id()).decode().upper()
    mac = hexlify(wlan.config("mac")).decode().upper()
    return f"device_id: {c.DEVICE_ID}\n" + \
           f"frep:      {freq}\n" + \
           f"unique_id: {unique_id}\n" + \
           f"mac:       {mac}"
  except Exception as e:
    import sys
    sys.print_exception(e)
    return "failed to read"

main()
