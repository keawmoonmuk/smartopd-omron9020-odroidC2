import serial
import sys
import threading
import string
#import logging
import os
import os.path
from time import sleep
from datetime import datetime
#import datetime
import time
import socket
import binascii
import io
#from PIL import Image,ImageTk
from smartcard.System import readers
from smartcard.util import HexListToBinString, toHexString, toBytes
from smartcard.Exceptions import NoCardException
from PIL import ImageTk
from PIL import Image as PilImage
#tkinter
from tkinter import *
import tkinter as tk
from tkinter import Toplevel, Button, Tk, Menu
from tkinter import filedialog
from tkinter import messagebox

#import forder and sub directory 
from InterfaceSerial.InterfaceSerailport import ConnectSerialportOmron9020 , ConnectSerialPortInbody370

#Global
serialportOmron9020 = '/dev/ttyUSB0'    # Measuament 1  omron  9020
serialportInbody370 = '/dev/ttyUSB1'   # Measuaemt 2 BP Inbody Scala 370

#------Create varible global 
data_width = ""
data_height = ""
data_bmi =""
data_sys = ""
data_dia = ""
data_pr =""
cid  =  ""
firstname  =""      #th
lastname =""        #th
firstname_en  = ""  # en
lastname_en  = ""   # en

gender     = ""   
age  = ""
dateOfbrith = "" 

root = Tk()      # form
 
#Send to api
def Client_Toserver():

    global cid
    global firstname_en
    global lastname_en
    global gender
    global age
    global dateOfbrith
    
    global data_sys
    global data_dia
    global data_pr
    
     # Check insert smargt card
    print("Check insert smartcard")
    
    rpi_token_number = "[INBODY]-BP320_BSM-370"  # ชื่อ Device
    print(rpi_token_number)
    print("is sending to server.... ")
        
    data_format = ("Id card = {0}- Firstname = {1} - Lastname = {2} - DateofBrith = {3} - Gender = {4} - Age = {5} - Data-sys = {6} - Data-Dia = {7} - Data-Pr = {8} ".format(cid,firstname,lastname,dateOfbrith,gender,age,data_sys,data_dia,data_pr))
    print("Data format = {0}".format(data_format))
    if cid != "" and firstname_en != "" and lastname != "" and gender != "" and age != "" and dateOfbrith != "" and str(data_sys) != "" and str(data_dia) != "" and str(data_pr) !="" :
        print("ถ้าไม่เท่ากับค่าว่าง ")

        while(True):
            
                #-----check Smartcard insert...-----
                readerList = readers()
                print(readerList)
                print ("Available readers:")
                for readerIndex,readerItem in enumerate(readerList):
                    print(readerIndex, readerItem)

                readerSelectIndex = 0
                reader = readerList[readerSelectIndex]
                print ("Using:", reader)
                
                connection = reader.createConnection()
                print(connection)
                
                #When insert card
                try :
                    
                    connection.connect()                                 
                    import json
                    import requests
                    import urllib3
                    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)                    
                    try:                 
                        api_url = 'https://61.19.201.20:3343/meditop.php'
                        data = {"data":{"id":cid,"firstname":firstname,"lastname":lastname,"brithday":dateOfbrith,"gender":gender,"age":age,"sys":data_sys,"dia":data_dia,"pr":data_pr}}
                        header  = {'Content-type': 'application/x-www-form-urlencoded'}                       
                        r= requests.post(api_url,data=data, headers=header,verify=False)                 
                        if r.status_code != 200:
                            print('Falied  ')
                            print('Response', r.content)                          
                            print(r.status_code, r.reason, r.text)
                        else:
                            
                            print(r.status_code, r.reason)#print(" status 200 ok")
                    except Exception as e:
                     
                        print('Falied to send DATA')
                        print(e)        

                except:
                 
                    print("Please Insert To Smartcard....")
                    #MainDefault(root)                     
                    root.after(3000,SmartcartdataReader)   # 3 Secord to read bp 320
                    root.mainloop()
                               
    return

#-------------client to servert is pc--------------------
def SendToserver():
    
    global cid
    global firstname_en
    global lastname_en

    global firstname        #th
    global lastname         #th

    global gender
    global age
    global dateOfbrith
    global data_sys
    global data_dia
    global data_pr
    global  data_width
    global  data_height
    global  data_bmi 

    deviceomron = 'Device-Omron9020'     #   ชื่อ Device
    
    print("firstname ={0}, lastname = {1}".format(firstname,lastname))

    while(True):
      
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ipaddress = ''
        ipaddress = ReadIPserver()          #get ip from file ini
        host = ipaddress
        port = 12345                      

        try:
             
                s.connect((host, port))             
                print(s.recv(4096))         # message from server  

        except socket.error as ex_msg:
             
            print(ex_msg)

            while(True):

                time.sleep(3)

                for r in readers():
                            
                    try:

                        connection = r.createConnection()       
                        connection.connect()
                        
                    #except NoCardException :
                    except :

                        print(r, 'no card inserted in function inbody 370')
                        MainDefault(root)                     
                        root.after(1000,SmartcartdataReader)   # 1 Secord to read bp 320
                        root.mainloop()     

        now = datetime.now()
        dt = now.strftime("%Y%m%d%H%M%S") 

        MSH = "MSH|^~\&|"+ deviceomron +"|MEDITOP|HIS|BMS-HOSxP|"+dt+"||ORU^R01|5|P|2.3"
        PID = "PID|1|||"+ cid +" "; 
        PV1 = "PV1||O|||||||||||||||||"
        OBR = "OBR|1|||||"+dt+"||||||||"+dt+""
        OBX1 = "OBX|1|ST|WEIGHT||80.6|KG.|||||F|||"+dt+"|56CE01090"
        OBX2 = "OBX|2|ST|HEIGHT||181.3|CM.|||||F|||"+dt+"|56CE01090 "
        OBX3 = "OBX|3|ST|BMI||21.2| Kg/m2|||||F|||"+dt+"|56CE01090"
        OBX4 = "OBX|4|ST|SYSTOLIC||"+data_sys+"|mmHg|||||F|||"+dt+"|BP-9020"
        OBX5 = "OBX|5|ST|DIASTOLIC||"+data_dia+"|mmHg|||||F|||"+dt+"|BP-9020"
        OBX6 = "OBX|6|ST|PR||"+data_pr+"|RM|||||F|||"+dt+"||BP-9020"

        dataformatHL7 = cid +"\n" +  MSH +"\n"+ PID +"\n"+ PV1 +"\n"+ OBR +"\n"+ OBX1 +"\n"+ OBX2 +"\n"+ OBX3 +"\n"+ OBX4 +"\n"+ OBX5 +"\n"+ OBX6
        print(dataformatHL7)
     
        #**********For send to server format textfile***************
        #msg_data = "|{0}|{1}|{2}|{3}|{4}|{5}|{6}|{7}|{8}|{9}|{10}|{11}|{12}|{13}".format(deviceomron,cid,dt,firstname_en,lastname_en,dateOfbrith,gender,age,data_sys,data_dia,data_pr,data_width,data_height,data_bmi)
        #print(msg_data)
        #byte_encode = msg_data.encode('utf-8')

        byte_encode = dataformatHL7.encode('utf-8')   
        print("Sending To Server From Device 1 : ", dataformatHL7)

        s.send(byte_encode)             # message to server       
        s.close()
        time.sleep(0.5)

        while(True):

            time.sleep(2)

            for r in readers():
                        
                try:

                    connection = r.createConnection()       
                    connection.connect()
                    # print(r,toHexString(connection.getATR()))

                #except NoCardException :
                except :                  
                    
                    print(r, 'no card inserted in function inbody 370')
                    MainDefault(root)                     
                    root.after(1000,SmartcartdataReader)   # 1 Secord to read bp 320
                    root.mainloop()    

       # return

#------Insert image Bsm 370--------------------
def Imgbsm370():
    print("-------show iamge inbody 370--------------")
    width=root.winfo_screenwidth()
    height=root.winfo_screenheight() 
    load = PilImage.open("/home/odroid/SmartOpd/img/bsm370.jpg")
    load = load.resize((width,height))
    render = ImageTk.PhotoImage(load)
    img = Label(image=render)
    img.image = render  
    img.place(x=0, y= 0)
    print("-----------loading for read data for device Inbody 370----")
    root.after(3000,Getdatainbodybsm370)  # use 4 secord to read measument read scalar inbdoy370    

    root.mainloop()  
      
#-------------------convert data to int...----------------------------
def ConvertToInt(data):

    d = 0
    if(len(data) == 3):

        d = int(data) /10

        return d

    if(len(data) == 4):
    

        d = int(data) / 10

        return d

# ---------------------Read Buffer------------------------------------------
def Savebuffer(buffer):
    bytebuffer = []
    for b in buffer:     
        bytebuffer.append(b)      
    return bytebuffer

def SmartcartdataReader():

    #global varible          
    global cid                
    global firstname_en      
    global lastname_en          

    global firstname        #th
    global lastname         #th 

    global gender        
    global age
    global dateOfbrith
    
   # global data_width      
    #global data_height
    #global data_bmi
       
    global data_sys        
    global data_dia
    global data_pr
    print("-------loading for read data smartcard reader --------")
    print("-------cid   =" + cid)
    print("--------firstname  = " + firstname_en)
    print("---------lastname = "  + lastname_en)
    print("----------gender = " + gender)
    print("----------age  = " + age)
    print("----------dateOfbrith  ==" + dateOfbrith)
    
   # print(data_width)
   #  print(data_height)
   #  print(data_bmi)
     
    print("----------data sys = " + data_sys)
    print("-----------data dia  = " + data_dia)
    print("----------- data pr" + data_pr)
    
    if cid != "":

        print("------------if data in smartcard != null   on function smartcard reader---------")
        data_width = ""
        data_height = ""
        data_bmi =""      
        data_sys = ""
        data_dia =""
        data_pr =""
        cid  =  ""          
        firstname_en  =""    
        lastname_en =""
        gender     = ""   
        age  = ""
        dateOfbrith = "" 
        
    #----Func  Caculate age-------
    from datetime import date 
    def calculateAge(birthDate): 
        days_in_year = 365.2425 
        age = int((date.today() - birthDate).days / days_in_year) 

        return age 
    
    #----func unicode thaifullname ----
    def thaifullname(data):
        th  = ''
        print(data)
        values = bytearray(data)  # bytearray
        th =  values.decode("tis-620")
        print(thaifullname)
        
        return th
        
    # ---tis-620 to utf-8----
    def thai2unicode(data):
        result = ''
        
        if isinstance(data, list):
            for d in data:
                if (sys.version_info.major < 3):
                    result += chr(d)                                    
                    print(result)                                                    
                else :
                    result += chr(d)
                    print(result)
                           
        else :
            
            result = data.decode('utf-8')         
            print(result)
                
        return result.strip()
      
    #--------get data------
    def getData(cmd, req = [0x00, 0xc0, 0x00, 0x00]):
        
        data, sw1, sw2 = connection.transmit(cmd)
        data, sw1, sw2 = connection.transmit(req + [cmd[-1]])
        
        return [data, sw1, sw2]

    while True:
        
        time.sleep(2)
        print("----------loadin while for read smartcard-----------")
        #Check card
        SELECT = [0x00, 0xA4, 0x04, 0x00, 0x08]
        print("-------Check card select = {0}".format(SELECT))
        THAI_CARD = [0xA0, 0x00, 0x00, 0x00, 0x54, 0x48, 0x00, 0x01]     
        print("-------Check card Thai = {0}".format(THAI_CARD))
        # Id card
        CMD_CID = [0x80, 0xb0, 0x00, 0x04, 0x02, 0x00, 0x0d]
        print("------check  Id card = {0}".format(CMD_CID))
        # TH Fullname
        CMD_THFULLNAME = [0x80, 0xb0, 0x00, 0x11, 0x02, 0x00, 0x64]
        print("----------cmd th full name = {0}".format(CMD_THFULLNAME))
        # EN Fullname
        CMD_ENFULLNAME = [0x80, 0xb0, 0x00, 0x75, 0x02, 0x00, 0x64]
        print("-----------cmd en fullname = {0}".format(CMD_ENFULLNAME))
        # Date of Brith
        CMD_BIRTH = [0x80, 0xb0, 0x00, 0xD9, 0x02, 0x00, 0x08]
        print("------------cmd date fo brith = {0}".format(CMD_BIRTH))
        # Gender
        CMD_GENDER = [0x80, 0xb0, 0x00, 0xE1, 0x02, 0x00, 0x01]
        print("------------cmd gender = {0}".format(CMD_GENDER))
        
        for r in readers():                 
      
            try:

                connection = r.createConnection()       
                connection.connect()
                # print(r,toHexString(connection.getATR()))
                
                print('-------------smart card connect suecess......  ')

                atr = connection.getATR()
                print("----------data atr-----")
                print(atr)
                print ("-----------ATR: {0}".format(toHexString(atr)))
                if (atr[0] == 0x3B & atr[1] == 0x67):
                    req = [0x00, 0xc0, 0x00, 0x01]
                    print(req)
                else :
                    req = [0x00, 0xc0, 0x00, 0x00]
                    print(req)

                # Check card
                data, sw1, sw2 = connection.transmit(SELECT + THAI_CARD)
                print ("---------Select Applet: %02X %02X" % (sw1, sw2))

                # -----Get ID CARD----
                data = getData(CMD_CID, req)        #get data
                cid = thai2unicode(data[0])         # thaiUnicode

                print("--------data check card  = ")
                print(data)
                print ("---------CID-----------: " + cid)

                # -------Get TH Fullname-------นาย#เกรียงไกร#   
                data = getData(CMD_THFULLNAME, req)
                th_fullname = thaifullname(data[0])
                print(th_fullname)

                prefix = th_fullname.split('#')[0]          # Mr, Ms, Mrs.
                firstname = th_fullname.split('#')[1]       #Firstname
                lastname_strip = th_fullname.split('##')[1]       #Lastname
                lastname = lastname_strip.strip()    

                print("-----------prefix----" + prefix)
                print("-----------firstname  = " + firstname)
                print("-----------lastname   =" + lastname)
                print(len(lastname))
                #------Get  EN Fullname------
                data = getData(CMD_ENFULLNAME, req)
                en_fullname = thai2unicode(data[0])
                print ("-------------EN Fullname : {0}".format(en_fullname))
                    
                prefix_en = en_fullname.split('.')[0]          # Mr, Ms, Mrs.
                firstname_en = en_fullname.split('#')[1]       #Firstname
                lastname_en = en_fullname.split('##')[1]       #Lastname
                print("----------prefix english  = "  + prefix_en)
                print("----------firstname english ="  + firstname_en)
                print("----------lastname = " + lastname_en)
            
                #----Get Date of brith-----
                data = getData(CMD_BIRTH, req)
                data_dateOfdate = thai2unicode(data[0])     
                print("----------dateOfbrith   =="  + data_dateOfdate)
                    
                day = data_dateOfdate[6:8]            # Ex = 15
                month = data_dateOfdate[4:6]             # Ex = 02  
                date_year = data_dateOfdate[0:4]      # Ex = 2563
                print("--------day   == " + day)
                print("--------month    ="   + month)
                print("--------year   ="   + date_year)
                    
                #---Get format  dateOfbrith -----
                dateOfbrith = '{0}-{1}-{2}'.format(day,month,date_year)
                print("----------date Of brith set format  ==" + dateOfbrith)
                    
                #------Get calculate AGE-----
                age_year_convertInt = int(date_year)
                age_day = int(day)    # 15
                age_month = int(month)        # 02
                age_year = age_year_convertInt -543   #  1989
                    
                age_calculateYaer = calculateAge(date(age_year,age_month,age_day))
                age = str(age_calculateYaer)
                print("------------age current  ={0}".format(age))
                    
                #-----Get Gender-----
                #-----For detail (1 = mele, 2= female)
                data = getData(CMD_GENDER, req)
                data_gender = thai2unicode(data[0])
                print ("-----------Gender: {0}".format(data_gender))

                gender =  ""
                if data_gender  == '1':
                    
                    gender = "Male"
                else:
                    
                    gender = "Female"

                print("-----------set format gender =="   + gender)
                        
                if cid != "":
      
                    print("--------------IF cid != null in function Smartcarddatareader----")        
                    print("--------------cid  = " + cid)
                    print("--------------firstname = " + firstname_en)
                    print("--------------lastname  " +lastname_en)
                    print("---------------gender  = " + gender)
                    print("---------------age = " + age)
                    print("---------------dateOfbroth  = "  + dateOfbrith)
                    print("---------------data sys =  " + data_sys)
                    print("---------------data dia   ="  + data_dia)              
                    print("---------------data pr   = " + data_pr)
    
                    Getsmartcard(root)  
                    print("----------------show iamge Omron 9020...") 

                    root.after(1000,GetdataOmron9020)   

                    root.mainloop()  
                          
            #except NoCardException :
            except:
                
                print('--------no card inserted on function smartcardreader-----')
                MainDefault(root)                     
                root.after(1000,SmartcartdataReader)   # 1 Secord to read bp 320
                root.mainloop()

#handle_data 
def handle_data(data):
    print(data)

#-----------------------------------Read data for inbody 370--------------------------------
def Getdatainbodybsm370():
    
    global serialportInbody370 
    global cid
    global firstname_en
    global lastname_en
    global firstname        #th
    global lastname         #th
    global gender
    global age
    global dateOfbrith
    global data_width 
    global data_height
    global data_bmi
    
    global data_sys
    global data_dia
    global data_pr

    print("firstname ={0}, lastname = {1}".format(firstname,lastname))
    print("---------data sys  =="  + data_sys)
    print("---------data dia ==" + data_dia)
    print("----------data pr  =="  + data_pr)
    #print("---Read data for inbody 370...---")
    print("---CID = {0} ,firstname = {1}, lastname = {2}, gender = {3}, age = {4}, dateOfbrith = {5}".format(cid,firstname_en,lastname_en,gender,age,dateOfbrith))
   # print("---width = {0}, height = {1},bmi = {2}, sys = {3},dia = {4},pr = {5}".format(data_width,data_height,data_bmi,data_sys,data_dia,data_pr))
    print("-------Check Insert smart card in function GetdatInbody370----")

    for r in readers():
                              
        try:

            connection = r.createConnection()
            connection.connect()

            print(r, toHexString(connection.getATR()))

            print("------when Insert card for read data from inbody bsm 370--------")     
        
            print("idcard="+cid + "- firstname = "+firstname_en+" - lastname = "+lastname_en+"- gender = "+gender+"- age ="+age+"- sys = "+str(data_sys)+" -dia = "+str(data_dia)+"- pr ="+str(data_pr)+"- widht = "+str(data_width)+"- height = "+str(data_height)+"- bmi ="+str(data_bmi))
            
            ser1 = ConnectSerialPortInbody370(serialportInbody370)   # connect USB to Serialport On InbodyScala 370
        
            print("---------conenect serial port inbody 370")
           
            if ser1.isOpen():
                
                print("-----------Is Open SerialPort Inbody BSM 370  = {0}---".format(ser1.name))
                     
            while True:
                
                time.sleep(3)   
                #byteesToRead   =  b'\x02h\x19\nZK1806\x1b744\x1b227\x1b\x14\x03'         # data virtual           

                byteesToRead = ser1.read(ser1.inWaiting()) 
                print("------loadding read data for inbody 370")        
                print(list(byteesToRead)) 
                print(str(byteesToRead))
              #  print("--------byte to read = {0}".format(byteesToRead))          
           
                #*****Read data when data > 0   **********
                if len(byteesToRead) > 0:
                    print("---------if data > 0   inbody 370---------")
                    print("----read data suecess = {0}".format(byteesToRead))
                                 
                    buff = []                                      
                
                    buff = Savebuffer(byteesToRead)             
                    
                    print("-------Read buffer = {0}".format(buff))

                    print("-------------------------------------------------------")
                    # data height
                    h  = chr(buff[6]) + chr(buff[7]) + chr(buff[8]) + chr(buff[9])  # height
                    data_height  = ConvertToInt(h)
                    print(h)
                    print(data_height)

                    # data width
                    w  = chr(buff[11]) + chr(buff[12]) + chr(buff[13])  # width
                    #w  = "1015"
                    data_width = ConvertToInt(w)
                    print(w)
                    print(data_width)

                    # data bmi
                    bmi = chr(buff[15]) + chr(buff[16]) + chr(buff[17])   # bmi                 
                    data_bmi = ConvertToInt(bmi)
                    print(bmi)
                    print(data_bmi)
                    #data_bmi = bmi
                    print("width :(" + str(data_width) + ") height :(" + str(data_height)+") bmi :("+str(data_bmi)+")")

                    # If read data widht height bmi suecess....
                    if data_width != "" and data_height != "" and data_bmi != "":

                        print("--------if data with and height and bmi != null   ")
                        print("--------Read data inbody bsm370 secess---")
                        print("---------smart card insert -----")               
                        #backgroud     
                        Bg()
                        #show main default                  
                        MainSDP(root,cid,firstname_en,lastname_en,gender,age,dateOfbrith,data_sys,data_dia,data_pr, str(data_width), str(data_height), str(data_bmi))                            
                        #sent to server
                        root.after(1000,SendToserver)
                        root.mainloop()

                #for data == 0 
                
                else :                   
                
                    for r in readers():

                                                                                                   
                        try :
                            connection = r.createConnection()
                            connection.connect()
                            print(r, toHexString(connection.getATR()))
                                
                            #Getsmartcard(root)
                            root.after(1000,Getdatainbodybsm370)    

                            root.mainloop() 
                                
                        except :
                                
                            print(r, '---------when pull card exit on function omron 9020----')
                            MainDefault(root)                     
                            root.after(1000,SmartcartdataReader)   # 1 Secord to read bp 320
                            root.mainloop()
                           
        #except NoCardException :
        except :   
            print(r, 'no card inserted in function inbody 370')
            MainDefault(root)                     
            root.after(1000,SmartcartdataReader)   # 1 Secord to read bp 320
            root.mainloop() 

#-------------------------------- DATA SYS DIA PR-----------------------------------------
def MainSDP(root,cid,firstname_en,lastname_en,gender,age,dateOfbrith,sys,dia,pr,width,height,bmi):

    print("---main sdp -----------")
    print(width)
    print(height)
    print(bmi)
    #BP Secess...
    status1 = StringVar()
    status1.set("Finished Measurement")

    #Scala Secess..
    status2 = StringVar()
    status2.set("Finished Measurement")
       
    #time now
    now = datetime.today().strftime("%H:%M:%S")
    timenow = StringVar(root,value=now)
        # date now
    datenow_format = datetime.today().strftime("%d/%m/%Y")
    datenow = StringVar(root,value=datenow_format)

    # set insert data for cid, firstname, lastname, gender, age
    p_idcard = StringVar()
    p_idcard.set(cid)
    p_firstname = StringVar()
    p_firstname.set(firstname_en)
    p_lastname = StringVar()
    p_lastname.set(lastname_en)
    p_gender = StringVar()
    p_gender.set(gender)
    p_age = StringVar()
    p_age.set(age)
    p_dateofbrith = StringVar()
    p_dateofbrith.set(dateOfbrith)

    #sys dia pr
    data_sys = StringVar()
    data_sys.set(sys)
    data_dia = StringVar()
    data_dia.set(dia)
    data_pr = StringVar()
    data_pr.set(pr)
    #width height bmi
    d_width = StringVar()
    d_width.set(width)
    d_height = StringVar()
    d_height.set(height)
    d_bmi = StringVar()
    d_bmi.set(bmi)

    print("idcard="+cid + "- firstname = "+firstname_en+" - lastname = "+lastname_en+"- "+dateOfbrith+"- gender = "+gender+"- age ="+age+"- sys = "+str(sys)+" -dia = "+str(dia)+"- pr ="+str(pr))

    #*********************show data all*******************
    lbl_header = Label(root,text="SMART OPD", font=('Arial Bold', 36,'bold'),bg='#0071fe')
            
    lbl_IDCARD = Label(root, text="ID CARD :", font=('Arial Bold', 24,'bold'),bg='#0071fe')
    lbl_BrithOfDate = Label(root, text="BRITH OF DATE :", font=('Arial Bold', 24,'bold'), bg='#0071fe') 
    lbl_Firstname = Label(root, text="NAME : ", font=('Arial Bold', 24,'bold'), bg='#0071fe')
    lbl_Lastname = Label(root, text="SURNAME :  ", font=('Arial  Bold', 24,'bold'), bg='#0071fe')
    lbl_Gender = Label(root, text="GENDER :", font=('Arial Bold', 24,'bold'), bg='#0071fe')
    lbl_Age = Label(root, text="AGE :", font=('Arial Bold', 24,'bold'), bg='#0071fe')
    lbl_SYS = Label(root, text="SYS :", font=('Arial Bold', 24,'bold'), bg='#0071fe')      
    lbl_DIA = Label(root, text="DIA :", font=('Arial Bold', 24,'bold'), bg='#0071fe')    
    lbl_PR = Label(root, text="PR  :", font=('Arial Bold', 24,'bold'), bg='#0071fe')               
    lbl_WEIGHT = Label(root, text="WIDTH : ", font=('Arial Bold', 24,'bold'), bg='#0071fe')         
    lbl_HEIGTH = Label(root, text="HEIGHT :", font=('Arial Bold', 24,'bold'), bg='#0071fe')             
    lbl_BMI = Label(root, text="BMI :", font=('Arial Bold', 24,'bold'), bg='#0071fe')          
            
    lbl_DATE = Label(root, text="DATE :", font=('Arial Bold', 24,'bold'), bg='#0071fe')                  
    lbl_TIME = Label(root, text="TIME :", font=('Arial Bold', 24,'bold'), bg='#0071fe')                 
    lbl_STATUS = Label(root, text="STATUS :", font=('Arial Bold', 24,'bold'), bg='#0071fe')                   

    lbl_header.grid(row=1, column=0, sticky=W,  padx=20,pady=30)

    lbl_IDCARD.grid(row=3, column=0, sticky=W, padx=20, pady=10)
    lbl_Firstname.grid(row=4, column=0, sticky=W, padx=20, pady=10)
    lbl_Lastname.grid(row=5, column=0, sticky=W, padx=20, pady=10)
    lbl_BrithOfDate.grid(row=6, column=0, sticky=W, padx=20, pady=10)
    lbl_Gender.grid(row=7, column=0, sticky=W, padx=20, pady=10)
    lbl_Age.grid(row=8, column=0, sticky=W, padx=20, pady=10)
            
    lbl_DATE.grid(row=9, column=0, sticky=W, padx=20, pady=10)
           
    lbl_SYS.grid(row=3, column=2, sticky=W, padx=20, pady=10)
    lbl_DIA.grid(row=4, column=2, sticky=W, padx=20, pady=10)
    lbl_PR.grid(row=5, column=2, sticky=W, padx=20, pady=10)
    lbl_WEIGHT.grid(row=6, column=2, sticky=W, padx=20, pady=10)
    lbl_HEIGTH.grid(row=7, column=2, sticky=W, padx=20, pady=10)
    lbl_BMI.grid(row=8, column=2, sticky=W, padx=20, pady=10)
            
    lbl_TIME.grid(row=9, column=2, sticky=W, padx=20, pady=10)
            
    lbl_STATUS.grid(row=10, column=0, sticky=W, padx=20, pady=10)
    # ----------------create textbox-------------------------------------
    txt_IDCARD = Entry(root,textvar=p_idcard,width=13, font=("Arial Bold", 26)) 
    txt_BrithOfDate = Entry(root,textvar=p_dateofbrith,width=13, font=("Arial Bold", 26))  
    txt_FIRSTNAME = Entry(root,textvar=p_firstname,width=13, font=("Arial Bold", 26))
    txt_LASTNAME = Entry(root,textvar=p_lastname,width=13, font=("Arial Bold", 26))
    txt_GENDER = Entry(root,textvar=p_gender,width=13, font=("Arial Bold", 26))
    txt_AGE = Entry(root,width=13,textvar=p_age, font=("Arial Bold", 26))
            
    txt_DATE = Entry(root,width=13,textvariable= datenow, font=("Arial Bold", 26))

    txt_SYS = Entry(root,textvar=data_sys,width=13, font=("Arial Bold", 26))
    txt_DIA = Entry(root,textvar=data_dia,width=13, font=("Arial Bold", 26))
    txt_PR = Entry(root,textvar=data_pr,width=13, font=("Arial Bold", 26))
    txt_WEIGHT = Entry(root,textvar=d_width,width=13, font=("Arial Bold", 26))
    txt_HEIGTH = Entry(root,textvar=d_height,width=13, font=("Arial Bold", 26))
    txt_BMI = Entry(root,textvar=d_bmi,width=13, font=("Arial Bold", 26))
            
    txt_TIME = Entry(root,textvariable= timenow,width=13,  font=("Arial Bold", 26))

    lbltxt_STATUS = Label(root,textvar=status1, font=('Arial Bold', 26), bg='green')      # Status

    txt_IDCARD.grid(row=3, column=1,sticky=W, padx=0, pady=10)
    txt_FIRSTNAME.grid(row=4, column=1,sticky=W, padx=0, pady=10)
    txt_LASTNAME.grid(row=5, column=1,sticky=W, padx=0, pady=10)
    txt_BrithOfDate.grid(row=6,column=1,sticky=W, padx=0, pady=10)
    txt_GENDER.grid(row=7, column=1,sticky=W, padx=0, pady=10)
    txt_AGE.grid(row=8, column=1,sticky=W, padx=0, pady=10)
            
    txt_DATE.grid(row=9, column=1,sticky=W, padx=0, pady=10)

    txt_SYS.grid(row=3, column=3,sticky=W, padx=0, pady=10)
    txt_DIA.grid(row=4, column=3,sticky=W, padx=0, pady=10)
    txt_PR.grid(row=5, column=3,sticky=W, padx=0, pady=10)
    txt_WEIGHT.grid(row=6, column=3,sticky=W, padx=0, pady=10)
    txt_HEIGTH.grid(row=7, column=3,sticky=W, padx=0, pady=10)
    txt_BMI.grid(row=8, column=3,sticky=W, padx=0, pady=10)
    txt_TIME.grid(row=9, column=3,sticky=W, padx=0, pady=10)
    lbltxt_STATUS.grid(row=10, column=1,sticky=W, padx=0, pady=10)

    print("End data form inbody 370 suecess...")

    #return
    #*********************End show data all**************

#-----------------------------Get form  Read data form comport -------------------------------
def GetdataOmron9020():
   
    global serialportOmron9020
    global cid           
    global firstname_en      
    global lastname_en  
    global firstname        #th
    global lastname         #th
    global gender        
    global age
    global dateOfbrith  
    # global data_width 
   #  global data_height
    # global data_bmi
    global data_sys
    global data_dia
    global data_pr

    print("firstname ={0}, lastname = {1}".format(firstname,lastname))
    print("firstname ={0}, lastname = {1}".format(firstname_en,lastname_en))
    print("--------Omron 9020 ==>  CID = {0} ,firstname = {1}, lastname = {2}, gender = {3}, age = {4}, dateOfbrith = {5}".format(cid,firstname_en,lastname_en,gender,age,dateOfbrith))
    print("--------sys = {0},dia = {1},pr = {2}".format(data_sys,data_dia,data_pr))
    print("--------Check Insert smart card in function GetdatOmron 9020----")

    for r in readers():
                                                         
        try :

            print("-------Read data smart card and read data bp9020--------")
            print("-------when insert smart card in function GetOmron9020-----------")          
            connection = r.createConnection()
            connection.connect()
            print(r, toHexString(connection.getATR()))

            print("--------------Smart card insert")
            print("----idcard="+cid + "- firstname = "+firstname_en+" - lastname = "+lastname_en+"-"+dateOfbrith+"- gender = "+gender+"- age ="+age+"- sys = "+str(data_sys)+" -dia = "+str(data_dia)+"- pr ="+str(data_pr))

            ser = ConnectSerialportOmron9020(serialportOmron9020)  #coneect USB To SerialPort  Inbody 320
            print("----------connect serrial port Omron 9020----------")            
            if ser.isOpen():
    
                print(" --------Is Open SerialPort Omron 9020  = {0}----".format(ser.name))
            
          # byteesToRead = ser.read(ser.inWaiting())       
          # print("Serial port 320" + str(byteesToRead))    
            
            while True :
                    time.sleep(6)
                    
                    #byteesToRead = b'\x02h\x19\nZK1806\x1b744\x1b227\x1b\x14\x03\x02h\x19\nZK1806\x1b744\x1b227\x1b\x14\x03\x19\nZK1806\x1b744\x1b227\x1b\x14\x03'
                    
                    byteesToRead = ser.read(ser.inWaiting()) 
                    print(byteesToRead)
                    print(str(byteesToRead))
                    
                    print(len(byteesToRead))
                                     
                    if len(byteesToRead) > 0:               
                        print ("----------data byte to read > 0 ------------")
                        buff = []
                    
                        buff = Savebuffer(byteesToRead)
                        #buff = [98, 112, 45, 49, 50, 51, 52, 53, 54, 55, 56, 57, 49, 50, 51, 52, 53, 54, 55, 56, 57, 49, 48, 45, 50, 48, 49, 57, 47, 48, 54, 47, 49, 48, 45, 49, 49, 42, 51, 56, 45, 49, 49, 53, 45, 48, 55, 51, 45, 49, 49, 52, 45, 32, 57, 48, 45, 32]
                        print(buff)
                        
                        if len(byteesToRead) > 58:
                                    
                            print("---------if byteetoRead > 58 ---------------------------------------------")
                            data_sys = chr(buff[41]) + chr(buff[42]) + chr(buff[43])  # SYS
                            data_dia = chr(buff[49]) + chr(buff[50]) + chr(buff[51])  # DIA
                            data_pr_strip = chr(buff[53]) + chr(buff[54]) + chr(buff[55])   # PR
                          
                            data_pr = data_pr_strip.strip()
                            print(len(data_sys))
                            print(len(data_dia))
                            print(len(data_pr))

                            print("sys" +data_sys+"sys")
                            print("dia" +data_dia+"dia")
                            print("pr" +data_pr+"pr")

                            print("----------data sys = {0} ,data dia = {1}, data pr = {2}------".format(data_sys,data_dia,data_pr))

                            #read bp suecess...
                            if data_sys != "" and data_dia != "" and data_pr != "" :

                                print("-----------if data sys and data dia and data pr != Null  ")
                                print("----------When Read data Suecess ...In function GetdataOmron9020")                            
                                #backgroud     
                                Bg()                   
                                MainSDP(root,cid,firstname_en,lastname_en,gender,age,dateOfbrith,data_sys,data_dia,data_pr, str(data_width), str(data_height), str(data_bmi))                            
                              
                                #sent to server
                                root.after(1000,SendToserver)
                                #ser.close()
                                root.mainloop()          
                            
                    else:
                        
                        print("--------------loop else if  data Omron9020 != 59 or data < 58---- ")

                        for r in readers():                            
                                                                                                   
                            try :
                                connection = r.createConnection()
                                connection.connect()
                                print(r, toHexString(connection.getATR()))
                                
                                #Getsmartcard(root)
                                root.after(1000,GetdataOmron9020)      
                                root.mainloop() 
                                
                            except :
                                
                                print(r, '---------when pull card exit on function omron 9020----')
                                MainDefault(root)                     
                                root.after(1000,SmartcartdataReader)   # 1 Secord to read bp 320
                                root.mainloop()
                        
        #except NoCardException  :
        except  :
            print(r, '---------------no card inserted  on read data omron 9020---------------')
            MainDefault(root)                     
            root.after(1000,SmartcartdataReader)   # 1 Secord to read bp 320
            root.mainloop()
                   
def Bg():
      
    print("--------show image background-------")
    print("-----show image insert smart card------")
    width=root.winfo_screenwidth()
    height=root.winfo_screenheight()
    load = PilImage.open("/home/odroid/SmartOpd/img/bp.jpg")
    load = load.resize((width,height))
    render = ImageTk.PhotoImage(load)
    img = Label(image=render)
    img.image = render  
    img.place(x=0, y= 0)

#--------------------Form Default wait recive data------------------------------------

def MainDefault(root):
    print("-----show image insert smart card------")
    width=root.winfo_screenwidth()
    height=root.winfo_screenheight()
    load = PilImage.open("/home/odroid/SmartOpd/img/insertsmartcard.jpg")
    load = load.resize((width,height))
    render = ImageTk.PhotoImage(load)
    img = Label(image=render)
    img.image = render  
    img.place(x=0, y= 0)

#show img Insertsmartcard
def ShowimageInsertSmartcard(root):
    print("-----show image insert smart card------")
    width=root.winfo_screenwidth()
    height=root.winfo_screenheight()
    load = PilImage.open("/home/odroid/SmartOpd/img/insertsmartcard.jpg")
    load = load.resize((width,height))
    render = ImageTk.PhotoImage(load)
    img = Label(image=render)
    img.image = render  
    img.place(x=0, y= 0)

def Getsmartcard(root):
         
    print("--------on functtion Image smartcardOpd---------")
    width=root.winfo_screenwidth()
    height=root.winfo_screenheight() 
    load = PilImage.open("/home/odroid/SmartOpd/img/bp320.jpg")
    load = load.resize((width,height))
    render = ImageTk.PhotoImage(load)
    img = Label(image=render)
    img.image = render  
    img.place(x=0, y= 0)

def MainSDP1():
    
    lbl_header = Label(root,text="SMART OPD", font=('Arial Bold', 36,'bold'),bg='#1E90FF')
            
    lbl_IDCARD = Label(root, text="ID CARD :", font=('Arial Bold', 24,'bold'),bg='#1E90FF')
    lbl_BrithOfDate = Label(root, text="BRITH OF DATE :", font=('Arial Bold', 24,'bold'), bg='#1E90FF') 
    lbl_Firstname = Label(root, text="NAME : ", font=('Arial Bold', 24,'bold'), bg='#1E90FF')
    lbl_Lastname = Label(root, text="SURNAME :  ", font=('Arial  Bold', 24,'bold'), bg='#1E90FF')
    lbl_Gender = Label(root, text="GENDER :", font=('Arial Bold', 24,'bold'), bg='#1E90FF')
    lbl_Age = Label(root, text="AGE :", font=('Arial Bold', 24,'bold'), bg='#1E90FF')
    lbl_SYS = Label(root, text="SYS :", font=('Arial Bold', 24,'bold'), bg='#1E90FF')      
    lbl_DIA = Label(root, text="DIA :", font=('Arial Bold', 24,'bold'), bg='#1E90FF')    
    lbl_PR = Label(root, text="PR  :", font=('Arial Bold', 24,'bold'), bg='#1E90FF')               
    lbl_WEIGHT = Label(root, text="WIDTH : ", font=('Arial Bold', 24,'bold'), bg='#1E90FF')         
    lbl_HEIGTH = Label(root, text="HEIGHT :", font=('Arial Bold', 24,'bold'), bg='#1E90FF')             
    lbl_BMI = Label(root, text="BMI :", font=('Arial Bold', 24,'bold'), bg='#1E90FF')          
            
    lbl_DATE = Label(root, text="DATE :", font=('Arial Bold', 24,'bold'), bg='#1E90FF')                  
    lbl_TIME = Label(root, text="TIME :", font=('Arial Bold', 24,'bold'), bg='#1E90FF')                 
    lbl_STATUS = Label(root, text="STATUS :", font=('Arial Bold', 24,'bold'), bg='#1E90FF')                   

    lbl_header.grid(row=1, column=0, sticky=W,  padx=20,pady=30)

    lbl_IDCARD.grid(row=3, column=0, sticky=W, padx=20, pady=10)
    lbl_Firstname.grid(row=4, column=0, sticky=W, padx=20, pady=10)
    lbl_Lastname.grid(row=5, column=0, sticky=W, padx=20, pady=10)
    lbl_BrithOfDate.grid(row=6, column=0, sticky=W, padx=20, pady=10)
    lbl_Gender.grid(row=7, column=0, sticky=W, padx=20, pady=10)
    lbl_Age.grid(row=8, column=0, sticky=W, padx=20, pady=10)
            
    lbl_DATE.grid(row=9, column=0, sticky=W, padx=20, pady=10)
           
    lbl_SYS.grid(row=3, column=2, sticky=W, padx=20, pady=10)
    lbl_DIA.grid(row=4, column=2, sticky=W, padx=20, pady=10)
    lbl_PR.grid(row=5, column=2, sticky=W, padx=20, pady=10)
    lbl_WEIGHT.grid(row=6, column=2, sticky=W, padx=20, pady=10)
    lbl_HEIGTH.grid(row=7, column=2, sticky=W, padx=20, pady=10)
    lbl_BMI.grid(row=8, column=2, sticky=W, padx=20, pady=10)
            
    lbl_TIME.grid(row=9, column=2, sticky=W, padx=20, pady=10)
            
    lbl_STATUS.grid(row=10, column=0, sticky=W, padx=20, pady=10)
    # ----------------create textbox-------------------------------------
    txt_IDCARD = Entry(root,width=13, font=("Arial Bold", 26)) 
    txt_BrithOfDate = Entry(root,width=13, font=("Arial Bold", 26))  
    txt_FIRSTNAME = Entry(root,width=13, font=("Arial Bold", 26))
    txt_LASTNAME = Entry(root,width=13, font=("Arial Bold", 26))
    txt_GENDER = Entry(root,width=13, font=("Arial Bold", 26))
    txt_AGE = Entry(root,width=13, font=("Arial Bold", 26))
            
    txt_DATE = Entry(root,width=13,  font=("Arial Bold", 26))

    txt_SYS = Entry(root,width=13, font=("Arial Bold", 26))
    txt_DIA = Entry(root,width=13, font=("Arial Bold", 26))
    txt_PR = Entry(root,width=13, font=("Arial Bold", 26))
    txt_WEIGHT = Entry(root,width=13, font=("Arial Bold", 26))
    txt_HEIGTH = Entry(root,width=13, font=("Arial Bold", 26))
    txt_BMI = Entry(root,width=13, font=("Arial Bold", 26))
            
    txt_TIME = Entry(root,width=13,  font=("Arial Bold", 26))

    lbltxt_STATUS = Label(root, font=('Arial Bold', 26), bg='green')      # Status
    #------------------------manage grid textbox----------------------------
    txt_IDCARD.grid(row=3, column=1,sticky=W, padx=0, pady=10)
    txt_FIRSTNAME.grid(row=4, column=1,sticky=W, padx=0, pady=10)
    txt_LASTNAME.grid(row=5, column=1,sticky=W, padx=0, pady=10)
    txt_BrithOfDate.grid(row=6,column=1,sticky=W, padx=0, pady=10)
    txt_GENDER.grid(row=7, column=1,sticky=W, padx=0, pady=10)
    txt_AGE.grid(row=8, column=1,sticky=W, padx=0, pady=10)
            
    txt_DATE.grid(row=9, column=1,sticky=W, padx=0, pady=10)

    txt_SYS.grid(row=3, column=3,sticky=W, padx=0, pady=10)
    txt_DIA.grid(row=4, column=3,sticky=W, padx=0, pady=10)
    txt_PR.grid(row=5, column=3,sticky=W, padx=0, pady=10)
    txt_WEIGHT.grid(row=6, column=3,sticky=W, padx=0, pady=10)
    txt_HEIGTH.grid(row=7, column=3,sticky=W, padx=0, pady=10)
    txt_BMI.grid(row=8, column=3,sticky=W, padx=0, pady=10)
    txt_TIME.grid(row=9, column=3,sticky=W, padx=0, pady=10)
    lbltxt_STATUS.grid(row=10, column=1,sticky=W, padx=0, pady=10)

    print("End data form inbody 370 suecess...")

    return

def ReadIPserver():
    #Readfile  =  ""
    Path_open = open("hostserver.ini",'r')
    Readfile = Path_open.read()
    Path_open.close()
    print(Readfile)
    print(type(Readfile))
    return Readfile
    
if __name__ == "__main__":

    root.title("SMART OPD")                   
    root.attributes("-fullscreen", True)
    root.config(bg="#1E90FF")
    MainDefault(root)                       # show image imsert smart card
    root.resizable(True, True)    
    root.after(1000, SmartcartdataReader)   # 1 secord go to Function ReadSmartCard
    root.mainloop()
