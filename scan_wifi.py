import subprocess

p1 = subprocess.Popen(["iwlist","wlan0","scan"],stdout=subprocess.PIPE)
p2 = subprocess.Popen(["grep", "-oP", "SSID:\"\K[^\"]+"],stdin=p1.stdout,stdout=subprocess.PIPE)
#p2 = subprocess.Popen(["grep", "SSID:"],stdin=p1.stdout,stdout=subprocess.PIPE)

#p1.stdout.close()
#out,err = p2.communicate()
out,err = p2.communicate()
print(out)
essid = out.splitlines()
print(essid)
essid = list(set(essid))
print(essid)
print(len(essid))
#sudo iwlist wlan0 scan | grep -oP 'SSID:"\K[^"]+'
