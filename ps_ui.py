import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import random
from PyQt5.QtCore import *
from time import sleep

class Powersply_Simulation():
    def __init__(self, name):
        self.name = name
        self.current_min = 0.
        self.current_max = 100.
        self.voltage_min = 0.
        self.voltage_max = 100.

    def set_current(self, min: float, max: float):
        self.current_min = min
        self.current_max = max

    def set_Voltage(self, min: float, max: float):
        self.voltage_min = min
        self.voltage_max = max

    def get_current(self):
        return self.current_min, self.current_max

    def get_Voltage(self):
        return self.voltage_min, self.voltage_max

    def output_current(self):
        return random.uniform(self.current_min, self.current_max)

    def output_Voltage(self):
        return random.uniform(self.voltage_min, self.voltage_max)

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

    def init_Buttons(self):
        self.pushButton_CH1_Set.clicked.connect(
            lambda: [ 
                self.powersply_Object.set_current(
                    self.doubleSpinBox_CH1_current_Min.value(),
                    self.doubleSpinBox_CH1_current_Max.value()
                ),
                self.powersply_Object.set_Voltage(
                    self.doubleSpinBox_CH1_Voltage_Min.value(),
                    self.doubleSpinBox_CH1_Voltage_Max.value()
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
                self.powersply_Object.set_current(
                    self.doubleSpinBox_CH2_current_Min.value(),
                    self.doubleSpinBox_CH2_current_Max.value()

                ),
                self.powersply_Object.set_Voltage(
                    self.doubleSpinBox_CH2_Voltage_Min.value(),
                    self.doubleSpinBox_CH2_Voltage_Max.value()
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
                self.powersply_Object.set_current(
                    self.doubleSpinBox_CH3_current_Min.value(),
                    self.doubleSpinBox_CH3_current_Max.value()

                ),
                self.powersply_Object.set_Voltage(
                    self.doubleSpinBox_CH3_Voltage_Min.value(),
                    self.doubleSpinBox_CH3_Voltage_Max.value()
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
                self.powersply_Object.set_current(
                    self.doubleSpinBox_CH4_current_Min.value(),
                    self.doubleSpinBox_CH4_current_Max.value()

                ),
                self.powersply_Object.set_Voltage(
                    self.doubleSpinBox_CH4_Voltage_Min.value(),
                    self.doubleSpinBox_CH4_Voltage_Max.value()
                ),
                self.pushButton_CH3_Set_Event(True)
        ])
        self.pushButton_CH4_Get_Outputs.clicked.connect(
            self.read_All_Output
        )
        self.pushButton_CH4_Get_Settings.clicked.connect(
            self.read_All_Settings
        )

    #checkbox için uncheck methodu oluşturdum

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
        self.doubleSpinBox_CH1_current_Min.valueChanged.connect(
            lambda: self.pushButton_CH1_Set_Event(False)
        )
        self.doubleSpinBox_CH1_current_Max.valueChanged.connect(
            lambda: self.pushButton_CH1_Set_Event(False)
        )
        self.doubleSpinBox_CH1_Voltage_Min.valueChanged.connect(
            lambda: self.pushButton_CH1_Set_Event(False)
        )
        self.doubleSpinBox_CH1_Voltage_Max.valueChanged.connect(
            lambda: self.pushButton_CH1_Set_Event(False)
        )
        #CH2
        self.doubleSpinBox_CH2_current_Min.valueChanged.connect(
            lambda: self.pushButton_CH2_Set_Event(False)
        )
        self.doubleSpinBox_CH2_current_Max.valueChanged.connect(
            lambda: self.pushButton_CH2_Set_Event(False)
        )
        self.doubleSpinBox_CH2_Voltage_Min.valueChanged.connect(
            lambda: self.pushButton_CH2_Set_Event(False)
        )
        self.doubleSpinBox_CH2_Voltage_Max.valueChanged.connect(
            lambda: self.pushButton_CH2_Set_Event(False)
        )
        #CH3
        self.doubleSpinBox_CH3_current_Min.valueChanged.connect(
            lambda: self.pushButton_CH3_Set_Event(False)
        )
        self.doubleSpinBox_CH3_current_Max.valueChanged.connect(
            lambda: self.pushButton_CH3_Set_Event(False)
        )
        self.doubleSpinBox_CH3_Voltage_Min.valueChanged.connect(
            lambda: self.pushButton_CH3_Set_Event(False)
        )
        self.doubleSpinBox_CH3_Voltage_Max.valueChanged.connect(
            lambda: self.pushButton_CH3_Set_Event(False)
        )
        #CH4
        self.doubleSpinBox_CH4_current_Min.valueChanged.connect(
            lambda: self.pushButton_CH4_Set_Event(False)
        )
        self.doubleSpinBox_CH4_current_Max.valueChanged.connect(
            lambda: self.pushButton_CH4_Set_Event(False)
        )
        self.doubleSpinBox_CH4_Voltage_Min.valueChanged.connect(
            lambda: self.pushButton_CH4_Set_Event(False)
        )
        self.doubleSpinBox_CH4_Voltage_Max.valueChanged.connect(
            lambda: self.pushButton_CH4_Set_Event(False)
        )

    def init_Timers(self):
        self.qtimer_list.append(
            qtimer_Create_And_Run(
                self, 
                self.read_All_Output, 
                delay=100, 
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
        self.clear_All_Settings()

    def read_All_Output(self):
        if hasattr(self, "powersply_Object"):
            self.label_CH1_current_Output_Result.setText(
                    str(self.powersply_Object.output_current())
            )
            self.label_CH1_Voltage_Output_Result.setText(
                str(self.powersply_Object.output_Voltage())
            )
        else:
            print("CH1 Reading Output ERROR")
            delay = 1
            sleep(delay)

        if hasattr(self, "powersply_Object"):
            self.label_CH2_current_Output_Result.setText(
                    str(self.powersply_Object.output_current())
            )
            self.label_CH2_Voltage_Output_Result.setText(
                str(self.powersply_Object.output_Voltage())
            )
        else:
            print("CH2 Reading Output ERROR")
            delay = 1
            sleep(delay)

        if hasattr(self, "powersply_Object"):
            self.label_CH3_current_Output_Result.setText(
                    str(self.powersply_Object.output_current())
            )
            self.label_CH3_Voltage_Output_Result.setText(
                str(self.powersply_Object.output_Voltage())
            )
        else:
            print("CH3 Reading Output ERROR")
            delay = 1
            sleep(delay)


        if hasattr(self, "powersply_Object"):
            self.label_CH4_current_Output_Result.setText(
                    str(self.powersply_Object.output_current())
            )
            self.label_CH4_Voltage_Output_Result.setText(
                str(self.powersply_Object.output_Voltage())
            )
        else:
            print("CH4 Reading Output ERROR")
            delay = 1
            sleep(delay)

    def read_All_Settings(self):
        #CH1
        if hasattr(self, "powersply_Object"):
            current_min, current_max = self.powersply_Object.get_current()
            self.doubleSpinBox_CH1_current_Min.setValue(current_min)
            self.doubleSpinBox_CH1_current_Max.setValue(current_max)

            voltage_min, voltage_max = self.powersply_Object.get_Voltage()
            self.doubleSpinBox_CH1_Voltage_Min.setValue(voltage_min)
            self.doubleSpinBox_CH1_Voltage_Max.setValue(voltage_max)

            self.pushButton_CH1_Set_Event(True)
        else:
            print("CH1 Reading Settings Error")

        #CH2
        if hasattr(self, "powersply_Object"):
            current_min, current_max = self.powersply_Object.get_current()#is this duplicate?
            self.doubleSpinBox_CH2_current_Min.setValue(current_min)
            self.doubleSpinBox_CH2_current_Max.setValue(current_max)

            voltage_min, voltage_max = self.powersply_Object.get_Voltage()
            self.doubleSpinBox_CH2_Voltage_Min.setValue(voltage_min)
            self.doubleSpinBox_CH2_Voltage_Max.setValue(voltage_max)

            self.pushButton_CH2_Set_Event(True)
        else:
            print("CH2 Reading Settings Error")

        #CH3
        if hasattr(self, "powersply_Object"):
            current_min, current_max = self.powersply_Object.get_current()
            self.doubleSpinBox_CH3_current_Min.setValue(current_min)
            self.doubleSpinBox_CH3_current_Max.setValue(current_max)

            voltage_min, voltage_max = self.powersply_Object.get_Voltage()
            self.doubleSpinBox_CH3_Voltage_Min.setValue(voltage_min)
            self.doubleSpinBox_CH3_Voltage_Max.setValue(voltage_max)

            self.pushButton_CH3_Set_Event(True)
        else:
            print("CH3 Reading Settings Error")

        #CH4
        if hasattr(self, "powersply_Object"):
            current_min, current_max = self.powersply_Object.get_current()
            self.doubleSpinBox_CH4_current_Min.setValue(current_min)
            self.doubleSpinBox_CH4_current_Max.setValue(current_max)

            voltage_min, voltage_max = self.powersply_Object.get_Voltage()
            self.doubleSpinBox_CH4_Voltage_Min.setValue(voltage_min)
            self.doubleSpinBox_CH4_Voltage_Max.setValue(voltage_max)

            self.pushButton_CH4_Set_Event(True)
        else:
            print("CH4 Reading Settings Error")

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