# -*- coding: utf-8 -*-

import webiopi
import datetime
import subprocess
import configparser
import sys
sys.path.append('/home/pi/prog/temperature/')
import temperature


webiopi.setDebug()

GPIO = webiopi.GPIO

# GPIO pin using BCM(GPIO) numbering
#IO_TV_POWER = 4         # SW1
#IO_TV_VOL_UP = 17       # SW2
#IO_TV_VOL_DOWN = 27     # SW3
#IO_TV_CH_UP = 18        # SW4
#IO_TV_CH_DOWN = 5       # SW5
#IO_AIRCON_ON = 6        # SW6
#IO_AIRCON_OFF = 13      # SW7
#IO_AUDIO_POWER = 12     # SW8
#IO_AUDIO_AUX = 22       # SW9
#IO_PC_ROOM_LIGHT = 23   # SW10

# Scheduling aircon control settings
AIRCON_USE_TIMER = 'false'
AIRCON_MODE = "0"
AIRCON_ON_TIME  = datetime.time(5,30)
AIRCON_OFF_TIME = datetime.time(7,15)
AIRCON_HEAT_ON_TEMP = 16
AIRCON_COOL_ON_TEMP = 25
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
KEY_ONTIME = 'onTime'
KEY_OFFTIME = 'offTime'
KEY_USETIMER = 'useTimer'
KEY_MODE = 'mode'
KEY_HEATONTEMP = 'heatOnTemp'
KEY_COOLONTEMP = 'coolOnTemp'


# setup function is automatically called at WebIOPi startup
def setup():
    # This sleep need for the purpuse of clear "Errno 19"
    webiopi.sleep(20)

    # set the GPIO used by the light to output
    #GPIO.setFunction(IO_TV_POWER, GPIO.OUT)
    #GPIO.setFunction(IO_TV_POWER, GPIO.OUT)
    #GPIO.setFunction(IO_TV_VOL_UP, GPIO.OUT)
    #GPIO.setFunction(IO_TV_VOL_DOWN, GPIO.OUT)
    #GPIO.setFunction(IO_TV_CH_UP, GPIO.OUT)
    #GPIO.setFunction(IO_TV_CH_DOWN, GPIO.OUT)
    #GPIO.setFunction(IO_AIRCON_ON, GPIO.OUT)
    #GPIO.setFunction(IO_AIRCON_OFF, GPIO.OUT)
    #GPIO.setFunction(IO_AUDIO_POWER, GPIO.OUT)
    #GPIO.setFunction(IO_AUDIO_AUX, GPIO.OUT)
    #GPIO.setFunction(IO_PC_ROOM_LIGHT, GPIO.OUT)

    # Update Config
    readIniFile()

    # Run Temperature Thread
    #temperature.startGetTempThread()


# Read Config File
def readIniFile():
    global AIRCON_USE_TIMER, AIRCON_MODE, AIRCON_ON_TIME, AIRCON_OFF_TIME

    inifile = configparser.ConfigParser()
    inifile.read(INI_FILE_PASS, 'UTF-8')

    on = inifile.get(SECTION_AICRCONTIMER, KEY_ONTIME)
    off = inifile.get(SECTION_AICRCONTIMER, KEY_OFFTIME)
    # 引数を分割して設定
    array_on  = on.split(":")
    array_off = off.split(":")
    AIRCON_ON_TIME  = datetime.time(int(array_on[0]),int(array_on[1]))
    AIRCON_OFF_TIME = datetime.time(int(array_off[0]),int(array_off[1]))

    AIRCON_USE_TIMER = inifile.get(SECTION_AICRCONTIMER, KEY_USETIMER)
    AIRCON_MODE = inifile.get(SECTION_AICRCONTIMER, KEY_MODE)
    AIRCON_HEAT_ON_TEMP = inifile.get(SECTION_AICRCONTIMER, KEY_HEATONTEMP)
    AIRCON_COOL_ON_TEMP = inifile.get(SECTION_AICRCONTIMER, KEY_COOLONTEMP)


# loop function is repeatedly called by WebIOPi
def loop():
    # retrieve current datetime
    now = datetime.datetime.now()
    airconTimer(now)
    uploadTempToIFTTT(now)

    # gives CPU some time before looping again
    webiopi.sleep(1)


# Auto ON/OFF Aicrconditioner at every morning.
def airconTimer(now):
    if (AIRCON_USE_TIMER == 'false'):
        return

    # Exceptionally, don't execute program at holiday
    if ((now.weekday() == DATE_SATURDAY) or (now.weekday() == DATE_SUNDAY)):
        return

    # TODO:現在温度と閾値温度を比較してOFF/ONを決める　*****************

    # toggle ON all days at the correct time
    if ((now.hour == AIRCON_ON_TIME.hour) and (now.minute == AIRCON_ON_TIME.minute) and (now.second == 0)):
        if (AIRCON_MODE == "0"): # 暖房
            subprocess.call(["sh", "/home/pi/webiopi/I2C0x52-IR/command02.sh", "airconPowerOnHeat20.dat"])
        else: # 冷房
            subprocess.call(["sh", "/home/pi/webiopi/I2C0x52-IR/command02.sh", "airconPowerOnCool27.dat"])
        #subprocess.call(["sh", "/home/pi/webiopi/I2C0x52-IR/command02.sh", "lightPcRoom.dat"])

    # toggle OFF
    if ((now.hour == AIRCON_OFF_TIME.hour) and (now.minute == AIRCON_OFF_TIME.minute) and (now.second == 0)):
        subprocess.call(["sh", "/home/pi/webiopi/I2C0x52-IR/command02.sh", "airconPowerOff.dat"])
        #subprocess.call(["sh", "/home/pi/webiopi/I2C0x52-IR/command02.sh", "lightPcRoom.dat"])


# Auto upload temperature info to IFTTT
def uploadTempToIFTTT(now):
    if (((now.minute % 30)  == 0) and (now.second == 0)):     # every 30 minutes
        temperature.uploadIFTTT()



# destroy function is called at WebIOPi shutdown
#def destroy():
    #GPIO.digitalWrite(LIGHT, GPIO.LOW)


# ---------------------------- Call From Webiopi JavaScript -------------------------
@webiopi.macro
def setGpio(ioNum):
    gpio = int(ioNum)
    GPIO.digitalWrite(gpio, GPIO.LOW)
    webiopi.sleep(0.5)
    GPIO.digitalWrite(gpio, GPIO.HIGH)
    return 1


@webiopi.macro
def sendIr(targetName):
    #webiopi.debug(targetName)
    subprocess.call(["sh", "/home/pi/webiopi/I2C0x52-IR/command02.sh", targetName])
    return 1

@webiopi.macro
def getAirconTimer():
    # Config -> Global
    readIniFile()

    #動作モード（暖房、冷房、ドライ）を取得
    isHeat = "false"
    isCool = "false"
    if (AIRCON_MODE == "0"):
        isHeat = "true"
        isCool = "false"
    else:
        isHeat = "false"
        isCool = "true"

    return "%s;%s;%s;%s;%s" % (AIRCON_ON_TIME.strftime("%H:%M"),AIRCON_OFF_TIME.strftime("%H:%M"),AIRCON_USE_TIMER,isHeat,isCool)

@webiopi.macro
def setAirconTimer(on, off, sw, isHeat, isCool):
    #webiopi.debug(on)
    #webiopi.debug(off)
    #webiopi.debug(sw)
    #webiopi.debug(isHeat)
    #webiopi.debug(isCool)

    #動作モード（暖房、冷房、ドライ）を判定
    mode = "0"
    if(isHeat == "true"):
       mode = "0"     #暖房
    else:
       mode = "1"     #冷房

    # Configファイルに保存
    inifile = configparser.ConfigParser()
    inifile.read(INI_FILE_PASS, 'UTF-8')
    inifile.set(SECTION_AICRCONTIMER, KEY_USETIMER, sw)
    inifile.set(SECTION_AICRCONTIMER, KEY_MODE, mode)
    inifile.set(SECTION_AICRCONTIMER, KEY_ONTIME, on)
    inifile.set(SECTION_AICRCONTIMER, KEY_OFFTIME, off)
    with open(INI_FILE_PASS, 'w', encoding='utf8') as file:
        inifile.write(file)

    # Config -> Global
    readIniFile()
    return getAirconTimer()

@webiopi.macro
def getCurrentTemperature():
    temperature.getTempBySocket()
    #webiopi.debug('TEMP : ' + str(temperature.getTemperature()))
    #webiopi.debug('HUMI : ' + str(temperature.getHumidity()))
    return "%s;%s" % (temperature.getTemperature(), temperature.getHumidity())


