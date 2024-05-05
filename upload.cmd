set PORT=COM3

ampy -p %PORT% bme680.py
ampy -p %PORT% config.py
ampy -p %PORT% mhz19c.py
ampy -p %PORT% net.py
ampy -p %PORT% boot.py
