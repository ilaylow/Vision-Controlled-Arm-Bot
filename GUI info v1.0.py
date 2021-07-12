#!/usr/bin/python
# -*- coding: UTF-8 -*-
# File name   : client.py
# Description : client  
# Website    : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date      : 2018/08/22

import sys
import os
import base64
import hashlib
import socket
import threading
import time
import Adeept
import struct



import threading as thread
import tkinter as tk
import math
import Adeept
thread_flag = 0
thread_flag1 =0


tcpClicSock = ''
stat = 0
ip_stu=1
stop_stu = 1
x_range = 1
conn = 0
addr = 0

fun_flag = 1
class Functions(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(Functions, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()
        self.__flag.clear()

        self.exec_do = ''
        

    def pause(self):
        global thread_flag
        thread_flag = 0
        self.__flag.clear()
        

    def resume(self):
        global thread_flag,fun_flag
        #thread_flag = 0
        #print("**********")
        self.__flag.set()
       

    def strinput(self, stri):
        self.pause()
        #print(stri)
        self.exec_do = stri
        self.resume()


    def run(self):
        while 1:
            global fun_flag
            self.__flag.wait()
            fun_flag = 1
            print("##########")
            #print(self.exec_do)
            exec(self.exec_do)
            #self.exec_do = ''
            self.__flag.clear()
            
            pass
            

threadX = Functions()
threadX.start()

def send_msg(conn, msg_bytes):
    token = b"\x81"
    length = len(msg_bytes)
    if length < 126:
        token += struct.pack("B", length)
    elif length <= 0xFFFF:
        token += struct.pack("!BH", 126, length)
    else:
        token += struct.pack("!BQ", 127, length)

    msg = token + msg_bytes
    conn.sendall(msg)
    return True          
class recv_thread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(recv_thread, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()
        self.__flag.clear()
    def pause(self):
        thread_flag1 = 0
        
        self.__flag.clear()
        
    def resume(self):
        global thread_flag1
        #thread_flag = 0
        thread_flag1 = 1;
        self.__flag.set()
        #print(thread_flag1);

    def run(self):
        global fun_flag
        while 1:
            self.__flag.wait()
           
            data = conn.recv(8096)
            headers = get_headers(data)

            # Encrypt the sec-websocket-key in the request header
            response_tpl = "HTTP/1.1 101 Switching Protocols\r\n" \
                       "Upgrade:websocket\r\n" \
                       "Connection: Upgrade\r\n" \
                       "Sec-WebSocket-Accept: %s\r\n" \
                       "WebSocket-Location: ws://%s%s\r\n\r\n"

            magic_string = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
            # Confirm the handshake Sec-WebSocket-Key fixed format: Sec-WebSocket-Key+'258EAFA5-E914-47DA-95CA-C5AB0DC85B11' in headers
            value = headers['Sec-WebSocket-Key'] + magic_string
            ac = base64.b64encode(hashlib.sha1(value.encode('utf-8')).digest())
            response_str = response_tpl % (ac.decode('utf-8'), headers['Host'], headers['url'])

            # Response [Handshake] message
            conn.send(bytes(response_str, encoding='utf-8'))

            # Can communicate--receive messages sent by the client
            while thread_flag1:
                
                data = conn.recv(8096)
                if len(data) < 9:
                    break
                data = get_data(data)
                
                send_msg(conn,b"data_success");   
                
                #s = str(data)
                #print(s)
                
                threadX.pause()
                
                #print(thread_flag)
               
                
                threadX.strinput(data)
                #time.sleep(0.5)
                threadX.resume()
                
                while 1:
                    threadX.resume()
                    time.sleep(0.1)
                    #print(fun_flag)
                    if fun_flag == 1:
                        fun_flag = 0
                        break;
            self.__flag.clear()
                
            pass


# instantiate PyMata with a 2 second start up delay to allow an Uno to complete its reset
#board = PyMata3(2)


threadT = recv_thread()
threadT.start()

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")

myname = socket.getfqdn(socket.gethostname())
myaddr = socket.gethostbyname(myname)
print(myaddr)
sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind host, default port 5000
sock.bind((myaddr, 5678))
sock.listen(5)
 
 
def get_headers(data):
    """
    Convert request header to dictionary
    :param data: Parse the data of the request header
    :return: Request header dictionary
    """
    header_dict = {}
    data = str(data, encoding="utf-8")
    """
    Request header format:
    b'
        GET / HTTP/1.1\r\n
        Host: 127.0.0.1:8080\r\n
        Connection: Upgrade\r\n
        Pragma: no-cache\r\n
        Cache-Control: no-cache\r\n
        Upgrade: websocket\r\n
        Origin: http://localhost:63342\r\n
        Sec-WebSocket-Version: 13\r\n
        User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36\r\n
        Accept-Encoding: gzip, deflate, br\r\n
        Accept-Language: zh-CN,zh;q=0.8\r\n
        Sec-WebSocket-Key: +uL/aiakjNABjEoMzAqm6Q==\r\n
        Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits\r\n\r\n'
    """
    header, body = data.split("\r\n\r\n", 1)  # Because the end of the request header information is \r\n, and the last part is \r\n\r\n;
                                              # So split by
    header_list = header.split("\r\n")
    for i in range(0, len(header_list)):
        if i == 0:
            if len(header_list[0].split(" ")) == 3:
                header_dict['method'], header_dict['url'], header_dict['protocol'] = header_list[0].split(" ")
        else:
            k, v = header_list[i].split(":", 1)
            header_dict[k] = v.strip()
    return header_dict
 
 
def get_data(info):
    """
    Decode the return message
    :param info: Original message
    :return: Chinese characters after decoding
    """
    payload_len = info[1] & 127
    if payload_len == 126:
        extend_payload_len = info[2:4]
        mask = info[4:8]
        decoded = info[8:]
    elif payload_len == 127:
        extend_payload_len = info[2:10]
        mask = info[10:14]
        decoded = info[14:]
    else:
        extend_payload_len = None
        mask = info[2:6]
        decoded = info[6:]
    bytes_list = bytearray()  # Use bytes to collect all the data, then go to string encoding, so that it will not cause Chinese garbled
    for i in range(len(decoded)):
        chunk = decoded[i] ^ mask[i % 4]  # Decoding method
        bytes_list.append(chunk)
    body = str(bytes_list, encoding='utf-8')
    return body


def connect_click():       #Call this function to connect with the server
    ip_adr=E1.get()    #Get the IP address from Entry                          #Thread starts
    print(ip_adr)
    Adeept.com_init(ip_adr,115200,1)
    Adeept.wiat_connect()
    while True:  
        # Waiting for user to connect
        global conn, addr 
        conn, addr = sock.accept()
        
        threadX.pause()

        threadT.pause()
        #time.sleep(0.5)
        
        threadT.resume()
        
        #print("conn from==>", conn, addr)
        # Get handshake message, magic string, sha1 encryption
        # Send to client
        # Handshake message
        
            
            #exec(data)

def loop():                   #GUI
    global color_can,color_line,target_color,color_oval,tcpClicSock,root,E1,connect,l_ip,l_ip_4,l_ip_5,color_btn,color_text,Btn14,CPU_TEP_lab,CPU_USE_lab,RAM_lab,canvas_ultra,color_text,var_R,var_B,var_G,Btn_Steady,Btn_FindColor,Btn_WatchDog,Btn_Fun4,Btn_Fun5,Btn_Fun6,Btn_Switch_1,Btn_Switch_2,Btn_Switch_3,Btn_Smooth,canvas_battery,Btn_RightSide   #The value of tcpClicSock changes in the function loop(),would also changes in global so the other functions could use it.
    while True:
        color_bg='#000000'      #Set background color
        color_text='#E1F5FE'      #Set text color
        color_btn='#0277BD'    #Set button color
        color_line='#01579B'      #Set line color
        color_can='#212121'    #Set canvas color
        color_oval='#2196F3'      #Set oval color
        target_color='#FF6D00'

        root = tk.Tk()          #Define a window named root
        root.title('Adeept Arduino Robot')    #Main window title
        root.geometry('380x100')  #Main window size, middle of the English letter x.
        root.config(bg=color_bg)  #Set the background color of root window

        E1 = tk.Entry(root,show=None,width=16,bg="#37474F",fg='#eceff1')
        E1.place(x=50,y=40)                             #Define a Entry and put it in position
        
        Btn14= tk.Button(root, width=8,height=2, text='Connect',fg=color_text,bg=color_btn,command=connect_click,relief='ridge')
        Btn14.place(x=200,y=15)                       #Define a Button and put it in position

       

        global stat
        if stat==0:           # Ensure the mainloop runs only once
            root.mainloop()  # Run the mainloop()
            stat=1         # Change the value to '1' so the mainloop() would not run again.


if __name__ == '__main__':
    try:
        loop()                 # Load GUI
    except:
        tcpClicSock.close()       # Close socket or it may not connect with the server again
        pass
