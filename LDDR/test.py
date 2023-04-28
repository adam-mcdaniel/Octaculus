from LDR3_MODEL import LDR3_MODEL
import collections
import numpy as np
import time
import csv
import pandas as pd
from scipy import ndimage

bigDq = collections.deque(maxlen=20)  #for the prediction
smlDq = collections.deque(maxlen=20)  #for the 5 row moving average
sleepInterval = .005
rf_model =LDR3_MODEL() 

directionClasses = { 0: 'up',
                     1: 'upright',
                     2: 'right',
                     3: 'downright',
                     4: 'down',
                     5: 'downleft',
                     6: 'left',
                     7: 'upleft'}    

cursor = 0
test=[]


def getCSVData(fname):
    List_data=[]
    with open(fname) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            List_data.append(row)
            line_count+=1  
    return List_data

#load test data
test = getCSVData('test_data.txt')



def getDataFromLDR():
    global cursor
    channelArray = np.array(test[cursor][1:4]).astype('int64')
    cursor+=1
    return channelArray

def predictDirection(aa):
    dfObj = pd.DataFrame(aa) 
    Cx = ndimage.center_of_mass(dfObj[0].values)
    Cy = ndimage.center_of_mass(dfObj[1].values)
    Cz = ndimage.center_of_mass(dfObj[2].values)
    pred_data = list([[Cx[0], Cy[0], Cz[0]]])
    d = rf_model.model_predict(pred_data)
    direction = directionClasses.get(d)
    return direction




roll_past = 0
prev_average = None
flag_data_predictor=False

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
    bigDq.append(list_percent_change)  #stack the percent change
    
    if (any(np.array(list_percent_change)>=0.01)):
        flag_data_predictor = True
    
    if (flag_data_predictor):    
        if(roll_past >= 20):
            print(predictDirection(bigDq))
            roll_past = 0
            flag_data_predictor=False
        else:
            # print(roll_past)
            roll_past+=1
    else:
        continue
    