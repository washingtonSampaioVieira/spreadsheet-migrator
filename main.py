# -*- coding: utf-8 -*001-
from resources.Help import init_parabrisa
import time

try:
    while True:
        init_parabrisa()
        print("\n----------------------------------\n")
        time.sleep(86400000)

except KeyboardInterrupt:
    print('Stoping observer')
