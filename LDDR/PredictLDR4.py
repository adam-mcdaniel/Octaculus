###############################################################################
# Dan Scott - Nov 2022
#
# Reading MCP3008 ADC input
###############################################################################

###############################################################################
#The MCP3008 specs state: 
# 200 ksps max. sampling rate at VDD = 5V
# 75 ksps max. sampling rate at VDD = 2.7V
# therefore there may be over 100 ksps at ~3.3V
#
# ksps = Kilosample(s) per second (thousands of samples per second)
# https://cdn-shop.adafruit.com/datasheets/MCP3008.pdf
###############################################################################

import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import collections
import numpy as np
from LDR4_MODEL import LDR4_MODEL
import pandas as pd
from scipy import ndimage

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P0)
chan1 = AnalogIn(mcp, MCP.P1)
chan2 = AnalogIn(mcp, MCP.P2)
chan3 = AnalogIn(mcp, MCP.P3)

#this is a general sleep interval.  
sleepInterval = 0.005

print(f'ADC Voltage: {str(chan0.voltage)}V, {str(chan1.voltage)}V, {str(chan2.voltage)}V')
print(f'Raw ADC Values: {chan0.value} {chan1.value} {chan2.value}')

print(mcp.reference_voltage)

rf_model =LDR4_MODEL() 

outputFile = 'output.txt'


def writeEvent(l_Array):
    with open(outputFile, 'a') as f:
        joined_list = ",".join(str(item) for item in l_Array)
        print(joined_list , file = f)

bigDq = collections.deque(maxlen=20)  #for the prediction
smlDq = collections.deque(maxlen=18)  #for the 5 row moving average

LDR0 = 1
LDR1 = 1
LDR2 = 1
LDR3 = 1

def getDataFromLDR():
    global LDR0, LDR1, LDR2, LDR3
    LDR0 = chan0.value
    LDR1 = chan1.value
    LDR2 = chan2.value
    LDR3 = chan3.value
    channelArray=[LDR0, LDR1, LDR2, LDR3]
    return channelArray
    
directionClasses = { 0: 'up',
                     1: 'upright',
                     2: 'right',
                     3: 'downright',
                     4: 'down',
                     5: 'downleft',
                     6: 'left',
                     7: 'upleft'}    


def predictDirection(aa):
    dfObj = pd.DataFrame(aa) 
    Cw = ndimage.center_of_mass(dfObj[0].values)
    Cx = ndimage.center_of_mass(dfObj[1].values)
    Cy = ndimage.center_of_mass(dfObj[2].values)
    Cz = ndimage.center_of_mass(dfObj[3].values)


    pred_data = np.array(list([Cw[0], Cx[0], Cy[0], Cz[0]])).reshape(1, -1)
    d = rf_model.model_predict(pred_data)
    direction = directionClasses.get(d)
    return direction

flag_data_predictor=False
roll_past = 0
prev_average = None
try:
    while True:
        data = getDataFromLDR()
        smlDq.append(data)
        time.sleep(sleepInterval)
        new_average = np.average(smlDq, axis=0)
        if prev_average is None:
            prev_average = new_average
        percent_change = np.subtract(new_average, prev_average)/prev_average
        list_percent_change = list(percent_change)
        prev_average=new_average
        bigDq.append(list_percent_change)  #stack the percent change (this is the last item in the queue (append is on the right))
        
        if (any(np.array(list_percent_change)>=0.01)):
            flag_data_predictor = True
        
        if (flag_data_predictor):    
            if(roll_past >= 19):  #get the next 19 items before doing the prediction (19 + the first one from above)
                print(predictDirection(bigDq))
                roll_past = 0
                flag_data_predictor=False
            else:
                roll_past+=1
        else:
            continue
    
      



except KeyboardInterrupt:
    print('Ctrl-C - Exiting program')
finally:
    print('Program finished')

