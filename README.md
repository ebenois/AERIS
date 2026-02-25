# AERIS - Télémétrie & Aide au Vol par Liaison Radio
## Présentation
AERIS est un écosystème de monitoring de vol haute performance conçu pour les aéronefs téléguidés (avion, planeur, drone). En utilisant une liaison radio dédiée, le système permet de s'affranchir des limites de portée du Wi-Fi standard, offrant ainsi une télémétrie fiable même lors de vols à longue distance.

## Architecture du Système
- **AERIS Air (FDR)** : Module embarqué récupérant les données d'attitude et d'altitude. Il transmet les informations via un module radio (émetteur) pour une robustesse maximale du signal.
- **AERIS Ground (PFD)** : Logiciel Python/PyQt traitant le flux binaire pour animer les instruments de bord en temps réel.

## Spécifications Hardware
- **Microcontrôleur** : ESP32 — Gère l'acquisition et le protocole de communication.
- **Transmission Radio** : Module radio (HC-12) — Assure la liaison de données stable à longue portée.
- **IMU** : ICM-20948 (9 axes) — Pour un horizon artificiel stable et réactif.
- **Baromètre** : BME280 — Pour une altimétrie et une variométrie de haute précision.
- **Énergie** : Alimentation autonome par batterie Li-Po 3.7V.

## Fonctionnalités Clés
- **Écran de vol principal** : Visualisation des paramètres de vol.
- **Système Expert AERIS** : Analyse continue des paramètres de vol pour fournir des recommandations stratégiques au pilote.
- **Liaison Radio Robuste** : Transmission optimisée pour résister aux interférences et couvrir de larges périmètres de vol.

## Installation
- Connectez-vous au point d'accès Wi-Fi généré par l'ESP32.
- Lancez l'interface : `python software\main.py`.
- Les données s'affichent automatiquement dès réception du premier paquet UDP.

## Galerie du Projet
### AERIS Air
### AERIS Ground
#### Etat déconnecté 
![État actuel de AERIS Ground si un appareil n'est pas connecté](https://github.com/ebenois/AERIS/blob/prototype/assets/EtatActuelDeconnecte.png?raw=true)
#### Etat connecté 
![État actuel de AERIS Ground si un appareil est connecté](https://github.com/ebenois/AERIS/blob/prototype/assets/EtatActuelConnecte.png?raw=true)

