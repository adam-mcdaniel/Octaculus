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

print(f'ADC Voltage: {str(chan0.voltage)}V, {str(chan1.voltage)}V, {str(chan2.voltage)}V, {str(chan3.voltage)}V')
print(f'Raw ADC Values: {chan0.value} {chan1.value} {chan2.value} {chan3.value}')

print(mcp.reference_voltage)


outputFile = 'output_4.txt'


def writeEvent(l_Array):
    with open(outputFile, 'a') as f:
        joined_list = ",".join(str(item) for item in l_Array)
        print(joined_list , file = f)


try:
    while True:

        ts = time.time()
        LDR0 = chan0.value
        LDR1 = chan1.value
        LDR2 = chan2.value
        LDR3 = chan3.value
        writeEvent([ts, LDR0, LDR1, LDR2, LDR3])
        time.sleep(sleepInterval)

except KeyboardInterrupt:
    print('Ctrl-C - Exiting program')
finally:
    print('Program finished')

