import socket
import io
import os
import logging
from time import sleep
from datetime import datetime
import time
import mysql.connector
from mysql.connector import Error

# ---------------------Buffer------------------------------------------


def Savebuffer(buffer):
    bytebuffer = []
    for b in buffer:
        bytebuffer.append(b)
    return bytebuffer


def InsertToDb(cid, formathl7):

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    datetimeformat = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
    print(type(datetimeformat))
    print(datetimeformat)

    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='bms_scn',
                                             user='root',
                                             password='mdt1234')
        if connection.is_connected():
            print(connection)
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)

            insertinto = "insert into scn_result(scn_result_id,scn_identify_patient_type,scn_result_no,scn_result_msg_type,scn_result_data,scn_result_stamp_datetime,scn_result_receive_status,scn_result_receive_datetime) \
                values(get_serialnumber('scn_result_id'),'cid','"+cid+"','ORU^R01','"+formathl7+"','"+now+"','N','NULL')"
            print(insertinto)
            cursor = connection.cursor()
            cursor.execute(insertinto)
            connection.commit()
            connection.close()
            record = cursor.fetchone()
            print("Your connected to database: ", record)

    except Error as e:

        print("Error while connecting to MySQL", e)

    finally:

        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

        return


def Getdataserver():

    host_server = '192.168.109.76'     # ip server
    port_server = 8889                 # port
    address = (host_server, port_server)
    sizebuffer = 4096

    date_time = datetime.today().strftime("%d-%m-%Y")

    # Create Socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Create Socket...")
    print("Waiting Connectin from Client...")
    try:

        s.bind((address))    # connect suecess

    except socket.error as ex:

        print(ex)

    s.listen(5)

    while True:

        dataFile_Dir = os.getcwd() + 'DATASERVER'
        file_path_date = os.getcwd() + 'DATASERVER' + '\\' + date_time

        # Not Forder Gave Create Folder
        if not os.path.exists(dataFile_Dir):
            os.makedirs(dataFile_Dir)

        if not os.path.exists(file_path_date):
            os.makedirs(file_path_date)

        conn, addr = s.accept()  # Connect with Client
        print("Connect From :", addr)
        to_client = "Thank you at Connection..."
        tc = to_client.encode()
        conn.send(tc)                   # send data to client

        client_data = conn.recv(sizebuffer)
        print(client_data)

        buff = Savebuffer(client_data)
        print(buff)

        data_idcard = chr(buff[0]) + chr(buff[1]) + chr(buff[2]) + chr(buff[3]) + chr(buff[4]) + chr(buff[5]) + chr(
            buff[6]) + chr(buff[7]) + chr(buff[8]) + chr(buff[9]) + chr(buff[10]) + chr(buff[11]) + chr(buff[12])

        print(data_idcard)
        print(date_time)
        # 1234200112456-20-02-2020.txt
        data_save = data_idcard + "_" + str(date_time) + ".hl7"

        file = io.open(file_path_date + '\\' + data_save, "w+")
        #file = io.open(file_path_date + '\\' + data_save, "a+")

        if not client_data:

            break  # ไม่มี data

        data_fromCilent = client_data.decode('utf-8')

        print(data_fromCilent)
        formatspitdata = data_fromCilent[14:]

        # Coneect to mysql and insert database
        InsertToDb(data_idcard, formatspitdata)
        # print(spit_format)

        file.write(formatspitdata + '\n')

        file.close()

    conn.close()


if __name__ == "__main__":

    Getdataserver()
