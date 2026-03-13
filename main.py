# -*- coding:utf-8 -*-

import time
import l76K
import l76_config
import time
import math
from machine import UART, Pin, WDT

Button = machine.Pin( 15, Pin.IN, Pin.PULL_UP)       # Button
Buzzer = machine.Pin( 17, Pin.OUT)                   # Buzzer

led = machine.Pin("LED", machine.Pin.OUT)  # On board Pi Pico LED

WDTset = 10                                                          # set to 0 to disable WDT for testing.
                                                                     # from machine import WDT
if WDTset != 0 :
    wdt = WDT(timeout=8000)                                          # enable WDT with a timeout of 8s


uart_print = UART(0,baudrate=9600,tx=Pin(0),rx=Pin(1))
#uart_print = UART(1,baudrate=9600,tx=Pin(4),rx=Pin(5))
StandBy = Pin(17,Pin.OUT)
StandBy.value(0)
ForceOn = Pin(14,Pin.OUT)
ForceOn.value(0)
rxData = bytes()
rxDataTemp = bytes()
#rxData = ''
# 
# while True:
#     while uart_print.any() > 0:
#         rxDataTemp = uart_print.read(1)
#         if rxDataTemp.decode('utf-8') == "\n" :
# #            print(rxData.decode('utf-8')[:7])
#             if "$GNRMC" in rxData.decode('utf-8') :
#                 print(rxData.decode('utf-8'))
#             if "$GNGGA" in rxData.decode('utf-8') :
#                 print(rxData.decode('utf-8'))
#             rxData = bytes()
#         rxData = rxData + rxDataTemp
# #   print(rxData)
#    if rxData.decode('utf-8')[:6] == '$GNRMC' :
#    print(rxData.decode('utf-8'))
#    print(rxData)         

# time.sleep(10)
x=l76K.L76X()
x.L76X_Set_Baudrate(9600)
x.L76X_Send_Command(x.SET_NMEA_BAUDRATE_115200)
time.sleep(2)
x.L76X_Set_Baudrate(115200)

x.L76X_Send_Command(x.SET_POS_FIX_500MS);

#Set output message
x.L76X_Send_Command(x.SET_NMEA_OUTPUT);

time.sleep(2)
x.L76X_Exit_BackupMode();
#x.L76X_Send_Command(x.SET_SYNC_PPS_NMEA_ON) # Not used on L76K

#x.L76X_Send_Command(x.SET_STANDBY_MODE)
#time.sleep(10)
#x.L76X_Send_Command(x.SET_NORMAL_MODE)
#x.config.StandBy.value(1)
#time.sleep(7)

# test1 = Uart_ReceiveString(1,2)
# print(test1)
if WDTset != 0 :
    wdt.feed()					# To prevent the WDT rebooting the pi during normal operation

while(1):
    x.L76X_Gat_GNRMC() 
    if(x.Status == 1):
        print ('Already positioned')
    else:
        print ('No positioning')
    print ('Time %02d: %02d : %02d'%(x.Time_H,x.Time_M,x.Time_S))

    print ('Lon = %f  Lat = %f'%(x.Lon,x.Lat))
    print ('Speed (Knots) = %02d'%(x.Speed))
    if int(x.Speed) > 34 : #49 * 0.86 :  # Convert to Knots
        print("Too fast for single carriageway")
        Buzzer.on()
    else :
        print("Speed OK")
        Buzzer.off()
    
    file = open ("locations.txt","a")
    file.write(('Time =%02d:%02d:%02d'%(x.Time_H,x.Time_M,x.Time_S))+","+str(x.Lat)+","+str(x.Lon)+", Speed (Kts) = "+str(x.Speed)+"\n")
    file.close()
    
    led.toggle()    
    time.sleep(10)
    if WDTset != 0 :
        wdt.feed()					# To prevent the WDT rebooting the pi during normal operation

#     print (x.Lat,chr(x.Lat_area),x.Lon,chr(x.Lon_area))
#     x.L76X_Baidu_Coordinates(x.Lat, x.Lon)
#     print ('Baidu coordinate %f ,%f'%(x.Lat_Baidu,x.Lon_Baidu))
#     x.L76X_Google_Coordinates(x.Lat,x.Lon)
#     print ('Google coordinate %f ,%f'%(x.Lon_Google,x.Lat_Google))
#     if Button.value() == 1 :
#         Buzzer.on()
#     time.sleep(5)
#     Buzzer.off()
