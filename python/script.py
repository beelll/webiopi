import webiopi
import datetime

GPIO = webiopi.GPIO

#LIGHT = 23 # GPIO pin using BCM numbering


IO_AIRCON_ON = 6
IO_AIRCON_OFF = 13
IO_LIGHT_PC_ROOM = 23
IO_TV_POWER = 4

HOUR_ON  = 5  # Turn ON  at 05:00
MINUTE_ON  = 30
HOUR_OFF = 22  # Turn OFF at 07:00
MINUTE_OFF = 16
# setup function is automatically called at WebIOPi startup
def setup():
    # set the GPIO used by the light to output
    GPIO.setFunction(IO_AIRCON_ON, GPIO.OUT)
    GPIO.setFunction(IO_AIRCON_OFF, GPIO.OUT)
    GPIO.setFunction(IO_LIGHT_PC_ROOM, GPIO.OUT)
    GPIO.setFunction(IO_TV_POWER, GPIO.OUT)

    # retrieve current datetime
    now = datetime.datetime.now()

    # test if we are between ON time and tun the light ON
    #if ((now.hour >= HOUR_ON) and (now.hour < HOUR_OFF)):
    #    GPIO.digitalWrite(LIGHT, GPIO.HIGH)



# loop function is repeatedly called by WebIOPi
def loop():
    # retrieve current datetime
    now = datetime.datetime.now()

    # toggle ON all days at the correct time
    if ((now.hour == HOUR_ON) and (now.minute == MINUTE_ON) and (now.second == 0)):
        #setGpio(IO_AIRCON_ON)
        print("Call ON 1")
        GPIO.digitalWrite(IO_AIRCON_ON, GPIO.LOW)
        webiopi.sleep(0.5)
        GPIO.digitalWrite(IO_AIRCON_ON, GPIO.HIGH)

    # toggle OFF
    if ((now.hour == HOUR_OFF) and (now.minute == MINUTE_OFF) and (now.second == 0)):
        #setGpio(IO_AIRCON_OFF)
        print("Call OFF 1")
        GPIO.digitalWrite(IO_AIRCON_OFF, GPIO.LOW)
        webiopi.sleep(0.5)
        GPIO.digitalWrite(IO_AIRCON_OFF, GPIO.HIGH)

    # gives CPU some time before looping again
    webiopi.sleep(1)



# destroy function is called at WebIOPi shutdown
#def destroy():
    #GPIO.digitalWrite(LIGHT, GPIO.LOW)


@webiopi.macro
def setGpio(ioNum):
    gpio = int(ioNum)
    #print(gpio)
    GPIO.digitalWrite(gpio, GPIO.LOW)
    webiopi.sleep(0.5)
    GPIO.digitalWrite(gpio, GPIO.HIGH)
    #print("High")
    #print("Low")
    #webiopi.sleep(1)
        #subprocess.call(["sudo", "./home/pi/Desktop/Study/Servomotor/turnLeft"])
    #else:
    #    GPIO.digitalWrite(IO_LIGHT_PC_ROOM, GPIO.LOW)
    #    print("Low")
    return 1
