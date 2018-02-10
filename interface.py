import RPi.GPIO as GPIO
import time
import Adafruit_SSD1306
GPIO.setmode(GPIO.BOARD)
#-----------------Variables---------------------------
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
Selected_Character = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U',
		      'a','b','c','d','e','f','g','h','i','j','k','l','m','n','i','o','q','r','s','t','u',
	              'V','W','X','Y','Z',1,2,3,4,5,6,7,8,9,0,'_','.','/',
		      'v','w','x','y','z','!','@','#','$','%','^','&','*','(',')','\','<','>']

d_up = 29                       #direction pad up
d_down = 31                     #direction pad down
back = 32                       #back button
d_left = 33                     #direction pad left
d_right = 35                    #direction pad right
select =  37                    #select button
Selected_Char= 0		#Highlighted character
Button_Select = 0		#Counter for select
Button_Back = 0			#Counter for back
Button_Enter = 0		#Counter for enter

#-------------Port Initialization-----------------------------------
GPIO.setup(d_up, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
GPIO.add_event_detect(d_up, GPIO.FALLING, callback=debounce_callback, bounce_time=300)
GPIO.setup(d_down, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
GPIO.add_event_detect(d_down, GPIO.FALLING, callback=debounce_callback, bounce_time=300)
GPIO.setup(d_left, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
GPIO.add_event_detect(d_left, GPIO.FALLING, callback=debounce_callback, bounce_time=300)
GPIO.setup(d_right, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
GPIO.add_event_detect(d_right, GPIO.FALLING, callback=debounce_callback, bounce_time=300)
GPIO.setup(select, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
GPIO.add_event_detect(select, GPIO.FALLING, callback=debounce_callback, bounce_time=300) 
GPIO.setup(back, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
GPIO.add_event_detect(back, GPIO.FALLING, callback=debounce_callback, bounce_time=300)
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
font = ImageFont.load_default()
#---------------Function Declerations---------------------------
def Main_Menu():
	Button_Back = 0
	Button_Enter = 0
	Button_Select = 0

	text_main = '1)Setup Email        2)Setup Wifi Password3)Enter Wifi SSID    4)Scan For Wifi'
	draw.text(0,8,text_main,1)
	text_main_select = ' Select:1234'
	draw.text(0,43,text_main_select,1)
	text_main_input = ' Your Selection : '
	draw.text(0,50,text_main_input,1)
	

	if: GPIO.event_detected(d_up):
		Selected_Char += 1
		if: Selected_Char > 3
			Selected_Char = 0

	else if: GPIO.event_detected(d_down):
		Selected_Char -= 1
		if: Selected_char < 0
			Selected_Char = 3

	else if: GPIO.event_detected(d_left):
		Selected_Char -= 1
		if: Selected_char < 0
			Selected_Char = 3

	else if: GPIO.event_detected(d_right):
		Selected_Char += 1
		if: Selected_Char > 3
			Selected_Char = 0

	else if: GPIO.event_detected(back):
		Button_Back = 0			#Not needed for main menu

	else: GPIO.event_detected(select):
		Button_Select = 1
