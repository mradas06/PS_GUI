import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import random
from PyQt5.QtCore import *
from time import sleep, time
from PyQt5 import QtCore, QtGui
from pyqtgraph import PlotWidget
import pyqtgraph as pg
# import os
from collections import deque




class Powersply_Simulation():
    def __init__(self, name):
        self.name = name

        self.Current_min_CH1 = 0.
        self.Current_max_CH1 = 10.
        self.Voltage_min_CH1 = 0.
        self.Voltage_max_CH1 = 10.

        self.Current_min_CH2 = 0.
        self.Current_max_CH2 = 10.
        self.Voltage_min_CH2 = 0.
        self.Voltage_max_CH2 = 10.

        self.Current_min_CH3 = 0.
        self.Current_max_CH3 = 10.
        self.Voltage_min_CH3 = 0.
        self.Voltage_max_CH3 = 10.

        self.Current_min_CH4 = 0.
        self.Current_max_CH4 = 10.
        self.Voltage_min_CH4 = 0.
        self.Voltage_max_CH4 = 10.

    def set_Current(self, min: float, max: float, channel:int):
        if channel == 1:
            self.Current_min_CH1 = min
            self.Current_max_CH1 = max

        if channel == 2:
            self.Current_min_CH2 = min
            self.Current_max_CH2 = max
            
        if channel == 3:
            self.Current_min_CH3 = min
            self.Current_max_CH3 = max

        if channel == 4:
            self.Current_min_CH4 = min
            self.Current_max_CH4 = max

    def set_Voltage(self, min: float, max: float, channel:int):
        if channel == 1:
            self.Voltage_min_CH1 = min
            self.Voltage_max_CH1 = max

        if channel == 2:
            self.Voltage_min_CH2 = min
            self.Voltage_max_CH2 = max
            
        if channel == 3:    
            self.Voltage_min_CH3 = min
            self.Voltage_max_CH3 = max

        if channel == 4:
            self.Voltage_min_CH4 = min
            self.Voltage_max_CH4 = max

    def get_Current_Settings(self, channel:int):
        if channel == 1:
                return (self.Current_min_CH1, self.Current_max_CH1)
        if channel == 2:
                return (self.Current_min_CH2, self.Current_max_CH2)
        if channel == 3:
                return (self.Current_min_CH3, self.Current_max_CH3)
        if channel == 4:
                return (self.Current_min_CH4, self.Current_max_CH4)

    def get_Voltage_Settings(self, channel:int):
        if channel == 1:
                return (self.Voltage_min_CH1, self.Voltage_max_CH1)
        if channel == 2:
                return (self.Voltage_min_CH2, self.Voltage_max_CH2)
        if channel == 3:
                return (self.Voltage_min_CH3, self.Voltage_max_CH3)
        if channel == 4:
                return (self.Voltage_min_CH4, self.Voltage_max_CH4)
        
    def output_Current(self, channel:int):
        if channel == 1:
                return random.uniform(self.Current_min_CH1, self.Current_max_CH1)
        if channel == 2:
                return random.uniform(self.Current_min_CH2, self.Current_max_CH2)
        if channel == 3:
                return random.uniform(self.Current_min_CH3, self.Current_max_CH3)
        if channel == 4:
                return random.uniform(self.Current_min_CH4, self.Current_max_CH4)

    def output_Voltage(self, channel:int):
        if channel == 1:
                return random.uniform(self.Voltage_min_CH1, self.Voltage_max_CH1)
        if channel == 2:
                return random.uniform(self.Voltage_min_CH2, self.Voltage_max_CH2)
        if channel == 3:
                return random.uniform(self.Voltage_min_CH3, self.Voltage_max_CH4)
        if channel == 4:
                return random.uniform(self.Voltage_min_CH4, self.Voltage_max_CH4)                        



class PS_UI(QMainWindow):

    def __init__(self, *args, ui_path, obj=None, **kwargs):
        super(PS_UI, self).__init__(*args, **kwargs)

        self.qtimer_list = list()
    
        # self.setupUi(self)
        uic.loadUi(ui_path, self)  # Load the .ui file
        #uic.loadUi(UI_File_Path, UI) if UI_File_Path != "" else None
        self.init_Buttons()
        self.init_Others()
        self.init_Timers()
        self.init_Checkbox()

        # Fixed self.time_counter: int | qtimer confusion
        self.time_counter = 0
        
        log_maxlen = 50
        self.log_structure = {
            1:{
                "time": deque(maxlen=log_maxlen),
                "current": deque(maxlen=log_maxlen),
                "voltage": deque(maxlen=log_maxlen),
            },
            2:{
                "time": deque(maxlen=log_maxlen),
                "current": deque(maxlen=log_maxlen),
                "voltage": deque(maxlen=log_maxlen),
            },
            3:{
                "time": deque(maxlen=log_maxlen),
                "current": deque(maxlen=log_maxlen),
                "voltage": deque(maxlen=log_maxlen),
            },
            4:{
                "time": deque(maxlen=log_maxlen),
                "current": deque(maxlen=log_maxlen),
                "voltage": deque(maxlen=log_maxlen),
            }
        }

        # Moved to init_timer
        # Fixed self.time_counter: int | qtimer confusion
        # self.time_counter = QtCore.QTimer()
        # self.time_counter.setInterval(100)
        # self.time_counter.timeout.connect(self.update_plot)
        # self.time_counter.start()

        self.graph_pen = pg.mkPen(
            color=(255, 0, 0), 
            width=3, 
            style=QtCore.Qt.DashLine
        )
        self.widget_Historical_Graph_CH1.setBackground("w")

    def add_log(self, channel, voltage, current):
        if len(self.log_structure[channel]["time"]) > 0:
            self.log_structure[channel]["time"].append(self.log_structure[channel]["time"][-1] - round(time(), 2))
        else:
            self.log_structure[channel]["time"].append(
                round(time(), 2)
            )

        self.log_structure[channel]["voltage"].append(voltage)
        self.log_structure[channel]["current"].append(current)

    def update_plot(self):
        # Fixed no attribute powersply_Object error when click to disconnect
        if hasattr(self, "powersply_Object"):
            current_time = [self.time_counter]

            self.plot(
                1,
                [0, 1, 2, 3], 
                [self.powersply_Object.output_Current(channel=1), 3, 6, 8]
            )
            self.plot(
                2,
                current_time,
                [self.powersply_Object.output_Current(channel=2)]
            )
            self.plot(
                3,
                current_time, 
                [self.powersply_Object.output_Current(channel=3)]
            )
            self.plot(
                4,
                current_time, 
                [self.powersply_Object.output_Current(channel=4)]
            )

            # self.plot(current_time, [
            #           self.powersply_Object.output_Voltage(channel=1)])
            # self.plot(current_time, [
            #           self.powersply_Object.output_Voltage(channel=2)])
            # self.plot(current_time, [
            #           self.powersply_Object.output_Voltage(channel=3)])
            # self.plot(current_time, [
            #           self.powersply_Object.output_Voltage(channel=4)])

            # Plus one for every loop in
            self.time_counter += 1
        
    def update_plot_v2(self):
        # Fixed no attribute powersply_Object error when click to disconnect
        if hasattr(self, "powersply_Object"):
            channel_list = [1, 2, 3, 4]
            
            for channel in channel_list:
                self.plot(
                    channel,
                    list(self.log_structure[channel]["time"]), 
                    list(self.log_structure[channel]["current"])
                )

        
    def plot(self, channel, time, voltage):
        # Fixed add self.time_counter at every plot 

        # https://www.pythonguis.com/tutorials/plotting-pyqtgraph/
        # self.widget_Historical_Graph_CH1.clear()
        # voltage[0] = round(voltage[0])
        # print("time, voltage", time, voltage)
        if channel == 1:
            self.widget_Historical_Graph_CH1.clear()
            self.widget_Historical_Graph_CH1.plot(
                time, voltage, 
                # symbol='*'
                pen=self.graph_pen,
                symbolSize=7,
            )
        elif channel == 2:
            self.widget_Historical_Graph_CH2.clear()
            self.widget_Historical_Graph_CH2.plot(
                time, voltage, 
                # pen=self.graph_pen,
                symbolSize=5
            )
        elif channel == 3:
            self.widget_Historical_Graph_CH3.clear()
            self.widget_Historical_Graph_CH3.plot(
                time, voltage, 
                pen=self.graph_pen,
                symbolSize=5
            )
        elif channel == 4:
            self.widget_Historical_Graph_CH4.clear()
            self.widget_Historical_Graph_CH4.plot(
                time, voltage, 
                pen=self.graph_pen,
                symbolSize=5
            )

    def init_Buttons(self):
        self.pushButton_CH1_Set.clicked.connect(
            lambda: [ 
                self.powersply_Object.set_Current(
                    self.doubleSpinBox_CH1_Current_Min.value(),
                    self.doubleSpinBox_CH1_Current_Max.value(),
                    1
                ),
                self.powersply_Object.set_Voltage(
                    self.doubleSpinBox_CH1_Voltage_Min.value(),
                    self.doubleSpinBox_CH1_Voltage_Max.value(),
                    1
                ),
                self.pushButton_CH1_Set_Event(True)
        ])
        self.pushButton_CH1_Get_Outputs.clicked.connect(
            self.read_All_Output
        )
        self.pushButton_CH1_Get_Settings.clicked.connect(
            self.read_All_Settings
        )
        self.pushButton_Connect.clicked.connect(
            self.connect_Comport
        )
        self.pushButton_Disconnect.clicked.connect(
            self.disconnect_Comport
        )
        #comport butonu buraya eklenebilir

        self.pushButton_CH2_Set.clicked.connect(
            lambda: [
                self.powersply_Object.set_Current(
                    self.doubleSpinBox_CH2_Current_Min.value(),
                    self.doubleSpinBox_CH2_Current_Max.value(),
                    2

                ),
                self.powersply_Object.set_Voltage(
                    self.doubleSpinBox_CH2_Voltage_Min.value(),
                    self.doubleSpinBox_CH2_Voltage_Max.value(),
                    2
                ),
                self.pushButton_CH2_Set_Event(True)
        ])
        self.pushButton_CH2_Get_Outputs.clicked.connect(
            self.read_All_Output
        )
        self.pushButton_CH2_Get_Settings.clicked.connect(
            self.read_All_Settings
        )

        self.pushButton_CH3_Set.clicked.connect(
            lambda: [
                self.powersply_Object.set_Current(
                    self.doubleSpinBox_CH3_Current_Min.value(),
                    self.doubleSpinBox_CH3_Current_Max.value(),
                    3
                ),
                self.powersply_Object.set_Voltage(
                    self.doubleSpinBox_CH3_Voltage_Min.value(),
                    self.doubleSpinBox_CH3_Voltage_Max.value(),
                    3
                ),
                self.pushButton_CH3_Set_Event(True)
        ])
        self.pushButton_CH3_Get_Outputs.clicked.connect(
            self.read_All_Output
        )
        self.pushButton_CH3_Get_Settings.clicked.connect(
            self.read_All_Settings
        )

        self.pushButton_CH4_Set.clicked.connect(
            lambda: [
                self.powersply_Object.set_Current(
                    self.doubleSpinBox_CH4_Current_Min.value(),
                    self.doubleSpinBox_CH4_Current_Max.value(),
                    4

                ),
                self.powersply_Object.set_Voltage(
                    self.doubleSpinBox_CH4_Voltage_Min.value(),
                    self.doubleSpinBox_CH4_Voltage_Max.value(),
                    4
                ),
                self.pushButton_CH3_Set_Event(True)
        ])
        self.pushButton_CH4_Get_Outputs.clicked.connect(
            self.read_All_Output
        )
        self.pushButton_CH4_Get_Settings.clicked.connect(
            self.read_All_Settings
        )

    #checkbox için uncheck metodu oluşturdum

    def uncheck(self, state):
  
        # checking if state is checked
        if state == Qt.Checked:
  
            # if first check box is selected
            if self.sender() == self.checkBox_CH1_ON:
  
                # making other check box to uncheck
                self.checkBox_CH1_OFF.setChecked(False)
                
  
            # if second check box is selected
            elif self.sender() == self.checkBox_CH1_OFF:
  
                # making other check box to uncheck
                self.checkBox_CH1_ON.setChecked(False)
                
            if self.sender() == self.checkBox_CH2_ON:
  
                # making other check box to uncheck
                self.checkBox_CH2_OFF.setChecked(False)
                
  
            # if second check box is selected
            elif self.sender() == self.checkBox_CH2_OFF:
  
                # making other check box to uncheck
                self.checkBox_CH2_ON.setChecked(False)

            if self.sender() == self.checkBox_CH3_ON:
  
                # making other check box to uncheck
                self.checkBox_CH3_OFF.setChecked(False)
                
  
            # if second check box is selected
            elif self.sender() == self.checkBox_CH3_OFF:
  
                # making other check box to uncheck
                self.checkBox_CH3_ON.setChecked(False)


            if self.sender() == self.checkBox_CH4_ON:
  
                # making other check box to uncheck
                self.checkBox_CH4_OFF.setChecked(False)
                
  
            # if second check box is selected
            elif self.sender() == self.checkBox_CH4_OFF:
  
                # making other check box to uncheck
                self.checkBox_CH4_ON.setChecked(False)

    def init_Checkbox(self):
        self.checkBox_CH1_ON.stateChanged.connect(self.uncheck)
        self.checkBox_CH1_OFF.stateChanged.connect(self.uncheck)
        
        self.checkBox_CH2_ON.stateChanged.connect(self.uncheck)
        self.checkBox_CH2_OFF.stateChanged.connect(self.uncheck)
        
        self.checkBox_CH3_ON.stateChanged.connect(self.uncheck)
        self.checkBox_CH3_OFF.stateChanged.connect(self.uncheck)
        
        self.checkBox_CH4_ON.stateChanged.connect(self.uncheck)
        self.checkBox_CH4_OFF.stateChanged.connect(self.uncheck)
        
    def init_Others(self):
        #CH1
        self.doubleSpinBox_CH1_Current_Min.valueChanged.connect(
            lambda: self.pushButton_CH1_Set_Event(False)
        )
        self.doubleSpinBox_CH1_Current_Max.valueChanged.connect(
            lambda: self.pushButton_CH1_Set_Event(False)
        )
        self.doubleSpinBox_CH1_Voltage_Min.valueChanged.connect(
            lambda: self.pushButton_CH1_Set_Event(False)
        )
        self.doubleSpinBox_CH1_Voltage_Max.valueChanged.connect(
            lambda: self.pushButton_CH1_Set_Event(False)
        )
        #CH2
        self.doubleSpinBox_CH2_Current_Min.valueChanged.connect(
            lambda: self.pushButton_CH2_Set_Event(False)
        )
        self.doubleSpinBox_CH2_Current_Max.valueChanged.connect(
            lambda: self.pushButton_CH2_Set_Event(False)
        )
        self.doubleSpinBox_CH2_Voltage_Min.valueChanged.connect(
            lambda: self.pushButton_CH2_Set_Event(False)
        )
        self.doubleSpinBox_CH2_Voltage_Max.valueChanged.connect(
            lambda: self.pushButton_CH2_Set_Event(False)
        )
        #CH3
        self.doubleSpinBox_CH3_Current_Min.valueChanged.connect(
            lambda: self.pushButton_CH3_Set_Event(False)
        )
        self.doubleSpinBox_CH3_Current_Max.valueChanged.connect(
            lambda: self.pushButton_CH3_Set_Event(False)
        )
        self.doubleSpinBox_CH3_Voltage_Min.valueChanged.connect(
            lambda: self.pushButton_CH3_Set_Event(False)
        )
        self.doubleSpinBox_CH3_Voltage_Max.valueChanged.connect(
            lambda: self.pushButton_CH3_Set_Event(False)
        )
        #CH4
        self.doubleSpinBox_CH4_Current_Min.valueChanged.connect(
            lambda: self.pushButton_CH4_Set_Event(False)
        )
        self.doubleSpinBox_CH4_Current_Max.valueChanged.connect(
            lambda: self.pushButton_CH4_Set_Event(False)
        )
        self.doubleSpinBox_CH4_Voltage_Min.valueChanged.connect(
            lambda: self.pushButton_CH4_Set_Event(False)
        )
        self.doubleSpinBox_CH4_Voltage_Max.valueChanged.connect(
            lambda: self.pushButton_CH4_Set_Event(False)
        )

        # groupBox_Historical_Graph_CH1_Layout = QVBoxLayout()
    	# groupBox_Historical_Graph_CH1_Layout.addWidget(
        #     self.graphWidget = pg.PlotWidget()
        # )
        # self.groupBox_Historical_Graph_CH1.setLayout(
        #     groupBox_Historical_Graph_CH1_Layout
        # )

        # self.groupBox_Historical_Graph_CH1.setLayout()

    def init_Timers(self):
        self.qtimer_list.append(
            qtimer_Create_And_Run(
                self, 
                self.read_All_Output, 
                delay=250, 
                is_needed_start=True, 
                is_single_shot=False
            )
        )

        self.qtimer_list.append(
            qtimer_Create_And_Run(
                self,
                self.update_plot_v2,
                delay=500,
                is_needed_start=True,
                is_single_shot=False
            )
        )

    def connect_Comport(self):
        self.powersply_Object = Powersply_Simulation("powersply alfa v123")
        self.label_CH1_Is_Connected_Event(True),
        self.label_CH2_Is_Connected_Event(True),
        self.label_CH3_Is_Connected_Event(True),
        self.label_CH4_Is_Connected_Event(True),
        self.read_All_Settings()

    def disconnect_Comport(self):
        if hasattr(self, "powersply_Object"):
            delattr(self, "powersply_Object")

        self.label_CH1_Is_Connected_Event(False)
        self.label_CH2_Is_Connected_Event(False),
        self.label_CH3_Is_Connected_Event(False),
        self.label_CH4_Is_Connected_Event(False),
        
        # TODO: Fix missing clear_All_Settings method.
        # self.clear_All_Settings()

    def read_All_Output(self):
        if hasattr(self, "powersply_Object"):
            channel = 1
            voltage = self.powersply_Object.output_Voltage(channel=channel)
            current = self.powersply_Object.output_Current(channel=channel)

            self.label_CH1_Current_Output_Result.setText(
                str(voltage)

            )
            self.label_CH1_Voltage_Output_Result.setText(
                str(current)
            )
            self.add_log(
                channel=channel,
                voltage=voltage,
                current=current
            )
            
            channel = 2
            voltage = self.powersply_Object.output_Voltage(channel=channel)
            current = self.powersply_Object.output_Current(channel=channel)

            self.label_CH2_Current_Output_Result.setText(
                str(voltage)

            )
            self.label_CH2_Voltage_Output_Result.setText(
                str(current)
            )
            self.add_log(
                channel=channel,
                voltage=voltage,
                current=current
            )
            
            channel = 3
            voltage = self.powersply_Object.output_Voltage(channel=channel)
            current = self.powersply_Object.output_Current(channel=channel)

            self.label_CH3_Current_Output_Result.setText(
                str(voltage)

            )
            self.label_CH3_Voltage_Output_Result.setText(
                str(current)
            )
            self.add_log(
                channel=channel,
                voltage=voltage,
                current=current
            )

            channel = 4
            voltage = self.powersply_Object.output_Voltage(channel=channel)
            current = self.powersply_Object.output_Current(channel=channel)

            self.label_CH4_Current_Output_Result.setText(
                str(voltage)

            )
            self.label_CH4_Voltage_Output_Result.setText(
                str(current)
            )
            self.add_log(
                channel=channel,
                voltage=voltage,
                current=current
            )

    def read_All_Settings(self):
        if hasattr(self, "powersply_Object"):
            #CH1
            Current_min, Current_max = self.powersply_Object.get_Current_Settings(
                channel=1)
            self.doubleSpinBox_CH1_Current_Min.setValue(Current_min)
            self.doubleSpinBox_CH1_Current_Max.setValue(Current_max)

            Voltage_min, Voltage_max = self.powersply_Object.get_Voltage_Settings(
                channel=1)
            self.doubleSpinBox_CH1_Voltage_Min.setValue(Voltage_min)
            self.doubleSpinBox_CH1_Voltage_Max.setValue(Voltage_max)

            self.pushButton_CH1_Set_Event(True)

            #CH2
            Current_min, Current_max = self.powersply_Object.get_Current_Settings(
                channel=2)
            self.doubleSpinBox_CH2_Current_Min.setValue(Current_min)
            self.doubleSpinBox_CH2_Current_Max.setValue(Current_max)

            Voltage_min, Voltage_max = self.powersply_Object.get_Voltage_Settings(
                channel=2)
            self.doubleSpinBox_CH2_Voltage_Min.setValue(Voltage_min)
            self.doubleSpinBox_CH2_Voltage_Max.setValue(Voltage_max)

            self.pushButton_CH2_Set_Event(True)

            #CH3
            Current_min, Current_max = self.powersply_Object.get_Current_Settings(
                channel=3)
            self.doubleSpinBox_CH3_Current_Min.setValue(Current_min)
            self.doubleSpinBox_CH3_Current_Max.setValue(Current_max)

            Voltage_min, Voltage_max = self.powersply_Object.get_Voltage_Settings(
                channel=3)
            self.doubleSpinBox_CH3_Voltage_Min.setValue(Voltage_min)
            self.doubleSpinBox_CH3_Voltage_Max.setValue(Voltage_max)

            self.pushButton_CH3_Set_Event(True)

            #CH4
            Current_min, Current_max = self.powersply_Object.get_Current_Settings(
                channel=4)
            self.doubleSpinBox_CH4_Current_Min.setValue(Current_min)
            self.doubleSpinBox_CH4_Current_Max.setValue(Current_max)

            Voltage_min, Voltage_max = self.powersply_Object.get_Voltage_Settings(
                channel=4)
            self.doubleSpinBox_CH4_Voltage_Min.setValue(Voltage_min)
            self.doubleSpinBox_CH4_Voltage_Max.setValue(Voltage_max)

            self.pushButton_CH4_Set_Event(True)

    def pushButton_CH1_Set_Event(self, is_Updated: bool = False):
        if is_Updated:
            self.pushButton_CH1_Set.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(0, 255, 0);")
        else:
            self.pushButton_CH1_Set.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(255, 0, 0);")

    def label_CH1_Is_Connected_Event(self, is_Updated: bool = False):
        if is_Updated:
            self.label_CH1_Is_Connected.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(0, 255, 0);")
        else:
            self.label_CH1_Is_Connected.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(255, 0, 0);")

    def pushButton_CH2_Set_Event(self, is_Updated: bool = False):
        if is_Updated:
            self.pushButton_CH2_Set.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(0, 255, 0);")
        else:
            self.pushButton_CH2_Set.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(255, 0, 0);")

    def label_CH2_Is_Connected_Event(self, is_Updated: bool = False):
        if is_Updated:
            self.label_CH2_Is_Connected.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(0, 255, 0);")
        else:
            self.label_CH2_Is_Connected.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(255, 0, 0);")

    def pushButton_CH3_Set_Event(self, is_Updated: bool = False):
        if is_Updated:
            self.pushButton_CH3_Set.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(0, 255, 0);")
        else:
            self.pushButton_CH3_Set.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(255, 0, 0);")

    def label_CH3_Is_Connected_Event(self, is_Updated: bool = False):
        if is_Updated:
            self.label_CH3_Is_Connected.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(0, 255, 0);")
        else:
            self.label_CH3_Is_Connected.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(255, 0, 0);")

    def pushButton_CH4_Set_Event(self, is_Updated: bool = False):
        if is_Updated:
            self.pushButton_CH4_Set.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(0, 255, 0);")
        else:
            self.pushButton_CH4_Set.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(255, 0, 0);")

    def label_CH4_Is_Connected_Event(self, is_Updated: bool = False):
        if is_Updated:
            self.label_CH4_Is_Connected.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(0, 255, 0);")
        else:
            self.label_CH4_Is_Connected.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(255, 0, 0);")



def qtimer_Create_And_Run(parent, connection, delay=100, is_needed_start=True, is_single_shot=False):
    timer = QTimer(parent)
    timer.setInterval(delay)
    timer.timeout.connect(connection)
    timer.setSingleShot(is_single_shot)
    if is_needed_start:
        timer.start()
    return timer

def qtimer_All_Stop(qtimer):
    qtimer.stop() if qtimer.isActive() else None


if __name__ == "__main__":

    app = QApplication(sys.argv)
    
    UI = PS_UI(ui_path="ps_gui.ui")
    UI.setWindowTitle("Powersply UI")

    UI.show()  # Show at default window size#

    sys.exit(app.exec())