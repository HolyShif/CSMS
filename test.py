import time
from subprocess import call

call(['wlist', 'wlan0', 'scan', '|', 'grep', '-m1' 'ESSID'])
