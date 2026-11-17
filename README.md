# Système Smart Badge pour un évenement de Networking

Ce dépôt contient l'infrastructure technique et les scripts d'automatisation développés pour la gestion des inscriptions, la synchronisation des données et la génération automatique de **Smart Badges** avec QR Codes de réseautage pour l'événement **Youth Startups 2.0** (organisé par JCI Monastir).

## Aperçu

<img width="1920" height="1080" alt="generic" src="https://github.com/user-attachments/assets/67a3d469-a215-4a19-a943-5078eca4cf95" />

<img width="1696" height="2528" alt="Badge_MAHDI MEL" src="https://github.com/user-attachments/assets/0e25638f-1a6d-4f84-ac19-e714bb5cd9d9" />

<img width="2058" height="3931" alt="testing" src="https://github.com/user-attachments/assets/53ce8c58-3cb9-4421-bd3b-1d79becaadbe" />

---

## 🏗️ Architecture & Flux de Données

Le système repose sur un pipeline automatisé en 3 étapes permettant de passer d'une inscription en ligne à un badge prêt à l'impression :

1. **Collecte & Confirmation (Google Forms + Google Apps Script)** :
   * Lorsqu'un participant s'inscrit via le formulaire, un déclencheur exécute un script qui extrait ses informations (Nom, Rôle, WhatsApp, LinkedIn, Portfolio, ...).
   * Envoi automatique d'un e-mail de confirmation HTML personnalisé récapitulant les données qui seront encodées dans son futur QR Code.
   * Synchronisation en temps réel des données vers une base **Supabase** ou import groupé via CSV.

2. **Génération des QR Codes** :
   * Création des QR Codes uniques encodant les liens de réseautage pour chaque participant.

3. **Assemblage des Smart Badges** :
   * Normalisation automatique des rôles issus de la base de données (`FOUNDER`, `EXPLORER`, `FREELANCER`, `STAFF`, `GUEST`, ...).
   * Sélection dynamique du modèle graphique correspondant au rôle.
   * Incrustation précise du QR Code et du nom du participant avec ajustement des coordonnées (X, Y) et de la typographie selon la géométrie de chaque template.

4. **Lors de l'Evénement: Interface Web & Réseautage QR Code** :
   * Pages web connectées à Supabase, accessibles directement lors du scan du QR Code d'un badge pour faciliter la mise en relation instantanée durant l'événement.

5. **Envoi des mails de données de réseautage** :
   * Envoi d'un e-mail à chaque participant contenant les données des participants qui a scanné ses badges.  

---

## Installation et Utilisation

### 1. Prérequis
Assurez-vous d'avoir Python 3 installé sur votre machine, puis installez les dépendances nécessaires :

```bash
pip install Pillow pandas
```

### 2. Préparation des fichiers
1. Exportez la liste des inscrits depuis Supabase au format `.csv` et nommez le fichier `attendees.csv` à la racine du projet.
2. Vérifiez que les QR codes sont bien générés dans le dossier `qrcodes/` en respectant la nomenclature `Prenom_Nom_QR.png`.
3. Vérifiez que les modèles graphiques des badges se trouvent bien dans le dossier `templates/`.

### 3. Génération des badges
Exécutez le script Python depuis votre terminal :

```bash
python generate_badges.py
```

Les badges finaux haute qualité seront automatiquement générés et classés dans le répertoire `badges_finaux/` selon le rôle de chaque participant (`badges_finaux/FOUNDER/`, `badges_finaux/STAFF/`, etc.).

---

## 🛠️ Technologies Utilisées

* **Développement Web** : HTML, CSS, JavaScript (e-mails transactionnels HTML & page de l'événement)
* **Google Workspace** (Google Forms, Google Sheets, Google Apps Script)
* **Base de données** : Supabase (PostgreSQL / API REST)
* **Traitement d'image & Data** : Python , `Pillow` (PIL), `Pandas`


---
