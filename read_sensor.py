import time
import serial
import sys
import pandas as pd
from datetime import datetime
import ast



ser = serial.Serial('/dev/ttyACM0',9600, timeout = 5)

# listen for the input, exit if nothing received in timeout period
line=""

dataframe_columns=['Temp','Hum','Vis','IR']

#dfC = pd.DataFrame(columns=dataframe_columns,index=['date'])
count=0

while True:

    #bytesToRead = ser.inWaiting()
    #line=ser.read(bytesToRead)
    date_hour=datetime.now()
    line =ser.readline().decode("utf-8")
    if len(line)!=0:
        #df.append()
        if(line[0]=='{'):
            frame_dict=ast.literal_eval(line)
            frame_dict['date']=date_hour
            print(frame_dict)

            df=pd.DataFrame(frame_dict.items()).T
            df.columns=frame_dict.keys()
            df=df[1:] # remve first line
            df.index=df['date']
            df=df[dataframe_columns]

            if count==0:
                dfc=df.copy()
            else:
                dfc=dfc.append(df)


            #print(dfc)
            count+=1
