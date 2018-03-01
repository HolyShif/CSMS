
import RPi.GPIO as GPIO
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess
#GPIO.setmode(GPIO.BOARD)
#-----------------Variables---------------------------
RST = None
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3D)
#List of Character for passwords or email input
Selected_Character  = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U"]
Selected_Character += ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","i","o","q","r","s","t","u"]
Selected_Character += ["V","W","X","Y","Z","1","2","3","4","5","6","7","8","9","0","_",".","/"]
Selected_Character += ["v","w","x","y","z","!","@","#","$","%","^","&","*","(",")","\\","<",">"]

#All Buttons Use BCM
d_up = 5                        #Up button
d_down = 6                      #Down Button
back = 12                       #Back Button 
d_left = 13                     #Left Button
d_right = 19                    #Right Button
select =  26                    #Select Button
enter = 22                      #Enter Button

Selected_Char= 0		#Highlighted character
WIFI_PASSWORD = []              #List for WIFI PASSWORD
Adafruit_Info = []              #List for Adafruit Address
SSID_Info = []                  #List for WIFI SSID
#-------------Port Initialization-----------------------------------
GPIO.setup(d_up, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
GPIO.setup(d_down, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
GPIO.setup(d_left, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
GPIO.setup(d_right, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
GPIO.setup(select, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
GPIO.setup(back, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(enter, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
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
        x = True
        while x == True:
                global Selected_Char

                if GPIO.input(d_up) == False:
                        Selected_Char += 1
                        if Selected_Char > 3:
                                Selected_Char = 0
                        Main_Disp()
                        

                elif GPIO.input(d_down) == False:
                        Selected_Char -= 1
                        if Selected_Char < 0:
                                Selected_Char = 3
                        Main_Disp()

                elif GPIO.input(d_left) == False:
                        Selected_Char -= 1
                        if Selected_Char < 0:
                                Selected_Char = 3
                        Main_Disp()

                elif GPIO.input(d_right) == False:
                        Selected_Char += 1
                        if Selected_Char > 3:
                                Selected_Char = 0
                        Main_Disp()

                elif GPIO.input(select) == False:
                        x = False
                         
        if Selected_Char == 0:
                Selected_Char = 0
                Adafruit_Info = []
                Setup_Adafruit()

        elif Selected_Char == 1:
                Selected_Char = 0
                WIFI_PASSWORD = []
                WIFI_PASS_Disp()
                print("calling wifi password")
                WIFI_Password()
                              
        elif Selected_Char == 2:
                Selected_Char = 0
                SSID_Info = []
                Setup_SSID()

        elif  Selected_Char == 3:
                Selected_Char = 0
                #Call the "Scan for WIFI Function"

                      
def WIFI_Password():
        global WIFI_PASSWORD
        T = 0
        L = True
        while L == True:
                global Selected_Char
                global Selected_Character
                
                if GPIO.input(d_up) == False:
                        if Selected_Char < 18:
                                Selected_Char += 60

                        elif (Selected_Char < 21) and (Selected_Char > 17):
                                Selected_Char += 21
                              
                        elif (Selected_Char < 42) and (Selected_Char > 20):
                                Selected_Char -= 21

                        elif (Selected_Char < 78) and (Selected_Char > 59):
                                Selected_Char -= 18

                        elif (Selected_Char < 60) and (Selected_Char > 41):
                                Selected_Char -= 21
                        WIFI_PASS_Disp()

                elif GPIO.input(d_down) == False:
                        if Selected_Char < 21:
                                Selected_Char += 21

                        elif (Selected_Char < 39) and (Selected_Char > 20):
                                Selected_Char += 21

                        elif (Selected_Char > 38) and (Selected_Char < 42):
                                Selected_Char -= 21

                        elif (Selected_Char < 60) and (Selected_Char > 41):
                                Selected_Char += 18

                        elif (Selected_Char > 59) and (Selected_Char < 78):
                                Selected_Char -= 60
                        WIFI_PASS_Disp()

                elif GPIO.input(d_left) == False:
                        Selected_Char -= 1
                        if Selected_Char == -1:
                                Selected_Char = 20
                              
                        elif Selected_Char == 20:
                                Selected_Char = 41

                        elif Selected_Char == 41:
                                Selected_Char = 59

                        elif Selected_Char == 59:
                                Selected_Char = 77
                        WIFI_PASS_Disp()
                              
                elif GPIO.input(d_right) == False:
                        Selected_Char += 1
                        if Selected_Char == 21:
                                Selected_Char = 0
                              
                        elif Selected_Char == 42:
                                Selected_Char = 21

                        elif Selected_Char == 60:
                                Selected_Char = 42

                        elif Selected_Char == 78:
                                Selected_Char = 60
                        WIFI_PASS_Disp()
                
                elif GPIO.input(back) == False:
                        T = 0
                        L = False
                        
                elif GPIO.input(select) == False:
                        time.sleep(.2)
                        WIFI_PASSWORD += Selected_Character[Selected_Char]      #Add selected character to wifi password list
                        print(WIFI_PASSWORD)
                        
                elif GPIO.input(enter) == False:
                        T = 1
                        L = False
        if T == 0:
                Confirmation_Back_Wifi_Pass() #Goes to Main_Menu()
        elif T == 1:
                Confirmation_Wifi_Pass() #Goes to Confirm_Wifi_Pass()
        

def Setup_Adafruit():
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        text_Adafruit = 'ENTER ADAFRUIT KEY'
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

                elif (Selected_Char < 21) and (Selected_Char > 17):
                        Selected_Char += 21
                      
                elif (Selected_Char < 42) and (Selected_Char > 20):
                        Selected_Char -= 21

                elif (Selected_Char < 78) and (Selected_Char > 59):
                        Selected_Char -= 18

                elif (Selected_Char < 60) and (Selected_Char > 41):
                        Selected_Char -= 21

        elif GPIO.event_detected(d_down):
                if Selected_Char < 21:
                        Selected_Char += 21

                elif (Selected_Char < 39) and (Selected_Char > 20):
                        Selected_Char += 21

                elif (Selected_Char > 38) and (Selected_Char < 42):
                        Selected_Char -= 21

                elif (Selected_Char < 60) and (Selected_Char > 41):
                        Selected_Char += 18

                elif (Selected_Char > 59) and (Selected_Char < 78):
                        Selected_Char -= 60

        elif GPIO.event_detected(d_left):
                Selected_Char -= 1
                if Selected_Char == -1:
                        Selected_Char = 20
                      
                elif Selected_Char == 20:
                        Selected_Char = 41

                elif Selected_Char == 41:
                        Selected_Char = 59

                elif Selected_Char == 59:
                        Selected_Char = 77
                      
        elif GPIO.event_detected(d_right):
                Selected_Char += 1
                if Selected_Char == 21:
                        Selected_Char = 0
                      
                elif Selected_Char == 42:
                        Selected_Char = 21

                elif Selected_Char == 60:
                        Selected_Char = 42

                elif Selected_Char == 78:
                        Selected_Char = 60
        
        elif GPIO.event_detected(back):
                Confirmation_Back_Adafruit()       #Confirm that you want to return to the main menu

        elif GPIO.event_detected(select):
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

                elif (Selected_Char < 21) and (Selected_Char > 17):
                        Selected_Char += 21
                      
                elif (Selected_Char < 42) and (Selected_Char > 20):
                        Selected_Char -= 21

                elif (Selected_Char < 78) and (Selected_Char > 59):
                        Selected_Char -= 18

                elif (Selected_Char < 60) and (Selected_Char > 41):
                        Selected_Char -= 21

        elif GPIO.event_detected(d_down):
                if Selected_Char < 21:
                        Selected_Char += 21

                elif (Selected_Char < 39) and (Selected_Char > 20):
                        Selected_Char += 21

                elif (Selected_Char > 38) and (Selected_Char < 42):
                        Selected_Char -= 21

                elif (Selected_Char < 60) and (Selected_Char > 41):
                        Selected_Char += 18

                elif (Selected_Char > 59) and (Selected_Char < 78):
                        Selected_Char -= 60

        elif GPIO.event_detected(d_left):
                Selected_Char -= 1
                if Selected_Char == -1:
                        Selected_Char = 20
                      
                elif Selected_Char == 20:
                        Selected_Char = 41

                elif Selected_Char == 41:
                        Selected_Char = 59

                elif Selected_Char == 59:
                        Selected_Char = 77
                      
        elif GPIO.event_detected(d_right):
                Selected_Char += 1
                if Selected_Char == 21:
                        Selected_Char = 0
                      
                elif Selected_Char == 42:
                        Selected_Char = 21

                elif Selected_Char == 60:
                        Selected_Char = 42

                elif Selected_Char == 78:
                        Selected_Char = 60
        
        elif GPIO.event_detected(back):
                Confirmation_Back_SSID()       #Confirm that you want to return to the main menu

        elif GPIO.event_detected(select):
                SSID_Info += Selected_Character[Selected_Char]         #Add the selected character the WIFI SSID list
        Setup_SSID()           #Loop back to Setup_SSID()
        
        #Add a check for if the enter button was pressed  this will mean the input is complete



def Confirmation_Back_Adafruit():
        #NEEDS FINISHED NEED EXIT VALUE FOR TRUE LOOP
        Conf_Back_Disp()
        C = True
        while C == True:
                if GPIO.event_detected(back):
                        Setup_Adafruit()           #Return to Setup_Adafruit

                elif GPIO.event_detected(select):
                        Adafruit_Info = []         #Reset Email information
                        Selected_Char = 0       #Reset character counter
                        Main_Menu()             #Return to Main menu


def Confirmation_Back_Wifi_Pass():
        Conf_Back_Disp()
        x = True
        T = 0
        while x == True:
                if GPIO.input(back) == False:
                        T = 0
                        x = False

                elif GPIO.input(select) == False:
                        T = 1
                        x = False
        if T == 0:
                WIFI_Password()         #Return to wifi_password
        elif T == 1:
                WIFI_PASSWORD = []      #Reset wifi password
                Selected_Char = 0       #Reset character counter
                Main_Menu()             #Return to main menu

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

        elif GPIO.event_detected(select):
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

        #elif GPIO.event_detected(select):        
                
        Confirmation_Adafruit()       #Loops back to the start of Confirmation_Adafruit()

def Confirmation_Wifi_Pass():
        Conf_WI_PASS_Disp()
        T = 0
        x = True
        while x == True:
                if GPIO.input(back) == False:
                        T = 0
                        x = False

                elif GPIO.input(select) == False:
                        T = 1
                        x = False
                        
        if T == 0:
                WIFI_Passwod()         #Return to wifi_password
        elif T == 1:
                Main_Disp()
                Main_Menu()

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

        #elif GPIO.event_detected(select):             

        Confirmation_SSID()       #Loops back to the start of Confirmation_SSSID()


def Main_Disp():
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        text_main1 ='0)ENTER ADAFRUIT KEY'
        text_main2 ='1)SETUP WIFI PASSWORD'
        text_main3 ='2)ENTER WIFI SSID'
        text_main4 ='3)SCAN FOR WIFI'
        text_main_input = 'Your Selection: '
        draw.text((0,0),text_main1,font=font, fill=255)
        draw.text((0,7),text_main2,font=font, fill=255)
        draw.text((0,15),text_main3,font=font, fill=255)
        draw.text((0,23),text_main4,font=font, fill=255)
        draw.text((0,30),text_main_input + str(Selected_Char), fill=255)	
        disp.image(image)
        disp.display()

def WIFI_PASS_Disp():
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

def Conf_WI_PASS_Disp():
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        text_enter1 = 'IS THIS CORRECT?'
        text_enter2 = 'YES)PRESS SELECT'
        text_enter3 = ' NO)PRESS BACK'
        draw.text((0,0),text_enter1,font=font, fill=255)
        draw.text((0,7),text_enter2,font=font, fill=255)
        draw.text((0,15),text_enter3,font=font, fill=255)
        draw.text((0,22),WIFI_PASSWORD,font=font, fill=255)
        disp.image(image)
        disp.display()

def Conf_Back_Disp():
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        text_con_back2 = 'EXIT TO MAIN MENU?'
        text_con_back3 = 'YES)PRESS SELECT'
        text_con_back4 = ' NO)PRESS BACK'
        draw.text((0,0),text_con_back2,font=font, fill=255)
        draw.text((0,7),text_con_back3,font=font, fill=255)
        draw.text((0,15),text_con_back4,font=font, fill=255)            
        disp.image(image)
        disp.display()
                
Main_Disp()
Main_Menu()
