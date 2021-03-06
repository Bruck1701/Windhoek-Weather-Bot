import time
import serial
import sys
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
