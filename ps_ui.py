import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import random
from PyQt5.QtCore import QTimer
from time import sleep

class Powersply_Simulation():
    def __init__(self, name):
        self.name = name
        self.ampere_min = 0.
        self.ampere_max = 100.
        self.voltage_min = 0.
        self.voltage_max = 100.

    def set_Ampere(self, min: float, max: float):
        self.ampere_min = min
        self.ampere_max = max

    def set_Voltage(self, min: float, max: float):
        self.voltage_min = min
        self.voltage_max = max

    def get_Ampere(self):
        return self.ampere_min, self.ampere_max

    def get_Voltage(self):
        return self.voltage_min, self.voltage_max

    def output_Ampere(self):
        return random.uniform(self.ampere_min, self.ampere_max)

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
                self.powersply_Object.set_Ampere(
                    self.doubleSpinBox_CH1_Ampere_Min.value(),
                    self.doubleSpinBox_CH1_Ampere_Max.value()
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

    def init_Others(self):
        self.doubleSpinBox_CH1_Ampere_Min.valueChanged.connect(
            lambda: self.pushButton_CH1_Set_Event(False)
        )
        self.doubleSpinBox_CH1_Ampere_Max.valueChanged.connect(
            lambda: self.pushButton_CH1_Set_Event(False)
        )
        self.doubleSpinBox_CH1_Voltage_Min.valueChanged.connect(
            lambda: self.pushButton_CH1_Set_Event(False)
        )
        self.doubleSpinBox_CH1_Voltage_Max.valueChanged.connect(
            lambda: self.pushButton_CH1_Set_Event(False)
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
        self.label_CH1_Is_Connected_Event(True)
        self.read_All_Settings()

    def disconnect_Comport(self):
        if hasattr(self, "powersply_Object"):
            delattr(self, "powersply_Object")
            #self.clear_All_Settings()

        self.label_CH1_Is_Connected_Event(False)

    def read_All_Output(self):
        if hasattr(self, "powersply_Object"):
            self.label_CH1_Ampere_Output_Result.setText(
                    str(self.powersply_Object.output_Ampere())
            )
            self.label_CH1_Voltage_Output_Result.setText(
                str(self.powersply_Object.output_Voltage())
            )
        else:
            print("error")
            delay = 1
            sleep(delay)
    def read_All_Settings(self):
        if hasattr(self, "powersply_Object"):
            ampere_min, ampere_max = self.powersply_Object.get_Ampere()
            self.doubleSpinBox_CH1_Ampere_Min.setValue(ampere_min)
            self.doubleSpinBox_CH1_Ampere_Max.setValue(ampere_max)

            voltage_min, voltage_max = self.powersply_Object.get_Voltage()
            self.doubleSpinBox_CH1_Voltage_Min.setValue(voltage_min)
            self.doubleSpinBox_CH1_Voltage_Max.setValue(voltage_max)

            self.pushButton_CH1_Set_Event(True)
        else:
            print("wtf")


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