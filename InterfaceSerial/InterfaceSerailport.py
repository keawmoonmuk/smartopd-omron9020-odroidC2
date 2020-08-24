import serial
import os
import os.path
import sys
import errno
from datetime import datetime


#----------connect device Omron 9020-------------
def ConnectSerialportOmron9020(serialport):

    try:    
        print("Is conect Omron 9020  = {0}".format(serialport))
        
        ser = serial.Serial(port=serialport, baudrate=2400, parity=serial.PARITY_EVEN,
                            stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS,timeout=1)
        #ser.flush()
        ser.flushInput()
        if ser.isOpen():
            print(ser.name + " is open Omron 9020...")
         
        return ser
    
    except:
         
        print("Can not conection to seriaport to 9020")
  
#connec device Inbody 370
def ConnectSerialPortInbody370(serialport):
    
    try:
        print("Is conect Inbody bp320  = {0}".format(serialport))
        
        ser = serial.Serial(port=serialport, baudrate=19200, parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS,timeout=1)
        #ser.flush()
        ser.flushInput()
        if ser.isOpen():
            print(ser.name + " is open  inbody 370...")
            #logging.info("Conport is open..")
        return ser

    except:       
        print("---Can not conection to seriaport Bsm 370----")
           