import time 
import serial

ser = 0

def int_to_str(a):
    b = str(a)
    b = '\''+b+'\''
    return b


def wiat_one_connect(a):
    global ser
    a = str(a)
    p1 = "{'start':"+'['+a+']'+'}'+'\n'
    
    while 1:
        ser.write(p1.encode("gbk"))
        #print(p1)
        line = ser.readline()
        if line:
            a = int(line)
            #print(a)
            return a

def wiat_one_function1(a):
    global ser
    a = str(a)
   
    p1 = "{'start':"+'['+a+']'+'}'+'\n'
    
    while 1:
        ser.write(p1.encode("gbk"))
        #print(p1)
        line = ser.readline()
        if line:
            a = line[0:1]
            b = max(a)
            b = chr(b)
            return b

def com_init(a,b,c):
    
    global ser
    
    ser = serial.Serial(a,b,timeout = c,writeTimeout = 10)

    #ser = serial.Serial("COM10",115200,timeout=3)
    

def wiat_connect():
    global ser
    while 1:
        ser.write("{'start':['setup']}\n".encode("gbk"))
        #print(11)
        line = ser.readline()
        if line:
            break
        
def one_function(a):
    global ser
    a = str(a)
    
    p1 = "{'start':"+'['+a+']'+'}'+'\n'
    ser.write(p1.encode("gbk"))
    #ser.write("{'start':['pinmode',13,1]}\n".encode("gbk"))


def two_function(a,b):
    global ser
    a = str(a)
    b = str(b)
    p1 = "{'start':"+'['+a+','+b+']'+'}'+'\n'
    #print(p1)
    ser.write(p1.encode("gbk"))
    
def LCD_function(a,b):
    global ser
    a = str(a)
    #b = str(b)
    b = int_to_str(b)
    p1 = "{'start':"+'['+a+','+b+']'+'}'+'\n'
    #print(p1)
    ser.write(p1.encode("gbk"))
    


def wiat_two_function(a,b):
    global ser
    a = str(a)
    b = str(b)
    p1 = "{'start':"+'['+a+','+b+']'+'}'+'\n'
    
    while 1:
        ser.write(p1.encode("gbk"))
        line = ser.readline()
        if line:
            a = int(line)
            return a


def three_function(a,b,c):
    global ser
    a = str(a)
    b = str(b)
    c = str(c)
    p1 = "{'start':"+'['+a+','+b+','+c+']'+'}'+'\n'
    #print(p1)
    ser.write(p1.encode("gbk"))
    #ser.write("{'start':['pinmode',13,0]}\n".encode("gbk"))

def wiat_three_function(a,b,c):
    global ser
    a = str(a)
    b = str(b)
    c = str(c)
    p1 = "{'start':"+'['+a+','+b+','+c+']'+'}'+'\n'
    
    while 1:
        ser.write(p1.encode("gbk"))
        #print(p1)
        line = ser.readline()
        if line:
            a = int(line)
            return a

def wiat_three_function1(a,b,c):
    global ser
    a = str(a)
    b = str(b)
    c = str(c)
    p1 = "{'start':"+'['+a+','+b+','+c+']'+'}'+'\n'
    
    while 1:
        ser.write(p1.encode("gbk"))
        #print(p1)
        line = ser.readline()
        if line:
            a = line[0:1]
            b = max(a)
            b = chr(b)
            return b

def four_function(a,b,c,d):
    global ser
    a = str(a)
    b = str(b)
    c = str(c)
    d = str(d)
    p1 = "{'start':"+'['+a+','+b+','+c+','+d+']'+'}'+'\n'
    #print(p1)
    ser.write(p1.encode("gbk"))
    #ser.write("{'start':['pinmode',13,0]}\n".encode("gbk"))



def five_function(a,b,c,d,e):
    global ser
    a = str(a)
    b = str(b)
    c = str(c)
    d = str(d)
    e = str(e)
    p1 = "{'start':"+'['+a+','+b+','+c+','+d+','+e+']'+'}'+'\n'
    #print(len(p1))
    ser.write(p1.encode("gbk"))
    #ser.write("{'start':['pinmode',13,0]}\n".encode("gbk"))


def close_ser():
    global ser
    ser.close()
