#CSMS main program
#Kyle Shiflett, Brain Clark, Steve Baker, Eddie Bierne, Evan Elliot

import RPi.GPIO as GPIO
import time
import Adafruit_DHT         #for DHT22

GPIO.setmode(GPIO.BOARD)    #board pin numbering, not Broadcom

#------Pin Definitions------
oled_rtc_i2c_data = 3       #i2c sda data bus for oled and rtc
oled_rtc_i2c_clk = 5        #i2c sdc clock bus for oled and rtc
oled_reset = 7              #reset for oled
temp_humid = 12             #DHT22 temp/humidity sensor
main_pow_on = 16            #main power indicator
low_batt = 18               #low battery indicator
d_up = 29                   #direction pad up
d_down = 31                 #direction pad down
back = 32                   #back button
d_left = 33                 #direction pad left
d_right = 35                #direction pad right
led_pwr = 36                #power indicator led
select = 37                 #select button
led_inet = 38               #internet indicator led
led_temp_stat = 40          #good temperature indicator led

#------Pin Setup------

#**do i2c setup**

GPIO.setup(oled_reset,GPIO.OUT)
GPIO.setup(temp_humid,GPIO.IN)
GPIO.setup(main_pow_on,GPIO.IN)
GPIO.setup(low_batt,GPIO.IN)
GPIO.setup(d_up,GPIO.IN)
GPIO.setup(d_down,GPIO.IN)
GPIO.setup(back,GPIO.IN)
GPIO.setup(d_left,GPIO.IN)
GPIO.setup(d_right,GPIO.IN)
GPIO.setup(led_pwr,GPIO.OUT)
GPIO.setup(select,GPIO.IN)
GPIO.setup(led_inet,GPIO.OUT)
GPIO.setup(led_temp_stat,GPIO.OUT)

#------Variables------
sensor = Adafruit_DHT.DHT22
temperature = 0
humidity = 0

#------Function Definitions------
def get_temp_humid(humidity,temperature)        #function for reading the DHT22
    humidity, temperature = Adafruit_DHT.read_retry(sensor,temp_humid)
    #print "Humidity = " + humidity + " ::: Temperature = " + temperature
    return


#main loop





