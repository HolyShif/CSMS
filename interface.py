
import RPi.GPIO as GPIO
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess
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

essid = []
Val = 0
Size_Limit = 0
MAX_SIZE = 41
Selected_Char= 0		#Highlighted character
WIFI_PASSWORD = ''              #List for WIFI PASSWORD
Adafruit_Info = ''              #List for Adafruit Address
SSID_Info = ''                  #List for WIFI SSID
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
        Main_Disp()
        global Size_Limit
        global Selected_Char
        global Adafruit_Info
        global WIFI_PASSWORD
        global SSID_Info
        Bool_Val = True
        while Bool_Val == True:
                if GPIO.input(d_down) == False:
                        time.sleep(.1)
                        Selected_Char += 1
                        if Selected_Char > 4:
                                Selected_Char = 0
                        Main_Disp()
                        

                elif GPIO.input(d_up) == False:
                        time.sleep(.1)
                        Selected_Char -= 1
                        if Selected_Char < 0:
                                Selected_Char = 4
                        Main_Disp()

                elif GPIO.input(d_left) == False:
                        time.sleep(.1)
                        Selected_Char -= 1
                        if Selected_Char < 0:
                                Selected_Char = 4
                        Main_Disp()

                elif GPIO.input(d_right) == False:
                        time.sleep(.1)
                        Selected_Char += 1
                        if Selected_Char > 4:
                                Selected_Char = 0
                        Main_Disp()

                elif GPIO.input(select) == False:
                        time.sleep(.2)
                        Bool_Val = False


                elif GPIO.input(enter) == False:
                        time.sleep(.2)
                        Bool_Val = False
                         
        if Selected_Char == 0:
                Selected_Char = 0
                Size_Limit = 0
                Adafruit_Info = ''
                Setup_Adafruit()

        elif Selected_Char == 1:
                Selected_Char = 0
                Size_Limit = 0
                WIFI_PASSWORD = ''
                WIFI_Password()
                              
        elif Selected_Char == 2:
                Size_Limit = 0
                Selected_Char = 0
                SSID_Info = ''
                Setup_SSID()

        elif  Selected_Char == 3:
                Selected_Char = 0
                Scan_Wifi()
                
        elif Selected_Char == 4:
                Selected_Char = 0
                Disp_Inputs()
               
                      
def WIFI_Password():
        WIFI_PASS_Disp()
        global WIFI_PASSWORD
        global Size_Limit
        global Selected_Char
        global Selected_Character
        global MAX_SIZE
        Choice = 0
        Bool_Val = True
        while Bool_Val == True:
                if Size_Limit > MAX_SIZE:
                        Choice = 2
                        Bool_Val = False
                        
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
                        time.sleep(.2)
                        Choice = 0
                        Bool_Val = False
                        
                elif GPIO.input(select) == False:
                        Size_Limit += 1
                        WIFI_PASSWORD += Selected_Character[Selected_Char]      #Add selected character to wifi password list
                        WIFI_PASS_Disp()
                        
                elif GPIO.input(enter) == False:
                        time.sleep(.2)
                        Choice = 1
                        Bool_Val = False
                        
        if Choice == 0:
                Confirmation_Back_Wifi_Pass() #Goes to Main_Menu()
                
        elif Choice == 1:
                Confirmation_Wifi_Pass() #Goes to Confirm_Wifi_Pass()

        elif Choice == 2:
                WIFI_PASSWORD = ''      #Reset wifi password
                Size_Limit = 0
                Selected_Char = 0       #Reset character counter
                Size_Disp()
                Main_Menu()

def Setup_Adafruit():
        Set_Ada_Disp()
        global Size_Limit
        global Adafruit_Info
        global Selected_Char
        global Selected_Character
        global MAX_SIZE
        Bool_Val = True
        Choice = 0
        
        while Bool_Val == True:
                if Size_Limit > MAX_SIZE:
                        Choice = 2
                        Bool_Val = False
                        
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
                        Set_Ada_Disp()

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
                        Set_Ada_Disp()

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
                        Set_Ada_Disp()
                              
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
                        Set_Ada_Disp()
                
                elif GPIO.input(back) == False:
                        time.sleep(.2)
                        Choice = 0
                        Bool_Val = False

                elif GPIO.input(select) == False:
                        Size_Limit += 1
                        Adafruit_Info += Selected_Character[Selected_Char]         #Add the selected character the Adafruit address list
                        Set_Ada_Disp()

                elif GPIO.input(enter) == False:
                        time.sleep(.2)
                        Choice = 1
                        Bool_Val = False
        if Choice == 0:
                Confirmation_Back_Adafruit()       #Confirm that you want to return to the main menu

        elif Choice == 1:
                Confirmation_Adafruit()

        elif Choice == 2:
                Adafruit_Info = ''         
                Selected_Char = 0       #Reset character counter
                Size_Limit = 0
                Size_Disp()
                Main_Menu()
                
def Setup_SSID():
        Set_SSID_Disp()
        global Size_Limit
        global SSID_Info
        global Selected_Char
        global Selected_Character
        global MAX_SIZE
        Bool_Val = True
        Choice = 0

        while Bool_Val == True:
                if Size_Limit > MAX_SIZE:
                        Choice = 2
                        Bool_Val = False
                        
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
                        Set_SSID_Disp()                                

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
                        Set_SSID_Disp()

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
                        Set_SSID_Disp()
                              
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
                        Set_SSID_Disp()
                
                elif GPIO.input(back) == False:
                        time.sleep(.2)
                        Choice = 0
                        Bool_Val = False
                        
                elif GPIO.input(enter) == False:
                        time.sleep(.2)
                        Choice = 1
                        Bool_Val = False

                elif GPIO.input(select) == False:
                        Size_Limit += 1
                        SSID_Info += Selected_Character[Selected_Char]         #Add the selected character the WIFI SSID list
                        Set_SSID_Disp()  

        if Choice == 0:
                Confirmation_Back_SSID()       #Confirm that you want to return to the main menu

        elif Choice == 1:
                Confirmation_SSID()

        elif Choice == 2:
                SSID_Info = ''          #Reset SSID information
                Selected_Char = 0       #Reset character counter
                Size_Limit = 0
                Size_Disp()
                Main_Menu()

def Confirmation_Back_Adafruit():
        Conf_Back_Disp()
        global Selected_Char
        global Adafruit_Info
        global Size_Limit
        Bool_Val = True
        Choice = 0
        while Bool_Val == True:
                if GPIO.input(back) == False:
                        time.sleep(.2)
                        Choice = 0
                        Bool_Val = False

                elif GPIO.input(select) == False:
                        time.sleep(.2)
                        Choice = 1
                        Bool_Val = False
                        
                elif GPIO.input(enter) == False:
                        time.sleep(.2)
                        Choice = 1
                        Bool_Val = False
        if Choice == 0:
                Setup_Adafruit()           #Return to Setup_Adafruit

        elif Choice == 1:
                Adafruit_Info = ''         #Reset Email information
                Selected_Char = 0       #Reset character counter
                Size_Limit = 0
                Main_Menu()             #Return to Main menu
                

def Confirmation_Back_Wifi_Pass():
        Conf_Back_Disp()
        global WIFI_PASSWORD
        global Selected_Char
        global Size_Limit
        Bool_Val = True
        Choice = 0
        while Bool_Val == True:
                if GPIO.input(back) == False:
                        time.sleep(.2)
                        Choice = 0
                        Bool_Val = False

                elif GPIO.input(select) == False:
                        time.sleep(.2)
                        Choice = 1
                        Bool_Val = False
                        
                elif GPIO.input(enter) == False:
                        time.sleep(.2)
                        Choice = 1
                        Bool_Val = False
                        
        if Choice == 0:
                WIFI_Password()         #Return to wifi_password
                
        elif Choice == 1:
                WIFI_PASSWORD = ''      #Reset wifi password
                Size_Limit = 0
                Selected_Char = 0       #Reset character counter
                Main_Menu()             #Return to main menu

def Confirmation_Back_SSID():
        Conf_Back_Disp()
        global Selected_Char
        global SSID_Info
        global Size_Limit
        Bool_Val = True
        Choice = 0

        while Bool_Val == True:
                if GPIO.input(back) == False:
                        time.sleep(.2)
                        Choice = 0
                        Bool_Val = False

                elif GPIO.input(select) == False:
                        time.sleep(.2)
                        Choice = 1
                        Bool_Val = False

                elif GPIO.input(enter) == False:
                        time.sleep(.2)
                        Choice = 1
                        Bool_Val = False

        if Choice == 0:
                Setup_SSID()           #Return to Setup_SSID
                
        elif Choice ==1:
                SSID_Info = ''          #Reset SSID information
                Selected_Char = 0       #Reset character counter
                Size_Limit = 0
                Main_Menu()             #Return to Main menu                

def Confirmation_Adafruit():
        global Selected_Char
        global Adafruit_Info
        Bool_Val = True
        Choice = 0
        
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        text_enter1 = 'IS THIS CORRECT?'
        text_enter2 = 'Y PRESS SELECT/ENTER'
        text_enter3 = 'N PRESS BACK'

        if len(Adafruit_Info) < 22:
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                draw.text((0,0),text_enter1,font=font, fill=255)
                draw.text((0,7),text_enter2,font=font, fill=255)
                draw.text((0,15),text_enter3,font=font, fill=255)
                draw.text((0,23),Adafruit_Info,font=font, fill=255)
                disp.image(image)
                disp.display()
        elif len(Adafruit_Info) > 21:
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                draw.text((0,0),text_enter1,font=font, fill=255)
                draw.text((0,7),text_enter2,font=font, fill=255)
                draw.text((0,15),text_enter3,font=font, fill=255)
                draw.text((0,23),Adafruit_Info[0:21],font=font, fill=255)
                draw.text((0,31),Adafruit_Info[21:42],font=font, fill=255)
                disp.image(image)
                disp.display()
             
        while Bool_Val == True:
                if GPIO.input(back) == False:
                        time.sleep(.2)
                        Choice = 0
                        Bool_Val = False

                elif GPIO.input(select) == False:
                        time.sleep(.2)
                        Choice = 1
                        Bool_Val = False
                        
                elif GPIO.input(enter) == False:
                        time.sleep(.2)
                        Choice = 1
                        Bool_Val = False
                        
        if Choice == 0:
                Setup_Adafruit()           #Return to Setup_Adafruit
        elif Choice == 1:
                Selected_Char = 0
                Main_Menu()

def Confirmation_Wifi_Pass():
        global WIFI_PASSWORD
        global Selected_Char
        Choice = 0
        Bool_Val = True
        
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        text_enter1 = 'IS THIS CORRECT?'
        text_enter2 = 'Y PRESS SELECT/ENTER'
        text_enter3 = 'N PRESS BACK'
        if len(WIFI_PASSWORD) < 22:
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                draw.text((0,0),text_enter1,font=font, fill=255)
                draw.text((0,7),text_enter2,font=font, fill=255)
                draw.text((0,15),text_enter3,font=font, fill=255)
                draw.text((0,23),WIFI_PASSWORD,font=font, fill=255)
                disp.image(image)
                disp.display()
        elif len(WIFI_PASSWORD) > 21:
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                draw.text((0,0),text_enter1,font=font, fill=255)
                draw.text((0,7),text_enter2,font=font, fill=255)
                draw.text((0,15),text_enter3,font=font, fill=255)
                draw.text((0,23),WIFI_PASSWORD[0:21],font=font, fill=255)
                draw.text((0,31),WIFI_PASSWORD[21:42],font=font, fill=255)
                disp.image(image)
                disp.display()     

        while Bool_Val == True:
                if GPIO.input(back) == False:
                        time.sleep(.2)
                        Choice = 0
                        Bool_Val = False

                elif GPIO.input(select) == False:
                        time.sleep(.2)
                        Choice = 1
                        Bool_Val = False

                elif GPIO.input(enter) == False:
                        time.sleep(.2)
                        Choice = 1
                        Bool_Val = False
                        
        if Choice == 0:
                WIFI_Password()         #Return to wifi_password
        elif Choice == 1:
                Selected_Char = 0
                Main_Menu()

def Confirmation_SSID():
        global Selected_Char
        global SSID_Info
        Bool_Val = True
        Choice = 0
        
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        text_enter1 = 'IS THIS CORRECT?'
        text_enter2 = 'Y PRESS SELECT/ENTER'
        text_enter3 = 'N PRESS BACK'
        if len(SSID_Info) < 22:
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                draw.text((0,0),text_enter1,font=font, fill=255)
                draw.text((0,7),text_enter2,font=font, fill=255)
                draw.text((0,15),text_enter3,font=font, fill=255)
                draw.text((0,23),SSID_Info,font=font, fill=255)
                disp.image(image)
                disp.display()
        elif len(SSID_Info) > 21:
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                draw.text((0,0),text_enter1,font=font, fill=255)
                draw.text((0,7),text_enter2,font=font, fill=255)
                draw.text((0,15),text_enter3,font=font, fill=255)
                draw.text((0,23),SSID_Info[0:21],font=font, fill=255)
                draw.text((0,31),SSID_Info[21:42],font=font, fill=255)
                disp.image(image)
                disp.display()  

        while Bool_Val == True:
                if GPIO.input(back) == False:
                        time.sleep(.2)
                        Choice = 0
                        Bool_Val = False

                elif GPIO.input(select) == False:
                        time.sleep(.2)
                        Choice = 1
                        Bool_Val = False

                elif GPIO.input(enter) == False:
                        time.sleep(.2)
                        Choice = 1
                        Bool_Val = False

        if Choice == 0:
                Setup_SSID()           #Return to Setup_SSID

        elif Choice == 1:
                Selected_Char = 0
                Main_Menu()


def Main_Disp():
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        text_main1 ='0)ENTER ADAFRUIT KEY'
        text_main2 ='1)SETUP WIFI PASSWORD'
        text_main3 ='2)ENTER WIFI SSID'
        text_main4 ='3)SCAN FOR WIFI'
        text_main5 ='4)DISPLAY INPUTS'
        text_main_input = 'Your Selection: '
        draw.text((0,0),text_main1,font=font, fill=255)
        draw.text((0,7),text_main2,font=font, fill=255)
        draw.text((0,15),text_main3,font=font, fill=255)
        draw.text((0,23),text_main4,font=font, fill=255)
        draw.text((0,31),text_main5, font=font,fill=255)
        draw.text((0,39),text_main_input + str(Selected_Char),font=font, fill=255)
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
        text_size = 'SIZE OF INPUT: '
        draw.text((0,15),text_size + str(Size_Limit),font=font, fill=255)
        draw.text((0,0),text_wifi_pass1,font=font, fill=255)
        draw.text((0,7),text_wifi_pass6 + Selected_Character[Selected_Char],font=font, fill=255)
        draw.text((0,31),text_wifi_pass2,font=font, fill=255)
        draw.text((0,39),text_wifi_pass3,font=font, fill=255)
        draw.text((0,47),text_wifi_pass4,font=font, fill=255)
        draw.text((0,55),text_wifi_pass5,font=font, fill=255)	
        disp.image(image)
        disp.display()

def Set_Ada_Disp():
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        text_Adafruit = 'ENTER ADAFRUIT KEY'
        text_Adafruit2 = 'ABCDEFGHIJKLMNOPQRSTU'
        text_Adafruit3 = 'abcdefghijklmnopqrstu'
        text_Adafruit4 = 'VWXYZ1234567890_./'
        text_Adafruit5 = 'vwxyz!@#$%^&*()\<>'
        text_Adafruit6 = 'CURRENT SELECTION:'
        text_size = 'SIZE OF INPUT: '
        draw.text((0,15),text_size + str(Size_Limit),font=font, fill=255)
        draw.text((0,0),text_Adafruit,font=font, fill=255)
        draw.text((0,7),text_Adafruit6 + Selected_Character[Selected_Char],font=font, fill=255)
        draw.text((0,31),text_Adafruit2,font=font, fill=255)
        draw.text((0,39),text_Adafruit3,font=font, fill=255)
        draw.text((0,47),text_Adafruit4,font=font, fill=255)
        draw.text((0,55),text_Adafruit5,font=font, fill=255)	
        disp.image(image)
        disp.display()

def Set_SSID_Disp():
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        text_SSID1 = 'ENTER WIFI SSID'
        text_SSID2 = 'ABCDEFGHIJKLMNOPQRSTU'
        text_SSID3 = 'abcdefghijklmnopqrstu'
        text_SSID4 = 'VWXYZ1234567890_./'
        text_SSID5 = 'vwxyz!@#$%^&*()\<>'
        text_SSID6 = 'CURRENT SELECTION:'
        text_size = 'SIZE OF INPUT: '
        draw.text((0,15),text_size + str(Size_Limit),font=font, fill=255)
        draw.text((0,0),text_SSID1,font=font, fill=255)
        draw.text((0,7),text_SSID6 + Selected_Character[Selected_Char],font=font, fill=255)
        draw.text((0,31),text_SSID2,font=font, fill=255)
        draw.text((0,39),text_SSID3,font=font, fill=255)
        draw.text((0,47),text_SSID4,font=font, fill=255)
        draw.text((0,55),text_SSID5,font=font, fill=255)	
        disp.image(image)
        disp.display()

def Conf_Back_Disp():
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        text_con_back2 = 'EXIT TO MAIN MENU?'
        text_con_back3 = 'Y PRESS SELECT/ENTER'
        text_con_back4 = 'N PRESS BACK'
        draw.text((0,0),text_con_back2,font=font, fill=255)
        draw.text((0,7),text_con_back3,font=font, fill=255)
        draw.text((0,15),text_con_back4,font=font, fill=255)            
        disp.image(image)
        disp.display()

def Size_Disp():
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        text_enter1 = 'INPUT IS INVALID'
        text_enter2 = 'YOU HAVE REACHED THE'
        text_enter3 = 'MAX SIZE FOR INPUT'
        text_enter4 = 'INPUT WILL BE RESET'
        draw.text((0,0),text_enter1,font=font, fill=255)
        draw.text((0,7),text_enter2,font=font, fill=255)
        draw.text((0,15),text_enter3,font=font, fill=255)
        draw.text((0,23),text_enter4,font=font, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(5)

def Scan_Wifi():
        global Selected_Char
        global SSID_Info
        global Val
        global essid
        
        p1 = subprocess.Popen(["iwlist","wlan0","scan"],stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["grep", "-oP", "SSID:\"\K[^\"]+"],stdin=p1.stdout,stdout=subprocess.PIPE)

        p1.stdout.close()
        out,err = p2.communicate()
        #print(out)
        essid = out.splitlines()
        #print(essid)
        essid = list(set(essid))
        #print(essid)
        #print(len(essid))

        Val = len(essid)
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        text_enter1 = 'SELECT A WIFI SSID: '
        draw.text((0,0),text_enter1 + str(Selected_Char),font=font, fill=255)
        if len(essid) > 0:
                draw.text((0,7),essid[0],font=font,fill=255)
                if len(essid) >1:
                        draw.text((0,23),essid[1],font=font,fill=255)
        disp.image(image)
        disp.display()
        Bool_Val = True
        
        while Bool_Val == True:
                if GPIO.input(d_down) == False:
                        time.sleep(.1)
                        Selected_Char += 1
                        if Selected_Char > Val:
                                Selected_Char = 0
                        scan_disp()
                        
                elif GPIO.input(d_up) == False:
                        time.sleep(.1)
                        Selected_Char -= 1
                        if Selected_Char < 0:
                                Selected_Char = Val
                        scan_disp()

                elif GPIO.input(d_left) == False:
                        time.sleep(.1)
                        Selected_Char -= 1
                        if Selected_Char < 0:
                                Selected_Char = Val
                        scan_disp()

                elif GPIO.input(d_right) == False:
                        time.sleep(.1)
                        Selected_Char += 1
                        if Selected_Char > Val:
                                Selected_Char = 0
                        scan_disp()

                elif GPIO.input(select) == False:
                        time.sleep(.2)
                        Bool_Val = False


                elif GPIO.input(enter) == False:
                        time.sleep(.2)
                        Bool_Val = False

        SSID_Info = essid[Selected_Char]
              
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        text_con = 'YOUR SELECTION IS'
        draw.text((0,0),text_con,font=font, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(4)
        Main_Menu()
        
def scan_disp():
        global essid
        global Val
        if Val < 4:
        
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                text_enter1 = 'SELECT A WIFI SSID: '
                draw.text((0,0),text_enter1 + str(Selected_Char),font=font, fill=255)
                draw.text((0,7),essid[0],font=font,fill=255)
                draw.text((0,23),essid[1],font=font,fill=255)
                disp.image(image)
                disp.display()
        

def Disp_Inputs():
        global Adafruit_Info
        global WIFI_PASSWORD
        global SSID_Info
        Bool_Val = True
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        text_in = 'YOUR INPUTS WILL'
        text_in2 = 'BE DISPLAYED'
        text_in3 = 'PRESS SELECT/ENTER'
        text_in4 = 'TO GO TO NEXT SCREEN'
        draw.text((0,0),text_in,font=font, fill=255)
        draw.text((0,7),text_in2,font=font, fill=255)
        draw.text((0,15),text_in3,font=font, fill=255)
        draw.text((0,23),text_in4,font=font, fill=255)
        disp.image(image)
        disp.display()
        while Bool_Val == True:
                if GPIO.input(select) == False:
                        time.sleep(.2)
                        Bool_Val = False
                        
                elif GPIO.input(enter) == False:
                        time.sleep(.2)
                        Bool_Val = False
        Bool_Val = True
        
        text_ssid = 'YOUR WIFI SSID'
        text_wifi = 'YOUR WIFI PASSWORD'
        text_ada = 'YOUR ADAFRUIT KEY'

        if len(SSID_Info) < 21:
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                draw.text((0,0),text_ssid,font=font, fill=255)
                draw.text((0,7),SSID_Info,font=font, fill=255)
                disp.image(image)
                disp.display()
        elif len(SSID_Info) > 21:
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                draw.text((0,0),text_ssid,font=font, fill=255)
                draw.text((0,7),SSID_Info[0:21],font=font, fill=255)
                draw.text((0,15),SSID_Info[21:42],font=font, fill=255)
                disp.image(image)
                disp.display()

        while Bool_Val == True:
                if GPIO.input(select) == False:
                        time.sleep(.2)
                        Bool_Val = False
                        
                elif GPIO.input(enter) == False:
                        time.sleep(.2)
                        Bool_Val = False
        Bool_Val = True

        if len(WIFI_PASSWORD) < 21:
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                draw.text((0,0),text_wifi,font=font, fill=255)
                draw.text((0,7),WIFI_PASSWORD,font=font, fill=255)
                disp.image(image)
                disp.display()
        elif len(WIFI_PASSWORD) > 21:
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                draw.text((0,0),text_wifi,font=font, fill=255)
                draw.text((0,7),WIFI_PASSWORD[0:21],font=font, fill=255)
                draw.text((0,15),WIFI_PASSWORD[21:42],font=font, fill=255)
                disp.image(image)
                disp.display()

        while Bool_Val == True:
                if GPIO.input(select) == False:
                        time.sleep(.2)
                        Bool_Val = False
                        
                elif GPIO.input(enter) == False:
                        time.sleep(.2)
                        Bool_Val = False
        Bool_Val = True

        if len(Adafruit_Info) < 21:
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                draw.text((0,0),text_ada,font=font, fill=255)
                draw.text((0,7),Adafruit_Info,font=font, fill=255)
                disp.image(image)
                disp.display()
        elif len(Adafruit_Info) > 21:
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                draw.text((0,0),text_ada,font=font, fill=255)
                draw.text((0,7),Adafruit_Info[0:21],font=font, fill=255)
                draw.text((0,15),Adafruit_Info[21:42],font=font, fill=255)
                disp.image(image)
                disp.display()

        while Bool_Val == True:
                if GPIO.input(select) == False:
                        time.sleep(.2)
                        Bool_Val = False
                        
                elif GPIO.input(enter) == False:
                        time.sleep(.2)
                        Bool_Val = False
        Main_Menu()
        
Main_Menu()
