#CSMS main program
#Kyle Shiflett, Brain Clark, Steve Baker, Eddie Bierne, Evan Elliot

import RPi.GPIO as GPIO
import time
import threading
from Adafruit_IO import Client       #adafruit io lib, current using REST not MQTT
import Adafruit_DHT             #for DHT22
import inet_check
import Queue
import subprocess

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
print "past client"

#------Variables------
sensor = Adafruit_DHT.DHT22
#temperature = 0
#humidity = 0
#thresh_up = 0		#degrees celsius
#above_thresh = 0
#tmp = 0
alert_queue = Queue.Queue(maxsize=100)
data_queue = Queue.Queue(maxsize=720)

#------Function Definitions------
def get_temp_humid(arg1, stop_event):      	#function for reading the DHT22, to be put in
						#thread to continuously run without interference
        #aio = Client('afe0b443290e43eaa49f6f7b55841bed')        #adafruit io key
        #sensor = Adafruit_DHT.DHT22
        print "in thread"
        GPIO.setup(temp_humid,GPIO.IN)
        print "past gpio setup in thread"
        #temperature = 0
        #humidity = 0
        thresh_up = 0		#degrees celsius
        above_thresh = 0

        #initial temp reading
        humidity, temperature = Adafruit_DHT.read_retry(sensor,temp_humid)
        
        send_data(temperature,humidity,not GPIO.input(main_pow_on))
        
        st_time = time.time()
        while(not stop_event.is_set()):
                end_time = time.time()
                #if ten minutes has passed
                if(ten_min(st_time,end_time) == True):
                        #print "time elapsed-----------------"
                        humidity, temperature = Adafruit_DHT.read_retry(sensor,temp_humid)
                        send_data(temperature,humidity,not GPIO.input(main_pow_on))
                        
                        if temperature > thresh_up:
                                if above_thresh == 0:
                                        send_alert("Temperature Has Raised Above Threshold\n")
                                        above_thresh = 1
                        else:
                                if above_thresh == 1:
                                        send_alert("Temperature Has Returned Below Threshold\n")
                                        above_thresh = 0
                                
                        st_time = end_time      #reset time interval


                if not alert_queue.empty() and (inet_check.check_connection('www.adafruit.io') == True):
                        aio.send('History',alert_queue.get())
                        time.sleep(3)   #throttle output
                else:
                        pass
                        #print "alert queue empty"
                if not data_queue.empty() and (inet_check.check_connection('www.adafruit.io') == True):
                        aio.send('History',data_queue.get())
                        time.sleep(3)   #throttle output
                else:
                        pass
                        #print "data_queue empty"
                        
                #print "waiting for temp"
                #humidity, temperature = Adafruit_DHT.read_retry(sensor,temp_humid)
                #print "Humidity = " + str(humidity) + " ::: Temperature = " + str(temperature) + "\n"
                #print temperature

                #if temperature > thresh_up:
                        #above_thresh = 1
                        #alert_str = "Temperature Is Above Threshold of " +str(thresh_up)+ " at " + str(temperature) + " Degrees Celsius\n"
                        #send_alert("Temp At " + str(temperature) + " Is Above Threshold\n")
                        #print "sent alert to Alerts feed for out of spec temperature\n"
                #else:
                        #above_thresh = 0

                #aio.send('Temperature', temperature)
                #print "Sent " + str(temperature) + " To Adafruit IO On Feed Temperature\n"
                #send_data(temperature,humidity,not GPIO.input(main_pow_on))

                #stop_event.wait(600)		#repeat every 10 minutes
                #stop_event.wait(10)
def ten_min(start,end):
        elapsed_sec = end-start
        #return True if 10 or more minutes have passed
        #return elapsed_sec >= 10*60
        return elapsed_sec >= 5
def send_alert(string):
        global alert_queue
        alert_str = time.strftime("%m/%d/%Y %H:%M:%S ") + string

        if(inet_check.check_connection('www.adafruit.io') == True):
                aio.send('Alerts', alert_str)
                print "Sent Alert"
        else:
                alert_queue.put(alert_str)
                print "pushed alert onto queue"
        return

def send_data(temp,humid,bat_on):
        global data_queue
        if(inet_check.check_connection('www.adafruit.io') == True):
                aio.send('Temperature', temp)
                aio.send('Humidity', humid)
                print "Sent Data"
        else:
                data_str = time.strftime("%m/%d/%Y %H:%M:%S") +" Temp=" + str(temp) + " Humid=" + str(humid) + " Bat_Active=" +str(bat_on)+'\n'
                data_queue.put(data_str)
                print "**BAT_ON =" + str(bat_on) + "**"
                print "pushed data onto queue"
        return

#1st priority interrupt
def low_battery(channel):
        print "Low Battery Triggered\n"
        global alert_queue
        global data_queue
        GPIO.cleanup()
        t1_stop.set()			#signal for thread to stop

        shut_str = "System Shutdown Due to Low Battery\n"
        send_alert(shut_str)

        #write alert queue to file
        f = open('aqueue.txt','w')
        if alert_queue.empty() == True:
                f.close()
        else:
                while(not alert_queue.empty()):
                        a = alert_queue.get()
                        print a
                        f.write(a)
                f.close()

        #write data queue to file
        f = open('dqueue.txt','w')
        if data_queue.empty() == True:
                f.close()
        else:
                while(not data_queue.empty()):
                        d = data_queue.get()
                        print a
                        f.write(d)
                f.close()


        #
        #
        #send shutdown command
        #subprocess.call(['sudo', 'shutdown', '-h', 'now'])
        #we want this thing to completely die, otherwise we cant wake it up?
        #
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
        #read in past alert queue from file
        f = open('aqueue.txt','r')
        for line in f:
                print line
                alert_queue.put(line)

        f.close()

        #read in past data queue from file
        f = open('dqueue.txt','r')
        for line in f:
                print line
                data_queue.put(line)

        f.close()

        while True:
                time.sleep(1)
                #
                #
                #CALL BRIANS MENU STUFF
                #
                #
                
                
except KeyboardInterrupt:	#exit on ctrl-c
        GPIO.cleanup()
        t1_stop.set()			#signal for thread to stop
#GPIO.cleanup()				#normal suceessful exit
t1_stop.set()				#signal for thread to stop
