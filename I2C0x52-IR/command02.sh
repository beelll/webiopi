#!/usr/bin/bash
echo $1
python /home/pi/webiopi/I2C0x52-IR/IR-remocon02-commandline.py t `cat /home/pi/webiopi/I2C0x52-IR/data_dir/$1`

