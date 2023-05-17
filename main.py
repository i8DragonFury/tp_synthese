from I2C_LCD import I2CLcd
from machine import I2C, Pin, PWM, ADC
from time import sleep
import sys
import _thread
from keypad import KeyPad

keypad = KeyPad(13,12,11,10,9,8,7,6)

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
i2c_add = i2c.scan()[0]
lcd = I2CLcd(i2c,i2c_add, 2,16)

ledVert = Pin(14,Pin.OUT)   #GREEN LED
ledRouge = Pin(15,Pin.OUT)   # RED LED

buzzer = Pin(21, Pin.OUT)  #Buzzer Sound Machine
BEAT = 0.4

#LIGHT CAPTURE
adc = ADC(26)
ledBleu = Pin(19, Pin.OUT)

pwm = PWM(ledBleu)
pwm.freq(30000000)

terminateThread = False
rep = ""
    
#######################################################################################################################

def lectureRep():
    global terminateThread, rep
    while True:
        if terminateThread:
            break
        
        rep = sys.stdin.readline().strip()
        print(rep)
        
_thread.start_new_thread(lectureRep, ())

def touche():
    valeur = keypad.scan()
    if valeur != None:
        print(valeur, end="\r\n")
        lcd.clear()
        lcd.putstr(valeur)
    return valeur

######################################################################################################################
try:
    while True:
        
        if rep.lower() == "inscrire":
            lcd.clear()
            lcd.putstr("Mettez votre code (4 chiffres)")
            print("inscrire works")
            #key = touche()    
            
            code = []
            
            # if len(code) <= 4: #Mettre le code
            #     #code.append(key)
            #     pass
            # else:
            #     lcd.clear()
            #     lcd.putstr("Validez votre code")
                
            #     codeVal = []
                
                # if len(codeVal) <= 4:
                #     codeVal.append(key)   
                
        if pwm.duty_u16(adc.read_u16()):#LIGHT ON  
            ledBleu.value(0)
            ledRouge.value(0)
            ledVert.value(0)
            
            for i in range(3):
                buzzer.value(1)
                sleep(1)
                buzzer.value(0)
                   
            if rep.lower() == "login":
                buzzer.value(0)
                
                lcd.clear()
                lcd.putstr("Mettez votre code")
                        
                #if code == code Class --> works ELSE 
                        
            if rep.lower() == "login_fail":
                buzzer.value(0)
                sleep(1)
                
                for i in range(10):
                            
                    ledRouge.value(1)
                    buzzer.value(1)
                    sleep(0.5)
                            
                    ledRouge.value(0)
                    buzzer.value(0)
                    sleep(0.5)
        else:
            buzzer.value(0)
            for i in range(10):
                ledBleu.value(0)
                ledVert.value(1)
                sleep(1)
                ledVert.value(0)
                ledRouge.value(1)
                sleep(1)
                ledRouge.value(0)
                ledBleu.value(1)
                sleep(1)
                
        
          
except:
    pwm.deinit()