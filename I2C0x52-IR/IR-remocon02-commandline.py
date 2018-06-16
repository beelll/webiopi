#!/usr/bin/python3
#coding: utf-8
#####!で始まる1行目の記述はShebangスクリプト自体を実行
#####2行目に、マジックコメントを記述文字エンコーディング
#
# ファイル名：IR-remocon02-commandline.py  python3用
# バージョン：2017/12/13 v1.0
#           2018/2/14   v2.0 python3用 

# ビット・トレード・ワン社提供のラズベリー・パイ専用 学習リモコン基板(型番：ADRSIR)用のツール
#　著作権者:(C) 2015 ビット・トレード・ワン社
#　ライセンス: ADL(Assembly Desk License)
#  実行方法：./IR-remocon02-commandline.py r 0
#
#　******使い方：コマンドライン　ツール
#学習リモコン→ラズハ゜イ　読込コマンド（r:)：、メモリＮＯ．(0-9)、 応答：データ
#　
#学習リモコン←ラズハ゜イ　書込コマンド（w:)：、メモリＮＯ．(0-9)、データ
#
#sample-data：ソニー	デジタルテレビ１	電源
#5B0018002E001800180018002E001800170018002E00190017001800170018002E00180018001800170018001700180017004F03

#
#　******Ｉ２Ｃ関係内部コマンド
# cmd R1_memo_no_write 0x15 bus-write(ADR,cmd,n)
# cmd R2_data_num_read 0x25 bus-read(ADR,cmd,n)
# cmd R3_data_read     0x35 bus-read(ADR,cmd,n)
# cmd W1_memo_no_write 0x19 bus-write(ADR,cmd,n)
# cmd W2_data_num_write0x29 bus-write(ADR,cmd,n)
# cmd W3_data_write    0x39 bus-read(ADR,cmd,n)
# cmd W4_flash_write   0x49 bus-read(ADR,cmd,n)
# cmd T1_trans_start   0x59 bus-write(ADR,cmd,n)
#

from __future__ import print_function
import smbus
import time
from time import sleep
#import commands
import subprocess
import os
import sys
import codecs

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This must match in the Arduino Sketch
#SLAVE_ADDRESS = 0x04
SLAVE_ADDRESS = 0x52
data_numH = 0x31
data_numL = 0x32
data_numHL = [0x00,0x31,0x32]
data_num = 10
memo_no = 0
block = []

#command
R1_memo_no_write = 0x15  #bus-write(ADR,cmd,1)
R2_data_num_read = 0x25 #bus-read(ADR,cmd,3)
R3_data_read           = 0x35 #bus-read(ADR,cmd,n)
W1_memo_no_write  = 0x19 #bus-write(ADR,cmd,1)
W2_data_num_write = 0x29 #bus-write(ADR,cmd,3)
W3_data_write           = 0x39 #bus-read(ADR,cmd,n)
W4_flash_write           = 0x49 #bus-read(ADR,cmd,n)
T1_trans_start             = 0x59 #bus-write(ADR,cmd,1)

############# read command
def read_command(memo_no):
# cmd R1_memo_no_write 0x15 bus-write(ADR,cmd,1)
    #print("memo_no write=",memo_no)
    bus.write_i2c_block_data(SLAVE_ADDRESS, R1_memo_no_write ,memo_no )   #= 0x15  #bus-write(ADR,cmd,1)

# cmd R2_data_num_read 0x25 bus-read(ADR,cmd,3)
    data_numHL = bus.read_i2c_block_data(SLAVE_ADDRESS, R2_data_num_read ,3 )#= 0x25 #bus-read(ADR,cmd,3)
    data_num = data_numHL[1]
    data_num *= 256
    data_num += data_numHL[2]
    if data_num < 65535:

     #print("data_num =",data_num )

# cmd R3_data_read           0x35 bus-read(ADR,cmd,n)
     block = []
     block_dat  = bus.read_i2c_block_data(SLAVE_ADDRESS, R3_data_read , 1)       #= 0x35 #bus-read(ADR,cmd,n)
     for i in range(data_num ):
      block_dat  = bus.read_i2c_block_data(SLAVE_ADDRESS, R3_data_read , 4)       #= 0x35 #bus-read(ADR,cmd,n)
      block.append(block_dat[0])
      block.append(block_dat[1])
      block.append(block_dat[2])
      block.append(block_dat[3])
    #print(block)  #for denug
    else:
     print("data_num error=",data_num )
     
    return block

################# write command
def write_command(memo_no,block2):
    #f = open(filename,'r')
    #block2 =f.read()
    #f.close()
    #print(block2)
    #print(len(block2))
    str_tmp = ""
    int_tmp = []
    #for i in range(len(block2)/2): #TypeError: 'float' object cannot be interpreted as an integer
    for i in range(int(len(block2)/2)):
    
        str_tmp = block2[i*2] + block2[i*2+1]
        int_tmp.append( int(str_tmp, 16))
    #print(int_tmp)  
    #print(len(int_tmp))
# cmd W1_memo_no_write 0x19 bus-write(ADR,cmd,1)
    bus.write_i2c_block_data(SLAVE_ADDRESS, W1_memo_no_write ,memo_no )   #= 
# cmd W2_data_num_write 0x29 bus-write(ADR,cmd,3)
    data_num = int(len(int_tmp)/4)  #for test
    data_numHL = [0x31,0x32] #for test
    data_numHL[0] = int(data_num/256)
    data_numHL[1] = int(data_num%256)
    #print(data_numHL ,data_numHL[0] ,data_numHL[1])
    bus.write_i2c_block_data(SLAVE_ADDRESS, W2_data_num_write ,  data_numHL)   #= 
    #TypeError: Third argument must be a list of at least one, but not more than 32 integers
# cmd W3_data_write           0x39 bus-read(ADR,cmd,n)
    #print(data_num)
    data_numHL = [0x31,0x32,0x33,0x34] #for test 
    for i in range(data_num):
         data_numHL[0] = int_tmp[i*4+0]
         data_numHL[1] = int_tmp[i*4+1]
         data_numHL[2] = int_tmp[i*4+2]
         data_numHL[3] = int_tmp[i*4+3]
         bus.write_i2c_block_data(SLAVE_ADDRESS, W3_data_write , data_numHL)   #= 
# cmd W4_flash_write           0x49 bus-read(ADR,cmd,n)
    bus.write_i2c_block_data(SLAVE_ADDRESS, W4_flash_write,memo_no)   #=

# #############trans command
def trans_command(block2):
    #f = open(filename,'r')
    #block2 =f.read()
    #f.close()
    #print(block2)
    #print(len(block2))
    str_tmp = ""
    int_tmp = []
    for i in range(int(len(block2)//2)):
    #for i in range(len(block2)/2):
        str_tmp = block2[i*2] + block2[i*2+1]
        int_tmp.append( int(str_tmp, 16))
    #print(int_tmp)  
    #print(len(int_tmp))
# cmd W2_data_num_write 0x29 bus-write(ADR,cmd,3)
    data_num = int(len(int_tmp)//4)  #for test
    data_numHL = [0x31,0x32] #for test
    data_numHL[0] = int(data_num//256)
    data_numHL[1] = int(data_num%256)
    bus.write_i2c_block_data(SLAVE_ADDRESS, W2_data_num_write ,  data_numHL)   #= 
# cmd W3_data_write           0x39 bus-read(ADR,cmd,n)
    #print(data_num)
    data_numHL = [0x31,0x32,0x33,0x34] #for test 
    for i in range(data_num):
         data_numHL[0] = int_tmp[i*4+0]
         data_numHL[1] = int_tmp[i*4+1]
         data_numHL[2] = int_tmp[i*4+2]
         data_numHL[3] = int_tmp[i*4+3]
         bus.write_i2c_block_data(SLAVE_ADDRESS, W3_data_write , data_numHL)   #= 
 # cmd T1_trans_start             0x59 bus-write(ADR,cmd,1)
    memo_no = [0x00 ] #for dummy
    bus.write_i2c_block_data(SLAVE_ADDRESS, T1_trans_start,memo_no )   #= 

###########################   main
dir_name = '/home/pi/I2C0x52-IR/'
os.chdir(dir_name)
    
while True:
    argvc = sys.argv
    argc = len(argvc)
#-------------------180413ここから
    if (argc == 1):
        print("usage:python3 IR-remocon02-commandline.py r 0")
        break

    command = argvc[1]
    memo_no = [0x0]

    if (argc == 2):
       if command == 't':
           block2 = sys.stdin.readline()
           trans_command(block2)
           break
#-------------------180413ここまで
    elif  (argc  == 3):
       if command == 'r' :
           res_data = [141,0,47,0] #bin num [0x141, 0x0, 0x68, 0x0]
           memo_no[0]= int(argvc[2])
           #print(memo_no)  
           res_data = read_command(memo_no)
           for i in range(len(res_data)):
             print('{:02X}'.format(res_data[i]), end=""); #141
           print('')          
           break
       elif command == 't' :
           #print("sys.argv[2]=",sys.argv[2])
           #print("trans_start")
           block2 = argvc[2]
           #print(block2)
           trans_command(block2)
           break
#-------------------180413ここから
       elif command == 'w':
           block2 = sys.stdin.readline()
           memo_no[0]=int(argvc[2])

           write_command(memo_no,block2)
           break
#-------------------180413ここまで
    elif  (argc  == 4):
       if command == 'w' :
           #print("sys.argv[3]=",sys.argv[3])
           
           #print("w_mode_start")
           block2 = argvc[3]
           #print(block2)
           memo_no[0]= int(argvc[2])

           write_command(memo_no,block2)
           break   


