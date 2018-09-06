import RPi.GPIO as GPIO
from firebase_admin import db
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import time
import urllib
import urllib.request
PIN_TRIGGER = 7
PIN_ECHO = 11
cred =credentials.Certificate('farm-672f9-firebase-adminsdk-2eud9-ba87c485bd.json') # name of the downloaded json file
default_app = firebase_admin.initialize_app(cred, {'databaseURL' :'https://farm-672f9.firebaseio.com//'}) # data base url of your project
root = db.reference()
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)#led
GPIO.setup(23, GPIO.IN) #PIR
GPIO.setup(24, GPIO.OUT) #BUzzer
GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)
base_url = " https://api.thingspeak.com/update?api_key=56CU24ALSVDFJM77"

def ultrasonic():
      GPIO.output(PIN_TRIGGER, GPIO.LOW)
      
      print("Transmitting Ultrasonic Waves")

      time.sleep(2)

      print("Calculating the object distance")

      GPIO.output(PIN_TRIGGER, GPIO.HIGH)

      time.sleep(0.00001)

      GPIO.output(PIN_TRIGGER, GPIO.LOW)

      while GPIO.input(PIN_ECHO)==0:
            pulse_start_time = time.time()
      while GPIO.input(PIN_ECHO)==1:
            pulse_end_time = time.time()

      pulse_duration = pulse_end_time - pulse_start_time
      distance = round(pulse_duration * 17150, 2)
      print("Object is at",distance,"cm")
time.sleep(2) # to stabilize sensor

def get():
    print("get");
    x = str(db.reference('farm-672f9/farm-672f9/Command/Command'.format()).get())
    print(x)
    if(x == '"ON"'):#Led on
         print("led is on")
         GPIO.output(18,1)
    if (x == '"OFF"'):#Led off
         print("led is off")
         GPIO.output(18,0)
    if(x == '"BON"'):#buzzer_on
         print("Buzzer on")
         GPIO.output(24, True)
    if(x == '"BOFF"'):#buzzer off
         print("Buzzer off")
         GPIO.output(24, False)
    if(x == '"UON"'):#Ultrasonic on
         print("Ultrasonic on")
         ultrasonic()
    if(x == '"UOFF"'):#ultrasonic off
         print("Ultrasonic off")
    if(x == '"ROFF"'):#Repellers off
         print("Repellers off")
         GPIO.output(24, False)
         GPIO.output(18,0)
    if(x == '"RON"'):#Repellers on
         print("Repellers on")
         GPIO.output(24, True)
         GPIO.output(18,1)
    if(x == '"MOFF"'):
         automatic()
    


def manual():
    print("manual")
    while True:
         print("testing")
         if GPIO.input(23):
                print("Motion Detected...")
                url = base_url+"&field1=1"
                print(url)
                f =  urllib.request.urlopen(url)
                response=f.read()
                print('response')
                print(response)
                f.close()
         get()
         time.sleep(1)    

def automatic():
    print("automatic")
    while True:
        x = str(db.reference('farm-672f9/farm-672f9/Command/Command'.format()).get())
        if(x == '"MOFF"'):
            if GPIO.input(23):
                print("Motion Detected...")
                url = base_url+"&field1=1"
                print(url)
                f =  urllib.request.urlopen(url)
                response=f.read()
                print('response')
                print(response)
                f.close()
                ultrasonic()
                GPIO.output(24, True)#buzzer
                GPIO.output(18, True)#led
                time.sleep(15) #Buzzer turns on for 0.5 sec
            else:
                print("not detected")
                GPIO.output(24, False)
                GPIO.output(18, False)
                time.sleep(1)
            time.sleep(0.1) #loop delay, should be less than detection delay
        if(x == '"MON"'):
            manual()    
while True:
    print("testing")
    x = str(db.reference('farm-672f9/farm-672f9/Command/Command'.format()).get())
 
    if (x=='"MON"'):
         
         manual()
    if(x=='"MOFF"'): 
         
         automatic()

    time.sleep(1)

