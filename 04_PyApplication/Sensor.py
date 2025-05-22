import sys
import serial.tools.list_ports
import serial
import time
import os
import math
from PyQt6.QtQuickWidgets import QQuickWidget
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QComboBox, QPushButton, QLabel, QVBoxLayout
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.uic import loadUi
from PyQt6.QtGui import QPixmap
import random
class SerialThread(QThread):
    data_received = pyqtSignal(int, int, int)  # émet 3 entiers reçus

    def __init__(self, port, baudrate=9600):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self._running = True
        self.ser =None

    def run(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)
            print(f"Connexion série via {self.port}")

            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()

            while self._running:

                ligne = self.ser.readline().decode('utf-8').strip()
                print(f"Ligne reçue: '{ligne}'")
                if ligne:
                    try:
                        a_str, b_str = ligne.split(',')
                        a = int(a_str)
                        b = int(b_str)
                        self.data_received.emit(a, b)
                    except ValueError:
                        print(f"Erreur de parsing : {ligne}")

            self.ser.close()
        except serial.SerialException as e:
            print(f"Erreur de connexion série : {e}")


    def send_data(self, data: str):
        if self.ser and self.ser.is_open:
            self.ser.write(data.encode('utf-8'))
            print(f"Envoyé : {data.strip()}")
        else:
            print("Port série non ouvert")

    def stop(self):
        self._running = False
        self.wait()



class MainInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        ui_path = "main_interface.ui"
        if not os.path.isfile(ui_path):
            raise FileNotFoundError(f"Fichier UI introuvable : {ui_path}")

        loadUi(ui_path, self)

        self._quit.clicked.connect(self.close)

        #Creation des objets de l'interface si ils ne sont pas là de base

        if not hasattr(self, "bluetooth_box") or self.bluetooth_box is None:
            self.bluetooth_box = QComboBox(self)
        if not hasattr(self, "bluetooth_confirm") or self.bluetooth_confirm is None:
            self.bluetooth_confirm = QPushButton("Confirmer", self)
        if not hasattr(self, "arduino_name") or self.arduino_name is None:
            self.arduino_name = QLabel(self)
        if not hasattr(self, "value") or self.value is None:
            self.value = QLabel(self)
        if not hasattr(self, "gain") or self.gain is None:
            self.gain = QLabel(self)
        if not hasattr(self, "spinBox") or self.spinBox is None:
            self.spinBox = QspinBox(self)
        if not hasattr(self, "send") or self.send is None:
            self.send = QPushButton(self.send_spinbox_value)
        if not hasattr(self, "R1") or self.R1 is None:
            self.R1 = QLabel(self)
        if not hasattr(self, "R2") or self.R2 is None:
            self.R2 = QLabel(self)

        self.populate_ports()

        self.send.clicked.connect(self.send_spinbox_value)
        self.R2.setText(f"Ramp = 100000 \u03A9")
        self.bluetooth_confirm.clicked.connect(self.confirm_selection)
        self.serial_thread = None
        
    def closeEvent(self, event):
        if self.serial_thread is not None:
            self.serial_thread.stop()
        event.accept()

    def populate_ports(self):
        ports = serial.tools.list_ports.comports()
        self.bluetooth_box.clear()
        for port in ports:
            display_text = f"{port.device}: {port.description} [{port.hwid}]"
            self.bluetooth_box.addItem(display_text, port.device)

    
    def confirm_selection(self):
        selected_port = self.bluetooth_box.currentData()
        print(f"Port sélectionné : {selected_port}")
        port_name = os.path.basename(selected_port) 
        self.arduino_name.setText(f"Arduino: {port_name}")
        self.value.setText("pls wait...")

        if self.serial_thread is not None:
                self.serial_thread.stop()
    
        try:
            # Tester l'ouverture avant de créer le thread
            test_serial = serial.Serial(selected_port, baudrate=9600, timeout=1)
            test_serial.close()
            self.serial_conn = serial.Serial(selected_port, baudrate=9600, timeout=1)

            self.serial_thread = SerialThread(selected_port,baudrate=9600)
            self.serial_thread.data_received.connect(self.update_values)
            self.serial_thread.start()
            self.value.setText("Connecté !")
    
        except serial.SerialException as e:
            print(f"Erreur de connexion : {e}")
            self.value.setText("Connexion failed")
        
    def update_values(self, a, b):
        sortie = a*5.0/1023.0 #conversion en volt
        gain = a / b if b != 0 else 0 #calcul gain observé, inutile ici
        self.value.setText(f"Mes = {sortie} V")
        self.gain.setText(f"Gain = {gain}")

    def send_spinbox_value(self):
        value = self.spinBox.value()
        MCP_res = 100000/(value -1)
        D = round(MCP_res-125*(256/50000))

        self.R1.setText(f"RMCP = {MCP_res:.1f} \u03A9")

        if isinstance(self.serial_thread, SerialThread):
            self.serial_thread.send_data(f"SET{D}\n")
        else:
            print("Aucune connexion série active pour l'envoi.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainInterface()
    window.show()
    sys.exit(app.exec())
