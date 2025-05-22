<h1 align = "center"> Projet Capteur Graphite 4A - GP <h1> 
<h2 align="center"> Par NOBLET Thomas </h2>
<h3 align="center"> INSA de Toulouse, département Génie Physique, année 2024 - 2025 </h3>
  
<p align="center">
  <a href="http://www.gnu.org/licenses/gpl-3.0">
    <img src="https://img.shields.io/badge/License-GPL%20v3-blue.svg" alt="License: GPL v3">
  </a>
</p>

## <h2 align = "center"> Mesure de contrainte sous arduino & python d'un capteur graphite <h1>

### 1. Description

*Contexte*

Le projet consiste à reproduire une technologie low-tech de capteur de flexion en graphite, se basant sur l'article "Pencil Drawn Strain Gauges and Chemiresistors on Paper" de Cheng-Wei Lin, Zhibo Zhao, Jaemyung Kim & Jiaxing Huang.

*Principe*

Des traces de crayons sur du papier se comportent comme des résistances dont la valeur varie en fonction de la courbure du papier sur lequels elles sont dessinées. 

*Contenu du projet*

Une datasheet du capteur a pu être réalisée à l'aide d'une carte Arduino Uno, d'un circuit d'amplification (dont le PCB a été réalisé sur KICAD) et d'une interface python.

***Matériel utilisé (non exhaustif)***
- **Capteur de contrainte en graphène** : Mine 4H minimum conseillée
- **LTC1050** : Amplificateur du circuit 
- **MCP 41050** : Varier le gain du circuit d'amplification
- **Module Bluetooth HC-05** : Récupérer les données en Bluetooth  
- **Ecran OLED SS1306 en I2C** : Affichage des données sur le PCB

### 2. Circuit d'amplification & PCB

Le circuit d'amplification utilise un amplificateur LTC1050 avec un gain de 1 + R2/R1. La résistance R1 est un potentiomètre MCP41050 donnant une plage de gain de 3 à 801.

Le PCB utilisé est celui-ci, avec les pins Rx et Tx de l'arduino connectées au HC05 (OldPCB). Cet configuartion est utilisable si on souhaite uploader le code arduino directement en bluetooth, mais il faut impérativement utiliser les pins 2 et 3 pour un upload depuis le port USB. Les pins 0 et 1 sont également utilisées par la liason série vers un PC, ce qui provoque des erreurs en utilisant la connexion bluetooth sur ce port.
<p align="center"><em>Old PCB</em></p>

En l'occurence, aucun des codes python et arduino fournis fonctionnera durablement avec le premier PCB (30s), une erreurs série arrivera relativement rapidement, le PCB a donc été modifié à l'aide de câble pour correspondre à ce nouveau PCB. 

<p align="center"><em>New PCB</em></p>

### 3. Interface & code Python 

La valeur du gain observé affichée permet simplement d'obtenir un ordre de grandeur, la sensibilité des mesures sur l'arduino étant de 4,88 mV et le signal d'entrée trop fraible (d'où l'intêret du circuit d'amplification).


### 4. Résultats

Les mesures ont étée effectuées à l'aide de cylindres de diamètre **D** de **2, 3 et 5 cm** ainsi que de crayons de mines HB, 2B et 4B.
Avec la déformation $\epsilon$ = e/D, e étant l'épaisseur du papier (0,1 mm)


<p align="center"><em>New PCB</em></p>

<p align="center"><em>New PCB</em></p>

<p align="center"><em>Comparaison avec un Flex sensor 1070 LLC </em></p>


### 5. Limites et perspectives

*Le Bluetooth du HC-05*

  La connexion entre le module HC-05 et un PC est **trop insable** pour utiliser seulement l'interface python fournie **sur Mac OS**, l'appairage échoue souvent ou se coupe régulièrement. 
  
*Utilisation d'un module Wifi ESP8266*

  Remplacer le HC-O5 par un module Wifi ESP8266 ou simplement utiliser une carte Arduino Uno Wifi pourrait permettre de se connecter plus aisément avec les OS Mac sur un même réseau. 
  
