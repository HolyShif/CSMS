import RPi.GPIO as GPIO
import time
import Adafruit_SSD1306
GPIO.setmode(GPIO.BOARD)
#-----------------Variables---------------------------
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
#List of Character for passwords or email input
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
WIFI_PASSWORD = []              #List for WIFI PASSWORD
Adafruit_Info = []              #List for Adafruit Address
SSID_Info = []                  #List for WIFI SSID
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
#initialize display
disp.begin()
disp.clear()
disp.display()
width = disp.width                      #set width of display
height = disp.height                    #set height of display
image = Image.new('1', (width, height))
font = ImageFont.load_default()
draw = ImageDraw.Draw(image)
#---------------Function Declerations---------------------------
def Main_Menu():
        draw.rectangle((0,0,width,height), outline=0, fill=0)
	text_main1 = '0)ENTER ADAFRUIT KEY'
        text_main2 = '1)SETUP WIFI PASSWORD'
        text_main3 = '2)ENTER WIFI SSID'
        text_main4 = '3)SCAN FOR WIFI'
        text_main_input = 'Your Selection: '
	draw.text((0,0),text_main1,font=font, fill=255)
        draw.text((0,7),text_main2,font=font, fill=255)
        draw.text((0,15),text_main3,font=font, fill=255)
        draw.text((0,23),text_main4,font=font, fill=255)
	draw.text((0,30),text_main_input + Selected_Char, fill=255)	
        disp.image(image)
        disp.display()
        time.sleep(.1)
	if GPIO.event_detected(d_up):
		Selected_Char += 1
		if Selected_Char > 3:
			Selected_Char = 0

	else if GPIO.event_detected(d_down):
		Selected_Char -= 1
		if Selected_char < 0:
			Selected_Char = 3

	else if GPIO.event_detected(d_left):
		Selected_Char -= 1
		if Selected_char < 0:
			Selected_Char = 3

	else if GPIO.event_detected(d_right):
		Selected_Char += 1
		if Selected_Char > 3:
			Selected_Char = 0

	else if GPIO.event_detected(select):
		if Selected_Char == 0:
                      Selected_Char = 0
                      Adafruit_Info = []
                      Setup_Adafruit()

                else if Selected_Char == 1:
                      Selected_Char = 0
                      WIFI_PASSWORD = []
                      WIFI_Password()
                      
                else if Selected_Char == 2:
                      Selected_Char = 0
                      SSID_Info = []
                      Setup_SSID()

                else if Selected_Char == 3:
                      Selected_Char = 0
                      #Call the "Scan for WIFI Function"
        Main_Menu()     #Loop to main_menu()
                      
def WIFI_Password():
        draw.rectangle((0,0,width,height), outline=0, fill=0)
	text_wifi_pass1 = 'ENTER WIFI PASSWORD'
        text_wifi_pass2 = 'ABCDEFGHIJKLMNOPQRSTU'
        text_wifi_pass3 = 'abcdefghijklmnopqrstu'
        text_wifi_pass4 = 'VWXYZ1234567890_./'
        text_wifi_pass5 = 'vwxyz!@#$%^&*()\<>'
        text_wifi_pass6 = 'CURRENT SELECTION:'                   
	draw.text((0,0),text_wifi_pass1,font=font, fill=255)
        draw.text((0,7),text_wifi_pass6 + Selected_Character[Selected_Char],font=font, fill=255)
        draw.text((0,31),text_wifi_pass2,font=font, fill=255)
        draw.text((0,39),text_wifi_pass3,font=font, fill=255)
        draw.text((0,47),text_wifi_pass4,font=font, fill=255)
	draw.text((0,55),text_wifi_pass5,font=font, fill=255)	
        disp.image(image)
        disp.display()
        time.sleep(.1)
	if GPIO.event_detected(d_up):
                if Selected_Char < 18:
                        Selected_Char += 60

                else if (Selected_Char < 21) and (Selected_Char > 17):
                        Selected_Char += 21
                      
		else if (Selected_Char < 42) and (Selected_Char > 20):
                        Selected_Char -= 21

                else if (Selected_Char < 78) and (Selected_Char > 59):
                        Selected_Char -= 18

                else if (Selected_Char < 60) and (Selected_Char > 41):
                        Selected_Char -= 21

	else if GPIO.event_detected(d_down):
		if Selected_Char < 21:
                        Selected_Char += 21

                else if (Selected_Char < 39) and (Selected_Char > 20):
                        Selected_Char += 21

                else if (Selected_Char > 38) and (Selected_Char < 42):
                        Selected_Char -= 21

                else if (Selected_Char < 60) and (Selected_Char > 41):
                        Selected_Char += 18

                else if (Selected_Char > 59) and (Selected_Char < 78):
                        Selected_Char -= 60

	else if GPIO.event_detected(d_left):
		Selected_Char -= 1
		if Selected_Char == -1:
                      Selected_Char = 20
                      
                else if Selected_Char == 20:
                        Selected_Char = 41

                else if Selected_Char == 41:
                      Selected_Char = 59

                else if Selected_Char == 59:
                      Selected_Char = 77
                      
	else if GPIO.event_detected(d_right):
		Selected_Char += 1
		if Selected_Char == 21:
                      Selected_Char = 0
                      
                else if Selected_Char == 42:
                        Selected_Char = 21

                else if Selected_Char == 60:
                      Selected_Char = 42

                else if Selected_Char == 78:
                      Selected_Char = 60
        
	else if GPIO.event_detected(back):
                Confirmation_Back_Wifi_Pass()   #Confirma that you want to return to the main menu

	else if GPIO.event_detected(select):
                WIFI_PASSWORD += Selected_Character[Selected_Char]      #Add selected character to wifi password list
                        
        WIFI_Password()         #Loop back to Wifi_password()
        #Add a check for if the enter button was pressed  this will mean the input is complete

def Setup_Adafruit():
        draw.rectangle((0,0,width,height), outline=0, fill=0)
	text_Adafruit =  'ENTER ADAFRUIT KEY'
        text_Adafruit2 = 'ABCDEFGHIJKLMNOPQRSTU'
        text_Adafruit3 = 'abcdefghijklmnopqrstu'
        text_Adafruit4 = 'VWXYZ1234567890_./'
        text_Adafruit5 = 'vwxyz!@#$%^&*()\<>'
        text_Adafruit6 = 'CURRENT SELECTION:'                   
	draw.text((0,0),text_Adafruit,font=font, fill=255)
        draw.text((0,7),text_Adafruit6 + Selected_Character[Selected_Char],font=font, fill=255)
        draw.text((0,31),text_Adafruit2,font=font, fill=255)
        draw.text((0,39),text_Adafruit3,font=font, fill=255)
        draw.text((0,47),text_Adafruit4,font=font, fill=255)
	draw.text((0,55),text_Adafruit5,font=font, fill=255)	
        disp.image(image)
        disp.display()
        time.sleep(.1)
	if GPIO.event_detected(d_up):
                if Selected_Char < 18:
                        Selected_Char += 60

                else if (Selected_Char < 21) and (Selected_Char > 17):
                        Selected_Char += 21
                      
		else if (Selected_Char < 42) and (Selected_Char > 20):
                        Selected_Char -= 21

                else if (Selected_Char < 78) and (Selected_Char > 59):
                        Selected_Char -= 18

                else if (Selected_Char < 60) and (Selected_Char > 41):
                        Selected_Char -= 21


	else if GPIO.event_detected(d_down):
		if Selected_Char < 21
                        Selected_Char += 21

                else if (Selected_Char < 39) and (Selected_Char > 20):
                        Selected_Char += 21

                else if (Selected_Char > 38) and (Selected_Char < 42):
                        Selected_Char -= 21

                else if (Selected_Char < 60) and (Selected_Char > 41):
                        Selected_Char += 18

                else if (Selected_Char > 59) and (Selected_Char < 78):
                        Selected_Char -= 60

	else if GPIO.event_detected(d_left):
		Selected_Char -= 1
		if Selected_Char == -1:
                      Selected_Char = 20
                      
                else if Selected_Char == 20:
                        Selected_Char = 41

                else if Selected_Char == 41:
                      Selected_Char = 59

                else if Selected_Char == 59:
                      Selected_Char = 77
                      
	else if GPIO.event_detected(d_right):
		Selected_Char += 1
		if Selected_Char == 21:
                      Selected_Char = 0
                      
                else if Selected_Char == 42:
                        Selected_Char = 21

                else if Selected_Char == 60:
                      Selected_Char = 42

                else if Selected_Char == 78:
                      Selected_Char = 60
        
	else if GPIO.event_detected(back):
		Confirmation_Back_Adafruit()       #Confirm that you want to return to the main menu

	else if GPIO.event_detected(select):
                Adafruit_Info += Selected_Character[Selected_Char]         #Add the selected character the Adafruit address list
        Setup_Adafruit()           #Loop back to Setup_Adafruit()
        #Add a check for if the enter button was pressed  this will mean the input is complete

def Setup_SSID():
        draw.rectangle((0,0,width,height), outline=0, fill=0)
	text_SSID1 = 'ENTER WIFI SSID'
        text_SSID2 = 'ABCDEFGHIJKLMNOPQRSTU'
        text_SSID3 = 'abcdefghijklmnopqrstu'
        text_SSID4 = 'VWXYZ1234567890_./'
        text_SSID5 = 'vwxyz!@#$%^&*()\<>'
        text_SSID6 = 'CURRENT SELECTION:'                   
	draw.text((0,0),text_SSID1,font=font, fill=255)
        draw.text((0,7),text_SSID6 + Selected_Character[Selected_Char],font=font, fill=255)
        draw.text((0,31),text_SSID2,font=font, fill=255)
        draw.text((0,39),text_SSID3,font=font, fill=255)
        draw.text((0,47),text_SSID4,font=font, fill=255)
	draw.text((0,55),text_SSID5,font=font, fill=255)	
        disp.image(image)
        disp.display()
        time.sleep(.1)
	if GPIO.event_detected(d_up):
                if Selected_Char < 18:
                        Selected_Char += 60

                else if (Selected_Char < 21) and (Selected_Char > 17):
                        Selected_Char += 21
                      
		else if (Selected_Char < 42) and (Selected_Char > 20):
                        Selected_Char -= 21

                else if (Selected_Char < 78) and (Selected_Char > 59):
                        Selected_Char -= 18

                else if (Selected_Char < 60) and (Selected_Char > 41):
                        Selected_Char -= 21


	else if GPIO.event_detected(d_down):
		if Selected_Char < 21
                        Selected_Char += 21

                else if (Selected_Char < 39) and (Selected_Char > 20):
                        Selected_Char += 21

                else if (Selected_Char > 38) and (Selected_Char < 42):
                        Selected_Char -= 21

                else if (Selected_Char < 60) and (Selected_Char > 41):
                        Selected_Char += 18

                else if (Selected_Char > 59) and (Selected_Char < 78):
                        Selected_Char -= 60

	else if GPIO.event_detected(d_left):
		Selected_Char -= 1
		if Selected_Char == -1:
                      Selected_Char = 20
                      
                else if Selected_Char == 20:
                        Selected_Char = 41

                else if Selected_Char == 41:
                      Selected_Char = 59

                else if Selected_Char == 59:
                      Selected_Char = 77
                      
	else if GPIO.event_detected(d_right):
		Selected_Char += 1
		if Selected_Char == 21:
                      Selected_Char = 0
                      
                else if Selected_Char == 42:
                        Selected_Char = 21

                else if Selected_Char == 60:
                      Selected_Char = 42

                else if Selected_Char == 78:
                      Selected_Char = 60
        
	else if GPIO.event_detected(back):
		Confirmation_Back_SSID()       #Confirm that you want to return to the main menu

	else if GPIO.event_detected(select):
                SSID_Info += Selected_Character[Selected_Char]         #Add the selected character the WIFI SSID list
        Setup_SSID()           #Loop back to Setup_SSID()
        
        #Add a check for if the enter button was pressed  this will mean the input is complete



def Confirmation_Back_Adafruit():
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        text_con_back2 = 'EXIT TO MAIN MENU?'
        text_con_back3 = 'YES)PRESS SELECT'
        text_con_back4 = ' NO)PRESS BACK'
	draw.text((0,0),text_con_back2,font=font, fill=255)
	draw.text((0,7),text_con_back3,font=font, fill=255)
	draw.text((0,15),text_con_back4,font=font, fill=255)            
        disp.image(image)
        disp.display()
        time.sleep(.1)

        if GPIO.event_detected(back):
                Setup_Adafruit()           #Return to Setup_Adafruit

	else if GPIO.event_detected(select):
                Adafruit_Info = []         #Reset Email information
                Selected_Char = 0       #Reset character counter
                Main_Menu()             #Return to Main menu

        Confirmation_Back_Adafruit()       #Loops back to the start of Confirmation_Back_Adafruit()

def Confirmation_Back_Wifi_Pass():
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        text_con_back2 = 'EXIT TO MAIN MENU?'
        text_con_back3 = 'YES)PRESS SELECT'
        text_con_back4 = ' NO)PRESS BACK'
	draw.text((0,0),text_con_back2,font=font, fill=255)
	draw.text((0,7),text_con_back3,font=font, fill=255)
	draw.text((0,15),text_con_back4,font=font, fill=255)            
        disp.image(image)
        disp.display()
        time.sleep(.1)

        if GPIO.event_detected(back):
                WIFI_Password()         #Return to wifi_password

	else if GPIO.event_detected(select):
                WIFI_PASSWORD = []      #Reset wifi password
                Selected_Char = 0       #Reset character counter
                Main_Menu()             #Return to main menu

        Confirmation_Back_Wifi_Pass()   #Loops back to start of Confirmation_Back_Wifi_Pass()

def Confirmation_Back_SSID():
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        text_con_back2 = 'EXIT TO MAIN MENU?'
        text_con_back3 = 'YES)PRESS SELECT'
        text_con_back4 = ' NO)PRESS BACK'
	draw.text((0,0),text_con_back2,font=font, fill=255)
	draw.text((0,7),text_con_back3,font=font, fill=255)
	draw.text((0,15),text_con_back4,font=font, fill=255)            
        disp.image(image)
        disp.display()
        time.sleep(.1)

        if GPIO.event_detected(back):
                Setup_Email()           #Return to Setup_email

	else if GPIO.event_detected(select):
                SSID_Info = []          #Reset SSID information
                Selected_Char = 0       #Reset character counter
                Main_Menu()             #Return to Main menu

        Confirmation_Back_SSID()       #Loops back to the start of Confirmation_Back_SSID()

def Confirmation_Adafruit():
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        text_enter1 = 'IS THIS CORRECT?'
        text_enter2 = 'YES)PRESS SELECT'
        text_enter3 = ' NO)PRESS BACK'
        draw.text((0,0),text_enter1,font=font, fill=255)
        draw.text((0,7),text_enter2,font=font, fill=255)
        draw.text((0,15),text_enter3,font=font, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(.1)

        if GPIO.event_detected(back):
                Setup_Adafruit()           #Return to Setup_Adafruit

	else if GPIO.event_detected(select):
                

        Confirmation_Adafruit()       #Loops back to the start of Confirmation_Adafruit()

def Confirmation_Wifi_Pass():
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        text_enter1 = 'IS THIS CORRECT?'
        text_enter2 = 'YES)PRESS SELECT'
        text_enter3 = ' NO)PRESS BACK'
        draw.text((0,0),text_enter1,font=font, fill=255)
        draw.text((0,7),text_enter2,font=font, fill=255)
        draw.text((0,15),text_enter3,font=font, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(.1)

        if GPIO.event_detected(back):
                WIFI_Password()         #Return to wifi_password

	else if GPIO.event_detected(select):


        Confirmation_Wifi_Pass()       #Loops back to the start of Confirmation_Wifi_Pass()   


def Confirmation_SSID():
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        text_enter1 = 'IS THIS CORRECT?'
        text_enter2 = 'YES)PRESS SELECT'
        text_enter3 = ' NO)PRESS BACK'
        draw.text((0,0),text_enter1,font=font, fill=255)
        draw.text((0,7),text_enter2,font=font, fill=255)
        draw.text((0,15),text_enter3,font=font, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(.1)

        if GPIO.event_detected(back):
                Setup_SSID()           #Return to Setup_SSID

	else if GPIO.event_detected(select):
                

        Confirmation_SSID()       #Loops back to the start of Confirmation_SSSID()
