# AERIS - Télémétrie & Aide au Vol par Liaison Radio
## Présentation
AERIS est un écosystème de monitoring de vol haute performance conçu pour les aéronefs téléguidés (avion, planeur, drone). En utilisant une liaison radio dédiée, le système permet de s'affranchir des limites de portée du Wi-Fi standard, offrant ainsi une télémétrie fiable même lors de vols à longue distance.

## Architecture du Système
- **AERIS Core (Air)** : Module embarqué récupérant les données d'attitude et d'altitude. Il transmet les informations via un module radio (émetteur) pour une robustesse maximale du signal.
- **AERIS Ground (Terre)** : Station au sol équipée d'un récepteur radio relié au PC. L'application Python/PyQt traite le flux binaire pour animer les instruments de bord en temps réel.

## Spécifications Hardware
- **Microcontrôleur** : ESP32 — Gère l'acquisition et le protocole de communication.
- **Transmission Radio** : Module radio (ex: LoRa ou HC-12) — Assure la liaison de données stable à longue portée.
- **IMU** : ICM-20948 (9 axes) — Pour un horizon artificiel stable et réactif.
- **Baromètre** : BME280 — Pour une altimétrie et une variométrie de haute précision.
- **Énergie** : Alimentation autonome par batterie Li-Po 3.7V.

## Fonctionnalités Clés
- **Horizon Artificiel (PFD)** : Visualisation de l'attitude (tangage/roulis) même à grande distance.
- **Variomètre Radio** : Monitoring des ascendances thermiques en temps réel pour les planeurs téléguidés.
- **Système Expert AERIS** : Analyse continue des paramètres de vol pour fournir des recommandations stratégiques au pilote.
- **Liaison Radio Robuste** : Transmission optimisée pour résister aux interférences et couvrir de larges périmètres de vol.

## Structure du Dépôt
- `software/` : Application Python/PyQt et décodage du flux radio entrant.

## Installation
- Connectez-vous au point d'accès Wi-Fi généré par l'ESP32.
- Lancez l'interface : `python software\main.py`.
- Les données s'affichent automatiquement dès réception du premier paquet UDP.

## Galerie du Projet
### Interface de Pilotage (IHM)


