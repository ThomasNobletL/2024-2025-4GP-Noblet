#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 15 15:27:11 2025

@author: thomasnoblet
"""



import serial
import time

# Remplace par ton port série Bluetooth :
# Windows : "COM5", "COM6", etc.
# macOS : "/dev/tty.HC-05-DevB", ou utilise `ls /dev/tty.*` pour trouver le bon
port = "/dev/cu.HC0501"       # <-- À adapter à ton système
baudrate = 9600

try:
    ser = serial.Serial(port, baudrate, timeout=1)
    print(f"Connecté à {port} à {baudrate} bauds.")
    time.sleep(2)  # Laisser le temps à la connexion série de s'établir

    while True:
        if ser.in_waiting:
            ligne = ser.readline().decode('utf-8').strip()
            if ligne:
                try:
                    # On suppose que les données arrivent sous forme "1,2,3"
                    a_str, b_str, c_str = ligne.split(',')
                    a = int(a_str)
                    b = int(b_str)
                    c = int(c_str)
                    print(f"Reçu : a={a}, b={b}, c={c}")
                except ValueError:
                    print(f"Erreur de parsing : {ligne}")
except serial.SerialException as e:
    print(f"Erreur de connexion : {e}")
except KeyboardInterrupt:
    print("\nArrêt du programme.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Port série fermé.")
