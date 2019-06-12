from variables import *     #importing all variables from variables library 
import smbus  #import smbus library
import time#time module for delay
import numpy as np
import matplotlib.pyplot as plt
bus=smbus.SMBus(1) #creating an instance of object SMBus for opening i2c channel 1
def READ_STS(): #defining function to read status
    global status   #creating global variable to store status values
    status=bus.read_byte_data(AS726X_ADDR,AS72XX_SLAVE_STATUS_REG) #reading one byte of data from status register with headecimal device address and status register address
    print(bin(status))
    return status #return status to main programme
    
def READ(address):#defining function to read to a virtual register with adress 'address'
    global data
    while True:#opening infinite loop
        status=bus.read_byte_data(AS726X_ADDR,AS72XX_SLAVE_STATUS_REG)#reading status register
        if status&AS72XX_SLAVE_TX_VALID==0:#comparing status register value with binary 1 to know is TX valid bit is zero ie bit1
                    bus.write_byte_data(AS726X_ADDR,AS72XX_SLAVE_WRITE_REG,address)#writing address of virtual register to be read
                    while True:
                        status=bus.read_byte_data(AS726X_ADDR,AS72XX_SLAVE_STATUS_REG)#polling status register
                        if status&AS72XX_SLAVE_RX_VALID!=0:#checking if RX valid bit is 1 to ensure data is available in read register 
                            data=bus.read_byte_data(AS726X_ADDR,AS72XX_SLAVE_READ_REG)#reading data and storing to 'data'
                            return data
                            break    
def WRITE(address,data):#defining function to write 'data' toa virtual register with address'address'
    while True:
        status=bus.read_byte_data(AS726X_ADDR,AS72XX_SLAVE_STATUS_REG)# reading status register
        if status&AS72XX_SLAVE_TX_VALID==0:#checking if slave ready to receive data by polling rx_valid bit ie bit 1 of atatus register
                        bus.write_byte_data(AS726X_ADDR,AS72XX_SLAVE_WRITE_REG,(address|0x80))#writing virtual register address to write register settin MS Bit to 1 to indiacate pending write 
                        while True:#loop to poll status
                                status=bus.read_byte_data(AS726X_ADDR,AS72XX_SLAVE_STATUS_REG)#read status
                                if status&AS72XX_SLAVE_TX_VALID==0:#checking if slave is ready
                                    bus.write_byte_data(AS726X_ADDR,AS72XX_SLAVE_WRITE_REG,data)##writing data
                                    return
                                    break
         
def READ_HRD():#read hardware version and display hardware id
        READ(AS726x_HW_VERSION)#read harware version register with read function
        if data==0b111110:#checkin if it is AS7262 visible sensor
            print('AS7262 VISIBLE SENSOR')
        else:
            print('AS7263 IR SENSOR')
def RESET():#reset device
    global data#declaring global variable 'data' to store data from register for future use
    READ(AS726x_CONTROL_SETUP)#read controle setup register
    data&=0b01111111#clearing first bit correspondin to reset function
    WRITE(AS726x_CONTROL_SETUP,(data|0x80))#setting value 1 to bit for reset
def INT_ENB_DIS(a):#enable interupt
    global data
    READ(AS726x_CONTROL_SETUP)
    data &= 0b10111111
    WRITE(AS726x_CONTROL_SETUP,(data|(a<<6)))#shifting user value 6 places left to set 6th bit
def GAIN(a):#setting gain
    global data
    READ(AS726x_CONTROL_SETUP)
    data &= 0b11001111
    WRITE(AS726x_CONTROL_SETUP,(data|(a<<4)))
def BANK(a):#setting bank mode
    global data
    READ(AS726x_CONTROL_SETUP)
    data &= 0b11110011
    WRITE(AS726x_CONTROL_SETUP,(data|(a<<2)))
def DATA_RDY():#enabling or disabling data rdy bit
    global data
    READ(AS726x_CONTROL_SETUP)
    data = str(data)
    return int(data[1])
def TEMPR():#reading temprature
    global data
    READ(AS726x_DEVICE_TEMP)
    return data
    
def LEDS_ENB_DIS(a):#enable disable source led
    global data
    READ(AS726x_LED_CONTROL)
    data&=0b11110111
    WRITE(AS726x_LED_CONTROL,(data|a<<3))
    
def LEDI_ENB_DIS(a):#enable disable indicator led
    global data
    READ(AS726x_LED_CONTROL)
    data&=0b11111110
    WRITE(AS726x_LED_CONTROL,(data|a))
def LEDI_CURRENT(a):#setting led current for indicator led
    global data
    READ(AS726x_LED_CONTROL)
    data&=0b11111001
    WRITE(AS726x_LED_CONTROL,(data|a<<1))
def LEDS_CURRENT(a): # inbuild led maximum current rating not known so setting to minimum
    global data
    READ(AS726x_LED_CONTROL)
    data&=0b11001111
    WRITE(AS726x_LED_CONTROL,(data))
def DATA_V_UNCAL():#reading uncalibrated reading from channel v
    global data
    global d
    READ(AS7262_V_H)#getting 8 high data bits
    d=data<<8#shifting them to bit 16 to bit9 and storing to d
    READ(AS7262_V_L)#reading 8 low data bits
    d=d|data#storing them to s
    return d
def DATA_B_UNCAL():#reading uncalibrated reading from channel b
    global data
    global d
    READ(AS7262_B_H)
    d=data<<8
    READ(AS7262_B_L)
    d=d|data
    return d
def DATA_G_UNCAL():#reading uncalibrated reading from channel g
    global data
    global d
    READ(AS7262_G_H)
    d=data<<8
    READ(AS7262_G_L)
    d=d|data
    return d
def DATA_Y_UNCAL():#reading uncalibrated reading from channel y
    global data
    global d
    READ(AS7262_Y_H)
    d=data<<8
    READ(AS7262_Y_L)
    d=d|data
    return d
def DATA_O_UNCAL():#reading uncalibrated reading from channel o
    global data
    global d
    READ(AS7262_O_H)
    d=data<<8
    READ(AS7262_O_L)
    d=d|data
    return d
def DATA_R_UNCAL():#reading uncalibrated reading from channel r
    global data
    global d
    READ(AS7262_R_H)
    d=data<<8
    READ(AS7262_R_L)
    d=d|data
    return d
def UNCAL_DATA_READ():#reading uncalibrated reading from all channel and printing them
    DATA_V_UNCAL()
    print(d)
    DATA_B_UNCAL()
    print(d)
    DATA_G_UNCAL()
    print(d)
    DATA_Y_UNCAL()
    print(d)
    DATA_O_UNCAL()
    print(d)
    DATA_R_UNCAL()
def DATA_V_CALI():
    global data #declaring global variable for getting data varible from read function
    global value
    d=0 #for processing data from sensor
    data=0#data from sensor
    a=0#variable for intermediate processing
    while a<3:#loop to read data from 4 registers
        READ(AS7262_V_CAL+a)#read data from register
        d=d|(data<<((3-a)*8))#storing value to variable d after shifting left
        a+=1#incrementing address bit
    a=format(d,'032b')#converting output to 32 bit string
    s=int(a[0])#sign bit to varible for sign
    e=int(a[1:9],base=2)#exponent bits to variable for exponent
    v=[]#intermediate value list
    value=0#value variable
    for i in range(10,32):# loop for converting to float
        b=int(a[i],base=2)#converting eaach bit to integer and storing to to b
        v.append((b*(2**(-i+10))))#calculating value inside summation for ieee 754 standard
    value=((-1)**s)*(1+sum(v))*(2**(e-127))#substituting variables in equation 
    return value#returning caliberated value
def DATA_B_CALI():
    global data #declaring global variable for getting data varible from read function
    global value
    d=0 #for processing data from sensor
    data=0#data from sensor
    a=0#variable for intermediate processing
    while a<3:#loop to read data from 4 registers
        READ(AS7262_B_CAL+a)#read data from register
        d=d|(data<<((3-a)*8))#storing value to variable d after shifting left
        a+=1#incrementing address bit
    a=format(d,'032b')#converting output to 32 bit string
    s=int(a[0])#sign bit to varible for sign
    e=int(a[1:9],base=2)#exponent bits to variable for exponent
    v=[]#intermediate value list
    value=0#value variable
    for i in range(10,32):# loop for converting to float
        b=int(a[i],base=2)#converting eaach bit to integer and storing to to b
        v.append((b*(2**(-i+10))))#calculating value inside summation for ieee 754 standard
    value=((-1)**s)*(1+sum(v))*(2**(e-127))#substituting variables in equation 
    return value#returning caliberated value
def DATA_G_CALI():
    global data #declaring global variable for getting data varible from read function
    global value
    d=0 #for processing data from sensor
    data=0#data from sensor
    a=0#variable for intermediate processing
    while a<3:#loop to read data from 4 registers
        READ(AS7262_G_CAL+a)#read data from register
        d=d|(data<<((3-a)*8))#storing value to variable d after shifting left
        a+=1#incrementing address bit
    a=format(d,'032b')#converting output to 32 bit string
    s=int(a[0])#sign bit to varible for sign
    e=int(a[1:9],base=2)#exponent bits to variable for exponent
    v=[]#intermediate value list
    value=0#value variable
    for i in range(10,32):# loop for converting to float
        b=int(a[i],base=2)#converting eaach bit to integer and storing to to b
        v.append((b*(2**(-i+10))))#calculating value inside summation for ieee 754 standard
    value=((-1)**s)*(1+sum(v))*(2**(e-127))#substituting variables in equation 
    return value#returning caliberated value
def DATA_Y_CALI():
    global data #declaring global variable for getting data varible from read function
    global value
    d=0 #for processing data from sensor
    data=0#data from sensor
    a=0#variable for intermediate processing
    while a<3:#loop to read data from 4 registers
        READ(AS7262_Y_CAL+a)#read data from register
        d=d|(data<<((3-a)*8))#storing value to variable d after shifting left
        a+=1#incrementing address bit
    a=format(d,'032b')#converting output to 32 bit string
    s=int(a[0])#sign bit to varible for sign
    e=int(a[1:9],base=2)#exponent bits to variable for exponent
    v=[]#intermediate value list
    value=0#value variable
    for i in range(10,32):# loop for converting to float
        b=int(a[i],base=2)#converting eaach bit to integer and storing to to b
        v.append((b*(2**(-i+10))))#calculating value inside summation for ieee 754 standard
    value=((-1)**s)*(1+sum(v))*(2**(e-127))#substituting variables in equation 
    return value#returning caliberated value
def DATA_O_CALI():
    global data #declaring global variable for getting data varible from read function
    global value
    d=0 #for processing data from sensor
    data=0#data from sensor
    a=0#variable for intermediate processing
    while a<3:#loop to read data from 4 registers
        READ(AS7262_O_CAL+a)#read data from register
        d=d|(data<<((3-a)*8))#storing value to variable d after shifting left
        a+=1#incrementing address bit
    a=format(d,'032b')#converting output to 32 bit string
    s=int(a[0])#sign bit to varible for sign
    e=int(a[1:9],base=2)#exponent bits to variable for exponent
    v=[]#intermediate value list
    value=0#value variable
    for i in range(10,32):# loop for converting to float
        b=int(a[i],base=2)#converting eaach bit to integer and storing to to b
        v.append((b*(2**(-i+10))))#calculating value inside summation for ieee 754 standard
    value=((-1)**s)*(1+sum(v))*(2**(e-127))#substituting variables in equation 
    return value#returning caliberated value
def DATA_R_CALI():
    global data #declaring global variable for getting data varible from read function
    global value
    d=0 #for processing data from sensor
    data=0#data from sensor
    a=0#variable for intermediate processing
    while a<3:#loop to read data from 4 registers
        READ(AS7262_R_CAL+a)#read data from register
        d=d|(data<<((3-a)*8))#storing value to variable d after shifting left
        a+=1#incrementing address bit
    a=format(d,'032b')#converting output to 32 bit string
    s=int(a[0])#sign bit to varible for sign
    e=int(a[1:9],base=2)#exponent bits to variable for exponent
    v=[]#intermediate value list
    value=0#value variable
    for i in range(10,32):# loop for converting to float
        b=int(a[i],base=2)#converting eaach bit to integer and storing to to b
        v.append((b*(2**(-i+10))))#calculating value inside summation for ieee 754 standard
    value=((-1)**s)*(1+sum(v))*(2**(e-127))#substituting variables in equation 
    return value#returning caliberated value
def cal_data_read():
    DATA_V_CALI()
    print(value)
    DATA_B_CALI()
    print(value)
    DATA_G_CALI()
    print(value)
    DATA_Y_CALI()
    print(value)
    DATA_O_CALI()
    print(value)
    DATA_R_CALI()

#def DATA_R_cal_test():
#    global data
#    global d
#    d=0
#    READ(AS7262_V_CAL)
#    d=d|data<<24
#    READ(AS7262_V_CAL+1)
#    d=d|data<<16
#    READ(AS7262_V_CAL+2)
#    d=d|data<<8
#    READ(AS7262_V_CAL+2)
#    d=d|data    
#    return d  
        
    
    
    


    
    

    
    
      
        
    
        
        
    


    
