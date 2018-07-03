import webiopi
import datetime
import subprocess

webiopi.setDebug()

GPIO = webiopi.GPIO

# GPIO pin using BCM(GPIO) numbering
IO_TV_POWER = 4         # SW1
IO_TV_VOL_UP = 17       # SW2
IO_TV_VOL_DOWN = 27     # SW3
IO_TV_CH_UP = 18        # SW4
IO_TV_CH_DOWN = 5       # SW5
IO_AIRCON_ON = 6        # SW6
IO_AIRCON_OFF = 13      # SW7
IO_AUDIO_POWER = 12     # SW8
IO_AUDIO_AUX = 22       # SW9
IO_PC_ROOM_LIGHT = 23   # SW10

# Scheduling aircon control settings
HOUR_ON  = 5
MINUTE_ON  = 30
HOUR_OFF = 7
MINUTE_OFF = 15
DATE_MONDAY = 0
DATE_TUESDAY = 1
DATE_WEDNESDAY = 2
DATE_THURSDAY = 3
DATE_FRIDAY = 4
DATE_SATURDAY = 5
DATE_SUNDAY = 6

# IR Data Pass
IR_AIR_POWER_OFF = "../I2C0x5-IR/data_dir/airconPowerOff.dat"
IR_AIR_POWER_ON = "../I2C0x5-IR/data_dir/airconPowerOn.dat"


# setup function is automatically called at WebIOPi startup
def setup():
    # This sleep need for the purpuse of clear "Errno 19"
    webiopi.sleep(20)

    # set the GPIO used by the light to output
    GPIO.setFunction(IO_TV_POWER, GPIO.OUT)
    GPIO.setFunction(IO_TV_POWER, GPIO.OUT)
    GPIO.setFunction(IO_TV_VOL_UP, GPIO.OUT)
    GPIO.setFunction(IO_TV_VOL_DOWN, GPIO.OUT)
    GPIO.setFunction(IO_TV_CH_UP, GPIO.OUT)
    GPIO.setFunction(IO_TV_CH_DOWN, GPIO.OUT)
    GPIO.setFunction(IO_AIRCON_ON, GPIO.OUT)
    GPIO.setFunction(IO_AIRCON_OFF, GPIO.OUT)
    GPIO.setFunction(IO_AUDIO_POWER, GPIO.OUT)
    GPIO.setFunction(IO_AUDIO_AUX, GPIO.OUT)
    GPIO.setFunction(IO_PC_ROOM_LIGHT, GPIO.OUT)


# loop function is repeatedly called by WebIOPi
def loop():
    #webiopi.debug(">> Call loop 1")






    # Scheduling AirContos is disabled.
    webiopi.sleep(1000)
    return








    # retrieve current datetime
#    now = datetime.datetime.now()

    # Exceptionally, don't execute program at holiday
#    if ((now.weekday() == DATE_SATURDAY) or (now.weekday() == DATE_SUNDAY)):
#        webiopi.sleep(1)
#        return

    # toggle ON all days at the correct time
#   if ((now.hour == HOUR_ON) and (now.minute == MINUTE_ON) and (now.second == 0)):
        #setGpio(IO_AIRCON_ON)
#        GPIO.digitalWrite(IO_AIRCON_ON, GPIO.LOW)
#        webiopi.sleep(0.5)
#        GPIO.digitalWrite(IO_AIRCON_ON, GPIO.HIGH)

    # toggle OFF
#    if ((now.hour == HOUR_OFF) and (now.minute == MINUTE_OFF) and (now.second == 0)):
        #setGpio(IO_AIRCON_OFF)
#        GPIO.digitalWrite(IO_AIRCON_OFF, GPIO.LOW)
#        webiopi.sleep(0.5)
#        GPIO.digitalWrite(IO_AIRCON_OFF, GPIO.HIGH)

    # gives CPU some time before looping again
#    webiopi.sleep(1)



# destroy function is called at WebIOPi shutdown
#def destroy():
    #GPIO.digitalWrite(LIGHT, GPIO.LOW)


@webiopi.macro
def setGpio(ioNum):
    gpio = int(ioNum)
    GPIO.digitalWrite(gpio, GPIO.LOW)
    webiopi.sleep(0.5)
    GPIO.digitalWrite(gpio, GPIO.HIGH)
    #print("Low")
    #webiopi.sleep(1)
        #subprocess.call(["sudo", "./home/pi/Desktop/Study/Servomotor/turnLeft"])
    #else:
    #    GPIO.digitalWrite(IO_PC_ROOM_LIGHT, GPIO.LOW)
    #    print("Low")
    return 1


@webiopi.macro
def sendIr(dummy):
    webiopi.debug(">> Call sendIr")
    cmd = 'python ../I2C0x52-IR/IR-remocon02-commandline.py t \`cat ../I2C0x52-IR/data_dir/airconPowerOff.dat\`'
    #subprocess.call(cmd.split())
    subprocess.call(["sh", "../I2C0x52-IR/command02.sh", "data_dir/airconPowerOff.dat"])
    return 1

