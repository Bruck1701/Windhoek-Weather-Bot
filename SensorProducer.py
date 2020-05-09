import time
import serial
import sys
import pandas as pd
from datetime import datetime
import ast



class ArduinoSensor:
    def __init__(self):

        self.ser = serial.Serial('/dev/ttyACM0',9600, timeout = 5)
    # listen for the input, exit if nothing received in timeout period

    def ReadInput(self):


        line=""
        dataframe_columns=['Temp','Hum','Vis','IR']
        date_hour=datetime.now()

        while True:
            line =self.ser.readline().decode("utf-8")
            if len(line)!=0:
                if(line[0]=='{'):
                    #print(line)
                    frame_dict=ast.literal_eval(line)
                    frame_dict['date']=date_hour
                    #print(dict(frame_dict))
                    return(frame_dict)


#print(ArduinoSensor().ReadInput())

            # df=pd.DataFrame(frame_dict.items()).T
            # df.columns=frame_dict.keys()
            # df=df[1:] # remve first line
            # df.index=df['date']
            # df=df[dataframe_columns]
            #
            # if count==0:
            #     dfc=df.copy()
            # else:
            #     dfc=dfc.append(df)


            #count+=1
