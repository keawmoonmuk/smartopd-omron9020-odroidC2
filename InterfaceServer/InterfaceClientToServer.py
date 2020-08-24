import sys
import datetime
import time
import socket
import logging
#from PIL import Image,ImageTk
from smartcard.System import readers
from smartcard.util import HexListToBinString, toHexString, toBytes
from smartcard.Exceptions import NoCardException

#-----------Send to api-----------------
def Client_Toserver():

    global cid
    global firstname
    global lastname
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
    if cid != "" and firstname != "" and lastname != "" and gender != "" and age != "" and dateOfbrith != "" and str(data_sys) != "" and str(data_dia) != "" and str(data_pr) !="" :
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
                    root.after(3000,SmartcartdataReader)   # 1 Secord to read bp 320
                    root.mainloop()
                               
    return


#---------------------client to servert is socket--------------------
def SendToserver():
    
    global cid
    global firstname
    global lastname
    global gender
    global age
    global dateOfbrith
    
    global data_sys
    global data_dia
    global data_pr

    global  data_width
    global  data_height
    global  data_bmi 

    rpi_token_number = '#smartopd-01'     #   ชื่อ Device
    
    while(True):
      
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '192.168.137.1'              #ip server
        port = 12345                        #port to connect
       
        try:
             
                s.connect((host, port))
                
                print(s.recv(4096))         # message from server  

        except socket.error as ex_msg:
               
                print(ex_msg)

        now = datetime.now()
       
        dt = now.strftime("%Y-%m-%d %H:%M:%S") 

        msg_data = "|{0}|{1}|{2}|{3}|{4}|{5}|{6}|{7}|{8}|{9}|{10}|{11}|{12}|".format(cid,dt,firstname,lastname,dateOfbrith,gender,age,data_sys,data_dia,data_pr,data_width,data_height,data_bmi)

        byte_encode = msg_data.encode('utf-8')
      
        print("Sending To Server From Device 1 : ", msg_data )

        s.send(byte_encode)             # message to server       
        s.close()
        time.sleep(0.5)

        return






   
