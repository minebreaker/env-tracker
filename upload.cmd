set PORT=COM3

ampy -p %PORT% put bme680.py
ampy -p %PORT% put config.py
ampy -p %PORT% put led.py
ampy -p %PORT% put mhz19c.py
ampy -p %PORT% put net.py
ampy -p %PORT% put net.py
ampy -p %PORT% put pins.py
ampy -p %PORT% put tgs8100.py

ampy -p %PORT% put main.py
ampy -p %PORT% put boot.py
