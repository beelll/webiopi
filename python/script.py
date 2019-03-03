# -*- coding: utf-8 -*-

import webiopi
import datetime
import subprocess
import configparser

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
AIRCON_USE_TIMER = 'false'
AIRCON_ON_TIME  = datetime.time(5,30)
AIRCON_OFF_TIME = datetime.time(7,15)
DATE_MONDAY = 0
DATE_TUESDAY = 1
DATE_WEDNESDAY = 2
DATE_THURSDAY = 3
DATE_FRIDAY = 4
DATE_SATURDAY = 5
DATE_SUNDAY = 6

# INI File Define
INI_FILE_PASS = '/home/pi/webiopi/python/config.ini'
SECTION_AICRCONTIMER = 'AIRCONTIMER'
KEY_USETIMER = 'useTimer'
KEY_ONTIME = 'onTime'
KEY_OFFTIME = 'offTime'



# setup function is automatically called at WebIOPi startup
def setup():
    global AIRCON_USE_TIMER, AIRCON_ON_TIME, AIRCON_OFF_TIME

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

    # Config Load
    inifile = configparser.ConfigParser()
    inifile.read(INI_FILE_PASS, 'UTF-8')
    AIRCON_USE_TIMER = inifile.get(SECTION_AICRCONTIMER, KEY_USETIMER)
    on = inifile.get(SECTION_AICRCONTIMER, KEY_ONTIME)
    off = inifile.get(SECTION_AICRCONTIMER, KEY_OFFTIME)
    # 引数を分割して設定
    array_on  = on.split(":")
    array_off = off.split(":")
    AIRCON_ON_TIME  = datetime.time(int(array_on[0]),int(array_on[1]))
    AIRCON_OFF_TIME = datetime.time(int(array_off[0]),int(array_off[1]))
    webiopi.debug(AIRCON_USE_TIMER)
    webiopi.debug(AIRCON_ON_TIME)
    webiopi.debug(AIRCON_OFF_TIME)


# loop function is repeatedly called by WebIOPi
def loop():
    #webiopi.debug(">> Call loop 1")
    # Scheduling AirContos is disabled.
#    webiopi.sleep(1000)
#    return

    # retrieve current datetime
    now = datetime.datetime.now()

    # Exceptionally, don't execute program at holiday
    if ((now.weekday() == DATE_SATURDAY) or (now.weekday() == DATE_SUNDAY)):
        webiopi.sleep(1)
        return

    # toggle ON all days at the correct time
    if ((now.hour == AIRCON_ON_TIME.hour) and (now.minute == AIRCON_ON_TIME.minute) and (now.second == 0)):
        subprocess.call(["sh", "/home/pi/webiopi/I2C0x52-IR/command02.sh", "airconPowerOnHeat20.dat"])

    # toggle OFF
    if ((now.hour == AIRCON_OFF_TIME.hour) and (now.minute == AIRCON_OFF_TIME.minute) and (now.second == 0)):
        subprocess.call(["sh", "/home/pi/webiopi/I2C0x52-IR/command02.sh", "airconPowerOff.dat"])

    # gives CPU some time before looping again
    webiopi.sleep(1)




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
def sendIr(targetName):
    #webiopi.debug(targetName)
    subprocess.call(["sh", "/home/pi/webiopi/I2C0x52-IR/command02.sh", targetName])
    return 1

@webiopi.macro
def getAirconTimer():
    webiopi.debug(">> Call getAirconTimer")
    return "%s;%s" % (AIRCON_ON_TIME.strftime("%H:%M"),AIRCON_OFF_TIME.strftime("%H:%M"))

@webiopi.macro
def setAirconTimer(on, off):
    webiopi.debug(">> Call setAirconTimer")
    webiopi.debug(on)
    webiopi.debug(off)
    global AIRCON_ON_TIME, AIRCON_OFF_TIME
    # 引数を分割して設定
    array_on  = on.split(":")
    array_off = off.split(":")
    AIRCON_ON_TIME  = datetime.time(int(array_on[0]),int(array_on[1]))
    AIRCON_OFF_TIME = datetime.time(int(array_off[0]),int(array_off[1]))

     # Configファイルに保存
    inifile = configparser.ConfigParser()
    inifile.add_section(SECTION_AICRCONTIMER)
    inifile.set(SECTION_AICRCONTIMER, KEY_ONTIME, on)
    inifile.set(SECTION_AICRCONTIMER, KEY_OFFTIME, off)
    with open(INI_FILE_PASS, 'w', encoding='utf8') as file:
        inifile.write(file)

    # ToDo
    # トグルスイッチと連動
    return getAirconTimer()

