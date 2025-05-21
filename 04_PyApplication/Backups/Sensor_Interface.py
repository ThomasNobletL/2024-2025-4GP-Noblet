import sys
import serial.tools.list_ports
import serial
import time
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QComboBox, QPushButton, QLabel
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.uic import loadUi

class SerialThread(QThread):
    data_received = pyqtSignal(int, int, int)  # émet 3 entiers reçus

    def __init__(self, port, baudrate=9600):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self._running = True

    def run(self):
        try:
            ser = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # laisser le temps à la connexion de s'établir
            print(f"Connexion série via {self.port}")


            while self._running:
                if ser.in_waiting:
                    ligne = ser.readline().decode('utf-8').strip()
                    if ligne:
                        try:
                            a_str, b_str, c_str = ligne.split(',')
                            a = int(a_str)
                            b = int(b_str)
                            c = int(c_str)
                            self.data_received.emit(a, b, c)
                        except ValueError:
                            print(f"Erreur de parsing : {ligne}")

            ser.close()
        except serial.SerialException as e:
            print(f"Erreur de connexion série : {e}")

    def stop(self):
        self._running = False
        self.wait()



class MainInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        ui_path = "/Users/thomasnoblet/Not In Paris Now Dropbox/Thomas Noblet/x3 Capteur/05 QtInterfaces/main_interface.ui"
        if not os.path.isfile(ui_path):
            raise FileNotFoundError(f"Fichier UI introuvable : {ui_path}")

        loadUi(ui_path, self)

        # Assure-toi que tous les widgets existent sinon les créer par défaut
        self._quit.clicked.connect(self.close)
        
        if not hasattr(self, "bluetooth_box") or self.bluetooth_box is None:
            self.bluetooth_box = QComboBox(self)
        if not hasattr(self, "bluetooth_confirm") or self.bluetooth_confirm is None:
            self.bluetooth_confirm = QPushButton("Confirmer", self)
        if not hasattr(self, "widget_3D") or self.widget_3D is None:
            self.widget_3D = QWidget(self)
        if not hasattr(self, "arduino_name") or self.arduino_name is None:
            self.arduino_name = QLabel(self)
        if not hasattr(self, "value") or self.value is None:
            self.value = QLabel(self)
        if not hasattr(self, "widget_SVG") or self.widget_SVG is None:
            self.widget_SVG = QWidget(self)
            
            
        self.populate_ports()
        self.bluetooth_confirm.clicked.connect(self.confirm_selection)
        self.serial_thread = None
        
    def closeEvent(self, event):
        # Stopper le thread proprement avant de fermer la fenêtre
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
        # Exemple pour mettre à jour les labels :
        port_name = os.path.basename(selected_port) 
        self.arduino_name.setText(f"Arduino: {port_name}")
        self.value.setText("pls wait...")

        if self.serial_thread is not None:
                self.serial_thread.stop()
    
        try:
            # Tester l'ouverture avant de créer le thread
            test_serial = serial.Serial(selected_port, baudrate=9600, timeout=1)
            test_serial.close()
    
            # Lancer le thread réel
            self.serial_thread = SerialThread(selected_port, baudrate=9600)
            self.serial_thread.data_received.connect(self.update_values)
            self.serial_thread.start()
            self.value.setText("Connecté !")
    
        except serial.SerialException as e:
            print(f"Erreur de connexion : {e}")
            self.value.setText("Connexion failed")
        
    def update_values(self, a, b, c):
        # Mettre à jour le label 'value' avec les données reçues
        self.value.setText(f"a={a}, b={b}, c={c}")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainInterface()
    window.show()
    sys.exit(app.exec())
