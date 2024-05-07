import time
import sys

from led import led_exception, led_error, led_serious_error
import mhz19c
import bme680
from net import remote_log


def main():
  try:
    while True:
      try:
        bme680.read_tph()
      except Exception as e:
        handle_exception(e)
      try:
        mhz19c.read_co2()
      except Exception as e:
        handle_exception(e)

      time.sleep(30)

  except Exception as e:
    try:
      remote_log("ERROR", "uncaught error in main:\n" + str(e))
      led_error()
    except Exception as e2:
      try:
        print("exception during handling exception in main")
        sys.print_exception(e2)
      finally:
        led_serious_error()
    raise e


def handle_exception(e):
  try:
    try:
      remote_log("WARN", "uncaught error in the exception handler:\n" + str(e))
    finally:
      pass
    sys.print_exception(e)
    led_exception()
  except Exception as e2:
    print("exception during handling exception in the exception handler")
    sys.print_exception(e2)


main()
