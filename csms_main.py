#CSMS main program
#Kyle Shiflett, Brain Clark, Steve Baker, Eddie Bierne, Evan Elliot

import RPi.GPIO as GPIO
import time
import threading
from Adafruit_IO import Client       #adafruit io lib, current using REST not MQTT
import Adafruit_DHT             #for DHT22

GPIO.setmode(GPIO.BCM)        #board pin numbering, not Broadcom

#------Pin Definitions------
oled_rtc_i2c_data = 2           #i2c sda data bus for oled and rtc
oled_rtc_i2c_clk = 3            #i2c sdc clock bus for oled and rtc
oled_reset = 4                  #reset for oled
temp_humid = 18                 #DHT22 temp/humidity sensor
main_pow_on = 23                #main power indicator
low_bat = 17                    #low battery indicator
d_up = 5                        #direction pad up
d_down = 6                      #direction pad down
back = 12                       #back button
d_left = 13                     #direction pad left
d_right = 19                    #direction pad right
led_pwr = 16                    #power indicator led
select = 26                     #select button
led_inet = 20                   #internet indicator led
led_temp_stat = 21              #good temperature indicator led

#------Pin Setup------

#**do i2c setup**

GPIO.setup(oled_reset,GPIO.OUT)
GPIO.setup(temp_humid,GPIO.IN)
GPIO.setup(main_pow_on,GPIO.IN)
GPIO.setup(low_bat,GPIO.IN)
GPIO.setup(d_up,GPIO.IN)
GPIO.setup(d_down,GPIO.IN)
GPIO.setup(back,GPIO.IN)
GPIO.setup(d_left,GPIO.IN)
GPIO.setup(d_right,GPIO.IN)
GPIO.setup(led_pwr,GPIO.OUT)
GPIO.setup(select,GPIO.IN)
GPIO.setup(led_inet,GPIO.OUT)
GPIO.setup(led_temp_stat,GPIO.OUT)

#------Adafruit IO Setup------
aio = Client('afe0b443290e43eaa49f6f7b55841bed')        #adafruit io key


#------Variables------
sensor = Adafruit_DHT.DHT22
#temperature = 0
#humidity = 0
#thresh_up = 0		#degrees celsius
#above_thresh = 0
#tmp = 0

#------Function Definitions------
def get_temp_humid(arg1, stop_event):      	#function for reading the DHT22, to be put in
						#thread to continuously run without interference
        #aio = Client('afe0b443290e43eaa49f6f7b55841bed')        #adafruit io key
        #sensor = Adafruit_DHT.DHT22
        GPIO.setup(temp_humid,GPIO.IN)
        #temperature = 0
        #humidity = 0
        thresh_up = 0		#degrees celsius
        above_thresh = 0
        while(not stop_event.is_set()):
                humidity, temperature = Adafruit_DHT.read_retry(sensor,temp_humid)
                #print "Humidity = " + str(humidity) + " ::: Temperature = " + str(temperature) + "\n"
                print temperature

                if temperature > thresh_up:
                        above_thresh = 1
                        alert_str = "Temperature Is Above " + str(temperature) + " Degrees Celsius\n"
                        aio.send('Alerts', alert_str)
                        print "sent alert to Alerts feed for out of spec temperature\n"
                else:
                        above_thresh = 0

                aio.send('Temperature', temperature)
                print "Sent " + str(temperature) + " To Adafruit IO On Feed Temperature\n"

                #stop_event.wait(600)		#repeat every 10 minutes
                stop_event.wait(10)

#1st priority interrupt
def low_battery(channel):
	print "Low Battery Triggered\n"
	return

def bat_on(channel):
        print "Battery Activated"
        return

def mains_on(channel):
        print "Main Power Restored"
        return

#------Interrupt Callback Setup------
#low battery
GPIO.add_event_detect(low_bat, GPIO.FALLING, callback=low_battery, bouncetime=300)
#battery activation
GPIO.add_event_detect(main_pow_on, GPIO.FALLING, callback=bat_on, bouncetime=300)
#main power restoration
#GPIO.add_event_detect(main_pow_on, GPIO.RISING, callback=mains_on, bouncetime=300)

#------Thread Setup------
t1_stop = threading.Event()
t1 = threading.Thread(target=get_temp_humid, args=(1, t1_stop))
t1.start()




#main loop
try:
        while True:
                time.sleep(1)
except KeyboardInterrupt:	#exit on ctrl-c
        GPIO.cleanup()
        t1_stop.set()			#signal for thread to stop
#GPIO.cleanup()				#normal suceessful exit
t1_stop.set()				#signal for thread to stop
