import RPi.GPIO as GPIO
import time
import Adafruit_SSD1306
GPIO.setmode(GPIO.BOARD)
#-----------------Variables---------------------------
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
Selected_Character  = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U"]
Selected_Character += ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","i","o","q","r","s","t","u"]
Selected_Character += ["V","W","X","Y","Z",1,2,3,4,5,6,7,8,9,0,"_",".","/"]
Selected_Character += ["v","w","x","y","z","!","@","#","$","%","^","&","*","(",")","\\","<",">"]

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
WIFI_PASSWORD = ""              #List for WIFI PASSWORD
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
image = Image.new('1', (width, height))
font = ImageFont.load_default()
draw = ImageDraw.Draw(image)
#---------------Function Declerations---------------------------
def Main_Menu():
        draw.rectangle((0,0,width,height), outline=0, fill=0)
	text_main1 = '0)SETUP EMAIL'
        text_main2 = '1)SETUP WIFI PASSWORD'
        text_main3 = '2)ENTER WIFI SSID'
        text_main4 = '3)SCAN FOR WIFI'
        text_main5 = 'Select:0 1 2 3'
	draw.text((0,0),text_main1,font=font, fill=255)
        draw.text((0,7),text_main2,font=font, fill=255)
        draw.text((0,15),text_main3,font=font, fill=255)
        draw.text((0,23),text_main4,font=font, fill=255)
	draw.text((0,39),text_main5 ,font=font, fill=255)
	text_main_input = 'Your Selection: '
	draw.text((0,47),text_main_input + Selected_Char,1)
	
        disp.image(image)
        disp.display()
        time.sleep(.1)
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
		if: Selected_Char == 0
                      Selected_Char = 0
                      Setup_Email()

                else if: Selected_Char == 1
                      Selected_Char = 0
                      WIFI_Password()
                      
                else if: Selected_Char == 2
                      Selected_Char = 0
                      #Call the "Enter the WIFI SSD Function"

                else if: Selected_Char == 3
                      Selected_Char = 0
                      #Call the "Scan for WIFI Function"
        Main_Menu()
                      
def WIFI_Password():
        draw.rectangle((0,0,width,height), outline=0, fill=0)

	text_wifi_pass1 = 'ENTER WIFI PASSWORD'
        text_wifi_pass2 = 'ABCDEFGHIJKLMNOPQRSTU'
        text_wifi_pass3 = 'abcdefghijklmnopqrstu'
        text_wifi_pass4 = 'VWXYZ1234567890_./'
        text_wifi_pass5 = 'vwxyz!@#$%^&*()\<>'
        text_wifi_pass6 = 'CURRENT SELECTION:'           
        
	draw.text((0,0),text_wifi_pass1,font=font, fill=255)
        draw.text((0,7),text_wifi_pass6 + Selected_Character(Selected_Char),font=font, fill=255)
        draw.text((0,31),text_wifi_pass2,font=font, fill=255)
        draw.text((0,39),text_wifi_pass3,font=font, fill=255)
        draw.text((0,47),text_wifi_pass4,font=font, fill=255)
	draw.text((0,55),text_wifi_pass5,font=font, fill=255)
	
        disp.image(image)
        disp.display()
        time.sleep(.1)
	if: GPIO.event_detected(d_up):
                if: Selected_Char < 18
                        Selected_Char += 60

                else if: (Selected_Char < 21) and (Selected_Char > 17)
                        Selected_Char += 21
                      
		else if: (Selected_Char < 42) and (Selected_Char > 20)
                        Selected_Char -= 21

                else if: (Selected_Char < 78) and (Selected_Char > 59)
                        Selected_Char -= 18

                else if: (Selected_Char < 60) and (Selected_Char > 41)
                        Selected_Char -= 21


	else if: GPIO.event_detected(d_down):
		if: Selected_Char < 21
                        Selected_Char += 21

                else if: (Selected_Char < 39) and (Selected_Char > 20)
                        Selected_Char += 21

                else if: (Selected_Char > 38) and (Selected_Char < 42)
                        Selected_Char -= 21

                else if: (Selected_Char < 60) and (Selected_Char > 41)
                        Selected_Char += 18

                else if: (Selected_Char > 59) and (Selected_Char < 78)
                        Selected_Char -= 60

	else if: GPIO.event_detected(d_left):
		Selected_Char -= 1
		if: Selected_Char == -1
                      Selected_Char = 20
                      
                else if: Selected_Char == 20
                        Selected_Char = 41

                else if: Selected_Char == 41
                      Selected_Char = 59

                else if: Selected_Char == 59
                      Selected_Char = 77
                      
	else if: GPIO.event_detected(d_right):
		Selected_Char += 1
		if: Selected_Char == 21
                      Selected_Char = 0
                      
                else if: Selected_Char == 42
                        Selected_Char = 21

                else if: Selected_Char == 60
                      Selected_Char = 42

                else if: Selected_Char == 78
                      Selected_Char = 60
        
	else if: GPIO.event_detected(back):
                #Clear Wifi Password
                Confirmation_Back_Wifi_Pass()

	else if: GPIO.event_detected(select):
                #Will add Selected_Character(Selected_Char) to a list
        WIFI_Password()
        #Add a check for if the enter button was pressed  this will mean the input is complete

def Setup_Email():
        draw.rectangle((0,0,width,height), outline=0, fill=0)

	text_email = 'ENTER EMAIL'
        text_email2 = 'ABCDEFGHIJKLMNOPQRSTU'
        text_email3 = 'abcdefghijklmnopqrstu'
        text_email4 = 'VWXYZ1234567890_./'
        text_email5 = 'vwxyz!@#$%^&*()\<>'
        text_email6 = 'CURRENT SELECTION:'           
        
	draw.text((0,0),text_email,font=font, fill=255)
        draw.text((0,7),text_email6 + Selected_Character(Selected_Char),font=font, fill=255)
        draw.text((0,31),text_email2,font=font, fill=255)
        draw.text((0,39),text_email3,font=font, fill=255)
        draw.text((0,47),text_email4,font=font, fill=255)
	draw.text((0,55),text_email5,font=font, fill=255)
	
        disp.image(image)
        disp.display()
        time.sleep(.1)
	if: GPIO.event_detected(d_up):
                if: Selected_Char < 18
                        Selected_Char += 60

                else if: (Selected_Char < 21) and (Selected_Char > 17)
                        Selected_Char += 21
                      
		else if: (Selected_Char < 42) and (Selected_Char > 20)
                        Selected_Char -= 21

                else if: (Selected_Char < 78) and (Selected_Char > 59)
                        Selected_Char -= 18

                else if: (Selected_Char < 60) and (Selected_Char > 41)
                        Selected_Char -= 21


	else if: GPIO.event_detected(d_down):
		if: Selected_Char < 21
                        Selected_Char += 21

                else if: (Selected_Char < 39) and (Selected_Char > 20)
                        Selected_Char += 21

                else if: (Selected_Char > 38) and (Selected_Char < 42)
                        Selected_Char -= 21

                else if: (Selected_Char < 60) and (Selected_Char > 41)
                        Selected_Char += 18

                else if: (Selected_Char > 59) and (Selected_Char < 78)
                        Selected_Char -= 60

	else if: GPIO.event_detected(d_left):
		Selected_Char -= 1
		if: Selected_Char == -1
                      Selected_Char = 20
                      
                else if: Selected_Char == 20
                        Selected_Char = 41

                else if: Selected_Char == 41
                      Selected_Char = 59

                else if: Selected_Char == 59
                      Selected_Char = 77
                      
	else if: GPIO.event_detected(d_right):
		Selected_Char += 1
		if: Selected_Char == 21
                      Selected_Char = 0
                      
                else if: Selected_Char == 42
                        Selected_Char = 21

                else if: Selected_Char == 60
                      Selected_Char = 42

                else if: Selected_Char == 78
                      Selected_Char = 60
        
	else if: GPIO.event_detected(back):
                #Clear email input
		Confirmation_Back_Email()

	else: GPIO.event_detected(select):
		#Will add Selected_Character(Selected_Char) to a list
        Setup_Email()
        #Add a check for if the enter button was pressed  this will mean the input is complete

def Confirmation_Back_Email():
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        text_con_back = 'DO YOU WANT TO'
        text_con_back2 = 'EXIT TO MAIN MENU?'
        text_con_back3 = 'PRESS SELECT TO CONFIRM'
        text_con_back4 = 'PRESS SELECT TO RETURN'
	draw.text((0,0),text_con_back,font=font, fill=255)
	draw.text((0,7),text_con_back2,font=font, fill=255)
	draw.text((0,15),text_con_back3,font=font, fill=255)
	draw.text((0,23),text_con_back4,font=font, fill=255)            
        disp.image(image)
        disp.display()
        time.sleep(.1)

        if: GPIO.event_detected(back):
                Setup_Email()

	else if: GPIO.event_detected(select):
                #Clear lists
                Main_Menu()

        Confirmation_Back_Email()

def Confirmation_Back_Wifi_Pass():
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        text_con_back = 'DO YOU WANT TO'
        text_con_back2 = 'EXIT TO MAIN MENU?'
        text_con_back3 = 'PRESS SELECT TO CONFIRM'
        text_con_back4 = 'PRESS SELECT TO RETURN'
	draw.text((0,0),text_con_back,font=font, fill=255)
	draw.text((0,7),text_con_back2,font=font, fill=255)
	draw.text((0,15),text_con_back3,font=font, fill=255)
	draw.text((0,23),text_con_back4,font=font, fill=255)            
        disp.image(image)
        disp.display()
        time.sleep(.1)

        if: GPIO.event_detected(back):
                WIFI_Password()

	else if: GPIO.event_detected(select):
                #Clear lists
                Main_Menu()

        Confirmation_Back_Wifi_Pass()

        

