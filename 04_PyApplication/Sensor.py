import pyqtgraph as pg
import sys
import serial.tools.list_ports
import serial
import time
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PyQt6.QtCore import QThread, pyqtSignal, QTimer
from PyQt6.uic import loadUi


###Thread pour la connexion série et bluetooth###

class SerialThread(QThread):
    data_received = pyqtSignal(int, int, int)  # émet 3 entiers reçus

    def __init__(self, port, baudrate=9600):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self._running = True
        self.ser =None

    # Recupération des messages depuis le port
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

    #Envoie des commandes pour controler la MCP41050
    def send_data(self, data: str):
        if self.ser and self.ser.is_open:
            self.ser.write(data.encode('utf-8'))
            print(f"Envoyé : {data.strip()}")
        else:
            print("Port série non ouvert")

    def stop(self):
        self._running = False
        self.wait()


###Classe de l'interface###

class MainInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        ui_path = "main_interface.ui"
        if not os.path.isfile(ui_path):
            raise FileNotFoundError(f"Fichier UI introuvable : {ui_path}")

        loadUi(ui_path, self)
        #Connexions aux boutons
        self.pushButton_Run.clicked.connect(self.toggle_recording)
        self.pushButton_Save.clicked.connect(self.save_data)
        self._quit.clicked.connect(self.close)
        self.send.clicked.connect(self.send_spinbox_value)
        self.R2.setText(f"Ramp = 100000 \u03A9")
        self.bluetooth_confirm.clicked.connect(self.confirm_selection)

        #Initialisation du tableau de mesures
        self.recording = False
        self.data_storage = []
        self.index = 0

        #Initialisation du graphique
        self.graphWidget = pg.PlotWidget()
        layout = QVBoxLayout(self.graph_container)
        layout.addWidget(self.graphWidget)
        self.graphWidget.setBackground('w')
        self.graphWidget.setTitle("Tension sortie (V)")
        self.graphWidget.setLabel('left', 'Voltage', units='V')
        self.graphWidget.setLabel('bottom', 'Points')
        self.graphWidget.showGrid(x=True, y=True)
        self.x = []
        self.y = []
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pg.mkPen(color='b', width=2))

        #Recherches des ports disponibles
        self.populate_ports()

        #Par défaut, aucun thread actif
        self.serial_thread = None

    # Fonction de ermeture propre du programme
    def closeEvent(self, event):
        if self.serial_thread is not None:
            self.serial_thread.stop()
        event.accept()

    # Fonction de recherche des ports disponibles
    def populate_ports(self):
        ports = serial.tools.list_ports.comports()
        self.bluetooth_box.clear()
        for port in ports:
            display_text = f"{port.device}: {port.description} [{port.hwid}]"
            self.bluetooth_box.addItem(display_text, port.device)

    # Fonction de connexion avec le port choisi
    def confirm_selection(self):
        selected_port = self.bluetooth_box.currentData()
        print(f"Port sélectionné : {selected_port}")
        port_name = os.path.basename(selected_port) 
        self.arduino_name.setText(f"Arduino: {port_name}")
        self.value.setText("pls wait...")

        if self.serial_thread is not None:
                self.serial_thread.stop()
                self.serial_thread = None
        # Test de la connexion sur le port avant de creer le thread
        try:

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

    # Mises à jour des valeurs dans l'interface, le tableau et le graphique
    def update_values(self, a, b):
        sortie = a*5.0/1023.0 #conversion en volt
        gain = a / b if b != 0 else 0 #calcul gain observé, inutile ici
        self.value.setText(f"Mes = {sortie} V")
        self.gain.setText(f"Gain = {gain}")

        if self.recording:
            self.data_storage.append((self.index, sortie)) #Stockage pour le txt

            self.x.append(self.index) #Update du graphique
            self.y.append(sortie)
            self.data_line.setData(self.x, self.y)
            self.index += 1

    # Fonction d'envoie des valeurs de résistances au MCP41050
    def send_spinbox_value(self):
        value = self.spinBox.value()
        MCP_res = 100000/value
        D = round(MCP_res-125*(256/50000))

        self.R1.setText(f"RMCP = {MCP_res:.1f} \u03A9")

        if isinstance(self.serial_thread, SerialThread):
            self.serial_thread.send_data(f"SET{D}\n")
        else:
            print("Aucune connexion liaison série active pour l'envoi.")

    #  Fonction de sauvegarde du tableau récupéré

    def save_data(self):
        if not self.data_storage:
            print("Aucune donnée à sauvegarder.")
            return
        filename = "FlexOutMes.txt"
        try:
            with open(filename, "w") as f:
                f.write("Index\tSortie(V)\n")
                for x, y in self.data_storage:
                    f.write(f"{x}\t{y:.6f}\n")
            print(f"Données sauvegardées dans {filename}")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")

    # Fonction de début de stockage dans la tableau

    def toggle_recording(self):
        self.recording = not self.recording
        if self.recording:
            self.pushButton_Run.setText("STOP")
            self.data_storage.clear()
            self.index = 0              #Reinitialisation des mesures precedentes
            self.x.clear()
            self.y.clear()
            self.data_line.setData([], [])
        else:
            self.pushButton_Run.setText("RUN")
        print(f"Enregistrement {'RUN' if self.recording else 'STOP'}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainInterface()
    window.show()
    sys.exit(app.exec())
