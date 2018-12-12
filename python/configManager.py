# -*- coding: utf-8 -*-

import ConfigParser


inifile = ConfigParser.SafeConfigParser()
inifile.read('./config.ini')


def initConfig():
    return

def getConfig(section, key):
    print inifile.get('AirConTimer', 'useTimer')
    return inifile.get('AirConTimer', 'useTimer')


def setConfig(section, key):
    inifile.set('AirConTimer', 'useTimer', 'false')


# for Debug
setConfig(1,1)
getConfig(1,1)


