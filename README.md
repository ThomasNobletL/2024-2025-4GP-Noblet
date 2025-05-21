<h1 align = "center"> Projet Capteur Graphène 4A - GP <h1> 
<h2 align="center"> Par NOBLET Thomas </h2>
<h3 align="center"> INSA de Toulouse, département Génie Physique, année 2024 - 2025 </h3>
  
<p align="center">
  <a href="http://www.gnu.org/licenses/gpl-3.0">
    <img src="https://img.shields.io/badge/License-GPL%20v3-blue.svg" alt="License: GPL v3">
  </a>
</p>

## <h2 align = "center"> Mesure de contrainte sous arduino & python d'un capteur graphène <h1>

### 1. Description

*Contexte*

Le projet consiste à reproduire une technologie low-tech de capteur de pression en graphène, se basant sur l'article "Pencil Drawn Strain Gauges and Chemiresistors on Paper" de Cheng-Wei Lin, Zhibo Zhao, Jaemyung Kim & Jiaxing Huang.

*Principe*

Les traces de crayons sur du papier se comportent comme des résistances dont la valeur varie en fonction de la courbure du papier sur lequels elles sont dessinées. 

*Contenu du projet*

Une datasheet du capteur a pu être réalisée à l'aide d'une carte Arduino Uno, d'un circuit d'amplification (dont le PCB a été réalisé sur KICAD) et d'une interface python.

***Matériel utilisé (non exhaustif)***
- **Capteur de contrainte en graphène** : Mine 4H minimum conseillée
- **MCP 41050** : Varier le gain du circuit d'amplification
- **Module Bluetooth HC-05** : Récupérer les données en Bluetooth  
- **Ecran OLED SS1306 en I2C** : Affichage des données sur le PCB

